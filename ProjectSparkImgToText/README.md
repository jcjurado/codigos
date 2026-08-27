# Image to Text (OCR) — Conversión de Imágenes a Texto

Script en Python que extrae texto de imágenes (capturas de pantalla, documentos escaneados, dashboards, etc.) usando OCR y lo consolida en un archivo `.txt`.

## 🎯 Motivación

Automatizar la extracción de texto desde imágenes (por ejemplo, capturas de dashboards de BI, reportes o documentos escaneados) para poder indexar, buscar o procesar ese contenido sin transcripción manual.

## 🛠️ Tecnologías

- **Python 3.12**
- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** (motor de reconocimiento óptico de caracteres)
- **[pytesseract](https://pypi.org/project/pytesseract/)** — wrapper de Python para Tesseract
- **[Pillow (PIL)](https://pypi.org/project/Pillow/)** — procesamiento de imágenes
- Desarrollado y probado en **WSL (Windows Subsystem for Linux)**

## ⚙️ Instalación

1. Instalar el motor de OCR y el paquete de idioma español:
   ```bash
   sudo apt update
   sudo apt install tesseract-ocr tesseract-ocr-spa -y
   ```

2. Instalar las dependencias de Python:
   ```bash
   pip install pytesseract Pillow
   ```

3. Verificar la instalación:
   ```bash
   tesseract --version
   tesseract --list-langs   # debe incluir "spa"
   ```

## 🚀 Uso

1. Colocar las imágenes (`.png`, `.jpg`, `.jpeg`) a procesar en una carpeta.
2. Ajustar la ruta de entrada y de salida en el script (`img_dir` y la ruta del archivo `.txt`).
3. Ejecutar:
   ```bash
   python img2txt.py
   ```

El script:
- Detecta todas las imágenes soportadas dentro de la carpeta indicada.
- Aplica OCR en español a cada una.
- Muestra el progreso y el tiempo de procesamiento por imagen en consola.
- Escribe el nombre de cada imagen junto con el texto extraído en un archivo `.txt` consolidado.

## 📋 Ejemplo de salida (consola)

```
Imágenes encontradas: 1
------------------------------
captura_dashboard.jpg
------------------------------
convirtiendo imagen captura_dashboard.jpg......
Indicador
Evolución Mensual
Importe PVP
$ 24.653.398
...
Tiempo de conversión captura_dashboard.jpg: 0:00:00.398781
```

## ⚠️ Limitaciones y notas

- La precisión del OCR depende de la calidad de la imagen (resolución, contraste, ángulo). Imágenes con mucho ruido visual o texto muy pequeño pueden generar errores de reconocimiento.
- El OCR solo extrae texto **visible** en la imagen — no interpreta ni describe contenido visual sin texto (por ejemplo, fotografías sin texto no producen resultados).
- Posibles mejoras futuras:
  - Preprocesamiento de imagen (escala de grises, autocontraste, upscaling) para mejorar precisión.
  - Parametrizar rutas de entrada/salida por línea de comandos.
  - Soporte para múltiples idiomas configurable.
  - Exportar resultados en formato estructurado (JSON/CSV) además de texto plano.

## 👤 Autor

Proyecto desarrollado como parte de práctica de automatización y procesamiento de datos con Python.
