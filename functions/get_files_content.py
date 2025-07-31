import os
from functions.config import max_character
from google import genai
from google.genai import types

schema_get_files_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads files in the specified directory and displays their content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to read files from, relative to the working directory. If not provided, reads files in the working directory itself.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    joined_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(joined_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(joined_path, "r") as f:
            file = f.read(max_character)
            if f.read(1):
                return f'{file}[...File "{file_path}" truncated at 10000 characters]'
            else:
                return file
    except Exception as e:
        return f"Error: {str(e)}"