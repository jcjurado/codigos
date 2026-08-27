# PDF to Text — Extracción de Texto desde PDFs

Script en Python que extrae el texto de archivos PDF (documentos, reportes, informes) y lo consolida en un archivo `.txt`, respetando el layout original de cada página.

## 🎯 Motivación

Automatizar la extracción de texto desde documentos PDF para poder indexar, buscar o procesar ese contenido sin transcripción manual, evitando los problemas de fragmentación de texto que generan otras librerías más básicas.

## 🛠️ Tecnologías

- **Python 3.12**
- **[pdfplumber](https://github.com/jsvine/pdfplumber)** — extracción de texto respetando el layout y posicionamiento de cada página
- Desarrollado y probado en **WSL (Windows Subsystem for Linux)**

## ⚙️ Instalación

1. Instalar la dependencia:
   ```bash
   pip install pdfplumber
   ```

2. Verificar la instalación:
   ```bash
   python -c "import pdfplumber; print(pdfplumber.__version__)"
   ```

## 🚀 Uso

1. Colocar los archivos `.pdf` a procesar en una carpeta.
2. Ejecutar el script indicando la carpeta de entrada y la ruta del archivo de salida:
   ```python
   pdf2txt("/ruta/a/pdfs", "/ruta/salida/docpdf.txt")
   ```
   o directamente:
   ```bash
   python pdf2txt.py
   ```

El script:
- Detecta todos los archivos `.pdf` dentro de la carpeta indicada.
- Extrae el texto de cada página, identificando el número de página (`--- Página N ---`).
- Muestra el progreso y el tiempo de procesamiento por archivo en consola.
- Escribe el nombre de cada PDF junto con su texto extraído en un archivo `.txt` consolidado.
- Continúa con el siguiente archivo si uno falla, sin interrumpir el proceso completo.

## 📋 Ejemplo de salida (consola)

```
PDFs encontrados: 1
------------------------------
informe_ventas.pdf
------------------------------
convirtiendo pdf informe_ventas.pdf......

--- Página 1 ---
Introducción

Desde que trabajamos todos en conjunto, los resultados...

Tiempo de conversión informe_ventas.pdf: 0:00:00.412331
```

## ⚠️ Limitaciones y notas

- Solo extrae texto que ya existe digitalmente en el PDF (texto seleccionable). **No funciona con PDFs escaneados** (páginas guardadas como imagen) — para esos casos se necesita un enfoque de OCR (renderizar cada página como imagen y procesarla con `pytesseract`, similar al proyecto Image to Text).
- La calidad de extracción puede variar según cómo el PDF fue generado (texto justificado, columnas, tablas complejas pueden requerir ajustes adicionales).
- Se eligió `pdfplumber` sobre `PyPDF2` porque reconstruye mejor el flujo de texto y evita que cada palabra se interprete como una línea separada, un problema común con extractores más básicos.
- Posibles mejoras futuras:
  - Parametrizar rutas de entrada/salida por línea de comandos.
  - Extracción de tablas con `page.extract_table()`.
  - Exportar resultados en formato estructurado (JSON/CSV) además de texto plano.
  - Detección automática de PDFs escaneados para derivarlos a un flujo de OCR.
