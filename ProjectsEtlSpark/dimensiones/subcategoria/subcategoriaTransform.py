from utils.interface import Transformer
from pyspark.sql import DataFrame
from config.logging_config import get_logger
from utils.classError import TransformError


class subcategoriaTransformer(Transformer):

    def __init__(self,tabla, proceso):
        self.tabla = tabla
        self.proceso=proceso
        
    def transform(self, df:DataFrame):
        logger = get_logger(nombre=self.proceso)
        logger.info(f"Iniciando transformacion de {self.tabla}")
        try:

            df = df.select("ProductSubcategoryKey","EnglishProductSubcategoryName", "ProductCategoryKey")
            
            logger.info("Transformacion completada")
            return df
        except Exception as e: 
            raise TransformError("❌ Error de conexion: %s", e)