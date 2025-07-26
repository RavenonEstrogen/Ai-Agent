import os

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.join(working_directory, directory)
    if directory not in working_directory:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    