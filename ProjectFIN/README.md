#  📈 StockPricerque Crew

Proyecto personal sobre agentes usando crewai. Los mismos trabajan para buscar noticias sobre empresas, evalua el mercado y da un veredicto.
Se usa la herramienta PUSH para envia mensajes al celular sobre el veredicto final y genera un documento .md sobre un informe as profundo

Mensaje al celular
<img width="850" height="405" alt="image" src="https://github.com/user-attachments/assets/3abeb52c-74e6-41ff-a4fa-3a9f359f7b1c" />

Informe markdown final

<img width="665" height="606" alt="image" src="https://github.com/user-attachments/assets/aaf7e626-763b-48d7-bc50-5ac341f244ce" />

## 🚀Instalación

Asegúrate de tener Python >=3.10 <3.14 instalado en tu sistema. Este proyecto utiliza [UV](https://docs.astral.sh/uv/) para la gestión de dependencias y paquetes, ofreciendo una experiencia de configuración y ejecución sin complicaciones.

Primero, si aún no lo has hecho, instala uv:
```bash
pip install uv
```
```bash
uv venv --python 3.11
.venv\Scripts\activate
``` 
```bash
uv pip install crewai
```
```bash
crewai create crew <nombre>
```
Luego, navega al directorio de tu proyecto e instala las dependencias:

(Opcional) Ve a la carpeta creada recientemente por crewai. Bloquea las dependencias e instálalas usando el comando CLI:
```bash
crewai install
```
### Personalización

**Agrega tu `XXXX_API_KEY` en el archivo `.env`**

- Modifica `src/stock_pricerque/config/agents.yaml` para definir tus agentes
- Modifica `src/stock_pricerque/config/tasks.yaml` para definir tus tareas
- Modifica `src/stock_pricerque/crew.py` para agregar tu propia lógica, herramientas y argumentos específicos
- Modifica `src/stock_pricerque/main.py` para agregar entradas personalizadas para tus agentes y tareas

## Ejecutar el Proyecto

Para iniciar tu crew de agentes de IA y comenzar la ejecución de tareas, ejecuta esto desde la carpeta raíz de tu proyecto:
```bash
$ crewai run
```

Este comando inicializa el stock_pricerque Crew, ensamblando los agentes y asignándoles tareas según lo definido en tu configuración.

Este ejemplo, sin modificaciones, creará un archivo `.md` con el resultado de una investigación sobre LLMs en la carpeta raíz.

## Entendiendo Crew

El stock_pricerque Crew está compuesto por múltiples agentes de IA, cada uno con roles, objetivos y herramientas únicos. Estos agentes colaboran en una serie de tareas, definidas en `config/tasks.yaml`, aprovechando sus habilidades colectivas para alcanzar objetivos complejos. El archivo `config/agents.yaml` detalla las capacidades y configuraciones de cada agente en tu crew.



