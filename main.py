# type: ignore
from beaupy import select, confirm
from beaupy.spinners import Spinner, DOTS
from rich.console import Console

from tkinter import Tcl
import os
import keyboard
import shutil

console = Console()


def enter_exit():
    keyboard.read_key()
    exit()


def filter_ext(file_list, file_ext):
    file_list = [n for n in file_list if n.endswith(f".{file_ext}")]
    return file_list


def sort_1(file_list):
    return sorted(file_list)


def sort_2(file_list):
    return Tcl().call("lsort", "-dict", file_list)


def sort_3(file_list):
    return Tcl().call("lsort", "-ascii", file_list)


def print_each(file_list):
    for file in file_list:
        print(file)


def find_tuple_index(tuple, word):
    return tuple.index(word)


def sort_questions(file_list):
    # sort 1
    file_list = sort_1(file_list)
    print_each(file_list)
    if confirm("is this correctly sorted? : "):
        return file_list
    else:
        # sort 2
        file_list = sort_2(file_list)
        print_each(file_list)
        if confirm("is this correctly sorted? : "):
            return file_list
        else:
            # sort 3
            file_list = sort_3(file_list)
            print_each(file_list)
            if confirm("is this correctly sorted? :"):
                return file_list
            else:
                console.print("Nothing else at the moment :(")
                console.print("Press any key to exit...")
                enter_exit()


def get_extension(tuple, question):
    ext = select(tuple, cursor="🢧", cursor_style="cyan")
    if ext == "other":
        ext = input(question)
    return ext


def formatted_Folder_create(file_dir):
    new_formatted = os.path.join(file_dir, "Formatted")
    if not os.path.exists(new_formatted):
        os.mkdir(new_formatted)


# Ask Method from user
methods = (
    "Change subtitles to video names (Recommended)",
    "Change videos to subtitle names (invert of above)",
    "Rename subtitle names to a defined pattern",
    "Rename videos names to a defined pattern (invert of above)",
)
sub_ext = select(methods, cursor="🢧", cursor_style="cyan")
method_position = find_tuple_index(methods, sub_ext)

# Get path folder
file_path = input("Enter the path to the folder: ")
files = os.listdir(file_path)

# Get sub type
console.print("Select subtitle type")

# Extensions tuples
sub_ext_list = ("srt", "vtt", "txt", "ssa", "other")
video_ext_list = ("mp4", "mkv", "avi", "other")

dest_arg = ("Rename (Recommended)", "Copy (Backup version)")

# Get ext questions
sub_ext_q = "Enter desired subtitle file format: "
video_ext_q = "Enter desired video file format: "

spinner_tag = "Doing the Magic :)"
spinner = Spinner(DOTS, f"{spinner_tag}")

