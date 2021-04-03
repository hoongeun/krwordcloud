import json
import os
import tempfile
import datetime

import config
import pyorc
from dateutil import parser
from kafka import KafkaProducer

from hdfs import HdfsError, InsecureClient
from repository.interface import BaseRepository
from repository.singleton import singleton


KST = datetime.timezone(datetime.timedelta(hours=9))


@singleton
class HDFS(BaseRepository):
    def __init__(self, host: str, port, user: str):
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.prodcuer = None

    def connect(self):
        self.conn = InsecureClient(f"http://{self.host}:{self.port}",
                                   user=self.user)
        if os.environ.get("KAFKA_BOOTSTRAP", None):
            self.producer = KafkaProducer(
                bootstrap_servers=os.environ.get("KAFAKA_BOOTSTRAP",
                                                 "localhost:1234")
            )
        else:
            self.producer = None

    def disconnect(self):
        self.save_snapshot()
        if self.prodcuer:
            self.producer.close()

    def insert_rows(self, rows: list[(datetime, str, str, str, str, str)]):
        self.add_buff(rows)
        self.flush()

    def _last_datetime(self, category, date):
        if self.conn.status(f"/krwordcloud/add-article/{date}")['length'] == 0:
            return config.min_date
        tfname = ''
        with tempfile.NamedTemporaryFile("wb") as tf:
            tfname = tf.name
            with self.conn.read(f"/krwordcloud/add-article/{date}",
                                chunk_size=8096) as hf:
                for chunk in hf:
                    tf.write(chunk)
            with open(tfname, 'rb') as tf:
                reader = pyorc.Reader(tf)
                maximum = datetime.datetime \
                    .strptime(f"{date} GMT+0900", "%Y-%m-%d.orc GMT%z")
                for row in reader:
                    if row[0] > maximum and row[1] == category:
                        maximum = row[0]
                if (maximum < config.min_date):
                    return config.min_date
                elif maximum > datetime.datetime.now().replace(tzinfo=KST):
                    return datetime.datetime.now().replace(tzinfo=KST)
                else:
                    return maximum
        os.unlink(tfname)

    def make_entries(self):
        entries = dict()
        hdfs_entries = dict()
        lookup_hdfs = []

        self.load_snapshot()

        for category in config.categories:
            category_rows = list(
                filter(lambda row: row[1] == category, self.buff))
            if len(category_rows) > 0:
                last = max(category_rows, key=lambda row: row[0])
                entries[category] = last[0]
            else:
                lookup_hdfs.append(category)

        try:
            dates = self.conn.list("/krwordcloud/add-article/")
            if len(dates) > 0:
                for category in lookup_hdfs:
                    found = False
                    for last in reversed(dates):
                        try:
                            entries[category] = self._last_datetime(category,
                                                                    last)
                            found = True
                            break
                        except Exception as e:
                            print(e)
                            continue
                    if found is False:
                        entries[category] = config.min_date
            else:
                hdfs_entries = dict.fromkeys(lookup_hdfs, config.min_date)
        except HdfsError:
            entries[category] = config.min_date
        except Exception as e:
            print(e)
        return {k: v for k, v in sorted({**entries, **hdfs_entries}.items(),
                                        key=lambda item: item[1])}

    def save_snapshot(self):
        print('save_snapshot')
        with self.conn.write("/krwordcloud/snapshot.json", overwrite=True,
                             encoding="utf-8") as f:
            data = list(map(lambda x: (x[0].isoformat(), x[1], x[2], x[3],
                                       x[4], x[5]), self.buff))
            json.dump(data, f, ensure_ascii=False)

    def load_snapshot(self):
        print('load_snapshot')
        try:
            with self.conn.read("/krwordcloud/snapshot.json",
                                encoding="utf-8") as f:
                self.buff = list(map(
                    lambda x: (parser.parse(x[0]), x[1],
                               x[2], x[3], x[4], x[5]), json.load(f)))
        except Exception:
            self.buff = []

    def flush(self):
        dates = sorted(list(set(map(lambda row: row[0].date(), self.buff))))
        if len(dates) > 1:
            for d in dates[:-1]:
                data = list(filter(lambda row: row[0].date() == d, self.buff))
                if self.producer:
                    self._kafka_flush(d, data)
                else:
                    self._hdfs_flush(d, data)
            self.buff = list(filter(
                lambda row: row[0].date() == dates[-1], self.buff))
            self.save_snapshot()

    def _kafka_flush(self, date, data):
        self.producer.send(f"add-article-{date}", data)

    def _hdfs_flush(self, date, data):
        with self.conn.write(
            f"/krwordcloud/add-article/{date}.orc",
            overwrite=True
        ) as hf:
            tfname = ''
            with tempfile.NamedTemporaryFile(mode="wb+", delete=False) as tf:
                tfname = tf.name
                with pyorc.Writer(
                    tf,
                    schema="struct<field0:timestamp,field1:string," +
                        "field2:string,field3:string>",
                ) as of:
                    of.writerows(data)
            with open(tfname, 'rb') as tf:
                for line in tf:
                    hf.write(line)
            os.unlink(tfname)
