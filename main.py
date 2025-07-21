import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
model = "gemini-2.0-flash-001"
content_string = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(model=model, contents=content_string)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")