# 📊 Sales Analytics Dashboard — AdventureWorks 2022

Dashboard de análisis de ventas construido en **Power BI** sobre la base de datos **AdventureWorks2022**, con infraestructura de datos en Docker y publicación en Power BI Service / Microsoft Fabric.

---

## 🛠️ Herramientas y tecnologías

| Herramienta | Uso |
|---|---|
| Power BI Desktop | Modelado de datos, creación de medidas DAX y diseño del informe |
| Power BI Service / Microsoft Fabric | Publicación y acceso al dashboard en la nube |
| Docker + SQL Server | Contenedor con la instancia de SQL Server y la base de datos AdventureWorks2022 |
| On-premises Data Gateway | Conexión entre el SQL Server local (Docker) y Power BI Service |

---

## ⚙️ Configuración del entorno

### 1. Levantar SQL Server con Docker

```bash
docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=TuPassword123" \
  -p 1433:1433 --name sqlserver \
  -d mcr.microsoft.com/mssql/server:2022-latest
```

### 2. Restaurar la base de datos AdventureWorks2022

Descargar el backup desde el repositorio oficial de Microsoft y restaurarlo:

```sql
RESTORE DATABASE AdventureWorks2022
FROM DISK = '/ruta/AdventureWorks2022.bak'
WITH MOVE 'AdventureWorks2022' TO '/var/opt/mssql/data/AdventureWorks2022.mdf',
     MOVE 'AdventureWorks2022_Log' TO '/var/opt/mssql/data/AdventureWorks2022.ldf';
```

### 3. Instalar el On-premises Data Gateway

1. Descargar el gateway desde [aka.ms/datagateway](https://aka.ms/datagateway).
2. Instalar y configurar en la misma máquina donde corre Docker.
3. Registrar el gateway en Power BI Service bajo **Configuración → Administrar gateways**.
4. Agregar la fuente de datos apuntando al SQL Server en `localhost,1433`.

---

## 🗂️ Modelo de datos

El modelo sigue una arquitectura de **esquema estrella** con una tabla de hechos central y seis dimensiones.

```
                    Dim_Productos
                         │
   Dim_Customer ── Fact_SalesOrderDetail ── Dim_SalesTerritory
                         │
              Dim_CreditCard   Dim_ShipMethod
```

### Tabla de hechos

| Tabla | Descripción |
|---|---|
| `Fact_SalesOrderDetail` | Combinación de `Sales.SalesOrderDetail` y `Sales.SalesOrderHeader`. Contiene el detalle de cada línea de pedido junto con la información de cabecera (fecha, estado, territorio, cliente, etc.) |

### Dimensiones

| Dimensión | Tablas de origen | Descripción |
|---|---|---|
| `Dim_Productos` | `Production.Product` + `Production.ProductSubcategory` + `Production.ProductCategory` | Jerarquía completa de productos: categoría → subcategoría → producto |
| `Dim_Customer` | `Sales.Customer` | Información de clientes |
| `Dim_CreditCard` | `Sales.CreditCard` | Tipo de tarjeta de crédito usada en la venta |
| `Dim_ShipMethod` | `Purchasing.ShipMethod` | Método de envío |
| `Dim_SalesTerritory` | `Sales.SalesTerritory` | Territorio y región de la venta |

---

## 🔄 Proceso de transformación (Power Query)

- **`Fact_SalesOrderDetail`**: merge entre `Sales.SalesOrderDetail` (detalle de líneas) y `Sales.SalesOrderHeader` (cabecera de la orden) usando `SalesOrderID` como clave de unión.
- **`Dim_Productos`**: merge en cadena de `Product` → `ProductSubcategory` → `ProductCategory`, consolidando la jerarquía en una única tabla desnormalizada.
- Las demás dimensiones se cargaron directamente desde sus tablas de origen con limpieza de columnas innecesarias.

---

## 📁 Estructura del proyecto

```
📦 sales-analytics-powerbi
 ┣ 📄 SalesAnalytics.pbix       # Archivo principal de Power BI
 ┗ 📄 README.md
```

---

## 🚀 Cómo usar el proyecto

1. Clonar o descargar este repositorio.
2. Levantar el contenedor Docker con SQL Server y restaurar AdventureWorks2022 (ver pasos arriba).
3. Instalar y configurar el On-premises Data Gateway.
4. Abrir `SalesAnalytics.pbix` en Power BI Desktop.
5. Actualizar la cadena de conexión apuntando a `localhost,1433`.
6. Publicar en Power BI Service y asociar el dataset al gateway configurado.

---

## 📌 Notas

- La contraseña del contenedor Docker debe cambiarse por una segura antes de usar en producción.
- El gateway debe estar activo en la máquina local para que la actualización automática del dataset funcione en Power BI Service.
