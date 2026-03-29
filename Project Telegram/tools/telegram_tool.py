import emoji


def limpiar_emojis(texto: str) -> str:
    return emoji.replace_emoji(texto, replace="")


def normalizar_emojis(texto: str) -> str:
    texto = texto.replace("🟢", " (COMPRA, TODO OK) ")
    texto = texto.replace("⚠️", " (ADVERTENCIA) ")
    texto = texto.replace("🔴", " (VENTA, ALERTA, PELIGRO) ")
    return emoji.replace_emoji(texto, replace="")