import pandas as pd
from logging_config import get_logger

def load(process_name:str, data_cleaned:pd.DataFrame, engine, tabla:str):
    logger = get_logger(process_name)
    logger.info(f" 🖊  {len(data_cleaned)} registros a procesar")
    data_cleaned.to_sql(tabla, con=engine, index=False, if_exists='replace', chunksize=1000)
