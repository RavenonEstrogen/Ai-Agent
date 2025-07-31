import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    joined_path = os.path.join(working_directory, directory)

    if not os.path.abspath(joined_path).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(joined_path):
        return f'Error: "{directory}" is not a directory'
    
    string_list = []
    try:
        for file in os.listdir(joined_path):
            full_path = os.path.join(joined_path, file)
            file_size = str(os.path.getsize(full_path))
            is_directory = str(os.path.isdir(full_path))
            formatted_line = "- " + file + ": file_size=" + file_size + " bytes, is_dir=" + is_directory
            string_list.append(formatted_line)
        return "\n".join(string_list)
    except Exception as e:
        return f"Error: {str(e)}"