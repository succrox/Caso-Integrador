import os
import google.generativeai as genai
from transformers import pipeline
import scipy.io.wavfile
import numpy as np
from dotenv import load_dotenv

# 1. Cargar variables de entorno
load_dotenv()

# Configuración de Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Configuración del Pipeline de Audio de Hugging Face
# Modelo seleccionado por el usuario: nineninesix/kani-tts-400m-en
print("⏳ Cargando modelo de audio (facebook/mms-tts-eng)...")
synthesiser = pipeline("text-to-speech", model="facebook/mms-tts-eng")

def generar_guion_educativo(tema):
    """
    Usa Gemini para crear un guion corto en INGLÉS.
    (El modelo de audio kani-tts funciona mejor en inglés).
    """
    print(f"🤖 1. Google AI: Generando guion sobre '{tema}'...")
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Prompt diseñado para ser breve y compatible con TTS
    prompt = (
        f"Write a short educational explanation about '{tema}' for a student. "
        "Use simple English. Maximum 2 sentences. "
        "Do not use special characters or emojis."
    )
    response = model.generate_content(prompt)
    return response.text

def generar_audio_hf(texto):
    """Sintetiza el audio manejando listas o diccionarios."""
    print(f"🎙️ 2. Hugging Face: Sintetizando audio...")
    
    if not texto:
        raise ValueError("El texto para el audio está vacío.")

    # Generación
    result = synthesiser(texto)
    
    # CORRECCIÓN DE ERROR: Validar si devuelve lista o diccionario
    if isinstance(result, list):
        speech = result[0] # Si es lista, tomamos el primero
    else:
        speech = result    # Si es dict, lo usamos directo
        
    # Extraer datos con seguridad
    audio_data = speech.get('audio')
    sampling_rate = speech.get('sampling_rate')

    if audio_data is None or sampling_rate is None:
        # Fallback por si el modelo no reporta rate (MMS usa 16000 por defecto)
        sampling_rate = 16000 
        print("⚠️ Advertencia: Sampling rate no detectado, usando 16000Hz por defecto.")

    return audio_data, sampling_rate
def main():
    # Crear carpeta de salida si no existe
    if not os.path.exists("S3-CasoIntegrador"):
        os.makedirs("S3-CasoIntegrador")

    print("--- Generador de Podcast Educativo (Google AI + HF) ---")
    tema = input("🎓 Ingresa el tema (Ej: The Moon, Python, Cats): ")

    try:
        # Paso 1: Generar Texto
        guion = generar_guion_educativo(tema)
        print(f"\n📄 Guion:\n{guion}\n")
        
        # Guardar el texto
        with open(f"S3-CasoIntegrador/{tema}_script.txt", "w", encoding="utf-8") as f:
            f.write(guion)

        # Paso 2: Generar Audio
        audio_array, rate = generar_audio_hf(guion)
        
        # Guardar el audio (scipy espera el array transpuesto para este formato)
        ruta_audio = f"S3-CasoIntegrador/{tema}_podcast.wav"
        scipy.io.wavfile.write(ruta_audio, rate=rate, data=audio_array.T)
        
        print(f"✅ ¡Éxito! Archivos guardados en /S3-CasoIntegrador:")
        print(f"   - {ruta_audio}")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()