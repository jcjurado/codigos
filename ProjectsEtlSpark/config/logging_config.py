import logging
import sys

_configurado = False

def _configurar():
    global _configurado
    if _configurado:
        return
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("pipeline.log", mode="w", encoding="utf-8"),
        ],
    )
    _configurado = True

def get_logger(nombre:str=None):
    _configurar()
    return logging.getLogger(nombre)