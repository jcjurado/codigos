import os
import gradio as gr
from chat import chat

if __name__ == "__main__":
    chat = chat()
    foto_perfil = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "imagen.jpg")
    with gr.Blocks() as demo:
        
        # Header con foto
        with gr.Row():
            if os.path.exists(foto_perfil):
                gr.Image(
                    foto_perfil,
                    height=120,
                    width=120,
                    show_label=False,
                    container=False
                )
            with gr.Column():
                gr.Markdown("""
                # 🤖 Max Power
                ### Inteligencia Artificial
                Pregúntame sobre mi experiencia, habilidades y proyectos
                """)
        
        gr.Markdown("---")
        
        gr.ChatInterface(
            chat.chatbot,
            chatbot=gr.Chatbot(height=450)
        )
    
    demo.launch(theme=gr.themes.Soft())