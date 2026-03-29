from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
from logging_config import get_logger
from sqlalchemy.engine import URL


logger = get_logger('Etl_Covid')

class Base:
    def __init__(self):
         
        load_dotenv()

    def conection_db_postgre(self):
        logger.info("🔌 Conectando a la base de datos PostgreSQL...")
        try:

            user = os.getenv('PG_USER')
            password = os.getenv('PG_PASS')
            host = os.getenv('PG_HOST')
            puerto = os.getenv('PG_PORT')

            database_url =f"postgresql+psycopg2://{user}:{password}@{host}:{puerto}/postgres"
            engine = create_engine(database_url)

            if engine:
                logger.info("✅ Conexión a la base de datos exitosa")
            return  engine
        except Exception as e:
            logger.error(f"❌ Error al conectar a la base de datos: {e}")
            raise
    
    def conection_db_mysql(self):
        logger.info("🔌 Conectando a la base de datos MySql...")
        try:
            user = os.getenv('MYSQL_USER')
            password = os.getenv('MYSQL_PASS')
            host = os.getenv('MYSQL_HOST')
            puerto = os.getenv('MYSQL_PORT')
            
            connection_url = URL.create(
                drivername="mysql+mysqlconnector",
                username= user,
                password=password,
                host=host,
                port=puerto,
                database="prueba_conexion"
            )
            engine = create_engine(connection_url, pool_size=5, max_overflow=10)
            with engine.connect() as conn:
                logger.info("✅ Conexión a la base de datos exitosa")
            return  engine
        except Exception as e:
            logger.error(f"❌ Error al conectar a la base de datos: {e}")
            raise