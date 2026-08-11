from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("Google_API_Key")

client = genai.Client(api_key=API_KEY)

print("\nAVAILABLE MODELS:\n")

for model in client.models.list():
    print(model.name)