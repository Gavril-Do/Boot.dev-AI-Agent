from functions.get_files_info import *
from functions.get_files_content import *
from functions.write_file import *

print(
    f"==1==\n{write_file("calculator", "lorem_i.txt", "wait, this isn't lorem ipsum")}"
)
print(
    f"==1==\n{write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")}"
)
print(
    f"==1==\n{write_file("calculator", "/tmp/temp.txt", "this should not be allowed")}"
)
