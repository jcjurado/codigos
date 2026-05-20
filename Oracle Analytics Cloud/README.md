# 📊 Oracle Analytics Cloud — Data Warehouse con Mapas de Argentina

> Proyecto de Business Intelligence end-to-end sobre Oracle Cloud Infrastructure: modelado dimensional, ETL desde el esquema de ejemplo **SH**, visualizaciones geoespaciales con GeoJSON de provincias argentinas y dashboards interactivos en **OAC**.

---

## 🗂️ Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Dashboards en OAC](#dashboards-en-oac)
- [Arquitectura](#arquitectura)
- [Stack Tecnológico](#stack-tecnológico)
- [Esquema Fuente: SH](#esquema-fuente-sh)
- [Esquema Destino: DW\_SH](#esquema-destino-dw_sh)
- [Mapas con GeoJSON de Argentina](#mapas-con-geojson-de-argentina)

---

## Descripción General

Este proyecto implementa una solución completa de **Data Warehouse y Analytics** sobre Oracle Cloud, tomando como fuente el esquema de ejemplo **SH (Sales History)** de Oracle y transformándolo en un esquema dimensional propio llamado **DW\_SH**.

El objetivo es analizar ventas, clientes, productos, promociones y canales de distribución, con soporte de **visualización geográfica** a nivel de provincias argentinas mediante capas GeoJSON personalizadas en Oracle Analytics Cloud.

---

## Dashboards en OAC
### Tableros
<img width="1339" height="691" alt="image" src="https://github.com/user-attachments/assets/2e92a634-863a-4326-beeb-813b574c4c31" />

<img width="1355" height="697" alt="image" src="https://github.com/user-attachments/assets/411f5f99-7dfe-4b96-89a2-ab6f65d7c75f" />

<img width="1082" height="655" alt="image" src="https://github.com/user-attachments/assets/875fa1cf-4459-471c-9918-400c52233fc4" />

<img width="1075" height="697" alt="image" src="https://github.com/user-attachments/assets/67e1c3d4-021c-4202-9fda-759b6e02ea58" />

### Modelo Semantico
#### Capa Fisica
<img width="298" height="539" alt="image" src="https://github.com/user-attachments/assets/a8861dc0-f655-42dc-a89c-eb6d56444eae" />
#### Capa de Negocio
<img width="1008" height="644" alt="image" src="https://github.com/user-attachments/assets/c4ac85fe-62a9-4f0b-8213-de76a91c623b" />
#### Capa de Presentacion
<img width="981" height="434" alt="image" src="https://github.com/user-attachments/assets/48100f9f-8013-485f-a439-2c3cdd0631d8" />

---

## Arquitectura

```
┌──────────────────────────────────────────────────────────────────┐
│                    Oracle Cloud Infrastructure                   │
│                                                                  │
│   ┌─────────────┐     ETL / SQL      ┌──────────────────────┐   │
│   │  Esquema SH │ ─────────────────► │  Esquema DW_SH       │   │
│   │  (fuente)   │                    │  (destino / DW)      │   │
│   └─────────────┘                    └──────────┬───────────┘   │
│         │                                       │               │
│   Autonomous Database (ATP/ADW)                 │               │
│                                           Conexión JDBC         │
│                                                 │               │
│                                    ┌────────────▼────────────┐  │
│                                    │  Oracle Analytics Cloud  │  │
│                                    │  (OAC)                  │  │
│                                    │  · Datasets             │  │
│                                    │  · Mapas + GeoJSON ARG  │  │
│                                    │  · Dashboards           │  │
│                                    └─────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Base de datos | Oracle Autonomous Database (ADW) |
| Analítica | Oracle Analytics Cloud (OAC) |
| Esquema fuente | Oracle Sample Schema **SH** |
| Modelado | Dimensional (Star Schema) |
| Mapas | GeoJSON — Provincias de Argentina |
| Lenguaje ETL | SQL |
| Infraestructura | Oracle Cloud Infrastructure (OCI) |

---

## Esquema Fuente: SH

El esquema **SH (Sales History)** es el esquema de ejemplo incluido en Oracle Database, diseñado para demostrar capacidades OLAP y de reporting. Contiene datos históricos de ventas de una empresa ficticia.

### Tablas principales utilizadas

| Tabla | Descripción |
|---|---|
| `SALES` | Hechos de ventas (cantidad, importe, descuentos) |
| `CUSTOMERS` | Datos de clientes (nombre, región, demografía) |
| `PRODUCTS` | Catálogo de productos con categoría y subcategoría |
| `PROMOTIONS` | Campañas y tipos de promoción aplicados |
| `CHANNELS` | Canales de distribución (online, directo, partners) |
| `COUNTRIES` | Países y regiones de los clientes |
| `TIMES` | Dimensión tiempo (día, semana, mes, trimestre, año) |

---

## Esquema Destino: DW\_SH

El esquema **DW\_SH** es el data warehouse propio creado en la Autonomous Database. Sigue un modelo dimensional en **estrella (Star Schema)**, con tablas de dimensiones desnormalizadas y una tabla de hechos central.

### Modelo dimensional

```
                        ┌──────────────────┐
                        │   DIM_TIEMPO     │
                        │  PK: tiempo_id   │
                        └────────┬─────────┘
                                 │
  ┌──────────────┐     ┌─────────▼──────────┐     ┌──────────────────┐
  │ DIM_CANAL    │     │    FACT_VENTAS      │     │  DIM_PRODUCTO    │
  │ PK: canal_id ├────►│  FK: canal_id      │◄────│  PK: producto_id │
  └──────────────┘     │  FK: cliente_id    │     └──────────────────┘
                        │  FK: producto_id   │
  ┌──────────────┐     │  FK: promocion_id  │     ┌──────────────────┐
  │ DIM_CLIENTE  ├────►│  FK: pais_id       │◄────│  DIM_PROMOCION   │
  │ PK: clie_id  │     │  FK: tiempo_id     │     │  PK: promo_id    │
  └──────────────┘     │  ── ── ── ── ──    │     └──────────────────┘
                        │  cantidad          │
  ┌──────────────┐     │  importe           │
  │  DIM_PAIS    ├────►│  costo             │
  │  PK: pais_id │     │  descuento         │
  └──────────────┘     └────────────────────┘
```

### Tablas del esquema DW\_SH

#### `DIM_CANAL`
```sql
CREATE TABLE DW_SH.DIM_CANAL (
    canal_id        NUMBER        PRIMARY KEY,
    canal_desc      VARCHAR2(20)  NOT NULL,
    canal_clase     VARCHAR2(20),
    canal_total     VARCHAR2(13)
);
```

#### `DIM_CLIENTE`
```sql
CREATE TABLE DW_SH.DIM_CLIENTE (
    cliente_id      NUMBER        PRIMARY KEY,
    nombre          VARCHAR2(100),
    apellido        VARCHAR2(100),
    genero          CHAR(1),
    nivel_ingreso   VARCHAR2(30),
    nivel_educacion VARCHAR2(30),
    estado_civil    VARCHAR2(20),
    ocupacion       VARCHAR2(30),
    pais_id         NUMBER,
    ciudad          VARCHAR2(30),
    provincia       VARCHAR2(40),  -- clave para mapas GeoJSON
    CONSTRAINT fk_cliente_pais FOREIGN KEY (pais_id) REFERENCES DW_SH.DIM_PAIS(pais_id)
);
```

#### `DIM_PRODUCTO`
```sql
CREATE TABLE DW_SH.DIM_PRODUCTO (
    producto_id         NUMBER        PRIMARY KEY,
    descripcion         VARCHAR2(50),
    subcategoria        VARCHAR2(50),
    categoria           VARCHAR2(50),
    peso_clase          VARCHAR2(10),
    unidad_precio       NUMBER(8,2),
    unidad_costo        NUMBER(8,2),
    estado              VARCHAR2(20)
);
```

#### `DIM_PROMOCION`
```sql
CREATE TABLE DW_SH.DIM_PROMOCION (
    promocion_id        NUMBER        PRIMARY KEY,
    nombre              VARCHAR2(30),
    subcategoria        VARCHAR2(30),
    categoria           VARCHAR2(30),
    costo               NUMBER(10,2),
    fecha_inicio        DATE,
    fecha_fin           DATE
);
```

#### `DIM_PAIS`
```sql
CREATE TABLE DW_SH.DIM_PAIS (
    pais_id             NUMBER        PRIMARY KEY,
    iso_codigo          CHAR(2),
    nombre              VARCHAR2(40),
    subregion           VARCHAR2(30),
    region              VARCHAR2(20),
    total_paises        VARCHAR2(11)
);
```

#### `DIM_TIEMPO`
```sql
CREATE TABLE DW_SH.DIM_TIEMPO (
    tiempo_id           NUMBER        PRIMARY KEY,
    dia_fecha           DATE,
    dia_nombre          VARCHAR2(9),
    dia_numero          NUMBER,
    semana_numero       NUMBER,
    mes_numero          NUMBER,
    mes_nombre          VARCHAR2(9),
    trimestre_numero    NUMBER,
    trimestre_nombre    VARCHAR2(2),
    anio                NUMBER,
    anio_semana         VARCHAR2(7),
    anio_mes            VARCHAR2(7),
    anio_trimestre      VARCHAR2(7)
);
```

#### `FACT_VENTAS`
```sql
CREATE TABLE DW_SH.FACT_VENTAS (
    venta_id            NUMBER        PRIMARY KEY,
    producto_id         NUMBER        NOT NULL,
    cliente_id          NUMBER        NOT NULL,
    promocion_id        NUMBER        NOT NULL,
    canal_id            NUMBER        NOT NULL,
    tiempo_id           NUMBER        NOT NULL,
    pais_id             NUMBER        NOT NULL,
    cantidad            NUMBER        NOT NULL,
    importe_venta       NUMBER(10,2)  NOT NULL,
    importe_costo       NUMBER(10,2),
    CONSTRAINT fk_v_producto  FOREIGN KEY (producto_id)  REFERENCES DW_SH.DIM_PRODUCTO(producto_id),
    CONSTRAINT fk_v_cliente   FOREIGN KEY (cliente_id)   REFERENCES DW_SH.DIM_CLIENTE(cliente_id),
    CONSTRAINT fk_v_promocion FOREIGN KEY (promocion_id) REFERENCES DW_SH.DIM_PROMOCION(promocion_id),
    CONSTRAINT fk_v_canal     FOREIGN KEY (canal_id)     REFERENCES DW_SH.DIM_CANAL(canal_id),
    CONSTRAINT fk_v_tiempo    FOREIGN KEY (tiempo_id)    REFERENCES DW_SH.DIM_TIEMPO(tiempo_id),
    CONSTRAINT fk_v_pais      FOREIGN KEY (pais_id)      REFERENCES DW_SH.DIM_PAIS(pais_id)
);
```

### ETL: carga desde SH → DW\_SH

El proceso de carga se realiza mediante scripts SQL que transforman y cargan cada dimensión antes de poblar la tabla de hechos.

```sql
-- Ejemplo: carga de DIM_CANAL desde SH
INSERT INTO DW_SH.DIM_CANAL (canal_id, canal_desc, canal_clase, canal_total)
SELECT
    channel_id,
    channel_desc,
    channel_class,
    channel_total
FROM SH.CHANNELS;

-- Ejemplo: carga de FACT_VENTAS desde SH.SALES
INSERT INTO DW_SH.FACT_VENTAS (
    venta_id, producto_id, cliente_id, promocion_id,
    canal_id, tiempo_id, pais_id, cantidad, importe_venta, importe_costo
)
SELECT
    ROWNUM,
    s.prod_id,
    s.cust_id,
    s.promo_id,
    s.channel_id,
    s.time_id,
    c.country_id,
    s.quantity_sold,
    s.amount_sold,
    p.prod_cost * s.quantity_sold
FROM SH.SALES s
JOIN SH.CUSTOMERS c ON s.cust_id = c.cust_id
JOIN SH.PRODUCTS  p ON s.prod_id = p.prod_id;
```

---

## Mapas con GeoJSON de Argentina

Una de las funcionalidades destacadas del proyecto es la integración de **capas geoespaciales** en OAC usando un archivo GeoJSON con los polígonos de las **23 provincias y CABA** de Argentina.

### Configuración en OAC

1. **Subir el archivo GeoJSON** al repositorio de mapas de OAC (sección *Map Layers* en la consola de administración).
2. **Definir la clave de unión**: el campo `provincia` de `DIM_CLIENTE` se vincula con la propiedad `nombre` del GeoJSON.
3. **Crear la capa** en el canvas de OAC como tipo *Map* y asignar la métrica (ej. `SUM(importe_venta)`).

### Estructura del GeoJSON (fragmento)

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "nombre": "Córdoba",
        "iso": "AR-X",
        "region": "Centro"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [ [ [-65.1, -29.0], ["..."] ] ]
      }
    }
  ]
}
```

### Métricas visualizadas en el mapa

- Ventas totales por provincia (mapa de calor coroplético)
- Cantidad de clientes por provincia
- Ticket promedio por provincia
- Comparativa interanual por región geográfica

---

> *Proyecto desarrollado con fines de aprendizaje y demostración de capacidades en Oracle Cloud, modelado dimensional y Business Intelligence.*
