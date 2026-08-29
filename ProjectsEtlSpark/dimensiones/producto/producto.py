from config.logging_config import get_logger
from dimensiones.producto import productoExtract,productoTransform,productoLoad
from config.config import TABLAS
from utils.classError import ExtractError, LoadError, TransformError
import sys

class producto:

    def orq(self):
        tabla = TABLAS["DimProducto"]
        proceso = f"Modulo de {tabla}"
        logger = get_logger(proceso)
        try:
            df_prod_raw = productoExtract.extract(tabla, proceso)
            prod_transformer = productoTransform.productoTransformer(tabla, proceso)
            df_prod_transform = prod_transformer.transform(df_prod_raw)
            productoLoad.load(df_prod_transform, tabla, proceso)

        except (ExtractError, LoadError, TransformError) as e:
            logger.error(f"Pipeline abortado: {e}")
            sys.exit(1)

        except Exception as e:
            logger.exception(f"Error inesperado: {e}")
            sys.exit(1)

def main():
    prod = producto()
    prod.orq()

if __name__ == "__main__":
    main()
    