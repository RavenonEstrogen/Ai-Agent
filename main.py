import os
import sys
from google import genai
from dotenv import load_dotenv
from google.genai import types

from prompts import system_prompt
from available_functions import available_functions, call_function

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
    for i in range(0,21):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
            )

            for candidate in response.candidates:
                content = candidate.content
                messages.append(content)

            if response.text:
                print(response.text)
                return response.text

            if verbose:
                print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                print(f'Response tokens: {response.usage_metadata.candidates_token_count}')

            if not response.function_calls:
                return response.text
    
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                print("DEBUG function_call_result =", function_call_result)
                print("DEBUG type(function_call_result) =", type(function_call_result))
                actual_result = function_call_result.parts[0].function_response.response
                tool_message = types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part,
                            response=actual_result,
                        )
                    ],
                )
                messages.append(tool_message)

                if not function_call_result.parts or not getattr(function_call_result.parts[0], "function_response", None) or not getattr(function_call_result.parts[0].function_response, "response", None):
                    raise Exception("Fatal: No function response received from call_function.")
        
                print(f"-> {function_call_result.parts[0].function_response.response}")
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    if response.text:
        print(response.text)
        return response.text
    else:
        print("Agent reached 20 iterations without success.")
        return None

if __name__ == "__main__":
    main()
