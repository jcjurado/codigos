from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

class Extractor(ABC):
    @abstractmethod
    def extract(self):
        ...

class Load(ABC):
    @abstractmethod
    def load(self, df: DataFrame):
        ...


class Transformer(ABC):
    @abstractmethod
    def transform(self, *args, **kwargs)-> DataFrame:
        ...