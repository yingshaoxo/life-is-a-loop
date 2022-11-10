#!/usr/bin/env /opt/homebrew/opt/python@3.10/bin/python3.10
#!/usr/bin/env /usr/bin/python3
from signal import signal, SIGINT
from sys import exit
import os
from auto_everything.disk import Store
from auto_everything.python import Python
from pprint import pprint
from datetime import datetime


py = Python()
store = Store("todo_list_app_test")
# store.reset()
# exit()

todo_dict = {
    "index": None,
    "list": [],
    "progress_dict": {}
}

if store.has_key("todo_dict"):
    todo_dict = store.get("todo_dict", todo_dict)


def handler(signal_received, frame):
    #store.set("todo_dict", todo_dict)
    print('\nExiting gracefully')
    exit(0)


def add(text):
    todo_dict["list"].append(text)
    todo_dict["progress_dict"].update({
        str(len(todo_dict["list"])-1): []
    })

    if len(todo_dict["list"]) == 1:
        todo_dict["index"] = 0


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

    with open('log.txt', 'a') as f:
        f.write(one_part_of_the_log)


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

finish 0
        """)

