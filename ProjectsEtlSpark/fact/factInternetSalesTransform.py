from utils.interface import Transformer
from pyspark.sql import DataFrame, functions as F
from config.logging_config import get_logger
from utils.classError import TransformError



class factInternetSalesTransformer(Transformer):

    def __init__(self,tabla, proceso):
        self.tabla = tabla
        self.proceso=proceso
        
    def transform(self, df:DataFrame):
        logger = get_logger(nombre=self.proceso)
        logger.info(f"Iniciando transformacion de {self.tabla}")
        try:

            df = (
                df
                .select(
                    "SalesOrderNumber",
                    "ProductKey",
                    "CustomerKey",
                    "OrderDateKey",
                    "OrderQuantity",
                    "SalesAmount",
                    "TotalProductCost"
                )
                .withColumn(
                   "Margin",
                   (F.col("SalesAmount") - F.col("TotalProductCost"))/F.col("SalesAmount")
                                    
                )
                .withColumn(
                    "Balance",
                    F.col("SalesAmount") - F.col("TotalProductCost")
                )                   
            )
            
            logger.info("Transformacion completada")
            return df
        except Exception as e: 
            raise TransformError("❌ Error de conexion: %s", e)