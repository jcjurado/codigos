# 📈 StockPricerque: Inteligencia Colaborativa para Análisis Bursátil

**StockPricerque** es un sistema avanzado de agentes autónomos diseñado para automatizar el análisis financiero y la evaluación de activos. Utilizando el framework **crewAI**, este proyecto coordina múltiples especialistas digitales que colaboran en tiempo real para transformar datos crudos de mercado en informes estratégicos y accionables.

---

## 🚀 Configuración e Instalación

Este proyecto utiliza **UV** para una gestión de dependencias moderna y eficiente, garantizando un entorno de ejecución estable y de alto rendimiento.

### 1. Requisitos de Entorno
* Python **3.10** a **3.13**
* Instalación de UV: Ejecuta **pip install uv** en tu terminal.

### 2. Instalación de la Crew
Clona el repositorio y ejecuta el instalador automático **crewai install** para configurar el entorno virtual y las dependencias necesarias.

### 3. Variables de Entorno
Configura tus credenciales de API en un archivo llamado **.env** en la raíz del proyecto para habilitar el acceso a los modelos de lenguaje:
* **OPENAI_API_KEY**=tu_clave_aqui

---

## 🛠️ Arquitectura de la Solución

A diferencia de las automatizaciones lineales convencionales, **StockPricerque** opera mediante una estructura de agentes con roles especializados que interactúan entre sí:

* **Configuración de Agentes (agents.yaml):** Define las capacidades, roles y "backstory" de cada experto (ej. Analistas de Riesgo, Investigadores de Mercado o Especialistas en Sentimiento).
* **Definición de Tareas (tasks.yaml):** Establece el flujo de trabajo lógico, los criterios de éxito y la secuencia de colaboración entre los agentes.
* **Lógica de Negocio (crew.py):** El núcleo del sistema donde se integran herramientas personalizadas y se orquesta el comportamiento inteligente de la tripulación.
* **Entradas de Datos (main.py):** El punto de acceso principal para definir los parámetros y variables específicos de cada ejecución.

---

## 💻 Ejecución y Resultados

Para activar la tripulación de agentes y comenzar el proceso de investigación y análisis bursátil, ejecuta el comando **crewai run** desde la carpeta raíz.

Al finalizar, el sistema consolidará la inteligencia colectiva en un archivo de salida (por defecto **report.md**), proporcionando una visión integral, técnica y objetiva del mercado o activo analizado.

---

## ⚙️ Adaptación y Escalabilidad

El sistema es altamente modular y permite una personalización profunda para adaptarse a diferentes necesidades financieras:

1. **Nuevos Expertos:** Añade especialistas en sectores específicos modificando **src/stock_pricerque/config/agents.yaml**.
2. **Flujos a Medida:** Ajusta los objetivos y la profundidad del análisis en **src/stock_pricerque/config/tasks.yaml**.
3. **Herramientas Externas:** Integra APIs financieras propietarias o fuentes de datos alternativas dentro de **src/stock_pricerque/crew.py**.

---

## 🌐 Soporte y Ecosistema

Este desarrollo se apoya en la robustez de **crewAI**. Para explorar capacidades avanzadas o resolver dudas técnicas:

* **Documentación Técnica:** Visita docs.crewai.com
* **Repositorio Oficial:** github.com/joaomdmoura/crewai
* **Comunidad:** Únete al Discord oficial de crewAI.

---
**Desarrollado para maximizar la eficiencia en el análisis de datos financieros mediante IA colaborativa.**
