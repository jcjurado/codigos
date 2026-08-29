import extract as module_extract

def extract(tabla, proceso):
    subcat = module_extract.ServerExtractor(tabla, proceso)
    df = subcat.extract()
    return df