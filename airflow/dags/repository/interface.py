from abc import ABC, abstractmethod
from datetime import datetime


class BaseRepository(ABC):
    def __init__(self):
        self.buff = []
        super().__init__()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def load_snapshot(self):
        pass

    @abstractmethod
    def save_snapshot(self):
        pass

    @abstractmethod
    def make_entries(self):
        pass

    def insert_row(self, row: (datetime, str, str, str, str, str)):
        self.insert_rows([row])

    @abstractmethod
    def insert_rows(self, row: list[(datetime, str, str, str, str, str)]):
        pass

    def add_buff(self, rows: list[(datetime, str, str, str, str, str)]):
        self.buff.extend(rows)
