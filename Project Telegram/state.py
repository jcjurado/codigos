from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    fecha: str
    mensajes_telegram: str
    busquedas_realizadas: int
    messages: Annotated[list, add_messages]