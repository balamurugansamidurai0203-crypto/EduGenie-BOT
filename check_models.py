import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print("\nTEXT GENERATION MODELS AVAILABLE TO YOUR API KEY")
print("=" * 70)

for model in client.models.list():
    name = model.name or ""
    actions = getattr(model, "supported_actions", None) or []

    if "generateContent" in actions and "gemini" in name.lower():
        if not any(x in name.lower() for x in [
            "-tts",
            "-live",
            "-image",
            "-audio",
            "transcribe"
        ]):
            print(name)

print("=" * 70)