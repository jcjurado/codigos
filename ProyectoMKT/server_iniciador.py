# iniciar_campana.py
import asyncio
import os
from dotenv import load_dotenv

# Importamos el cerebro desde tu archivo de lógica
from sales_logic import execute_sales_campaign, EmailConfig

# Cargar variables de entorno (.env)
load_dotenv(override=True)

async def lanzar_campana_manual():
    print("🚀 Preparando lanzamiento de campaña manual...")

    # 1. CONFIGURACIÓN DEL OBJETIVO (¿A quién le escribimos?)
    # Aquí pones tu correo personal para recibir la prueba
    DESTINATARIO = "juradojuancruz@gmail.com"  
    
    # 2. CONFIGURACIÓN DEL REMITENTE
    # Debe coincidir con tu Sender Verificado de SendGrid
    REMITENTE = os.environ.get('SENDGRID_VERIFIED_SENDER', "ventas@juanlabor.site")

    # Sobrescribimos la configuración de la clase EmailConfig
    # Esto es la "Inyección de Dependencias" manual
    EmailConfig.RECIPIENT_EMAIL = DESTINATARIO
    EmailConfig.SENDER_EMAIL = REMITENTE

    print(f"📧 De: {EmailConfig.SENDER_EMAIL}")
    print(f"📧 Para: {EmailConfig.RECIPIENT_EMAIL}")
    print("-" * 40)

    # 3. EL MENSAJE INICIAL (El Prompt para el Manager)
    mensaje_inicial = (
        "Escribe un primer correo de contacto en frío para un Director de Tecnología (CTO). "
        "El objetivo es agendar una demo de nuestra herramienta de cumplimiento SOC2. "
        "Sé breve y persuasivo."
    )

    # 4. EJECUCIÓN
    try:
        print("🤖 El Manager de Ventas está trabajando...")
        resultado = await execute_sales_campaign(mensaje_inicial)
        
        print("\n✅ Campaña enviada con éxito.")
        print(f"📝 Texto final enviado:\n{resultado.final_output}")
        
    except Exception as e:
        print(f"\n❌ Error al lanzar campaña: {e}")

if __name__ == "__main__":
    asyncio.run(lanzar_campana_manual())