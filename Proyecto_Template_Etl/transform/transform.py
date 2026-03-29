import pandas as pd
from logging_config import get_logger
from functools import reduce

class transform_covid:

    def transform(self,process_name:str, data)->pd.DataFrame:
        logger = get_logger(process_name)
        try:

            data_cleaned = data.dropna()
            data_cleaned["report_date"] = pd.to_datetime(data_cleaned['report_date'])
            logger.info(f"  ✅ {len(data_cleaned)} registros transformados")
            return data_cleaned
        except Exception as e:
            logger.error(f"  ❌ Error en transform: {e}")
            raise
    
    def transform_setData(self, process_name:str, data_list:list)->pd.DataFrame:
        logger = get_logger(process_name)
        try:
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
            logger.info(f"  ✅ {len(data_ready)} registros transformados")
            return data_ready
        except Exception as e:
            logger.error(f"  ❌ Error en transform_setData: {e}")
            raise
