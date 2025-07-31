import os

from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content in files in the specified directory, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to write content in files from, relative to the working directory. If not provided, writes content in files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write in the specified file"
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    joined_path = os.path.join(working_directory, file_path)

    if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if os.path.dirname(joined_path):
        if not os.path.exists(os.path.dirname(joined_path)):
            os.makedirs(os.path.dirname(joined_path))

    try:
        with open(joined_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {str(e)}"