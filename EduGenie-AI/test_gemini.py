import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

print("Testing Gemini 3.1 Flash-lite...")

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Say exactly: EduGenie is working!"
)

print("\nRESULT:")
print(response.text)