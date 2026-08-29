from utils.interface import Load
from config.logging_config import get_logger
from utils.classError import LoadError



class ServerLoader(Load):
    def __init__(self,tabla:str, proceso:str):
        self.tabla = tabla
        self.proceso=proceso

    def load(self, df):
        logger = get_logger(self.proceso)
        logger.info(f"Iniciando carga de la tabla {self.tabla}")
        try:
            df.write.mode("overwrite").parquet(f"./output/{self.tabla}")

            cantidad = df.count()
            logger.info(f"Carga completada: {cantidad} filas cargadas")
        except Exception as e:
            raise LoadError(f"Fallo a la carga del parquet : {e}") from e