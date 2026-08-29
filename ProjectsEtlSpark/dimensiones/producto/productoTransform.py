from utils.interface import Transformer
from pyspark.sql import DataFrame, functions as F
from config.logging_config import get_logger
from utils.classError import TransformError

class productoTransformer(Transformer):

    def __init__(self,tabla, proceso):
        self.tabla = tabla
        self.proceso=proceso
        
    def transform(self, df:DataFrame):
        logger = get_logger(nombre=self.proceso)
        logger.info(f"Iniciando transformacion de {self.tabla}")
        try:
            df=(
                df
                .select("ProductKey","EnglishProductName","StandardCost","Color","ListPrice","Size","ProductLine")
                .withColumn(
                "Color",
                F.when(
                        (F.col("Color")=='NA') |
                        (F.col("Color").isNull())
                        , "No Color"
                    )
                    .otherwise(F.col("Color"))
                )
                .withColumn(
                    "ProductLine",
                    F.when(
                        F.col("ProductLine").isNull()
                        ,"No Line"
                    ).otherwise(F.col("ProductLine"))
                )
                .withColumn(
                    "ListPrice",
                    F.when(
                        F.col("ListPrice").isNull(),
                        F.lit(0)
                    ).otherwise(F.col("ListPrice"))
                )
                
            )
            
            logger.info("Transformacion completada")
            return df
        except Exception as e: 
            raise TransformError("❌ Error de conexion: %s", e)