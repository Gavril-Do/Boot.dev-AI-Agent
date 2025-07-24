import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        commands = ["python", file_path, *args]
        proc = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_working_dir,
        )

        ret_list = []
        if proc.stdout:
            ret_list.append(f"STDOUT:\n{proc.stdout}")
        if proc.stderr:
            ret_list.append(f"STDERR:\n{proc.stderr}")
        if proc.returncode != 0:
            ret_list.append(f"Process exited with code {proc.returncode}")
        ret_str = "\n".join(ret_list) if ret_list else "No output produced."

        return ret_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
