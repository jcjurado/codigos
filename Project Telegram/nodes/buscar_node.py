from langchain_core.messages import HumanMessage, SystemMessage
from state import State

PROMPT_SISTEMA = """Eres un asistente de investigación financiera.
Analizá el mensaje y decidí qué buscar:
- Si menciona acciones argentinas (YPF, Pampa, etc.) → buscá precio y noticias recientes
- Si menciona commodities (petróleo, soja, oro) → buscá precio actual y contexto
- Si menciona política o geopolítica (guerra, elecciones) → buscá el impacto financiero
Hacé UNA sola búsqueda con tavily_search sobre el tema más relevante."""


async def buscar(state: State, llm_with_tools) -> dict:
    """Busca contexto web sobre el tema del mensaje de Telegram."""
    print("🔎 Buscando contexto en la web...")

    prompt_usuario = f"""Fecha: {state['fecha']}
Mensaje de Telegram:
{state['mensajes_telegram']}

Identificá el tema principal y buscalo en la web. Mencioná la bibliografía o fuente."""

    response = await llm_with_tools.ainvoke([
        SystemMessage(content=PROMPT_SISTEMA),
        HumanMessage(content=prompt_usuario),
    ])
    return {"messages": [response]}