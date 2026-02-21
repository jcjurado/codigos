import logging
from datetime import datetime
import os

def get_logger(nombre):
    if not os.path.exists("./logs"):
        os.makedirs("./logs")

    fecha_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"./logs/logs_{fecha_str}.log"

    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[
                logging.FileHandler(log_file, mode='w', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    return logging.getLogger(nombre)



     