# Methods
match method_position:
    case 0:

        # Process videos
        console.print("\nLet's sort video files first :)")
        vid_ext = get_extension(video_ext_list, video_ext_q)
        video_files = filter_ext(files, vid_ext)
        video_files = sort_questions(video_files)

        # Process subtitles
        console.print("\nLet's sort subtitle files next :)")
        sub_ext = get_extension(sub_ext_list, sub_ext_q)
        sub_files = filter_ext(files, sub_ext)
        sub_files = sort_questions(sub_files)

        len_sub = len(sub_files)
        len_vid = len(video_files)
        m1_confirm = True
        count = len_vid
        if len_sub > len_vid:
            console.print(
                f"There are {len_sub-len_vid} more subtitle files than video files"
            )
            m1_confirm = confirm(
                "Not Recommended to continue. But wanna give it a go?\n if all video files are there, then doing this is fine"
            )
        elif len_sub < len_vid:
            console.print(
                f"There are {len_vid-len_sub} more video files than subtitle files"
            )
            count = len_sub
            m1_confirm = confirm(
                "Not ideal to Recommended. But wanna give it a go?\n if all subtitle files are there, then doing this is fine"
            )

        if not m1_confirm:
            console.print("Goodbye :)")
            enter_exit()
        else:
            console.print("Pick what to do :)")
            arg = select(dest_arg, cursor="🢧", cursor_style="cyan")
            arg_bool = arg == dest_arg[0]
            spinner.start()
            formatted_Folder_create(file_path)

            for i in range(count):
                sub_name = sub_files[i]
                vid_name = video_files[i]
                sub_split = os.path.splitext(sub_name)[0]
                vid_split = os.path.splitext(vid_name)[0]
                current_file_path = os.path.join(file_path, sub_name)

                if arg_bool:
                    new_file_path = os.path.join(file_path, f"{vid_split}.{sub_ext}")
                    os.rename(current_file_path, new_file_path)
                else:
                    new_file_path = os.path.join(
                        file_path, "Formatted", f"{vid_split}.{sub_ext}"
                    )
                    shutil.copy2(current_file_path, new_file_path)

            spinner.stop()

    case 1:
        # Process subtitles
        console.print("\nLet's sort subtitle files first :)\n")
        sub_ext = get_extension(sub_ext_list, sub_ext_q)
        sub_files = filter_ext(files, sub_ext)
        sub_files = sort_questions(sub_files)

        # Process videos
        console.print("\nLet's sort video files next :)\n")
        vid_ext = get_extension(video_ext_list, video_ext_q)
        video_files = filter_ext(files, vid_ext)
        video_files = sort_questions(video_files)

        len_sub = len(sub_files)
        len_vid = len(video_files)
        count = len_sub
        m1_confirm = True
        if len_sub > len_vid:
            console.print(
                f"There are {len_sub-len_vid} more subtitle files than video files"
            )
            m1_confirm = confirm(
                "Not Recommended to continue. But wanna give it a go?\n if all video files are there, then doing this is fine"
            )
            count = len_vid
        elif len_sub < len_vid:
            console.print(
                f"There are {len_vid-len_sub} more video files than subtitles files"
            )
            m1_confirm = confirm(
                "Not Recommended to continue. But wanna give it a go?\n if all subtitle files are there, then doing this is fine"
            )

        if not m1_confirm:
            console.print("Goodbye :)")
            enter_exit()
        else:
            console.print("Pick what to do :)")
            arg = select(dest_arg, cursor="🢧", cursor_style="cyan")
            arg_bool = arg == dest_arg[0]
            spinner.start()
            formatted_Folder_create(file_path)

            for i in range(count):
                vid_name = video_files[i]
                sub_name = sub_files[i]
                vid_split = os.path.splitext(vid_name)[0]
                sub_split = os.path.splitext(sub_name)[0]
                current_file_path = os.path.join(file_path, vid_name)

                if arg_bool:
                    new_file_path = os.path.join(
                        file_path, "Formatted", f"{sub_split}.{vid_ext}"
                    )
                else:
                    new_file_path = os.path.join(file_path, f"{sub_split}.{vid_ext}")
                    shutil.copy2(current_file_path, new_file_path)

            spinner.stop()
    case 2:

        rename_str = input(
            "Please enter the filename you need to rename with { n } tag to show the EP number )\nex: TV_series_Name{n}ep_name:"
        )

        rename_split = rename_str.split("{n}")
        print(
            "Sample name: " + rename_split[0] + "01" + rename_split[1] + "." + sub_ext
        )

        while "y" != input("is this correct ? : ").lower():
            rename_split = input(
                "Please enter the filename you need to rename with { n } tag to show the EP number )\nex: TV_series_Name{n}ep_name: "
            )
            rename_split = rename_str.split("{n}")
            print("Sample name:" + rename_split[0] + "01" + rename_split[1])

        start_ep = input("Enter the first ep number: ")

        spinner.start()
        num_zeros = (len(start_ep) - len(start_ep.lstrip("0"))) + 1
        count = int(start_ep)
        zero_arg=True
        for file in files:
            if zero_arg:
                ep_num = "0" * num_zeros + str(count)
            current_file_path = os.path.join(file_path, file)
            new_file_name = rename_split[0] + ep_num + rename_split[1] + "." + sub_ext
            new_file_path = os.path.join(new_formatted, new_file_name)
            shutil.copy2(current_file_path, new_file_path)
            count += 1

        spinner.stop()
    case 3:
        pass


console.print("All done xd\nPress any key to exit...")
enter_exit()
