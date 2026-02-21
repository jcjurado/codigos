import os
import requests
from pydantic import BaseModel, Field
from openai import pydantic_function_tool, OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)
openai = OpenAI(api_key=os.getenv("GOOGLE_API_KEY"),base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
model_name = "gemini-2.5-flash"

pushover_user = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url = "https://api.pushover.net/1/messages.json"

class recordUserDetails(BaseModel):
    nombre:str = Field(description="Nombre de la persona o usuario que esta chateando.")
    empresa:str = Field(description="Nombre de la empresa o compania para la cual el usuario trabaja o representa.")

class recordUnknownQuestion(BaseModel):
    question: str = Field(description="La pregunta que no se pudo responder")


class tool:
   
    @staticmethod
    def push(message:str):
        print(f"Mensaje a enviar por push: {message}")
        payload = {"user":pushover_user, "token":pushover_token, "message":message}
        requests.post(pushover_url,data=payload)
    
    @staticmethod
    def record_user_details(nombre, empresa="Nombre no proporcionado"):
        if not empresa or len(empresa.strip()) < 2:
            empresa = "Nombre no proporcionado"
            tool.push(F"Existe alguien que esta chateando. Su nombre es {nombre}, empresa {empresa}")
        else:
            tool.push(F"Existe alguien que esta chateando. Su nombre es {nombre}")
        return {"recorded":"ok"}

    @staticmethod
    def record_unknown_question(question):
        tool.push(f"Registrando pregunta no respondida: {question}")
        return {"recorded":"ok"}
        
    @staticmethod
    def getTools():
        tools = [pydantic_function_tool(
                    model=recordUserDetails,
                    name="record_user_details",
                    description="Utilice esta herramienta cuando el usuario especifico su nombre o apellido."),
                pydantic_function_tool(
                    model=recordUnknownQuestion,
                    name="record_unknown_question")
                ]
        return tools