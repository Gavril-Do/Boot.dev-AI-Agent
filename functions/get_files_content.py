import os
from config import *


def get_file_content(working_directory, file_path):
    if not os.path.isdir(working_directory):
        return f'Error: "{working_directory}" is not a directory'
    files_dir = os.path.join(working_directory, file_path)
    if not os.path.isfile(files_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not os.path.abspath(files_dir).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    # read file and return contents as string
    try:
        with open(files_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            truncated = len(f.read()) > MAX_CHARS
        # If the file is longer than 10000 characters, truncate it to 10000 characters and append this message to the end [...File "{file_path}" truncated at 10000 characters].
        if truncated:
            return (
                file_content_string
                + f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )
        return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"
    # If any errors are raised by the standard library functions, catch them and instead return a string describing the error.
    # Always prefix errors with "Error:".
