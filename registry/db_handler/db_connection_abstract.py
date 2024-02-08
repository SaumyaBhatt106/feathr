from abc import ABC, abstractmethod
from typing import List, Dict


class DbConnection(ABC):

    @property
    def is_sqlalchemy_supported(self):
        pass

    @abstractmethod
    def connect(self, autocommit: bool = True) -> any:
        pass

    @abstractmethod
    def query(self, sql: str, *args, **kwargs) -> List[Dict]:
        pass

    @abstractmethod
    def transaction(self) -> any:
        pass

    @abstractmethod
    def create_all_tables(self, file) -> None:
        pass