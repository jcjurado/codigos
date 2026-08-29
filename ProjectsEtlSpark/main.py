
from pyspark.sql import SparkSession
from dimensiones.categoria.categoria import categoria
from dimensiones.subcategoria.subcategoria import subcategoria
from dimensiones.producto.producto import producto
from fact.factInternetSales import factInternetSales
import time
from config.logging_config import get_logger
# from concurrent.futures import ThreadPoolExecutor

def ejecutar_dimension(dimension):
    instancia = dimension()
    instancia.orq()

def main():

    logger = get_logger()
    logger.info("===== INICIO DE PROCESO =====")
    inicio = time.time()
    cat = categoria()
    cat.orq()

    subcat = subcategoria()
    subcat.orq()

    prod = producto()
    prod.orq()

    fact = factInternetSales()
    fact.orq()
    duracion = time.time() - inicio
    logger.info(f"===== FIN PROCESO. DURACION: {round(duracion,2)} segundos =====")

    # EJEcuCION PARALELA DE LAS DIMENSIONES
    # logger = get_logger()
    # logger.info("===== INICIO DE PROCESO =====")

    # dimensiones = [
    #     categoria,
    #     subcategoria,
    #     producto,
    # ]

    # with ThreadPoolExecutor(max_workers=3) as executor:
    #     tareas = [
    #         executor.submit(ejecutar_dimension, dimension)
    #         for dimension in dimensiones
    #     ]

    #     for tarea in tareas:
    #         tarea.result()  # Propaga cualquier error ocurrido

    # fact = factInternetSales()
    # fact.orq()

    # logger.info("===== FIN PROCESO =====")

    spark = (
        SparkSession
             .builder
             .appName("read")
             .master("local[*]")
             .getOrCreate()
             )
    df = (spark
          .read
          .parquet('/home/sion/projects/pyspark-training/output/public."DimProductoCategoria"')
          )
    logger.info("Informacion de parquet de categoria \n%s", df._jdf.schema().treeString())

if __name__ == "__main__":
    main()