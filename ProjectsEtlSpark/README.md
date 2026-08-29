# ETL AdventureWorksDW con PySpark

Pipeline ETL desarrollado en **PySpark** que extrae datos desde **PostgreSQL** vía JDBC, los transforma y los persiste en formato **Parquet**, siguiendo un diseño orientado a objetos con interfaces abstractas, manejo de errores por etapa y logging desacoplado por proceso.

## Arquitectura

El proyecto se organiza bajo el patrón **Extract → Transform → Load (ETL)**, con clases base abstractas (`ABC`) que fuerzan un contrato común para cualquier extractor, transformador o cargador, sin importar la dimensión o el hecho que procesen.

```
utils/
├── interface.py        # Contratos abstractos: Extractor, Load, Transformer
└── classError.py        # Excepciones custom: ExtractError, LoadError, TransformError

extract.py                # ServerExtractor: lectura genérica desde Postgres vía JDBC
load.py                   # ServerLoader: escritura genérica a Parquet

dimensiones/
├── categoria/
│   ├── categoria.py              # Orquestador de la dimensión
│   ├── categoriaExtract.py
│   ├── categoriaTransform.py
│   └── categoriaLoad.py
├── subcategoria/                 # Mismo criterio que categoria
└── producto/
    ├── producto.py
    ├── productoExtract.py
    ├── productoTransform.py
    └── productoLoad.py

fact/
├── factInternetSales.py
├── factInternetSalesExtract.py
├── factInternetSalesTransform.py
└── factInternetSalesLoad.py

main.py                   # Orquestación general del pipeline
```

## Componentes principales

### Interfaces (`utils/interface.py`)
Definen el contrato que deben cumplir todas las implementaciones de extracción, carga y transformación:
- `Extractor.extract()`
- `Load.load(df)`
- `Transformer.transform(*args, **kwargs) -> DataFrame`

### Extracción (`extract.py`)
`ServerExtractor` lee una tabla de PostgreSQL vía JDBC usando `SparkSession`, valida que el resultado no esté vacío (lanza `ExtractError` si la fuente no tiene registros) y loguea el schema y la cantidad de filas extraídas.

### Carga (`load.py`)
`ServerLoader` escribe el DataFrame resultante en Parquet (modo `overwrite`) bajo `./output/{tabla}`, capturando cualquier falla como `LoadError`. La dimensión `producto` usa además una variante local con `partitionBy("ProductLine")`.

### Manejo de errores (`utils/classError.py`)
Tres excepciones custom, una por etapa del pipeline: `ExtractError`, `TransformError`, `LoadError`. Cada orquestador (`categoria`, `producto`, `factInternetSales`) las captura de forma específica antes de un catch-all genérico, registrando el error y abortando con `sys.exit(1)`.

### Orquestadores por entidad
Cada dimensión y hecho tiene una clase con método `orq()` que encadena extract → transform → load para su tabla correspondiente (definida en `config.TABLAS`), usando un logger nombrado por proceso (`get_logger(proceso)`).

### Transformaciones
- **categoria**: selección de columnas clave (`ProductCategoryKey`, `EnglishProductCategoryName`).
- **producto**: selección de columnas + limpieza de nulos (`Color`, `ProductLine`, `ListPrice`).
- **factInternetSales**: selección de columnas + cálculo de métricas derivadas (`Margin`, `Balance`).

### `main.py`
Ejecuta el pipeline de forma secuencial: `categoria → subcategoria → producto → factInternetSales`, midiendo la duración total. Incluye (comentado) un modo alternativo de ejecución paralela de las dimensiones con `ThreadPoolExecutor`.

## Tecnologías

- **PySpark** (SparkSession, DataFrame API, JDBC)
- **PostgreSQL** como fuente de datos (AdventureWorksDW)
- **Parquet** como formato de salida
- Logging configurado por proceso vía `config.logging_config`
- Configuración externalizada (`config.config`: `POSTGRES_CONEXION`, `TABLAS`)

## Ejecución

```bash
python main.py
```

Esto corre secuencialmente las dimensiones (`categoria`, `subcategoria`, `producto`) y el hecho (`factInternetSales`), dejando los Parquet resultantes en `./output/`.

## Posibles mejoras

- Activar la ejecución paralela de dimensiones (ya presente, comentada en `main.py`).
- Centralizar la lógica de limpieza de nulos en un helper reutilizable, ya que se repite entre transformadores.
- Agregar tests unitarios para cada `Transformer`.
