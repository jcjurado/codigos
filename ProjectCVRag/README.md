# 🤖Chatbot Personal con RAG


Chatbot personal basado en IA que responde preguntas sobre experiencia, habilidades y proyectos de **Juan Cruz Jurado Auzza**, utilizando Retrieval-Augmented Generation (RAG) sobre documentos propios (CV, resumen profesional, etc.).
## 🧠 ¿Cómo funciona?
1. Al iniciar, el sistema indexa los documentos de la carpeta `docs/` (PDFs y TXTs) en un vector store local con **Chroma**.
2. Cuando el usuario hace una pregunta, el sistema busca los fragmentos más relevantes del CV usando embeddings de **Google Gemini**.
3. El contexto recuperado se inyecta en el mensaje antes de enviarlo al modelo de lenguaje (**Gemini 2.5 Flash**), que responde en primera persona como Juan Cruz.
4. Si el usuario menciona su nombre o empresa, o hace una pregunta que no puede responderse, se disparan herramientas que envían notificaciones push vía **Pushover**.
## 🗂️ Estructura del proyecto
```
chat_rag/
├── app.py              # Interfaz Gradio (punto de entrada)
├── chat.py             # Lógica del chatbot y manejo de herramientas
├── rag.py              # Carga, indexación y búsqueda en vector store
├── tool.py             # Herramientas del agente + cliente OpenAI/Gemini
├── logging_config.py   # Configuración de logs
├── main.py             # Entrypoint alternativo
├── docs/               # Documentos fuente (PDFs, TXTs, imagen de perfil)
├── chroma_db/          # Vector store persistente (se genera automáticamente)
└── requirements.txt    # Dependencias del proyecto
```
## ⚙️ Instalación
### Requisitos
- Python 3.11+
- uv
### 1. Instalar dependencias
```bash
uv sync
# o con pip:
pip install -r requirements.txt
```
### 2. Configurar variables de entorno
Crear un archivo `.env` en la raíz del proyecto:
```env
GOOGLE_API_KEY=tu_api_key_de_google
PUSHOVER_USER=tu_user_key_de_pushover
PUSHOVER_TOKEN=tu_token_de_pushover
```
### 3. Agregar tus documentos
Colocá tus archivos PDF y/o TXT en la carpeta `docs/`. También podés agregar una imagen `docs/imagen.jpg` para la foto de perfil.
## 🚀 Ejecución
```bash
uv run app.py
# o con python directamente:
python app.py
```
## ☁️ Deploy en Hugging Face Spaces
```bash
uv run gradio deploy
```
> **Nota:** Asegurate de tener un `.huggingfaceignore` con las carpetas a excluir:
> ```
> .venv
> .env
> __pycache__
> .git
> chroma_db
> logs
> ```
> ## 🛠️ Tecnologías utilizadas
| Tecnología | Uso |
|---|---|
| [Gradio](https://gradio.app/) | Interfaz de usuario web |
| [LangChain](https://www.langchain.com/) | Pipeline RAG |
| [Chroma](https://www.trychroma.com/) | Vector store local |
| [Google Gemini](https://ai.google.dev/) | Embeddings + LLM |
| [Pushover](https://pushover.net/) | Notificaciones push |
| [uv](https://docs.astral.sh/uv/) | Gestión de entorno y dependencias |
---
