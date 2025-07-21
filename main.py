import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    args = sys.argv[1:]

    if not args:
        print("Error: No Prompt")
        sys.exit(1)

    verbose = False
    if args[-1] == "--verbose" or args[-1] == "Verbose":
        args = args[:-1]
        verbose = True
    args.append("Use less than 250 characters.")
    user_prompt = " ".join(args)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    if verbose is True:
        print(f"User prompt: '{user_prompt}'")
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
