import pandas as pd
from logging_config import get_logger
from functools import reduce

def extract(process_name:str, engine=None,query:str=None)->pd.DataFrame:
    logger = get_logger(process_name)
    data = pd.read_sql(query,engine)
    logger.info(f"  ✅ {len(data)} datos extraidos - {str.upper(engine.name)}")
    return data

def load(process_name:str, data_cleaned:pd.DataFrame, engine, tabla:str):
    logger = get_logger(process_name)
    logger.info(f" 🖊  {len(data_cleaned)} registros a cargar")
    data_cleaned.to_sql(tabla, con=engine, index=False, if_exists='replace', chunksize=1000)

class transform_covid:

    def transform(self,process_name:str, data)->pd.DataFrame:
        logger = get_logger(process_name)
        data_cleaned = data.dropna()
        data_cleaned["report_date"] = pd.to_datetime(data_cleaned['report_date'])
        logger.info(f"  ✅ {len(data_cleaned)} registros transformados")
        return data_cleaned
    
    def transform_setData(self, process_name:str, data_list:list)->pd.DataFrame:
        logger = get_logger(process_name)
        claves ={"id": "ID"}
        data_set = []
        for data in data_list:
            data_cleaned = data.rename(columns=claves)
            data_set.append(data_cleaned)

        data_ready = reduce(lambda left, right: pd.merge(left, right, on='ID', how='inner'), data_set)
        data_ready = data_ready.dropna()

        drop_columnas =["country_y", "report_date_y"]
        columnas = {"country_x":"country", "report_date_x":"report_date"}
        
        data_ready.drop(columns=drop_columnas,inplace=True)
        data_ready.rename(columns=columnas,inplace=True)
        return data_ready
