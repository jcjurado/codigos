from langchain_core.messages import HumanMessage
from state import State

FORMATO_ANALISIS = """
📌 TEMA: [nombre del tema en una línea]

📰 CONTEXTO
[Explicá qué está pasando. 2-4 oraciones claras y directas.]

📉📈 IMPACTO EN MERCADOS
[Qué sectores, activos o instrumentos se ven afectados y cómo.
Mencioná nombres concretos: acciones, bonos, commodities, divisas.]

⚠️ NIVEL DE RIESGO: [BAJO / MEDIO / ALTO]
[Una oración justificando el nivel.]

💡 OPINIÓN Y RECOMENDACIÓN
[Tu visión directa como asesor. Decí concretamente si comprar, vender, esperar o diversificar.
Mencioná activos o instrumentos específicos cuando sea posible.]

📚 FUENTES
[Mencioná dónde buscaste en la web.]
"""

REGLAS = """Eres un experto analista financiero con mentalidad de Buffett, Soros, Lynch y Dalio.

REGLAS:
- Respondé SIEMPRE en español.
- Sé directo y concreto. Sin disclaimers. Sin "consultá un asesor" o " La información proporcionada es solo una opinión" o "no debe considerarse como 
asesoramiento financiero". Vos SOS el asesor.
- Si no hay suficiente información web, usá tu conocimiento financiero para completar.
"""


def _extraer_contexto_web(messages: list, max_chars: int = 800) -> str:
    """Extrae y trunca el texto útil del historial de mensajes."""
    textos = []
    for m in messages:
        if hasattr(m, "content") and m.content:
            textos.append(str(m.content)[:500])
    return "\n".join(textos)[:max_chars]


async def analizar(state: State, llm) -> dict:
    """Redacta el análisis financiero final sin acceso a tools."""
    print("📊 Redactando análisis...")

    contexto_web = _extraer_contexto_web(state["messages"])

    prompt = f"""{REGLAS}

FORMATO OBLIGATORIO:{FORMATO_ANALISIS}

---
Mensaje de Telegram:
{state['mensajes_telegram']}

Contexto web:
{contexto_web}

Fecha: {state['fecha']}"""

    response = await llm.ainvoke([HumanMessage(content=prompt)])
    return {"messages": [response]}