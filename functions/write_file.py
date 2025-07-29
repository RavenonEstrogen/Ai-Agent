import os

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