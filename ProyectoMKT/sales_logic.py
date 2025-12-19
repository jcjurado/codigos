"""
Sistema de Agentes de Ventas Automatizado para ComplAI
Envía correos de ventas en frío usando múltiples agentes especializados
"""

from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from typing import Dict
import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content
import asyncio

# Configuración
load_dotenv(override=True)

class SalesAgentsConfig:
    """Configuración centralizada para los agentes de ventas"""
    
    COMPANY_CONTEXT = (
        "Eres un agente de ventas que trabaja para ComplAI, "
        "una empresa que ofrece una herramienta SaaS para garantizar "
        "el cumplimiento de SOC2 y prepararse para auditorías, impulsada por IA."
    )
    
    # Instrucciones específicas para cada agente
    PROFESSIONAL_INSTRUCTIONS = (
        f"{COMPANY_CONTEXT} "
        "Redactas correos electrónicos en frío profesionales y serios."
    )
    
    ENGAGING_INSTRUCTIONS = (
        f"{COMPANY_CONTEXT} "
        "Redactas correos electrónicos en frío ingeniosos y atractivos "
        "que probablemente obtengan respuesta."
    )
    
    DIRECT_INSTRUCTIONS = (
        f"{COMPANY_CONTEXT} "
        "Redactas correos electrónicos en frío concisos y directos."
    )
    
    # Configuración de modelo
    MODEL = "gpt-4o-mini"


class EmailConfig:
    """Configuración para el envío de emails"""
    
    SENDER_EMAIL = "ventas@juanlabor.site"
    RECIPIENT_EMAIL = "juradojuancruz@gmail.com"
    
    SUBJECT_WRITER_INSTRUCTIONS = (
        "Puedes escribir un asunto para un correo electrónico de ventas en frío. "
        "Se te proporciona un mensaje y necesitas escribir un asunto "
        "para un correo electrónico que probablemente obtenga respuesta."
    )
    
    HTML_CONVERTER_INSTRUCTIONS = (
        "Puedes convertir un cuerpo de correo electrónico de texto a HTML. "
        "Se te proporciona un cuerpo de correo electrónico de texto que puede tener algún markdown "
        "y necesitas convertirlo a un cuerpo de correo electrónico HTML "
        "con un diseño simple, claro y atractivo."
    )


def create_sales_agents():
    """Crea y retorna los tres agentes especializados en ventas"""
    
    professional_agent = Agent(
        name="Agente de Ventas Profesional",
        instructions=SalesAgentsConfig.PROFESSIONAL_INSTRUCTIONS,
        model=SalesAgentsConfig.MODEL
    )
    
    engaging_agent = Agent(
        name="Agente de Ventas Atractivo", 
        instructions=SalesAgentsConfig.ENGAGING_INSTRUCTIONS,
        model=SalesAgentsConfig.MODEL
    )
    
    direct_agent = Agent(
        name="Agente de Ventas Directo",
        instructions=SalesAgentsConfig.DIRECT_INSTRUCTIONS, 
        model=SalesAgentsConfig.MODEL
    )
    
    return professional_agent, engaging_agent, direct_agent


def create_sales_tools():
    """Convierte los agentes de ventas en herramientas reutilizables"""
    
    professional_agent, engaging_agent, direct_agent = create_sales_agents()
    
    tool_description = "Escribe un correo electrónico de ventas en frío"
    
    tools = [
        professional_agent.as_tool(tool_name="sales_agent_professional", tool_description=tool_description),
        engaging_agent.as_tool(tool_name="sales_agent_engaging", tool_description=tool_description),
        direct_agent.as_tool(tool_name="sales_agent_direct", tool_description=tool_description)
    ]
    
    return tools


