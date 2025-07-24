from functions.get_files_info import *
from functions.get_files_content import *
from functions.write_file import *
from functions.run_python_file import *

print(f"==1==\n{run_python_file("calculator", "lorem.txt")}")
print(f"==2==\n{run_python_file("calculator", "main.py")}")
print(f"==3==\n{run_python_file("calculator", "main.py", ["3 + 5"])}")
print(f"==4==\n{run_python_file("calculator", "tests.py")}")
print(f"==5==\n{run_python_file("calculator", "../main.py")}")
print(f"==6==\n{run_python_file("calculator", "nonexistent.py")}")
