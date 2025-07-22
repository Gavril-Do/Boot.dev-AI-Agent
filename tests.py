from functions.get_files_info import *

print(f"==1==\n{get_file_content("calculator", "main.py")}")
print(f"==2==\n{get_file_content("calculator", "pkg/calculator.py")}")
# print(f"==2==\n{get_file_content("calculator", "lorem.txt")}")
print(f"==3==\n{get_file_content("calculator", "/bin/cat")}")
print(f"==4==\n{get_file_content("calculator", "pkg/does_not_exist.py")}")
