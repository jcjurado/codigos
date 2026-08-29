import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_URI = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}"
    f"/{os.getenv('POSTGRES_DB')}"
    )

POSTGRES_CONEXION = {
    "url": f"jdbc:postgresql://{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}",
    "user": os.getenv('POSTGRES_USER'),
    "password": os.getenv('POSTGRES_PASSWORD'),
    "driver": "org.postgresql.Driver"
}

MS_URI = (
    f"mssql+pyodbc://"
    f"{os.getenv('MS_USER')}:{os.getenv('MS_PASSWORD')}"
    f"@{os.getenv('MS_HOST')}:{os.getenv('MS_PORT')}"
    f"/{os.getenv('MS_DB')}"
    f"?driver=SQL+Server"
)


TABLAS = {
    "DimProducto": 'public."DimProducto"',
    "DimCustomer": "SELECT CustomerKey, CustomerAlternateKey, FirstName, LastName, EmailAddress, BirthDate FROM  AdventureWorksDW2022.dbo.DimCustomer",
    "DimSubCategoria": 'public."DimProductoSubCategoria"',
    "DimCategoria": 'public."DimProductoCategoria"',
    "FactInternetSales": 'public."FactInternetSales"',
}