from config.logging_config import get_logger
from fact import factInternetSalesExtract,factInternetSalesTransform,factInternetSalesLoad
from config.config import TABLAS
from utils.classError import ExtractError, LoadError, TransformError
import sys

class factInternetSales:

    def orq(self):
        tabla = TABLAS["FactInternetSales"]
        proceso = f"Modulo de {tabla}"
        logger = get_logger(proceso)
        try:
            df_fact_raw = factInternetSalesExtract.extract(tabla, proceso)
            fact_transformer = factInternetSalesTransform.factInternetSalesTransformer(tabla, proceso)
            df_fact_transform = fact_transformer.transform(df_fact_raw)
            factInternetSalesLoad.load(df_fact_transform, tabla, proceso)

        except (ExtractError, LoadError, TransformError) as e:
            logger.error(f"Pipeline abortado: {e}")
            sys.exit(1)

        except Exception as e:
            logger.exception(f"Error inesperado: {e}")
            sys.exit(1)

def main():
    fact = factInternetSales()
    fact.orq()

if __name__ == "__main__":
    main()
    