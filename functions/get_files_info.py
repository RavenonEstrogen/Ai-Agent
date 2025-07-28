import os
from functions.config import max_character

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