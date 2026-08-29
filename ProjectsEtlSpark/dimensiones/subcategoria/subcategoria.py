from config.logging_config import get_logger
from dimensiones.subcategoria import subcategoriaExtract,subcategoriaTransform,subcategoriaLoad
from config.config import TABLAS
from utils.classError import ExtractError, LoadError, TransformError
import sys

class subcategoria:

    def orq(self):
        tabla = TABLAS["DimSubCategoria"]
        proceso = f"Modulo de {tabla}"
        logger = get_logger(proceso)
        try:
            df_subcategoria_raw = subcategoriaExtract.extract(tabla, proceso)
            subcategoria_transformer = subcategoriaTransform.subcategoriaTransformer(tabla, proceso)
            df_subcat_transform = subcategoria_transformer.transform(df_subcategoria_raw)
            subcategoriaLoad.load(df_subcat_transform, tabla, proceso)

        except (ExtractError, LoadError, TransformError) as e:
            logger.error(f"Pipeline abortado: {e}")
            sys.exit(1)

        except Exception as e:
            logger.exception(f"Error inesperado: {e}")
            sys.exit(1)

def main():
    subcat = subcategoria()
    subcat.orq()

if __name__ == "__main__":
    main()
    