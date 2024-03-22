#!/usr/bin/env /usr/bin/python3
#!/usr/bin/env /home/yingshaoxo/anaconda3/bin/python3
#!/usr/bin/env /home/yingshaoxo/anaconda3/bin/python
from signal import signal, SIGINT
from sys import exit
import os
from auto_everything.disk import Store, Disk
from auto_everything.python import Python
from auto_everything.io import IO
from pprint import pprint
from datetime import datetime
import json

py = Python()
disk = Disk()
store = Store("todo_list_app")
io_ = IO()
# store.reset()
# exit()


current_script_folder = disk.get_directory_path(os.path.realpath(__file__))

todo_dict = {
    "index": None,
    "list": [],
    "progress_dict": {}
}

if store.has_key("todo_dict"):
    todo_dict = store.get("todo_dict", todo_dict)
    io_.write(disk.join_paths(current_script_folder, "todo.txt"), content=json.dumps(todo_dict, indent=4, sort_keys=True))

def save():
    store.set("todo_dict", todo_dict)


def handler(signal_received, frame):
    save()
    print('\nExiting gracefully')
    exit(0)


def add(text):
    todo_dict["list"].append(text)
    todo_dict["progress_dict"].update({
        str(len(todo_dict["list"])-1): []
    })

    if len(todo_dict["list"]) == 1:
        todo_dict["index"] = 0

    save()


def remove(index):
    date_string = str(datetime.now()).split(".")[0]
    task_string = todo_dict["list"][index]
    a_list = todo_dict["progress_dict"][str(index)]
    progress_string = "\n".join([f"{index}. {task}" for index, task in enumerate(a_list)])
    one_part_of_the_log = date_string + "\n\n" + task_string + "\n\n" + progress_string
    one_part_of_the_log += "\n\n" + "----------" + "\n\n"

    del todo_dict["list"][index]
    del todo_dict["progress_dict"][str(index)]
    for i in range(index+1, len(todo_dict["list"])+1):
        progress = todo_dict["progress_dict"][str(i)]
        del todo_dict["progress_dict"][str(i)]
        todo_dict["progress_dict"].update({
            str(i-1): progress
        })

    with open(disk.join_paths(current_script_folder, 'log.txt'), 'a') as f:
        f.write(one_part_of_the_log)

    save()

def put_to_bottom(index):
    if 0 <= index < len(todo_dict["list"]):
        index_item = todo_dict["list"][index]
        index_progress_item = todo_dict["progress_dict"][str(index)].copy()

        del todo_dict["list"][index]
        del todo_dict["progress_dict"][str(index)]
        for i in range(index+1, len(todo_dict["list"])+1):
            progress = todo_dict["progress_dict"][str(i)]
            del todo_dict["progress_dict"][str(i)]
            todo_dict["progress_dict"].update({
                str(i-1): progress
            })

        todo_dict["list"] = todo_dict["list"] + [index_item]
        todo_dict["progress_dict"][str(len(todo_dict["progress_dict"]))] = index_progress_item

        save()

def display():
    a_list = todo_dict["list"]
    if len(a_list):
        print("\n".join([f"{index}. {task}" for index, task in enumerate(a_list)]))
    else:
        print("Congratulations! You have finished today's job!")


def display_one(index):
    try:
        print(str(index)+".", todo_dict["list"][index])
        print("\n\n".join(["\t"+text for text in todo_dict["progress_dict"][str(index)]]))
    except Exception as e:
        print(e)
        print(index)
        print(todo_dict["list"])


py.make_it_runnable()
py.make_it_global_runnable(executable_name="todo")

os.system('clear')
signal(SIGINT, handler)
print('Running. Press CTRL-C to exit.')
while True:
    text = input("\n--------------------\n\n").strip()
    os.system('clear')

    if text == "list":
        display()
    elif text[:len("add ")] == "add ":
        add(text[len("add "):])
        display()
    elif text[:len("finish ")] == "finish ":
        try:
            remove(int(text[len("finish "):]))
        except Exception as e:
            print("You should give me a number after 'finish', for example, 'finish 0'")
            continue
        display()
    elif text == "loop":
        if len(todo_dict["list"]) > 0:
            if (todo_dict["index"] == None) or (todo_dict["index"] > len(todo_dict["list"]) - 1):
                todo_dict["index"] = 0
            display_one(todo_dict["index"])
            todo_dict["index"] += 1
            if todo_dict["index"] > len(todo_dict["list"]) - 1:
                todo_dict["index"] = 0
        else:
            print("Congratulations! You have finished today's job!")
    elif text[:len("progress ")] == "progress ":
        progress = text[len("progress "):].strip()
        if progress[0] == '"' and progress[-1] == '"':
            progress = progress.strip('"')
        if todo_dict["index"] == 0:
            index = len(todo_dict["list"]) - 1
        else:
            index = todo_dict["index"] - 1
        todo_dict["progress_dict"][str(index)].append(progress)
        display_one(index)
        save()
    elif text[:len("check ")] == "check ":
        try:
            index = int(text[len("check "):])
        except Exception as e:
            print("You should give me a number after 'check', for example, 'check 0'")
            continue
        if 0 <= index < len(todo_dict["list"]):
            if index == len(todo_dict["list"]) - 1:
                todo_dict["index"] = 0
            else:
                todo_dict["index"] = index + 1
        display_one(index)
    elif text[:len("put_to_top ")] == "put_to_top ":
        try:
            index = int(text[len("put_to_top "):])
        except Exception as e:
            print("You should give me a number after 'put_to_top', for example, 'put_to_top 0'")
            continue
        if 0 <= index < len(todo_dict["list"]):
            index_item = todo_dict["list"][index]
            index_progress_item = todo_dict["progress_dict"][str(index)].copy()

            del todo_dict["list"][index]
            del todo_dict["progress_dict"][str(index)]
            for i in range(index+1, len(todo_dict["list"])+1):
                progress = todo_dict["progress_dict"][str(i)]
                del todo_dict["progress_dict"][str(i)]
                todo_dict["progress_dict"].update({
                    str(i-1): progress
                })

            todo_dict["list"] = [index_item] + todo_dict["list"]
            todo_dict["progress_dict"][str(-1)] = index_progress_item

            new_progress_dict = {}
            for key, value in todo_dict["progress_dict"].items():
                new_progress_dict[str(int(key)+1)] = value
            todo_dict["progress_dict"] = dict(sorted(new_progress_dict.copy().items()))

        os.system('clear')
        display()
        save()
    elif text[:len("put_to_bottom ")] == "put_to_bottom ":
        try:
            index = int(text[len("put_to_bottom "):])
        except Exception as e:
            print("You should give me a number after 'put_to_bottom', for example, 'put_to_bottom 0'")
            continue
        put_to_bottom(index)
        os.system('clear')
        display()
    elif text == "help":
        pprint(todo_dict)
    else:
        print("""
list

loop

add "..."

progress "..."

check 0

put_to_top 0

put_to_bottom 0

finish 0
        """)

