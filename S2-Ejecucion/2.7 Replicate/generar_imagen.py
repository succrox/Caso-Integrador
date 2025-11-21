import replicate
import requests
import os

# Asegúrate de que tu token esté configurado
os.environ["REPLICATE_API_TOKEN"] = "r8_EDZgvDUC1JlvOMdw86abULqJWGJqSG20k3wNY"

print("⚡ Ejecutando SDXL Lightning (4-Step)...")

# 2. Ejecutar el modelo de ByteDance
# Usamos la versión específica de 4 pasos
output = replicate.run(
    "bytedance/sdxl-lightning-4step:6f7a773af6fc3e8de9d5a3c00be77c17308914bf67772726aff83496ba1e3bbe",
    input={
        "prompt": "Retrato cinematográfico de un samurái en una ciudad de neón bajo la lluvia, alta definición, 8k",
        "width": 1024,
        "height": 1024,
        # IMPORTANTE: Este modelo requiere configuración específica
        "num_inference_steps": 4,  # Debe ser 4 para este modelo
        "guidance_scale": 0        # Lightning funciona mejor con guidance 0
    }
)

image_url = output[0]
print(f"✅ Imagen generada: {image_url}")

# 3. Guardar el archivo
print("💾 Guardando como 'lightning_result.png'...")
response = requests.get(image_url)

if response.status_code == 200:
    with open("lightning_result.png", "wb") as file:
        file.write(response.content)
    print("🎉 ¡Archivo guardado exitosamente!")
else:
    print("❌ Error al descargar la imagen.")