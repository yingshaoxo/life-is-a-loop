#!/usr/bin/env /usr/bin/python3
from signal import signal, SIGINT
from sys import exit
import os
from auto_everything.disk import Store
from auto_everything.python import Python
from pprint import pprint


py = Python()
store = Store("todo_list_app")
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
    store.set("todo_dict", todo_dict)
    print('\nExiting gracefully')
    exit(0)


def add(text):
    todo_dict["list"].append(text)
    todo_dict["progress_dict"].update({
        str(len(todo_dict["list"])-1): []
    })


def remove(index):
    del todo_dict["list"][index]
    del todo_dict["progress_dict"][str(index)]
    for i in range(index+1, len(todo_dict["list"])+1):
        progress = todo_dict["progress_dict"][str(i)]
        del todo_dict["progress_dict"][str(i)]
        todo_dict["progress_dict"].update({
            str(i-1): progress
        })


def display():
    a_list = todo_dict["list"]
    if len(a_list):
        print("\n".join([f"{index}. {task}" for index, task in enumerate(a_list)]))
    else:
        print("Congratulations! You have finished today's job!")


def display_one(index):
    print(str(index)+".", todo_dict["list"][index])
    print("\n\n".join(["\t"+text for text in todo_dict["progress_dict"][str(index)]]))


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
        remove(int(text[len("finish "):]))
        display()
    elif text == "loop":
        if len(todo_dict["list"]) > 0:
            if todo_dict["index"] == None:
                todo_dict["index"] = 0
            display_one(todo_dict["index"])
            todo_dict["index"] += 1
            if todo_dict["index"] > len(todo_dict["list"]) - 1:
                todo_dict["index"] = 0
        else:
            print("Congratulations! You have finished today's job!")
    elif text[:len("progress ")] == "progress ":
        progress = text[len("progress "):]
        if todo_dict["index"] == 0:
            index = len(todo_dict["list"]) - 1
        else:
            index = todo_dict["index"] - 1
        todo_dict["progress_dict"][str(index)].append(progress)
        display_one(index)
    elif text[:len("check ")] == "check ":
        index = int(text[len("check "):])
        if 0 <= index < len(todo_dict["list"]):
            if index == len(todo_dict["list"]) - 1:
                todo_dict["index"] = 0
            else:
                todo_dict["index"] = index + 1
        display_one(index)
    elif text == "help":
        pprint(todo_dict)
    else:
        print("""
list

loop

add "..."

progress "..."

check 0

finish 0
        """)

