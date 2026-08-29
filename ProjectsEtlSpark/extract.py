from utils.interface import Extractor
from config.logging_config import get_logger
from config.config import POSTGRES_CONEXION
from utils.classError import ExtractError
from pyspark.sql import SparkSession


class ServerExtractor(Extractor):

    def __init__(self, tabla:str, proceso:str):
        self.proceso = proceso
        self.tabla = tabla

    def extract(self):
        logger = get_logger(self.proceso)
        logger.info(f"Iniciando proceso de extraccion de la tabla >> {self.tabla}")
        
        spark = (SparkSession
                      .builder
                      .appName("readTablas")
                      .master("local[*]")
                      .config("spark.jars", "/home/sion/projects/jars/postgresql-42.7.4.jar")
                      .getOrCreate()
            )
        df = (
                spark.read
                    .format("jdbc")
                    .options(**POSTGRES_CONEXION)
                    .option("dbtable", self.tabla)
                    .load()
            )

        count = df.count()
        if count == 0:
                raise ExtractError(f"La fuente no tiene registros")
        logger.info("Información del esquema:\n%s", df._jdf.schema().treeString())
        logger.info(f"Filas extraidas de la tabla {self.tabla}: {count} filas")

        return df
        
