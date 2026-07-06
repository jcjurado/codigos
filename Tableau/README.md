# Proyecto Tableau — AdventureWorks DW (fuente CSV)

## Contexto

Dashboard construido en Tableau usando el dataset de **AdventureWorks DW 2022**, cargado a partir de archivos **CSV** (tablas de hechos y dimensiones exportadas), en lugar de conexión directa a la base de datos.

---
<img width="942" height="596" alt="image" src="https://github.com/user-attachments/assets/925766bb-2ab9-4724-b5c7-c60625050b09" />

<img width="1003" height="598" alt="image" src="https://github.com/user-attachments/assets/2e4503b7-9de9-421e-bef2-31eed406b953" />

## 1. Modelado de datos

- Carga de múltiples CSV correspondientes a tablas de **hechos** (ej. `FactInternetSales` / ventas) y **dimensiones** (`DimDate`, `DimProduct`, `DimCustomer`, `DimSalesTerritory`, etc.).
- Definición de **relaciones** entre tablas de hechos y dimensiones dentro del modelo de datos de Tableau (Data Model), evaluando cuándo conviene usar **relaciones lógicas** vs. **joins físicos** según el nivel de granularidad y el comportamiento esperado de los cálculos.
- Organización de campos en **carpetas** dentro del panel de datos, separando medidas, atributos de dimensión y campos calculados por categoría, para mantener el modelo prolijo y navegable.
- Creación de **jerarquías** (ej. Categoría > Subcategoría > Producto, o Año > Trimestre > Mes) para habilitar drill-down directo desde la vista.

<img width="1062" height="449" alt="image" src="https://github.com/user-attachments/assets/47819cd3-1c42-488d-a0db-06cc8d0ac2bc" />

---

## 2. Parámetros

- Parámetros creados para controlar la interactividad del dashboard sin depender de filtros de dimensión tradicionales.
- Uso principal: parámetro de **año de análisis** (ej. `Año seleccionado`), que permite comparar el período elegido contra el período anterior sin perder esos datos por un filtro convencional (evita el problema clásico de que el filtro de dimensión "borre" el año anterior antes de que el cálculo lo pueda usar).
- Parámetro adicional para **selección dinámica de medida** (ver punto siguiente).

## 3. Selección de medida vía parámetro

- Parámetro tipo lista con las medidas disponibles (ej. "Ventas", "Cantidad", "Utilidad").
- Campo calculado tipo `switch/CASE` que devuelve la medida correspondiente según el valor del parámetro:

```
CASE [Parámetro Medida]
    WHEN "Ventas" THEN SUM([SalesAmount])
    WHEN "Cantidad" THEN SUM([OrderQuantity])
    WHEN "Utilidad" THEN SUM([Profit])
END
```

- Esto permite que un mismo gráfico cambie de métrica dinámicamente sin duplicar hojas.

## 4. Sets

- Creación de **sets** (fijos y/o dinámicos) sobre dimensiones clave (ej. clientes top por ventas, productos por encima de un umbral, territorios seleccionados).
- Uso de sets como filtro visual, como campo para combinar con otras dimensiones ("in/out" del set), o como insumo para resaltar segmentos específicos dentro de una vista.

## 5. Cálculo YoY (Year over Year)

- Reemplazo del filtro de dimensión por un **filtro calculado booleano**, basado en el parámetro de año, que mantiene visibles tanto el año seleccionado como el anterior:

```
YEAR([OrderDate]) >= [Año seleccionado] - 1
AND YEAR([OrderDate]) <= [Año seleccionado]
```

- Separación de la medida en dos campos calculados (año actual / año anterior) usando `IF` sobre `YEAR([OrderDate])`.
- Cálculo de variación porcentual YoY a partir de ambos campos:

```
(SUM([Ventas Año Actual]) - SUM([Ventas Año Anterior]))
/ SUM([Ventas Año Anterior])
```

- Resultado: al cambiar el parámetro de año, el dashboard recalcula automáticamente la comparación contra el año anterior.

## 6. Drill Through / Navegación entre vistas

- Configuración de una **acción de filtro** entre hojas (equivalente al "drill through" de otras herramientas): al hacer clic sobre una marca en una vista resumen, se filtra automáticamente una hoja de detalle relacionada.
- Uso de **Dashboard Actions** (`Acciones` en el menú de Tableau) para pasar contexto (ej. producto, territorio o fecha seleccionada) desde el dashboard general hacia una vista de detalle.

## 7. Botón de navegación entre reportes

- Incorporación de un objeto **botón** en el dashboard, configurado con una **acción de navegación** (`Ir a hoja` / *Navigation Action*) que lleva de un dashboard a otro dentro del mismo workbook.
- Permite armar una experiencia tipo "menú": desde un dashboard principal, el usuario navega a reportes de detalle específicos con un clic.

---

## Resumen técnico

| Área | Técnica aplicada |
|---|---|
| Modelado | Relaciones vs. joins físicos, carpetas de campos, jerarquías |
| Interactividad | Parámetros (año, selección de medida) |
| Segmentación | Sets fijos y dinámicos |
| Análisis temporal | YoY con filtro calculado booleano + parámetro |
| Navegación | Drill through vía acciones de filtro, botón de navegación entre dashboards |

## Próximos pasos posibles
- Extender el patrón de YoY a QoQ / MTD / YTD con parámetro de fecha de corte.
- Documentar el diccionario de campos calculados (nombre, fórmula, propósito).
- Agregar control de performance si el volumen de filas CSV crece (extractos vs. live).
