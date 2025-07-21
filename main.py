import os, sys
from dotenv import load_dotenv
from google import genai

if len(sys.argv) == 1:
    print("Error: No prompt")
    sys.exit(1)
load_dotenv()
model = "gemini-2.0-flash-001"
content_string = sys.argv[1] + "Use no more than 250 characters."
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
response = client.models.generate_content(model=model, contents=content_string)
print(response.text)
print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")