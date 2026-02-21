import json
from tool import openai, model_name, tool
from rag import RAG


class chat:

    def __init__(self) -> None:
        # El vector store se carga UNA sola vez al arrancar
        self.rag = RAG()

        # System prompt mínimo: solo rol y comportamiento, SIN datos del perfil
        # Los datos vienen del vector store en cada turno
        self.system_prompt = """Eres Juan Cruz Jurado Auzza. Estás en tu propio sitio web personal respondiendo en primera persona.
REGLAS ESTRICTAS:
- Respondés ÚNICAMENTE con información que esté en el contexto provisto (fragmentos de tu CV y summary).
- Si la información NO está en el contexto, NO la inventes. En ese caso usá la herramienta record_unknown_question y decile al usuario que no tenés esa información disponible.
- Nunca agregues tecnologías, experiencias, habilidades o datos que no figuren explícitamente en el contexto.
- Respondés en primera persona: "yo", "mi", "mis".
- Nunca digas que eres una IA. Simplemente sos Juan Cruz.
- Sé profesional, amable y directo, como si hablaras con un reclutador o futuro empleador.
- Si el usuario menciona su nombre o empresa, usá la herramienta record_user_details.
"""
        self.funciones = {
            "record_user_details": tool.record_user_details,
            "record_unknown_question": tool.record_unknown_question,
        }

    def build_user_message(self, message: str) -> str:
        """
        Enriquece el mensaje del usuario con contexto RAG.
        El LLM recibe: los fragmentos relevantes + la pregunta original.
        """
        contexto = self.rag.buscar(message)

        if contexto:
            return (
                f"## Información de mi CV y documentos (usala para responder en primera persona):\n"
                f"{contexto}\n\n"
                f"---\n"
                f"## Pregunta del usuario:\n{message}"
            )
        else:
            # Sin contexto relevante, igual pasa la pregunta
            # El LLM usará record_unknown_question si no puede responder
            return message

    def handle_tool_calls(self, tool_calls):
        messages = []
        for tc in tool_calls:
            tool_name = tc.function.name
            arguments = json.loads(tc.function.arguments)
            print(f"Herramienta llamada: {tool_name}")
            print(f"Argumentos usados:   {arguments}")

            function_name = self.funciones.get(tool_name)
            result = function_name(**arguments) if function_name else {}
            messages.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tc.id
            })
        return messages

    def chatbot(self, message: str, history):
        # Mensaje del usuario enriquecido con contexto RAG
        enriched_message = self.build_user_message(message)

        messages = (
            [{"role": "system", "content": self.system_prompt}]
            + history
            + [{"role": "user", "content": enriched_message}]
        )

        while True:
            response = openai.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=tool.getTools()
            )

            choice = response.choices[0]
            print(f"finish_reason: {choice.finish_reason}")

            if choice.message.tool_calls:
                tool_results = self.handle_tool_calls(choice.message.tool_calls)
                messages.append(choice.message)
                messages.extend(tool_results)
            else:
                break

        return response.choices[0].message.content