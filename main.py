# type: ignore
from beaupy import select
from beaupy.spinners import Spinner, DOTS

from tkinter import Tcl
import os
import keyboard
import shutil

file_path = input("Enter the path to the folder: ")
sub_ext_list = ("srt", "vtt", "txt", "ssa", "other")
sub_ext = select(sub_ext_list, cursor="🢧", cursor_style="cyan")

if sub_ext == "other":
    sub_ext = input("Enter desired subtitle file format: ")

files = os.listdir(file_path)
files = [n for n in files if n.endswith(f".{sub_ext}")]
files = sorted(files)

for file in files:
    print(file)

if "y" == input("is this correctly sorted? (y/n): ").lower():
    pass
else:
    files = Tcl().call("lsort", "-dict", files)
    for file in files:
        print(file)
    if "y" == input("is this correctly sorted? (y/n): ").lower():
        pass
    else:
        files = Tcl().call("lsort", "-ascii", files)
        for file in files:
            print(file)
        if "y" == input("is this correctly sorted? (y/n): ").lower():
            pass
        else:
            print("Nothing else right now :(")
            print("Press any key to exit...")
            key = keyboard.read_key()
            exit()

rename_str = input(
    "Please enter the filename you need to rename with { n } tag to show the EP number )\nex: TV_series_Name{n}ep_name: "
)

rename_split = rename_str.split("{n}")
print("Sample name: " + rename_split[0] + "01" + rename_split[1])

while "y" != input("is this correct ? : ").lower():
    rename_split = input(
        "Please enter the filename you need to rename with { n } tag to show the EP number )\nex: TV_series_Name{n}ep_name: "
    )
    rename_split = rename_str.split("{n}")
    print("Sample name:" + rename_split[0] + "01" + rename_split[1])
    
start_ep = input("Enter the first ep number: ")

spinner_tag = "Doing the Magic :)"
spinner = Spinner(DOTS, f"{spinner_tag}")
new_formatted=os.path.join(file_path,"Formatted")
if not os.path.exists(new_formatted):
    os.mkdir(new_formatted)

spinner.start()
num_zeros = len(start_ep)-len(start_ep.lstrip('0'))
count = int(start_ep)
for file in files:
    ep_num='0'*num_zeros+str(count)
    current_file_path=os.path.join(file_path,file)
    new_file_name = rename_split[0]+ep_num+rename_split[1]
    new_file_path=os.path.join(new_formatted,new_file_name)
    shutil.copy2(current_file_path,new_file_path)
    count +=1

spinner.stop()
