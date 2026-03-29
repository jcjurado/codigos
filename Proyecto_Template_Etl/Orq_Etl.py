from extract import extract
from transform import transform
from load import load
from config import base_config
from logging_config import get_logger

process_name = "Etl_Covid"
tablas = ["vaccination_data","covid_cases"]

if __name__ == "__main__":
    logger = get_logger(process_name)
    logger.info("🚀 Iniciando el proceso...")

    try:
        dp_base = base_config.Base()
        engine_pg = dp_base.conection_db_postgre()

        logger.info(f"🔄 Iniciando proceso de extraccion con la base {str.upper(engine_pg.name)}")
        data_list = []
        for idx,tabla in enumerate(tablas):
            logger.info(f"📌  {idx+1}. Extrayendo datos de la tabla {tabla}")
            sql_extract = f"SELECT * FROM {tabla}" 
            data = extract.extract(process_name, engine_pg, sql_extract)
            data_list.append(data)
        logger.info("📌 Extracción finalizada")

        logger.info("🔄 Iniciando proceso de transformacion")
        transformer = transform.transform_covid()
        data_cleaned = transformer.transform_setData(process_name, data_list)
        logger.info("📌 Transformación finalizada")

        engine_mysql = dp_base.conection_db_mysql()
        tabla_destino = "covid_country_summary"

        logger.info(f"🔄 Iniciando proceso de carga a {str.upper(engine_mysql.name)}")
        logger.info(f"📌  Cargando datos a la tabla {tabla_destino}")
        load.load(process_name, data_cleaned, engine_mysql, tabla_destino)


        logger.info(f"✅ Proceso {process_name} finalizado exitosamente")

    except Exception as e:
        logger.error(f"❌ El proceso {process_name} falló: {e}", exc_info=True)
        raise
    