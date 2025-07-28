import os, sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from config import *
from call_functions import *


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    char_limit = "--char" in sys.argv
    token_limit = "--token" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--") and not arg.isdigit():
            args.append(arg)

    if not args:
        print("Error: No Prompt")
        sys.exit(1)

    if char_limit:
        if not int(sys.argv[sys.argv.index("--char") + 1]) >= 1000:
            print("Not enough characters. Exiting.")
            sys.exit(2)
        args.append(
            f"Use less than {sys.argv[sys.argv.index("--char") + 1]} characters."
        )
    elif token_limit:
        if not int(sys.argv[sys.argv.index("--token") + 1]) >= 400:
            print("Not enough tokens. Exiting.")
            sys.exit(2)
        args.append(f"Use less than {sys.argv[sys.argv.index("--token") + 1]} tokens.")
    user_prompt = " ".join(args)

    if verbose:
        print(f"User Prompt:\n{user_prompt}")

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iters = 0
    while True:
        iters += 1
        if iters > MAX_ITERS:
            print(f"Maximum iterations {MAX_ITERS} reached.")
            sys.exit(1)
        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print(f"Final response:\n{final_response}")
                break
        except Exception as e:
            print(f"Error in generate content: {e}")
            break


def generate_content(client, messages, verbose):
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
    if verbose:
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

    if response.candidates:
        for candidate in response.candidates:
            function_call_content = candidate.content
            messages.append(function_call_content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])
    if not function_responses:
        raise Exception("No function responses generated, exiting.")

    messages.append(
        types.Content(
            role="tool",
            parts=function_responses,
        )
    )


if __name__ == "__main__":
    main()
