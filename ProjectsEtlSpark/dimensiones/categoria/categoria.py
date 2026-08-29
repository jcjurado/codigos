from config.logging_config import get_logger
from dimensiones.categoria import categoriaExtract,categoriaTransform,categoriaLoad
from config.config import TABLAS
from utils.classError import ExtractError, LoadError, TransformError
import sys

class categoria:

    def orq(self):
        tabla = TABLAS["DimCategoria"]
        proceso = f"Modulo de {tabla}"
        logger = get_logger(proceso)
        try:
            df_categoria_raw = categoriaExtract.extract(tabla, proceso)
            categoria_transformer = categoriaTransform.categoriaTransformer(tabla, proceso)
            df_cat_transform = categoria_transformer.transform(df_categoria_raw)
            categoriaLoad.load(df_cat_transform, tabla, proceso)

        except (ExtractError, LoadError, TransformError) as e:
            logger.error(f"Pipeline abortado: {e}")
            sys.exit(1)

        except Exception as e:
            logger.exception(f"Error inesperado: {e}")
            sys.exit(1)

def main():
    cat = categoria()
    cat.orq()

if __name__ == "__main__":
    main()
    