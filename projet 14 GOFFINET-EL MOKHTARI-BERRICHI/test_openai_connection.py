import os
from dotenv import load_dotenv
from openai import OpenAI

# Charge les variables depuis ton fichier .env
load_dotenv()

# Vérifie que la clé est bien chargée
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ La variable OPENAI_API_KEY n'est pas définie. Vérifie ton fichier .env.")

# Initialise le client
client = OpenAI(api_key=api_key)

# Test simple
response = client.chat.completions.create(
    model="gpt-3.5-mini",
    messages=[
        {"role": "user", "content": "Bonjour, quel est le type de ce texte : Facture n°123, client: Jean Dupont, 100€ ?"}
    ]
)

print("✅ Réponse :", response.choices[0].message.content)
