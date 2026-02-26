from procesos_etl import extract, load, transform_covid
from base_config import Base
from logging_config import get_logger

process_name = "Etl_Covid"
logger = get_logger(process_name)
tablas = ["vaccination_data","covid_cases"]

if __name__ == "__main__":
    logger.info("🚀 Iniciando el proceso...")
    dp_base = Base()
    engine_pg = dp_base.conection_db_postgre()

    logger.info(f"🔄 Iniciando proceso de extraccion con la base {str.upper(engine_pg.name)}")
    data_list = []
    for idx,tabla in enumerate(tablas):
        logger.info(f"📌  {idx+1}. Extrayendo datos de la tabla {tabla}")
        sql_extract = f"SELECT * FROM {tabla}" 
        data = extract(process_name, engine_pg, sql_extract)
        data_list.append(data)
    logger.info("📌 Finalizando del proceso de extraccion")

    logger.info("🔄 Iniciando proceso de transformacion")
    transform = transform_covid()
    data_cleaned = transform.transform_setData(process_name, data_list)
    logger.info("📌 Finalizando proceso de transformacion")

       
    dp_base = Base()
    engine_mysql = dp_base.conection_db_mysql()
    tabla_destino = ["covid_country_summary"]

    logger.info(f"🔄 Iniciando proceso de carga a {str.upper(engine_mysql.name)}")
    for idx, (data,tabla) in enumerate(zip(data_list, tabla_destino)):
        logger.info(f"📌  {idx+1} .Cargando datos a la tabla {tabla}")
        load(process_name, data, engine_mysql, tabla)
    logger.info("✅ Proceso ETL de COVID-19 finalizado exitosamente")
    