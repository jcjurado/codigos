import emoji

def limpiar_emojis(texto: str) -> str:
    """Limpia emojis (usado para CSV histórico)"""
    return emoji.replace_emoji(texto, replace='')

def normalizar_emojis(texto: str) -> str:
    """Normaliza emojis financieros (usado en el flujo principal)"""
    texto = texto.replace("🟢", " (COMPRA, TODO OK) ")
    texto = texto.replace("⚠️", " (ADVERTENCIA) ")
    texto = texto.replace("🔴", " (VENTA, ALERTA, PELIGRO) ")
    return emoji.replace_emoji(texto, replace='')