# mistral_client.py
import os
from dotenv import load_dotenv
from openai import OpenAI # <-- The new library

# Load environment variables from the .env file
load_dotenv()

# --- Configuration ---
# Your credentials and app info
API_KEY = "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"
YOUR_SITE_URL = "http://localhost:3000" # For OpenRouter tracking
YOUR_APP_NAME = "Crop Doc"             # For OpenRouter tracking


# --- Error Handling & Initialization ---
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY is not set. Please create or check your .env file.")

# Initialize the OpenAI client once, when the module is loaded.
# This is more efficient than creating a new client for every request.
try:
    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=API_KEY,
    )
    print("OpenAI client initialized for OpenRouter.")
except Exception as e:
    print(f"Failed to initialize OpenAI client: {e}")
    client = None

# --- Prompt Engineering (No changes needed here) ---
# def generate_prompt(disease_name: str) -> str:
#     """Creates a detailed, well-structured prompt for the LLM."""
#     clean_name = disease_name.replace("___", " ").replace("_", " ")
#     prompt = f"""
#     You are an expert agronomist and plant pathologist providing advice for a mobile app.
#     A user's plant has been identified with the following issue: "{clean_name}".

#     Provide clear, concise, and actionable advice suitable for a home gardener or small-scale farmer. 
#     Structure your response in Markdown format as follows:

#     ### 🩺 Disease Overview
#     A brief, one or two-sentence summary of what this disease is and what it does to the plant.

#     ### ✅ Recommended Treatments
#     A numbered list of immediate actions the user should take. Include both organic and chemical options if applicable, but label them clearly.
#     1. **[Action 1]:** Description of the step.
#     2. **[Action 2]:** Description of the step.

#     ### Prevention Tips
#     A bulleted list of preventative measures to avoid this issue in the future.
#     *   Tip 1...
#     *   Tip 2...
    
#     Keep the language simple and easy to understand.
#     """
#     return prompt

# --- Main Function (Rewritten to use the OpenAI client) ---
def get_treatment_advice(disease_name: str) -> str:
    if not disease_name or "healthy" in disease_name.lower():
        return "The plant appears healthy. No treatment is necessary. Continue with standard watering, sunlight, and care."

    client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
    )

    prompt = "Potato___Early_blight"
    completion = client.chat.completions.create(
    extra_headers={
        "HTTP-Referer": "<YOUR_SITE_URL>", # Optional. Site URL for rankings on openrouter.ai.
        "X-Title": "<YOUR_SITE_NAME>", # Optional. Site title for rankings on openrouter.ai.
    },
    extra_body={},
    model="mistralai/mistral-small-3.2-24b-instruct:free",
    messages=[
                {
                "role": "system",
                "content": "You will be prompted by the diagnosis of a potato disease. Provide a solution for it, unless the diagnosis is that it is healthy", # Our prompt goes here. We don't send an image.
                },
                {
                "role": "user",
                "content": prompt,
                }
            ],
    )

    return completion.choices[0].message.content