# mistral_client.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")

if not API_KEY or not BASE_URL:
    raise ValueError("Make sure OPENAI_BASE_URL and OPENROUTER_API_KEY are set.")

client = OpenAI(base_url=BASE_URL, api_key=API_KEY)
print("✔️ OpenRouter client initialized.")

def get_treatment_advice(disease_name: str) -> str:
    if "healthy" in disease_name.lower():
        return "The plant is healthy..."

    response = client.chat.completions.create(
        model="mistralai/mistral-small-3.2-24b-instruct:free",
        messages=[
            {"role": "system", "content": "Provide plant disease advice."},
            {"role": "user", "content": disease_name},
        ],
    )
    return response.choices[0].message.content
