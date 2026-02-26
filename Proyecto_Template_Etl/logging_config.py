import logging
from datetime import datetime

def get_logger(nombre):
    if not logging.getLogger().hasHandlers():
        log_file = f"logs/etl_covid_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(log_file, mode='a', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    return logging.getLogger(nombre)