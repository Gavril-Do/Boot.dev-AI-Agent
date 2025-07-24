from functions.get_file_contents import *
from functions.get_files_info import *
from functions.run_python_file import *
from functions.write_file import *

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_run_python_file,
        schema_write_file,
    ]
)
