import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import *
from call_functions import *


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("Error: No Prompt")
        sys.exit(1)

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
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    response_functions = response.function_calls[0]
    function_response = call_function(response_functions, verbose)
    try:
        readable_function_response = function_response.parts[
            0
        ].function_response.response["result"]
    except Exception as e:
        return f"Fatal exception: {e}"
    if verbose:
        print(f"User prompt: '{user_prompt}'")
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")
        print(f"-> {readable_function_response}")

    if not response.function_calls:
        print(f"Response:\n{response.text}")
    for function_call in response.function_calls:
        print(f"Calling function: {function_call.name}({function_call.args})")


if __name__ == "__main__":
    main()
