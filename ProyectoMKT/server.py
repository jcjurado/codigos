# server.py (VERSIÓN INTEGRADA CON EL AGENTE)

from flask import Flask, request
from dotenv import load_dotenv
# Importaciones cruciales para el framework de Agentes y SendGrid
from agents import Agent, Runner, function_tool 
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
import asyncio
from typing import Dict

# Cargar variables de entorno (API Keys de OpenAI/Gemini y SendGrid)
load_dotenv(override=True)
# ----------------------------------------------------
# 1. HERRAMIENTA DE ENVÍO DE EMAIL ADAPTADA PARA RESPONDER
# ----------------------------------------------------

def send_reply_email(to_email: str, subject: str, body: str):
    """ Función auxiliar para enviar la respuesta del Agente al remitente. """
    
    # ⚠️ IMPORTANTE: Reemplaza "juangabriel@frogames.es" con TU remitente verificado en SendGrid.
    SENDER = os.environ.get('SENDGRID_VERIFIED_SENDER', "juradojuancruz@gmail.com")
    
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email(SENDER)
        to = To(to_email)
        content = Content("text/plain", body)
        
        # El 'subject' ya viene con el "RE:" agregado desde el inbound_handler.
        mail = Mail(from_email, to, subject, content).get() 
        response = sg.client.mail.send.post(request_body=mail)
        
        print(f"Correo de respuesta enviado. Status: {response.status_code}")
        return {"status": "success", "status_code": response.status_code}
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return {"status": "error", "message": str(e)}

# ----------------------------------------------------
# 2. DEFINICIÓN DE AGENTES Y FLUJO (Copiado de tu 2_lab2.ipynb)
# ----------------------------------------------------

# Instrucciones Agentes de Redacción (Celda 3)
instructions1 = "Eres un agente de ventas que trabaja para ComplAI, una empresa que ofrece una herramienta SaaS para garantizar el cumplimiento de SOC2 y prepararse para auditorías, impulsada por IA. Redactas correos electrónicos en frío profesionales y serios."
instructions2 = "Eres un agente de ventas con sentido del humor y atractivo que trabaja para ComplAI, una empresa que ofrece una herramienta SaaS para garantizar el cumplimiento de SOC2 y prepararse para auditorías, impulsada por IA. Redactas correos electrónicos en frío ingeniosos y atractivos que probablemente obtengan respuesta."
instructions3 = "Eres un agente de ventas muy activo que trabaja para ComplAI, una empresa que ofrece una herramienta SaaS para garantizar el cumplimiento de SOC2 y prepararse para auditorías, impulsada por IA. Redactas correos electrónicos en frío concisos y directos."

# Agentes de Redacción (Celda 4)
sales_agent1 = Agent(name="Agente de ventas profesional", instructions=instructions1, model="gpt-4o-mini")
sales_agent2 = Agent(name="Agente de ventas atractivo", instructions=instructions2, model="gpt-4o-mini")
sales_agent3 = Agent(name="Agente de ventas ocpado", instructions=instructions3, model="gpt-4o-mini")

# Agente Selector (Celda 7)
sales_picker = Agent(
    name="sales_picker",
    instructions="Elige el mejor correo electrónico de ventas en frío entre las opciones disponibles. Imagina que eres un cliente y elige el que probablemente te responda. No des explicaciones; responde solo con el correo electrónico seleccionado.",
    model="gpt-4o-mini"
)

# Convertir Agentes de Redacción a Herramientas para el Manager
description = "Escribe una respuesta de correo electrónico dirigida al cliente."
tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)
sales_picker_tool = sales_picker.as_tool(tool_name="sales_picker", tool_description="Elige el mejor correo de respuesta.")

# Agente Manager Simplificado (Genera el texto final)
sales_manager_instructions = """
Eres un gerente de ventas para ComplAI. El usuario te ha enviado un correo electrónico con una consulta.
Tu tarea es la siguiente:
1. Usa las herramientas 'sales_agent1', 'sales_agent2', y 'sales_agent3' una vez cada una para generar 3 respuestas distintas a la consulta del cliente.
2. Usa la herramienta 'sales_picker' para seleccionar la mejor de las tres respuestas generadas.
3. Devuelve SOLO el texto del mejor correo seleccionado, sin ninguna explicación o texto adicional.
"""

sales_manager = Agent(
    name="Manager de ventas",
    instructions=sales_manager_instructions,
    tools=[tool1, tool2, tool3, sales_picker_tool],
    model="gpt-4o-mini"
)

# ----------------------------------------------------
# 3. LÓGICA DEL FLASK APP CON EL AGENTE INTEGRADO
# ----------------------------------------------------
app = Flask(__name__)

@app.route('/recibir-correo', methods=['POST'])
def inbound_handler():
    # SendGrid envía los datos del correo
    remitente = request.form.get('from') # El correo del cliente
    asunto = request.form.get('subject') # Asunto original
    mensaje_texto = request.form.get('text') # Mensaje del cliente
    
    print("\n" + "="*30)
    print(f"📬 ¡CORREO RECIBIDO EN GODADDY!")
    print(f"De: {remitente}")
    print(f"Asunto: {asunto}")
    print(f"Mensaje:\n{mensaje_texto}")
    print("="*30 + "\n")

    # Lógica del Agente:
    try:
        print("🤖 El Agente de IA está procesando el mensaje...")
        
        # Ejecutar el Manager de Ventas con el cuerpo del email del cliente
        respuesta_ejecucion = asyncio.run(Runner.run(sales_manager, mensaje_texto))
        
        # Obtener el texto final del mejor correo de respuesta
        cuerpo_respuesta = respuesta_ejecucion.final_output
        
        print("--- Respuesta del Agente Generada ---")
        print(cuerpo_respuesta)
        print("--------------------------------------")
        
        # Enviar la respuesta al cliente
        send_reply_email(
            to_email=remitente,
            subject=f"RE: {asunto}",
            body=cuerpo_respuesta
        )
        
        print(f"✅ Respuesta del Agente enviada a {remitente}")

    except Exception as e:
        # Devuelve 200 para evitar que SendGrid reintente el correo.
        print(f"❌ ERROR AL PROCESAR EL CORREO: {e}")
        
    return "Recibido y Procesado", 200

if __name__ == '__main__':
    print("🎧 Servidor escuchando en el puerto 5000...")
    # Ejecutamos el servidor de forma síncrona
    app.run(port=5000)