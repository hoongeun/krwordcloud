import prestodb
from prestodb import transaction
from datetime import datetime, timezone
from repository.singleton import singleton
from repository.interface import BaseRepository
import config


@singleton
class PrestoSQL(BaseRepository):
    def __init__(self, host: str, port, user: str, password: str):
        super().__init__()
        self.host = host
        self.port = port
        self.user = user
        self.password = password

    def connect(self):
        self.conn = prestodb.dbapi.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            catalog="hive",
            schema="krwordcloud",
            isolation_level=transaction.IsolationLevel.AUTOCOMMIT,
        )

    def close(self):
        self.save_snapshot()
        self.conn.close()

    def insert_rows(self, rows: list[(datetime, str, str, str, str, str)]):
        self.add_buff(rows)
        self.flush()

    def query(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def flush(self):
        dates = sorted(list(set(map(lambda row: row[0].date(), self.buff))))
        data = self.buff = filter(
            lambda row: row[0].date() < dates[-1], self.buff)
        cursor = self.conn.cursor()
        query = "INSERT INTO article (date, category, press, title, content, \
            url) VALUES "
        query += ", ".join(
            map(
                lambda x: f"(from_unixtime({x[0].replace(tzinfo=timezone.utc).timestamp()}), \
                '{x[1]}', '{x[2]}', '{x[3]}', '{x[4]}', '{x[5]}')",
                data,
            )
        )
        try:
            cursor.execute(query)
            # FIXME: this sdk only committed with fetchone()
            cursor.fetchone()
        except Exception:
            pass
        cursor.close()
        self.buff = filter(
            lambda row: row[0].date() == dates[-1], self.buff)
        self.save_snapshot()

    def load_snapshot(self):
        if not self.buff:
            return
        self.buff.clear()
        cursor = self.conn.cursor()
        selectQuery = "SELECT date, category, press, title, content, url\
                       FROM snapshot"
        deleteQuery = "DELETE FROM snapshot"
        try:
            cursor.execute(selectQuery)
            for row in cursor:
                self.buff.append(row)
        except Exception:
            pass

        try:
            cursor.execute(deleteQuery)
            # FIXME: this sdk only committed with fetchone()
            cursor.fetchone()
        except Exception:
            pass
        cursor.close()

    def save_snapshot(self):
        if not self.buff:
            return
        cursor = self.conn.cursor()
        query = "INSERT INTO snapshot (date, category, press, title," + \
            " content, url) VALUES "
        query += ", ".join(
            map(
                lambda x: f"(from_unixtime({x[0].replace(tzinfo=timezone.utc).timestamp()}), \
                '{x[1]}', '{x[2]}', '{x[3]}', '{x[4]}', '{x[5]}')",
                self.buff,
            )
        )
        self.buff.clear()
        try:
            cursor.execute(query)
            # FIXME: this sdk only committed with fetchone()
            cursor.fetchone()
        except Exception:
            pass
        cursor.close()

    def make_entries(self):
        entries = dict()
        for category in config.categories:
            if category in self.buff and len(self.buff[category].keys()) > 0:
                last = max(self.buff[category].keys())
                if len(last) > 0:
                    article = max(self.buff[category][last],
                                  key=lambda x: x[1])
                    entries[category] = article[1]
                    continue
            cursor = self.conn.cursor()
            query = "SELECT max(date) FROM article" + \
                    f"WHERE category = '{category}'"
            cursor.execute(query)
            last_crawled = cursor.fetchone()
            if (
                last_crawled is None
                or last_crawled[0] is None
                or last_crawled[0] < config.min_date
            ):
                entries[category] = config.min_date
            elif last_crawled[0] > datetime.now():
                entries[category] = datetime.now()
            else:
                entries[category] = last_crawled[0]
        return entries
