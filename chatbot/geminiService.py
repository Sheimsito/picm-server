from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

manual = open("manual.md", encoding="utf-8") 
system_prompt = manual.read()
manual.close()

PICM_ASSISTANT_CONTEXT = """
Eres PICM-BOT, el asistente oficial del sistema de gestión de inventario PICM, para ayudar al usuario a resolver sus dudas de la plataforma.

Tu tarea:
- Responder cualquier pregunta del usuario basada SOLO en el manual.
- Guiar con pasos claros.
- Ser amable, preciso y corto.
- Si algo no está en el manual, di: “Esa funcionalidad no está documentada en PICM”.

"""


def generate_response(pregunta):
    full_prompt = PICM_ASSISTANT_CONTEXT + "\n\n" + system_prompt + "\n\n La pregunta es: " + pregunta 
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=full_prompt
    )
    
    return response.text

