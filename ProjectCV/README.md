
# 🤖AI Portfolio Chat

<img width="901" height="442" alt="image" src="https://github.com/user-attachments/assets/72d08259-86a3-400a-834e->

Chatbot conversacional que simula una entrevista con el candidato. Está entrenado con mi CV y un resumen personal, responde preguntas sobre experiencia y habilidades, y me notifica al celular cuando alguien del otro lado deja su nombre o empresa.

Desplegado en **Hugging Face Spaces** con interfaz **Gradio**.

---

## ¿Cómo funciona?

El bot actúa como "yo" en una conversación con un posible empleador o reclutador. Internamente tiene dos LLMs trabajando en conjunto:

- **Gemini 2.0 Flash** maneja la conversación principal y las herramientas
- **GPT-4o Mini** regenera la respuesta si el evaluador la rechaza

Después de cada respuesta, Gemini actúa también como evaluador (en un rol separado) para decidir si la respuesta fue apropiada. Si no pasa la evaluación, GPT-4o Mini reintenta con el feedback del rechazo como contexto.

```
Usuario escribe
      │
      ▼
Gemini responde  ──►  Gemini evalúa la respuesta
      │                     │
      │              ¿Es aceptable?
      │               Sí ──► se muestra
      │               No ──► GPT-4o reintenta con el feedback
      ▼
Respuesta final al usuario
```

Si en algún momento el usuario menciona su nombre, empresa o teléfono, el bot llama a una herramienta que dispara una **notificación push al celular** vía Pushover.

---

## Tecnologías

- Python 3.12+
- [Gradio](https://gradio.app/) — interfaz del chat
- [OpenAI SDK](https://github.com/openai/openai-python) — usado tanto para OpenAI como para Gemini (vía endpoint compatible)
- [Gemini 2.0 Flash](https://ai.google.dev/) — modelo principal y evaluador
- [GPT-4o Mini](https://platform.openai.com/docs/models) — modelo de respaldo
- [Pushover](https://pushover.net/) — notificaciones push al celular
- [pypdf](https://pypdf.readthedocs.io/) — lectura del CV en PDF
- python-dotenv, pydantic

---

## Estructura

```
portfolio-chat/
├── app.py                  # Toda la lógica del chat, evaluador y herramientas
└── me/
    ├── CV_JuanCruzJurado.pdf   # CV del candidato (fuente de contexto)
    ├── summary.txt             # Resumen personal, hobbies, perfil
    └── avatar.jpg              # Foto de perfil que aparece en el chat
```

---

## Configuración

El proyecto usa variables de entorno para las APIs. Crear un archivo `.env` en la raíz:

```
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=...
PUSHOVER_USER=...
PUSHOVER_TOKEN=...
```

En Hugging Face Spaces estas variables se configuran como **Secrets** en la sección de Settings del Space.

---

## Correrlo localmente

```bash
pip install -r requirements.txt
python app.py
```

Gradio levanta un servidor local y abre la interfaz en el navegador.

---

## Herramientas del agente

El bot tiene dos herramientas que puede invocar durante la conversación:

**`record_user_details`** — se activa cuando el usuario menciona su nombre, empresa o teléfono. Registra los datos y envía un push al celular con la información del contacto.

**`record_unknown_question`** — se activa cuando el bot no puede responder algo. Registra la pregunta y también envía un push, para saber qué preguntas quedan sin cubrir en el contexto.

---

## Cosas a tener en cuenta

- El CV se lee en tiempo de inicialización. Cualquier cambio al PDF requiere reiniciar la app.
- El evaluador usa `response_format=Evaluation` con Pydantic para forzar una respuesta estructurada (`is_acceptable` + `feedback`). Si el modelo no soporta structured outputs esto falla.
- En Hugging Face el archivo `app.py` tiene que estar en la raíz del Space y Gradio tiene que terminar con `demo.launch()` sin parámetros de host/port para que el entorno lo detecte correctamente.
- Este proyecto es una prueba de concepto. El contexto del bot está hardcodeado con nombre y archivos específicos; para adaptarlo a otro candidato basta con cambiar `self.name` y los archivos en la carpeta `me/`.

2f6d4ddbfdb8" />

