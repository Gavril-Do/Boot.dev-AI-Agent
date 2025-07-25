from google.genai import types

from functions.get_file_contents import *
from functions.get_files_info import *
from functions.run_python_file import *
from functions.write_file import *
from config import WORKING_DIR

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_run_python_file,
        schema_write_file,
    ]
)


def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    args = dict(function_call_part.args)
    args["working_directory"] = WORKING_DIR
    no_path = types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"file path required"},
            )
        ],
    )
    no_content = types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"content required"},
            )
        ],
    )
    match function_call_part.name:
        case "get_file_contents":
            if "file_path" not in function_call_part.args:
                return no_path
            function_result = get_file_contents(**function_call_part.args)
        case "get_files_info":
            function_result = get_files_info(**function_call_part.args)
        case "run_python_file":
            if "file_path" not in function_call_part.args:
                return no_path
            function_result = run_python_file(**function_call_part.args)
        case "write_file":
            if "file_path" not in function_call_part.args:
                return no_path
            if "content" not in function_call_part.args:
                return no_content
            function_result = write_file(**function_call_part.args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={
                            "error": f"Unknown function: {function_call_part.name}"
                        },
                    )
                ],
            )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )
