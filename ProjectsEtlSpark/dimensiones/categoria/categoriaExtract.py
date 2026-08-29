import extract as module_extract

def extract(tabla, proceso):
    cat = module_extract.ServerExtractor(tabla, proceso)
    df = cat.extract()
    return df