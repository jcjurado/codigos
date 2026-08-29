import extract as module_extract

def extract(tabla, proceso):
    prod = module_extract.ServerExtractor(tabla, proceso)
    df = prod.extract()
    return df