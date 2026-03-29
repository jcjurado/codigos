from telethon import TelegramClient
from state import State
from config import API_ID, API_HASH, CANAL_ID
from utils.helpers import normalizar_emojis


async def getTelegram(state: State) -> dict:
    """Extrae el último mensaje de texto de un canal de Telegram."""
    mensaje_normalizado = ""

    async with TelegramClient("session", API_ID, API_HASH) as client:
        print("📱" * 20)
        async for msg in client.iter_messages(CANAL_ID, limit=1):
            if msg.text:
                mensaje_normalizado = normalizar_emojis(msg.text)

    content = mensaje_normalizado or "No se encontró ningún mensaje de texto."
    print("✅ Telegram extraído")
    return {"mensajes_telegram": content}