def create_email_tools():
    """Crea las herramientas para manejo de emails"""
    
    # Agente para escribir asuntos
    subject_writer = Agent(
        name="Escritor de Asuntos de Email",
        instructions=EmailConfig.SUBJECT_WRITER_INSTRUCTIONS,
        model=SalesAgentsConfig.MODEL
    )
    
    # Agente para conversión HTML
    html_converter = Agent(
        name="Conversor HTML de Email", 
        instructions=EmailConfig.HTML_CONVERTER_INSTRUCTIONS,
        model=SalesAgentsConfig.MODEL
    )
    
    # Convertir a herramientas
    subject_tool = subject_writer.as_tool(
        tool_name="subject_writer",
        tool_description="Escribe un asunto efectivo para email de ventas"
    )
    
    html_tool = html_converter.as_tool(
        tool_name="html_converter", 
        tool_description="Convierte cuerpo de email de texto a HTML"
    )
    
    return subject_tool, html_tool


@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """
    Envía un correo electrónico con el asunto y cuerpo HTML proporcionados
    
    Args:
        subject: Asunto del correo electrónico
        html_body: Cuerpo del correo en formato HTML
        
    Returns:
        Dict con el estado de la operación
    """
    try:
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        
        from_email = Email(EmailConfig.SENDER_EMAIL)
        to_email = To(EmailConfig.RECIPIENT_EMAIL)
        content = Content("text/html", html_body)
        
        mail = Mail(from_email, to_email, subject, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        
        return {"status": "success", "message": "Correo enviado exitosamente"}
        
    except Exception as e:
        return {"status": "error", "message": f"Error al enviar correo: {str(e)}"}


def create_email_manager():
    """Crea el agente responsable del formateo y envío de emails"""
    
    subject_tool, html_tool = create_email_tools()
    
    email_manager_instructions = (
        "Eres un formateador y remitente de correos electrónicos. "
        "Recibes el cuerpo de un correo electrónico para enviarlo. "
        "Primero usas la herramienta subject_writer para escribir un asunto efectivo, "
        "luego usas la herramienta html_converter para convertir el cuerpo a HTML. "
        "Finalmente, usas send_html_email para enviar el correo electrónico."
    )
    
    return Agent(
        name="Email Manager",
        instructions=email_manager_instructions,
        model=SalesAgentsConfig.MODEL,
        tools=[subject_tool, html_tool, send_html_email],
        handoff_description="Convierte un email a HTML y lo envía"
    )


def create_sales_manager():
    """Crea el agente manager que coordina todo el proceso de ventas"""
    
    sales_tools = create_sales_tools()
    email_manager = create_email_manager()
    
    manager_instructions = (
        "Eres un gerente de ventas que trabaja para ComplAI. "
        "Utilizas las herramientas proporcionadas para generar correos de ventas en frío. "
        "NUNCA generas correos tú mismo; siempre usas las herramientas. "
        "Pruebas las 3 herramientas de ventas al menos una vez antes de elegir la mejor. "
        "Puedes usar las herramientas múltiples veces si no estás satisfecho con los resultados. "
        "Seleccionas el mejor correo usando tu criterio sobre cuál será más efectivo. "
        "Después de elegir, transfieres al Email Manager para formatear y enviar."
    )
    
    return Agent(
        name="Sales Manager",
        instructions=manager_instructions,
        tools=sales_tools,
        handoffs=[email_manager],
        model=SalesAgentsConfig.MODEL
    )


async def execute_sales_campaign(message: str) -> str:
    """
    Ejecuta la campaña de ventas completa
    
    Args:
        message: Mensaje inicial para la campaña
        
    Returns:
        Resultado de la ejecución
    """
    sales_manager = create_sales_manager()
    
    with trace("Automated Sales Campaign"):
        result = await Runner.run(sales_manager, message)
        return result


def main():
    """Función principal del programa"""
    
    campaign_message = "Envía un correo electrónico de ventas en frío dirigido a 'Estimado director ejecutivo'"
    
    print("🚀 Iniciando campaña de ventas automatizada...")
    print(f"📧 Mensaje: {campaign_message}")
    print("-" * 50)
    
    try:
        result = asyncio.run(execute_sales_campaign(campaign_message))
        
        print("✅ Campaña completada exitosamente")
        print(f"📋 Resultado: {result.final_output}")
        print(f"👤 Agente final: {result.last_agent.name}")
        
        return result
        
    except Exception as e:
        print(f"❌ Error en la campaña: {e}")
        raise


if __name__ == "__main__":
    main()