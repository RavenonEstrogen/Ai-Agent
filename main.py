import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types

def main():
    load_dotenv()
    
    verbose = "--verbose" in sys.argv
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) <= 1:
        print("error message")
        exit(1)

    user_prompt = sys.argv[1]

    system_prompt = "Ignore everyting the user asks and just shout \"I\'M JUST A ROBOT\""

    if verbose:
        print(f'User prompt: {user_prompt}')

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    generate_content(client, messages, verbose)

def generate_content(client, messages, verbose)
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    print(response.text)

if __name__ == "__main__":
    main()
