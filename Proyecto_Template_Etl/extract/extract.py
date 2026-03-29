from logging_config import get_logger
import pandas as pd

def extract(process_name:str, engine=None,query:str=None)->pd.DataFrame:
    logger = get_logger(process_name)
    data = pd.read_sql(query,engine)
    logger.info(f"  ✅ {len(data)} datos extraidos - {str.upper(engine.name)}")
    return data