import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types

from prompts import system_prompt
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file
from functions.config import max_iterations
from available_functions import available_functions, call_function

def main():
    load_dotenv()
    
    verbose = "--verbose" in sys.argv
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) <= 1:
        print("error message")
        sys.exit(1)

    user_prompt = sys.argv[1]

    if verbose:
        print(f'User prompt: {user_prompt}')

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    iterations = 0
    while True:
        iterations += 1
        if iterations > max_iterations:
            print(f"Maximum iterations reached before an answer.")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final repsonse:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    
    if response.candidates:
        for candidate in response.candidates:
                content = candidate.content
                messages.append(content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("Fatal: No function response received from call_function.")
        
        if verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses, exiting")
        
    messages.append(types.Content(role="tool", parts=[function_responses]))

if __name__ == "__main__":
    main()
