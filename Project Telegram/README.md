# 📊 Telegram Financial Analyzer

Bot de análisis financiero automatizado que extrae mensajes de un canal de Telegram y genera un análisis profesional usando un grafo de agentes con LangGraph y Groq.

---

## 🧠 ¿Qué hace?

1. **Extrae** el último mensaje de un canal de Telegram vía Telethon.
2. **Busca** contexto financiero en la web usando Tavily Search.
3. **Analiza** el mensaje con un LLM (Groq/LLaMA), produciendo un informe estructurado con contexto, impacto en mercados, nivel de riesgo y recomendación concreta.

---

## 🗂️ Estructura del proyecto

```
├── graph              	    
│   ├──builder.py	    # Construcción y compilación del grafo LangGraph
├── state.py                # Definición del estado compartido entre nodos
├── config.py               # Variables de entorno / configuración
├── nodes/
│   ├── telegram_node.py    # Nodo 1: extrae el último mensaje de Telegram
│   ├── buscar_node.py      # Nodo 2: búsqueda web con Tavily
│   └── analizar_node.py    # Nodo 3: redacta el análisis financiero final
├── tools/
│   └── search_tool.py      # Wrapper de TavilySearchResults
└── utils/
    └── helpers.py          # Utilidades: normalización y limpieza de emojis
```

---

## 🔄 Flujo del grafo

```
START
  │
  ▼
[telegram]  →  Extrae el último mensaje del canal
  │
  ▼
[buscar]    →  Decide qué buscar y llama a Tavily
  │
  ├── (si usó tool) ──▶ [tools] ──▶ [analizar]
  │
  └── (si no usó tool) ──────────▶ [analizar]
                                        │
                                        ▼
                                       END
```

El nodo `buscar` usa `tools_condition` de LangGraph para decidir dinámicamente si invocar la herramienta de búsqueda o pasar directamente al análisis.

---

## 🧩 Nodos

### 1. `telegram_node.py` — Extracción de Telegram

Conecta al canal configurado mediante **Telethon** y extrae el texto del último mensaje. Los emojis financieros clave se normalizan en texto legible antes de pasarlos al grafo:

| Emoji | Significado normalizado |
|-------|------------------------|
| 🟢 | (COMPRA, TODO OK) |
| ⚠️ | (ADVERTENCIA) |
| 🔴 | (VENTA, ALERTA, PELIGRO) |

---

### 2. `buscar_node.py` — Búsqueda web contextual

El LLM analiza el mensaje de Telegram y decide qué buscar según el tema detectado:

- **Acciones argentinas** (YPF, Pampa, etc.) → precio y noticias recientes
- **Commodities** (petróleo, soja, oro) → precio actual y contexto
- **Política / geopolítica** (guerras, elecciones) → impacto financiero

Realiza **una sola búsqueda** sobre el tema más relevante usando `tavily_search`.

---

### 3. `analizar_node.py` — Análisis financiero final

Genera un informe estructurado con el siguiente formato obligatorio:

```
📌 TEMA

📰 CONTEXTO

📉📈 IMPACTO EN MERCADOS

⚠️ NIVEL DE RIESGO: [BAJO / MEDIO / ALTO]

💡 OPINIÓN Y RECOMENDACIÓN

📚 FUENTES
```

El LLM actúa con mentalidad de analistas como Buffett, Soros, Lynch y Dalio. Responde siempre en español, de forma directa y sin disclaimers.

---

## ⚙️ Configuración

Creá un archivo `config.py` (o usá variables de entorno) con los siguientes valores:

```python
# Groq
GROQ_API_KEY = "tu_groq_api_key"
GROQ_MODEL   = "llama-3.3-70b-versatile"   # o el modelo que prefieras

# Telegram (via Telethon)
API_ID    = 123456789          # Tu API ID de Telegram
API_HASH  = "tu_api_hash"
CANAL_ID  = 123456789  # ID del canal a monitorear

# Tavily
TAVILY_API_KEY    = "tu_tavily_api_key"
TAVILY_MAX_RESULTS = 3
```

---

## 📦 Instalación

```bash
# 1. Cloná el repositorio
git clone https://github.com/tu-usuario/telegram-financial-analyzer
cd telegram-financial-analyzer

# 2. Creá un entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

# 3. Instalá dependencias
pip install langgraph langchain-groq langchain-community \
            telethon tavily-python emoji
```

---

## 🚀 Uso

```python
import asyncio
from builder import build_graph
from datetime import date

async def main():
    graph = build_graph()
    result = await graph.ainvoke({"fecha": str(date.today())})
    # El análisis final está en el último mensaje del estado
    print(result["messages"][-1].content)

asyncio.run(main())
```

> **Nota:** La primera vez que uses Telethon, te pedirá autenticarte con tu número de teléfono. Esto genera el archivo `session.session` que se reutiliza en ejecuciones posteriores.

---

## 🛠️ Stack tecnológico

| Componente | Tecnología |
|------------|-----------|
| Orquestación de agentes | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM | [Groq](https://groq.com) (LLaMA 3.x) |
| Búsqueda web | [Tavily](https://tavily.com) |
| Cliente Telegram | [Telethon](https://docs.telethon.dev) |
| Normalización de emojis | [emoji](https://pypi.org/project/emoji/) |

---

## 📝 Notas adicionales

- El grafo es **completamente asíncrono** (`async/await`).
- La inyección de dependencias (LLMs) se realiza con `functools.partial`, evitando variables globales.
- `helpers.py` incluye dos funciones: `normalizar_emojis` (para el flujo principal) y `limpiar_emojis` (para exportación a CSV histórico).
- El estado compartido entre nodos se define en `state.py` y contiene: `messages`, `mensajes_telegram` y `fecha`.
