import platform
import os
import sys
import prestodb
from prestodb import transaction
from datetime import datetime, timezone
from db.singleton import singleton


@singleton
class PrestoDB(object):
    def __init__(self, host: str, port, user: str, password: str):
        self.buff = list()
        self.conn = prestodb.dbapi.connect(
            host=host,
            port=port,
            user=user,
            catalog="hive",
            schema="krwordcloud",
            isolation_level=transaction.IsolationLevel.AUTOCOMMIT,
        )

    def insert_row(self, row: tuple[datetime, str, str, str, str, str]):
        self.buff.append(row)
        if len(self.buff) > 30:
            self.flush()

    def query(self, query: str):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def flush(self):
        if not self.buff:
            return
        cursor = self.conn.cursor()
        query = "INSERT INTO article (date, category, press, title, content, url) VALUES "
        query += ", ".join(map(
            lambda x: f"(from_unixtime({x[0].replace(tzinfo=timezone.utc).timestamp()}), '{x[1]}', '{x[2]}', '{x[3]}', '{x[4]}', '{x[5]}')", self.buff))
        self.buff.clear()
        try:
            cursor.execute(query)
            # FIXME: this sdk only committed with fetchone()
            cursor.fetchone()
        except Exception as e:
            pass
        cursor.close()

    def close(self):
        self.conn.close()
