import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    print("Available Models:")
    found_any = False
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            found_any = True
    if not found_any:
        print("No models found with 'generateContent' capability.")
except Exception as e:
    print(f"Error listing models: {e}")
