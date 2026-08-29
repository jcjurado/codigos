from pyspark.sql import DataFrame
from load import ServerLoader

def load(df:DataFrame, tabla: str, proceso:str):
    loader = ServerLoader(tabla, proceso)
    loader.load(df)