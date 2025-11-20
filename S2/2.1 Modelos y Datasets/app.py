import gradio as gr
from huggingface_hub import InferenceClient
import os

# 1. Configuración
# Intentamos obtener el token. Si no existe, el cliente intentará funcionar de forma anónima.
token = os.getenv("HF_TOKEN")

# CAMBIO IMPORTANTE: Usamos Qwen/Qwen2.5-72B-Instruct
# Este modelo es muy potente y suele estar siempre disponible en la API gratuita.
client = InferenceClient("Qwen/Qwen2.5-72B-Instruct", token=token)

def responder(mensaje, historia):
    messages = []
    
    # Opcional: System Prompt para darle personalidad
    # messages.append({"role": "system", "content": "Eres un asistente útil y amable."})

    for user_msg, bot_msg in historia:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": bot_msg})
    
    messages.append({"role": "user", "content": mensaje})

    response = ""

    try:
        # Ajustamos max_tokens a 1024 para respuestas más largas si es necesario
        for message in client.chat_completion(
            messages,
            max_tokens=1024, 
            stream=True,
            temperature=0.7,
            top_p=0.9,
        ):
            # Verificación de seguridad por si la API devuelve un formato diferente
            if message.choices and message.choices[0].delta.content:
                token_text = message.choices[0].delta.content
                response += token_text
                yield response
                
    except Exception as e:
        # Si ocurre un error, lo mostramos en el chat para depurar
        yield f"Error: {str(e)}. \nIntenta recargar la página o verifica tu HF_TOKEN."

# Interfaz
demo = gr.ChatInterface(
    fn=responder,
    title="🤖 Chatbot Qwen 2.5",
    description="Chatbot usando el modelo Qwen/Qwen2.5-72B-Instruct.",
    theme="soft",
    examples=["Hola, ¿cómo estás?", "Explícame la teoría de la relatividad en términos simples.", "Escribe un código en Python para sumar dos números."],
)

if __name__ == "__main__":
    demo.launch()