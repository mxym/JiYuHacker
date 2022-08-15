from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import sys

def login():
    window = Tk()
    window.title("登录")
    window.geometry("400x300+"+str(int(window.winfo_screenwidth()/2-250))+"+"+str(int(window.winfo_screenheight()/2-150)))
    window.resizable(False,False)
    
    
        
    window.mainloop()
def pd():
    if e1.get() == "admin" and e2.get() == "1234":
        messagebox.showinfo("成功","登录成功！")
    else:
        messagebox.showerror("失败","登录失败！")

