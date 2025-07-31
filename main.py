import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types

from prompts import system_prompt
from available_functions import available_functions

def main():
    load_dotenv()
    
    verbose = "--verbose" in sys.argv
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) <= 1:
        print("error message")
        exit(1)

    user_prompt = sys.argv[1]

    if verbose:
        print(f'User prompt: {user_prompt}')

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    if response.function_calls:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
    print(response.text)

if __name__ == "__main__":
    main()
