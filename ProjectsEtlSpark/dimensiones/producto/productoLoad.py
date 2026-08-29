from pyspark.sql import DataFrame
from load import ServerLoader
from config.logging_config import get_logger
from utils.classError import LoadError

def load(df:DataFrame, tabla: str, proceso:str):
    # loader = ServerLoader(tabla, proceso)
    # loader.load(df)

    logger = get_logger(proceso)
    logger.info(f"Iniciando carga de la tabla {tabla}")
    try:
        (df
         .write
         .mode("overwrite")
         .partitionBy("ProductLine")
         .parquet(f"./output/{tabla}")
        )
        cantidad = df.count()
        logger.info(f"Carga completada: {cantidad} filas cargadas")
    except Exception as e:
        raise LoadError(f"Fallo a la carga del parquet : {e}") from e