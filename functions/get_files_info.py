import os
from config import *


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
    contents = [f"result for '{directory}' directory:"]
    for item in os.listdir(files_dir):
        contents.append(
            f" - {item}: files_size={os.path.getsize(os.path.join(files_dir, item))}, is_dir={os.path.isdir(os.path.join(files_dir, item))}",
        )
    return "\n".join(contents)


def get_file_content(working_directory, file_path):
    if not os.path.isdir(working_directory):
        return f'Error: "{working_directory}" is not a directory'
    files_dir = os.path.join(working_directory, file_path)
    if not os.path.isfile(files_dir):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    if not os.path.abspath(files_dir).startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'
    # read file and return contents as string
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
    # If any errors are raised by the standard library functions, catch them and instead return a string describing the error.
    # Always prefix errors with "Error:".
    # Create a new "lorem.txt" file in the calculator directory.
    # Fill it with at least 20,000 characters of lorem ipsum text.
    # Update your tests.py file. Remove all the calls to get_files_info, and instead test get_file_content("calculator", "lorem.txt"). Ensure that it truncates properly.
    # Remove the lorem ipsum test, and instead test the following cases:
    #     get_file_content("calculator", "main.py")
    #     get_file_content("calculator", "pkg/calculator.py")
    #     get_file_content("calculator", "/bin/cat") (this should return an error string)
    #     get_file_content("calculator", "pkg/does_not_exist.py") (this should return an error string)
