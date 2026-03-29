from functools import partial
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from config import GROQ_API_KEY, GROQ_MODEL
from state import State
from tools.search_tool import get_search_tool
from nodes.telegram_node import getTelegram
from nodes.buscar_node import buscar
from nodes.analizar_node import analizar

def build_graph():
    """Construye y compila el grafo LangGraph."""

    # LLMs
    llm = ChatGroq(model=GROQ_MODEL, temperature=0, groq_api_key=GROQ_API_KEY)
    all_tools = [get_search_tool()]
    llm_with_tools = llm.bind_tools(all_tools)

    # Inyección de dependencias — los nodos reciben sus LLMs via partial
    buscar_node   = partial(buscar,   llm_with_tools=llm_with_tools)
    analizar_node = partial(analizar, llm=llm)

    # Construcción del grafo
    builder = StateGraph(State)

    builder.add_node("telegram", getTelegram)
    builder.add_node("buscar",   buscar_node)
    builder.add_node("tools",    ToolNode(tools=all_tools))
    builder.add_node("analizar", analizar_node)

    builder.add_edge(START,        "telegram")
    builder.add_edge("telegram",   "buscar")
    builder.add_conditional_edges("buscar", tools_condition)
    builder.add_edge("tools",      "analizar")
    builder.add_edge("buscar",     "analizar")
    builder.add_edge("analizar",   END)

    return builder.compile()