import asyncio
import datetime
import nest_asyncio

from graph.builder import build_graph
from state import State

nest_asyncio.apply()


async def procesar(graph) -> str:
    state: State = {
        "fecha": datetime.datetime.now().strftime("%d-%m-%Y"),
        "mensajes_telegram": "",
        "busquedas_realizadas": 0,
        "messages": [],
    }
    result = await graph.ainvoke(state, config={"recursion_limit": 6})
    return result["messages"][-1].content


def imprimir_resultado(contenido: str) -> None:
    separador = "=" * 60
    titulo = f"  ANÁLISIS FINANCIERO — {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}"
    print(f"\n{separador}\n{titulo}\n{separador}")
    print(contenido)
    print(separador)


async def main():
    graph = build_graph()
    contenido = await procesar(graph)
    imprimir_resultado(contenido)


if __name__ == "__main__":
    asyncio.run(main())