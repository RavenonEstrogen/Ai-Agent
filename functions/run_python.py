import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    joined_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(joined_path)
    abs_work_path = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_work_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not abs_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        output = subprocess.run(["python", abs_file_path] + args, capture_output=True, timeout=30, cwd=abs_work_path)
        lines = []
        stdout = output.stdout.decode()
        stderr = output.stderr.decode()
        if stdout:
            lines.append("STDOUT:" + stdout)
        if stderr:
            lines.append("STDERR:" + stderr)
        if output.returncode != 0:
            lines.append(f"Process exited with code {output.returncode}")
        if not lines:
            return "No output produced."
        return "\n".join(lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"