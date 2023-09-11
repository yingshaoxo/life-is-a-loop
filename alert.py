from time import sleep
from auto_everything.time import Time
time_ = Time()

saying = """
不能被分心，be focus

干扰太强, cut the connection with bad people,

For example, use earplugs.

(Sort tasks with new standards: start from easy tasks.





前途摧毁3要素：

1. 赌徒心理，先把你的钱吞掉

2. 繁殖欲心理，让美女诱惑你朝着错误的方向前进

3. 各种干扰，包括人声噪音，让你偏离你自己给自己设定的方向
    """.strip()

from tkinter import Tk, Label, messagebox, font, CENTER, Button

root_window = Tk()
root_window.title('')
root_window.geometry("1280x800")
root_window.configure(bg='white')

label=Label(root_window, text=saying, font='Helvetica 20 bold', background="white")
label.place(relx=0.5, rely=0.5, anchor=CENTER)

#messagebox.showinfo(title=None, message=saying)
  
def show_it_for_me():
    root_window.deiconify()
    root_window.update()

def hide_it_for_me():
    root_window.withdraw()
    root_window.update()

Button(root_window, text= "OK", command=hide_it_for_me, height=3, width=20).pack(pady = 20)

while True:
    root_window.update()

    show_it_for_me()
    while root_window.state() == "normal":
        sleep(1)
        root_window.update()
    
    sleep(60*60*6)
