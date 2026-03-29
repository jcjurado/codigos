# ETL Covid-19 con Python

Pipeline ETL que toma datos de COVID-19 desde **PostgreSQL**, los transforma con Pandas y los carga en **MySQL**. El proyecto nació como ejercicio personal y hoy lo uso como plantilla base para otros procesos de integración.

---

## ¿Qué hace?

Extrae dos tablas (`covid_cases` y `vaccination_data`) desde una base PostgreSQL, las combina en un único dataset consolidado y lo escribe en la tabla `covid_country_summary` en MySQL. Simple, pero cubre los patrones que más se repiten en proyectos reales.

---

## Tecnologías

- Python 3.9+
- Pandas + SQLAlchemy
- PostgreSQL y MySQL corriendo en **Docker Desktop** (Windows)
- python-dotenv para las credenciales

---

## Estructura

```
etl-covid/
├── extract
    ├── extract.py
├── transform
    ├── transform.py
├── load
    ├── load.py
├── config
    ├── base_config.py       # Conexiones a PostgreSQL y MySQL
├── Orq_Etl.py      # Orquestador, acá se configura qué tablas entran y cuál es el destino
├── logging_config.py    # Logger con salida a consola y archivo
└── logs/                # Se genera solo al correr el script
```

---

## Modelo de datos

### Tablas fuente — PostgreSQL

**`covid_cases`**

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | SERIAL PK | — |
| `country` | VARCHAR(100) | País |
| `report_date` | DATE | Fecha del reporte |
| `new_cases` | INTEGER | Nuevos casos diarios |
| `new_deaths` | INTEGER | Nuevas muertes diarias |

**`vaccination_data`**

| Columna | Tipo | Descripción |
|---|---|---|
| `id` | SERIAL PK | — |
| `country` | VARCHAR(100) | País |
| `report_date` | DATE | — |
| `new_vaccinations` | INTEGER | Vacunaciones del día |
| `total_vaccinations` | INTEGER | Acumulado |

### Tabla destino — MySQL

**`covid_country_summary`**

| Columna | Tipo |
|---|---|
| `id` | INT PK |
| `country` | VARCHAR(100) |
| `report_date` | DATE |
| `new_cases` | INT |
| `new_deaths` | INT |
| `new_vaccinations` | INT |
| `mortality_rate` | DECIMAL(10,4) |
| `vaccination_ratio` | DECIMAL(10,4) |
| `created_at` | TIMESTAMP |

---

## Cómo correrlo

### 1. Levantar las bases con Docker Desktop

```bash
# PostgreSQL
docker run --name pg_covid \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15

# MySQL
docker run --name mysql_covid \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=prueba_conexion \
  -p 3306:3306 \
  -d mysql:8
```

### 2. Cargar los datos de prueba

Los scripts DDL y DML están en `datos_prueba.txt`, separados por secciones. Ejecutar primero los de PostgreSQL (tablas fuente) y después los de MySQL (tabla destino vacía).

```bash
# PostgreSQL
docker exec -i pg_covid psql -U postgres -d postgres < datos_prueba_pg.sql

# MySQL
docker exec -i mysql_covid mysql -u root -proot prueba_conexion < datos_prueba_mysql.sql
```

### 3. Configurar credenciales

Crear un archivo `.env` en la raíz con este contenido:

```
PG_USER=postgres
PG_PASS=postgres
PG_HOST=localhost
PG_PORT=5432

MYSQL_USER=root
MYSQL_PASS=root
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

### 4. Instalar dependencias y ejecutar

```bash
pip install -r requirements.txt
mkdir logs
python main.py
```

---

## Módulos

**`Orq_Etl.py`** — Define las tablas a extraer y la tabla destino, y llama a las tres etapas en orden. Si querés adaptar el pipeline a otro proyecto, este es el archivo que más vas a tocar.

**`extract.py`** — Realiza la carga de los datos de origen.

**`transform_.py`** — La función `transform_setData()` hace el merge entre los dos datasets por `ID`, descarta nulos y normaliza los nombres de columnas duplicadas. Se puede adaptar de acuerdo a las necesidades

**`load.py`** — Realiza la carga de datos a destino.

**`base_config.py`** — Clase `Base` con un método por motor. Fácil de extender si necesitás agregar SQL Server u otro.

**`logging_config.py`** — Logger con salida simultánea a consola y a un archivo con timestamp en `logs/`. Se inicializa una sola vez gracias al chequeo `hasHandlers()`.

---

## Logs

Cada ejecución genera un archivo en `logs/` con el nombre `etl_covid_YYYYMMDD_HHMMSS.log`. El formato de cada línea es:

```
2024-01-15 10:23:01 | INFO     | Etl_Covid | ✅ Conexión a la base de datos exitosa
```

---

## Usar como plantilla

El flujo está pensado para ser fácil de reutilizar:

- **Cambiar las tablas fuente o destino** → modificar las listas `tablas` y `tabla_destino` en `main.py`
- **Invertir el flujo** (extraer de MySQL, cargar en PostgreSQL) → intercambiar los engines en `main.py`, sin tocar nada más
- **Agregar transformaciones** → extender la clase `transform_covid` en `procesos_etl.py`
- **Nuevo motor de base de datos** → agregar un método en `base_config.py` siguiendo el mismo patrón

---

## Cosas a tener en cuenta

- `load()` usa `if_exists='replace'`, o sea que **recrea la tabla destino en cada ejecución**. Cambiar a `'append'` si se necesita carga incremental.
- El merge en `transform_setData()` es `inner`, así que registros sin par en el otro dataset no van a aparecer en el resultado. Revisar si `'left'` o `'outer'` tiene más sentido según el caso.
- La carpeta `logs/` tiene que existir antes de la primera ejecución. Con `mkdir logs` alcanza.
