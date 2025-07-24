import os
from config import *
from google.genai import types


def get_files_info(working_directory, directory="."):
    # if directory arg is not a dir, return error
    if not os.path.isdir(working_directory):
        return f'Error: "{working_directory}" is not a directory'
    # if abs path is outside working dir, return error
    # .startswith()
    files_dir = os.path.join(working_directory, directory)
    if not os.path.isdir(files_dir):
        return f'Error: "{directory}" is not a directory'
    if not os.path.abspath(files_dir).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    # Build and return a string representing the contents of the directory. It should use this format:
    # - README.md: file_size=1032 bytes, is_dir=False
    # - src: file_size=128 bytes, is_dir=True
    # - package.json: file_size=1234 bytes, is_dir=False
    try:
        contents = [f"result for '{directory}' directory:"]
        for item in os.listdir(files_dir):
            contents.append(
                f" - {item}: files_size={os.path.getsize(os.path.join(files_dir, item))}, is_dir={os.path.isdir(os.path.join(files_dir, item))}",
            )
        return "\n".join(contents)
    except Exception as e:
        return f"Error listing files: {e}"


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
