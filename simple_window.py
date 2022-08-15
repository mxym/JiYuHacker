from tkinter import *
from tkinter import ttk, messagebox
from simple_widgets import *
import time
from ctypes import windll
from PIL import Image, ImageTk
#import pyperclip
import threading

class V(object):
    pass
p = V()

class SrWindow(object):
    def __init__(self, function, title='输入界面', zj=['e'], name=['输入：'], font='华文新魏', value=[], win_hei=0, win_wid=0, zj_wid=0, zj_hei=30, gap=20, top=False, tk=True, unresize=(False, False)):

        v_win_hei =  len(zj) * (gap+zj_hei) + gap+ 30 if win_hei == 0 else win_hei
        v_win_wid = 2 * v_win_hei if win_wid == 0 else win_wid

        if zj_wid == 0:
            v_zj_wid = win_wid

        if value == []:
            a = 0
            v_value = []
            for i in zj:
                if i == 'c':
                    a += 1
            for i in range(a):
                v_value.append([])
        else:
            v_value = value

        if tk:
            self.window = Tk()
        else:
            self.window = Toplevel()
        self.window.geometry(str(v_win_wid) + 'x' + str(v_win_hei) + '+' + str(int(self.window.winfo_screenwidth(
        ) / 2 - v_win_wid / 2)) + '+' + str(int(self.window.winfo_screenheight() / 2 - v_win_hei / 2)))
        self.window.title(title)

        if unresize[0] and unresize[1]:
            self.window.resizable(width=False, height=False)
        elif unresize[0] and not unresize[1]:
            self.window.resizable(width=False, height=True)
        elif unresize[1] and not unresize[0]:
            self.window.resizable(width=True, height=False)

        if top:
            self.window.wm_attributes('-topmost', 1)

        self.zjet = []
        label_list = []
        comb_num = 0
        for i in range(len(zj)):
            label_list.append(
                Label(self.window, text=name[i], font=(font, 16)))
            if zj[i] == 'c':
                self.zjet.append(ttk.Combobox(
                    self.window, value=v_value[comb_num], font=('微软雅黑', 12)))
                comb_num += 1
            elif zj[i] == 'e':
                self.zjet.append(ttk.Entry(self.window, font=('微软雅黑', 12)))

        for i in range(len(self.zjet)):
            label_list[i].place(x=25, y=gap + (gap+zj_hei) * i)
            label_list[i].update()
            self.zjet[i].place(x=25 + label_list[i].winfo_width() + 20, y=gap + (gap+zj_hei) * i +
                               0, width=v_win_wid - 50 - 20 - label_list[i].winfo_width(), height=zj_hei)
            self.zjet[i].bind('<Return>', function)

        self.qd = Button(self.window, text='确定',
                         relief='groove', command=function)
        self.qd.pack(side='bottom', fill='x')

    def destroy(self, jy=False):
        if jy:
            for i in range(51):
                self.window.wm_attributes('-alpha', 1 - i * 0.02)
                time.sleep(0.01)
                self.window.update()
        self.window.destroy()

    def mainloop(self, jy=False):
        if jy:
            for i in range(51):
                self.window.wm_attributes('-alpha', i * 0.02)
                time.sleep(0.01)
                self.window.update()
        self.window.mainloop()

    def givesign(self, nr='By:Bill', width=100):
        def close():
            self.window.destroy()
            tk = Tk()
            tk.wm_attributes('-topmost', 1)
            tk.geometry('%dx%d+%d+%d' % (width, 40, (tk.winfo_screenwidth() / 2) -
                                         (width / 2), (tk.winfo_screenheight() / 2) - (20 / 2)))
            tk.overrideredirect(True)
            Label(tk, text=nr, fg='black', font=(
                '华文新魏', 14), relief='ridge').place(relwidth=1, relheight=1)
            for i in range(101):
                tk.wm_attributes('-alpha', (i * 0.01))
                tk.update()
                time.sleep(0.01)
            tk.update()
            time.sleep(1)
            for i in range(101):
                tk.wm_attributes('-alpha', (1 - i * 0.01))
                tk.update()
                time.sleep(0.01)
            tk.destroy()
        self.window.protocol('WM_DELETE_WINDOW', close)


class ScWindow(SrWindow):
    def __init__(self, nr, title='输出界面', fs='a', font=('微软雅黑', 12), win_hei=0, win_wid=0, top=False, tk=True, unresize=(False, False), bgh=False, disabled=True):
        '''
        ScWindow是方便快捷的输出界面
        nr：输出内容
        title：输出界面标题
        fs：输出方式，有'a'和'b'两种，前者是用Label输出，后者是用Text输出
        win_hei：窗口高度
        win_wid：窗口宽度
        top：是否置顶
        tk：是否是用Tk()，否则使用Toplevel()
        unresize：窗口可否改变大小，需为一个含两项的元组，第一项代表左右方向能否改变，第二项代表上下方向能否改变
        bgh：暂时忘记了是什么
        disabled：Text是否disabled，只有当fs参数为'b'时此参数才有效
        '''
        if tk:
            self.window = Tk()
        else:
            self.window = Toplevel()

        self.window.title(title)
        if win_wid == 0 or win_hei == 0:
            pass
        else:
            self.window.geometry(str(win_wid) + 'x' + str(win_hei) + '+' + str(int(self.window.winfo_screenwidth(
            ) / 2 - win_wid / 2)) + '+' + str(int(self.window.winfo_screenheight() / 2 - win_hei / 2)))

        if unresize[0] and unresize[1]:
            self.window.resizable(width=False, height=False)
        elif unresize[0] and not unresize[1]:
            self.window.resizable(width=False, height=True)
        elif unresize[1] and not unresize[0]:
            self.window.resizable(width=True, height=False)

        if top:
            self.window.wm_attributes('-topmost', 1)
        if bgh:
            self.bg = Label()
            self.bg.place(relwidth=1, relheight=1)

        if fs == 'a':
            self.sc = Label(self.window, text=nr, font=font, bg='black', fg='white')
            self.sc.place(relwidth=1, relheight=1)
        elif fs == 'b':
            self.sc = Text(self.window, font=font)
            self.sc.insert('insert', nr)
            if disabled == True:
                self.sc['state'] = 'disabled'
            self.sc.place(relheight=0.8, relwidth=0.9,
                          relx=0.5, rely=0.5, anchor=CENTER)


class ChWindow(SrWindow):
    def __init__(self, function, name=['Button'], tk=True, win_wid=0, win_hei=0, zj_hei=0, ls=1, zjbg=0, title='选择', top=False, unresize=(False, False), jg=0):
        if tk:
            self.window = Tk()
        else:
            self.window = Toplevel()
        if win_wid == 0:
            if win_hei == 0:
                v_win_wid = 300
                v_win_hei = 200
            else:
                v_win_hei = win_hei
                v_win_wid = win_hei / 2 * 3
        elif win_hei == 0:
            v_win_wid = win_wid
            v_win_hei = win_wid * 2 / 3

        self.window.geometry(str(int(v_win_wid)) + 'x' + str(int(v_win_hei)) + '+' + str(int(self.window.winfo_screenwidth(
        ) / 2 - v_win_wid / 2)) + '+' + str(int(self.window.winfo_screenheight() / 2 - v_win_hei / 2)))

        self.window.title(title)
        if unresize[0] and unresize[1]:
            self.window.resizable(width=False, height=False)
        elif unresize[0] and not unresize[1]:
            self.window.resizable(width=False, height=True)
        elif unresize[1] and not unresize[0]:
            self.window.resizable(width=True, height=False)

        if top:
            self.window.wm_attributes('-topmost', 1)

        if ls == 1:
            if zj_hei == 0:
                zjet = []
                for i in range(len(name)):
                    self.window.update()
                    zjet.append(
                        Button(self.window, command=function[i], text=name[i]))
                    if 40 * len(name) + jg * (len(name) - 1) > self.window.winfo_height():
                        zjet[i].place(relwidth=1, relheight=1 / len(name), relx=0,
                                      rely=1 / len(name) * i)
                    else:
                        zjet[i].place(relwidth=1, height=40,
                                      anchor=CENTER, relx=0.5, y=40 * i + 40 / 2 + jg * i)
            else:
                pass
        else:
            if zj_hei == 0:
                pass
            else:
                pass


class Otk(Tk):
    '''
    *Otk已停止维护，建议使用OTk!
    使用如Tk一样，对象名=Otk()
    接着还要调用otk()，对象名.otk(参数详情见otk内注释)
    最后不能用mainloop，要用open，对象名.open(参数详情见open内注释)
    关闭窗口不能用destroy，要用close，对象名.close()
    '''

    def otk(self, title='去框的窗口', win_hei=563, win_wid=1000, top=False, button=['□', '×'], topbg='#66CDAA', abg=['<zdh-y>', '<close-y>'], command=['<zdh>', '<close>'], win_bg_lj=''):
        '''
        参数:
        title：标题，
        win_hei：窗口高度，
        win_wid：窗口长度，
        top：是否始终至于所有窗口顶层(True, False)，
        button：标题栏上的按钮，
        topbg：标题栏的背景颜色，
        abg：各个标题栏上的按钮碰到鼠标的两个颜色函数(，用元组扩起来，与button一一对应)，<zdh-y>代表最大化按钮的颜色函数，<close-y>代表关闭按钮的颜色函数
        command：各个按钮按下后执行的函数(<close>为关闭窗口，<zdh>为窗口最大化)
        win_bg_lj：窗口背景图片路径
        其他：
        窗口为对象名.window，
        按钮为对象名.button[x]，
        <zdh>的按钮必须为□，<zdh-y><close-y>必须分别为□×
        '''
        class V:
            pass
        v = V()
        # 创建窗口

        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = '#66CDAA'

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = '#66CDAA'

        def zdh(*event):    # 最大化按钮函数
            if v.cksfzdh == 0:
                v.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif v.cksfzdh == 1:
                v.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            pass
        else:
            command[command.index('<close>')] = self.close
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        self.title(title)
        self.wm_attributes('-alpha', 0)
        self.overrideredirect(True)
        self.geometry(str(win_wid) + 'x' + str(win_hei) + '+' + str(int(self.winfo_screenwidth() / 2 - (
            int(win_wid) / 2))) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30)))
        if top:
            self.wm_attributes('-topmost', True)
        if win_bg_lj != '' and '\\':
            a = Image.open(win_bg_lj)
            a = a.resize((self.winfo_screenwidth(), self.winfo_screenwidth()))
            b = ImageTk.PhotoImage(a)
            bg = Label(self, image=b)
            bg.place(relwidth=1, relheigh=1)
        # 窗口背景及属性设置

        self.update()

        def relxy(event):    # 拖动窗口函数，确定单击时的鼠标坐标
            v.mouse_relx = event.x_root - self.winfo_x()
            v.mouse_rely = event.y_root - self.winfo_y()
            v.window_relx = self.winfo_x()

        def top_click(event):    # 拖动窗口函数
            if event.y_root < self.winfo_screenheight() - 75 + v.mouse_rely:
                if v.cksfzdh == 1:
                    v.cksfzdh = 0
                    self.button_list[button.index('□')]['text'] = '□'
                    self.state("normal")

                self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                v.mouse_relx) + '+' + str(event.y_root - v.mouse_rely))
            else:
                self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                v.mouse_relx) + '+' + str(self.winfo_screenheight() - 75))

        top = Label(self, bg=topbg)
        top.place(relwidth=1, height=40, x=0, y=0)
        top.bind('<B1-Motion>', top_click)
        top.bind('<Button-1>', relxy)
        if '□' in button:
            top.bind('<Double-Button-1>', zdh)
        # 窗口上部绿色那一条

        button_frame = Frame(self)
        button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        v.cksfzdh = 0

        self.button_list = []
        for i in range(len(button)):
            self.button_list.append(Button(button_frame, text=button[i], font=(
                'Arail', 16), fg='white', bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            self.button_list[i].bind('<Enter>', abg[i][1])
            self.button_list[i].bind('<Leave>', abg[i][0])

        wid = Label(self, highlightthickness=0, borderwidth=1, padx=0, pady=0,
                    compound='center', font='楷体', text=title, fg='white', bg=topbg)
        wid.place(x=15, y=0, height=40, width=90)
        wid.bind('<B1-Motion>', top_click)
        wid.bind('<Button-1>', relxy)
        # 标题Label

        separator = Frame(self, height=2, bd=1, relief="sunken")
        separator.place(relx=0.5, y=40, anchor=CENTER, relwidth=1)
        # 分割线

    def close(self, jy=True):    # 关闭按钮函数
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', 1 - i * 0.02)
                time.sleep(0.01)
                self.update()
        self.destroy()

    def open(self, jy=True):
        '''
        参数：
        jy：是否渐隐显示窗口
        '''
        def set_appwindow(root):
            GWL_EXSTYLE = -20
            WS_EX_TOOLWINDOW = 0x00000080
            WS_EX_APPWINDOW = 0x00040000

            hwnd = windll.user32.GetParent(root.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            # re-assert the new window style
            root.wm_withdraw()
            root.after(10, lambda: root.wm_deiconify())

        self.after(0, lambda: set_appwindow(self))
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', i * 0.02)
                time.sleep(0.01)
                self.update()
        self.mainloop()


class Otoplevel(Toplevel, Otk):
    '''
    *Otoplevel已停止维护，建议使用OToplevel!
    使用如Toplevel一样，对象名=Otoplevel()
    接着还要调用otk()，对象名.otk(参数详情见otk内注释)
    最后不能用mainloop，要用open，对象名.open(参数详情见open内注释)
    关闭窗口不能用destroy，要用close，对象名.close()
    '''

    def otk(self, title='去框的窗口', win_hei=563, win_wid=1000, top=False, button=['□', '×'], topbg='#66CDAA', abg=['<zdh-y>', '<close-y>'], command=['<zdh>', '<close>'], win_bg_lj=''):
        '''
        参数:
        title：标题，
        win_hei：窗口高度，
        win_wid：窗口长度，
        top：是否始终至于所有窗口顶层(True, False)，
        button：标题栏上的按钮，
        topbg：标题栏的背景颜色，
        abg：各个标题栏上的按钮碰到鼠标的两个颜色函数(，用元组扩起来，与button一一对应)，<zdh-y>代表最大化按钮的颜色函数，<close-y>代表关闭按钮的颜色函数
        command：各个按钮按下后执行的函数(<close>为关闭窗口，<zdh>为窗口最大化)
        win_bg_lj：窗口背景图片路径
        其他：
        窗口为对象名.window，
        按钮为对象名.button[x]，
        <zdh>的按钮必须为□，<zdh-y><close-y>必须分别为□×
        '''
        class V:
            pass
        v = V()
        # 创建窗口

        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = '#66CDAA'

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = '#66CDAA'

        def zdh(*event):    # 最大化按钮函数
            if v.cksfzdh == 0:
                v.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif v.cksfzdh == 1:
                v.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            pass
        else:
            command[command.index('<close>')] = self.close
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        self.title(title)
        self.wm_attributes('-alpha', 0)
        self.overrideredirect(True)
        self.geometry(str(win_wid) + 'x' + str(win_hei) + '+' + str(int(self.winfo_screenwidth() / 2 - (
            int(win_wid) / 2))) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30)))
        if top:
            self.wm_attributes('-topmost', True)
        if win_bg_lj != '' and '\\':
            a = Image.open(win_bg_lj)
            a = a.resize((self.winfo_screenwidth(), self.winfo_screenwidth()))
            b = ImageTk.PhotoImage(a)
            bg = Label(self, image=b)
            bg.place(relwidth=1, relheigh=1)
        # 窗口背景及属性设置

        self.update()

        def relxy(event):    # 拖动窗口函数，确定单击时的鼠标坐标
            v.mouse_relx = event.x_root - self.winfo_x()
            v.mouse_rely = event.y_root - self.winfo_y()
            v.window_relx = self.winfo_x()

        def top_click(event):    # 拖动窗口函数
            if event.y_root < self.winfo_screenheight() - 75 + v.mouse_rely:
                if v.cksfzdh == 1:
                    v.cksfzdh = 0
                    self.button_list[button.index('□')]['text'] = '□'
                    self.state("normal")

                self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                v.mouse_relx) + '+' + str(event.y_root - v.mouse_rely))
            else:
                self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                v.mouse_relx) + '+' + str(self.winfo_screenheight() - 75))

        top = Label(self, bg=topbg)
        top.place(relwidth=1, height=40, x=0, y=0)
        top.bind('<B1-Motion>', top_click)
        top.bind('<Button-1>', relxy)
        if '□' in button:
            top.bind('<Double-Button-1>', zdh)
        # 窗口上部绿色那一条

        button_frame = Frame(self)
        button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        v.cksfzdh = 0

        self.button_list = []
        for i in range(len(button)):
            self.button_list.append(Button(button_frame, text=button[i], font=(
                'Arail', 16), fg='white', bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            self.button_list[i].bind('<Enter>', abg[i][1])
            self.button_list[i].bind('<Leave>', abg[i][0])

        wid = Label(self, highlightthickness=0, borderwidth=1, padx=0, pady=0,
                    compound='center', font='楷体', text=title, fg='white', bg=topbg)
        wid.place(x=15, y=0, height=40, width=90)
        wid.bind('<B1-Motion>', top_click)
        wid.bind('<Button-1>', relxy)
        # 标题Label

        separator = Frame(self, height=2, bd=1, relief="sunken")
        separator.place(relx=0.5, y=40, anchor=CENTER, relwidth=1)
        # 分割线


class OTk(Tk):
    '''
    使用如Tk一样，对象名=OTk(参数)

    参数:
    title：标题，
    win_hei：窗口高度，
    win_wid：窗口长度，
    top：是否始终置于所有窗口顶层(True, False)，如果置顶将会有阴影效果，
    button_color:鼠标飘过时的标题栏按钮颜色
    button：标题栏上的按钮，
    topbg：标题栏的背景颜色，
    abg：各个标题栏上的按钮碰到鼠标的两个颜色函数(，用元组扩起来，与button一一对应)，<zdh-y>代表最大化按钮的颜色函数，<close-y>代表关闭按钮的颜色函数
    tips：提示
    command：各个按钮按下后执行的函数(<close>为关闭窗口，<zdh>为窗口最大化)
    win_bg_lj：窗口背景图片路径
    其他：
    按钮为对象名.button_list[x]，
    <zdh>的按钮必须为□，<zdh-y><close-y>必须分别为□×
    '''
    def __init__(self, title='去框的窗口', win_hei=563, win_wid=1000, top=False, button_color='#40E0D0', button=['□', '×'], topbg='#66CDAA', abg=['<zdh-y>', '<close-y>'], tips=['最大化/还原', '关闭'], command=['<zdh>', '<close>'], win_bg_lj='', yy=False, oimage=True):
        Tk.__init__(self)
        topm = top
        self.top = topm
        self.topbg = topbg
        self.button_text = button
        self.button_color = button_color
        if topm:
            self.behind = Toplevel()
            self.behind.overrideredirect(True)
            self.behind.wm_attributes('-alpha', 0)
            self.behind.wm_attributes('-topmost', True)
            Label(self.behind, bg='black').place(relheight=1, relwidth=1)
            self.behind.geometry(str(win_wid + 10) + 'x' + str(win_hei + 10) + '+' + str(int(self.winfo_screenwidth(
            ) / 2 - (int(win_wid) / 2)) - 5) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 5))
            self.behind2 = Toplevel()
            self.behind2.overrideredirect(True)
            self.behind2.wm_attributes('-alpha', 0)
            self.behind2.wm_attributes('-topmost', True)
            Label(self.behind2, bg='black').place(relheight=1, relwidth=1)
            self.behind2.geometry(str(win_wid + 8) + 'x' + str(win_hei + 8) + '+' + str(int(self.winfo_screenwidth(
            ) / 2 - (int(win_wid) / 2)) - 4) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 4))
            self.behind3 = Toplevel()
            self.behind3.overrideredirect(True)
            self.behind3.wm_attributes('-alpha', 0)
            self.behind3.wm_attributes('-topmost', True)
            Label(self.behind3, bg='black').place(relheight=1, relwidth=1)
            self.behind3.geometry(str(win_wid + 6) + 'x' + str(win_hei + 6) + '+' + str(int(self.winfo_screenwidth(
            ) / 2 - (int(win_wid) / 2)) - 3) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 3))
            self.behind4 = Toplevel()
            self.behind4.overrideredirect(True)
            self.behind4.wm_attributes('-alpha', 0)
            self.behind4.wm_attributes('-topmost', True)
            Label(self.behind4, bg='black').place(relheight=1, relwidth=1)
            self.behind4.geometry(str(win_wid + 4) + 'x' + str(win_hei + 4) + '+' + str(int(self.winfo_screenwidth(
            ) / 2 - (int(win_wid) / 2)) - 2) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 2))

            def yyclick(*event):
                self.wm_attributes('-topmost', 0)
                self.wm_attributes('-topmost', 1)
            self.behind.bind('<Button-1>', yyclick)
            self.behind2.bind('<Button-1>', yyclick)
            self.behind3.bind('<Button-1>', yyclick)
            self.behind4.bind('<Button-1>', yyclick)

        # 创建窗口

        def turn_red(event, num):
            self.button_list[num]['bg'] = button_color

        def turn_green(event, num):
            self.button_list[num]['bg'] = topbg

        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = topbg

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = topbg

        def zdh(*event):    # 最大化按钮函数
            if self.cksfzdh == 0:
                self.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif self.cksfzdh == 1:
                self.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            self.protocol('WM_DELETE_WINDOW', command[button.index('×')])
        else:
            command[command.index('<close>')] = self.destroy
            self.protocol('WM_DELETE_WINDOW', self.destroy)
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        self.title(title)
        self.wm_attributes('-alpha', 0)
        self.overrideredirect(True)
        self.geometry(str(win_wid) + 'x' + str(win_hei) + '+' + str(int(self.winfo_screenwidth() / 2 - (
            int(win_wid) / 2))) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30)))
        if topm:
            self.wm_attributes('-topmost', True)
        if win_bg_lj != '':
            if oimage == True:
                a = Image.open(win_bg_lj)
            else:
                a = win_bg_lj
            if '□' in button:
                a = a.resize((self.winfo_screenwidth(), self.winfo_screenwidth()))
            else:
                a = a.resize((win_wid, win_hei))
            p.b = ImageTk.PhotoImage(a)
            bg = Label(self, image=p.b)
            bg.place(relwidth=1, relheigh=1)
        # 窗口背景及属性设置

        self.update()

        def relxy(event):    # 拖动窗口函数，确定单击时的鼠标坐标
            self.mouse_relx = event.x_root - self.winfo_x()
            self.mouse_rely = event.y_root - self.winfo_y()
            self.window_relx = self.winfo_x()

        def top_click(event):    # 拖动窗口函数
            if event.y_root < self.winfo_screenheight() - 75 + self.mouse_rely:
                if self.cksfzdh == 1:
                    self.cksfzdh = 0
                    self.button_list[button.index('□')]['text'] = '□'
                    self.state("normal")

                if topm:
                    self.behind.geometry(str(self.winfo_width() + 10) + 'x' + str(self.winfo_height() + 10) + '+' + str(
                        event.x_root - self.mouse_relx - 5) + '+' + str(event.y_root - self.mouse_rely - 5))
                    self.behind2.geometry(str(self.winfo_width() + 8) + 'x' + str(self.winfo_height() + 8) + '+' + str(
                        event.x_root - self.mouse_relx - 4) + '+' + str(event.y_root - self.mouse_rely - 4))
                    self.behind3.geometry(str(self.winfo_width() + 6) + 'x' + str(self.winfo_height() + 6) + '+' + str(
                        event.x_root - self.mouse_relx - 3) + '+' + str(event.y_root - self.mouse_rely - 3))
                    self.behind4.geometry(str(self.winfo_width() + 4) + 'x' + str(self.winfo_height() + 4) + '+' + str(
                        event.x_root - self.mouse_relx - 2) + '+' + str(event.y_root - self.mouse_rely - 2))
                if self.mouse_relx - self.window_relx > self.winfo_width()-40*len(button):
                    self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                self.mouse_relx - self.winfo_width()-40*len(button)+1) + '+' + str(event.y_root - self.mouse_rely))
                else:
                    self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                self.mouse_relx) + '+' + str(event.y_root - self.mouse_rely))
            else:
                if self.mouse_relx - self.window_relx > self.winfo_width()-40*len(button):
                    self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                self.mouse_relx - self.winfo_width()-40*len(button)+1) + '+' + str(event.y_root - self.mouse_rely))
                else:
                    self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                self.mouse_relx) + '+' + str(event.y_root - self.mouse_rely))
                if topm:
                    self.behind.geometry(str(self.winfo_width() + 10) + 'x' + str(self.winfo_height() + 10) + '+' + str(
                        event.x_root - self.mouse_relx - 5) + '+' + str(self.winfo_screenheight() - 40 - self.mouse_rely - 5))
                    self.behind2.geometry(str(self.winfo_width() + 8) + 'x' + str(self.winfo_height() + 8) + '+' + str(
                        event.x_root - self.mouse_relx - 4) + '+' + str(self.winfo_screenheight() - 40 - self.mouse_rely - 4))
                    self.behind3.geometry(str(self.winfo_width() + 6) + 'x' + str(self.winfo_height() + 6) + '+' + str(
                        event.x_root - self.mouse_relx - 3) + '+' + str(self.winfo_screenheight() - 40 - self.mouse_rely - 3))
                    self.behind4.geometry(str(self.winfo_width() + 4) + 'x' + str(self.winfo_height() + 4) + '+' + str(
                        event.x_root - self.mouse_relx - 2) + '+' + str(self.winfo_screenheight() - 40 - self.mouse_rely - 2))

        top = Label(self, bg=topbg)
        top.place(relwidth=1, height=40, x=0, y=0)
        top.bind('<B1-Motion>', top_click)
        top.bind('<Button-1>', relxy)
        if '□' in button:
            top.bind('<Double-Button-1>', zdh)
        # 窗口上部绿色那一条

        self.wid = Label(self, highlightthickness=0, borderwidth=1, padx=0, pady=0,
                    compound='center', font='楷体', text=title, fg='white', bg=topbg, justify='left')
        self.wid.place(x=15, y=0, height=40)
        self.wid.bind('<B1-Motion>', top_click)
        self.wid.bind('<Button-1>', relxy)
        # 标题Label

        self.button_frame = Frame(self)
        self.button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        self.cksfzdh = 0

        self.button_list = []
        for i in range(len(button)):
            if isinstance(button[i], str):
                self.button_list.append(Button(self.button_frame, text=button[i], font=(
                    'Arail', 16), fg='white', bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            else:
                self.self.button_list.append(Button(self.button_frame, image=button[i], bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            if button[i] != '×':
                Tips(self.button_list[i], tips[i], self, enterf=lambda event, i=i:turn_red(event, i), leavef=lambda event, i=i:turn_green(event, i))
            else:
                Tips(self.button_list[i], '关闭', self, enterf=enter_red, leavef=enter_green)
        # 各个按钮

        separator = Frame(self, height=2, bd=1, relief="sunken")
        separator.place(relx=0.5, y=40, anchor=CENTER, relwidth=1)
        # 分割线

    def destroy(self, jy=True):    # 关闭按钮函数
        if jy:
            for i in range(51):
                if self.top:
                    self.behind.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                    self.behind2.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                    self.behind3.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                    self.behind4.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                self.wm_attributes('-alpha', 1 - i * 0.02)
                time.sleep(0.01)
                if self.top:
                    self.behind.update()
                    self.behind2.update()
                    self.behind3.update()
                    self.behind4.update()
                self.update()
        Tk.destroy(self)
        if self.top:
            try:
                self.behind.destroy()
                self.behind2.destroy()
                self.behind3.destroy()
                self.behind4.destroy()
            except:
                pass

    def mainloop(self, jy=True):
        '''
        参数：
        jy：是否渐隐显示窗口
        '''
        def set_appwindow(root):
            GWL_EXSTYLE = -20
            WS_EX_TOOLWINDOW = 0x00000080
            WS_EX_APPWINDOW = 0x00040000

            hwnd = windll.user32.GetParent(root.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            # re-assert the new window style
            root.wm_withdraw()
            root.after(10, lambda: root.wm_deiconify())

        self.after(0, lambda: set_appwindow(self))
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', i * 0.02)
                if self.top:
                    self.behind.wm_attributes('-alpha', i * 0.02*0.1)
                    self.behind2.wm_attributes('-alpha', i * 0.02*0.1)
                    self.behind3.wm_attributes('-alpha', i * 0.02*0.1)
                    self.behind4.wm_attributes('-alpha', i * 0.02*0.1)
                time.sleep(0.01)
                self.update()
                if self.top:
                    self.behind.update()
                    self.behind2.update()
                    self.behind3.update()
                    self.behind4.update()
        Tk.mainloop(self)
    # TODO(Bill, 2020-10-23):重写title方法

    def geometry(self, wz):
        qwz = wz[:wz.find('+')] if '+' in wz else wz
        Toplevel.geometry(self, wz)
        try:
            self.behind.geometry(str(int(qwz.split('x')[0])+10)+'x'+str(int(qwz.split('x')[1])+10))
            self.behind2.geometry(str(int(qwz.split('x')[0])+8)+'x'+str(int(qwz.split('x')[1])+8))
            self.behind3.geometry(str(int(qwz.split('x')[0])+6)+'x'+str(int(qwz.split('x')[1])+6))
            self.behind4.geometry(str(int(qwz.split('x')[0])+4)+'x'+str(int(qwz.split('x')[1])+4))
        except:
            pass

    def topmost(self, bool):
        if bool:
            try:
                self.behind.deiconify()
                self.behind2.deiconify()
                self.behind3.deiconify()
                self.behind4.deiconify()
            except:
                pass
            self.wm_attributes('-topmost', 1)
        else:
            try:
                self.behind.withdraw()
                self.behind2.withdraw()
                self.behind3.withdraw()
                self.behind4.withdraw()
            except:
                pass
            self.wm_attributes('-topmost', 0)

# TODO:修改changebut和addbut，解决放置图片的奇怪问题
    def change_but(self, button=['□', '×'], abg=['<zdh-y>', '<close-y>'], tips=['最大化/还原', '关闭'], command=['<zdh>', '<close>'], button_color=''):
        if button_color == '':
            button_color = self.button_color

        self.button_text = button
        def turn_red(event, num):
            self.button_list[num]['bg'] = button_color

        def turn_green(event, num):
            self.button_list[num]['bg'] = self.topbg

        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = self.topbg

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = self.topbg

        def zdh(*event):    # 最大化按钮函数
            if self.cksfzdh == 0:
                self.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif self.cksfzdh == 1:
                self.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            self.protocol('WM_DELETE_WINDOW', command[button.index('×')])
        else:
            command[command.index('<close>')] = self.destroy
            self.protocol('WM_DELETE_WINDOW', self.destroy)
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        self.button_frame.place_forget()
        self.button_frame = Frame(self)
        self.button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        self.button_list = []
        for i in range(len(button)):
            if isinstance(button[i], str):
                self.button_list.append(Button(self.button_frame, text=button[i], font=(
                    'Arail', 16), fg='white', bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            else:
                self.self.button_list.append(Button(self.button_frame, image=button[i], bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            if button[i] != '×':
                Tips(self.button_list[i], tips[i], self, enterf=lambda event, i=i:turn_red(event, i), leavef=lambda event, i=i:turn_green(event, i))
            else:
                Tips(self.button_list[i], '关闭', self, enterf=enter_red, leavef=enter_green)
        # 各个按钮

    def add_but(self, button, abg, tips, command, button_color=''):
        '''
        abg为长度为二的元组，第0项是leave，1是enter
        '''
        if button_color == '':
            button_color = self.button_color

        def turn_red(event, num):
            self.button_list[num]['bg'] = button_color

        def turn_green(event, num):
            self.button_list[num]['bg'] = self.topbg

        self.button_text.insert(0, button)
        if isinstance(button, str):
            self.button_list.insert(0, Button(self.button_frame, text=button, font=(
                'Arail', 16), fg='white', bg=self.topbg, command=command, relief='flat', activebackground=self.topbg))
        else:
            self.button_list.insert(0, Button(self.button_frame, image=button, bg=self.topbg, command=command, relief='flat', activebackground=self.topbg))
        Tips(self.button_list[0], tips, self, enterf=lambda event:turn_red(event, 0), leavef=lambda event:turn_green(event, 0))
        for i in range(len(self.button_list)):
            self.button_list[i].place(
                relx=1 / len(self.button_list) * (i + 1), y=0, width=40, height=40, anchor=NE)
        self.button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * (len(self.button_list)), height=40)


class OToplevel(Toplevel): # 会被拖到任务栏下
    '''
    使用如Toplevel一样，对象名=OToplevel(参数)

    参数:
    title：标题，
    win_hei：窗口高度，
    win_wid：窗口长度，
    top：是否始终置于所有窗口顶层(True, False)，如果置顶将会有阴影效果，
    button_color：鼠标飘过时的标题栏按钮颜色
    button：标题栏上的按钮，
    topbg：标题栏的背景颜色，
    abg：各个标题栏上的按钮碰到鼠标的两个颜色函数(，用元组扩起来，与button一一对应)，<zdh-y>代表最大化按钮的颜色函数，<close-y>代表关闭按钮的颜色函数
    tips：提示
    command：各个按钮按下后执行的函数(<close>为关闭窗口，<zdh>为窗口最大化)
    win_bg_lj：窗口背景图片路径
    其他：
    按钮为对象名.button_list[x]，
    <zdh>的按钮必须为□，<zdh-y><close-y>必须分别为□×
    '''
    def __init__(self, title='去框的窗口', win_hei=563, win_wid=1000, top=False, button_color='#40E0D0', button=['□', '×'], topbg='#66CDAA', abg=['<zdh-y>', '<close-y>'], tips=['最大化/还原', '关闭'], command=['<zdh>', '<close>'], win_bg_lj='', yy=False, oimage=True):
        Toplevel.__init__(self)
        topm = top
        self.top = topm
        self.topbg = topbg
        self.button_text = button
        if topm:
            self.behind = Toplevel()
            self.behind.overrideredirect(True)
            self.behind.wm_attributes('-alpha', 0)
            self.behind.wm_attributes('-topmost', True)
            Label(self.behind, bg='black').place(relheight=1, relwidth=1)
            self.behind.geometry(str(win_wid + 10) + 'x' + str(win_hei + 10) + '+' + str(int(self.winfo_screenwidth(
            ) / 2 - (int(win_wid) / 2)) - 5) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 5))
            self.behind2 = Toplevel()
            self.behind2.overrideredirect(True)
            self.behind2.wm_attributes('-alpha', 0)
            self.behind2.wm_attributes('-topmost', True)
            Label(self.behind2, bg='black').place(relheight=1, relwidth=1)
            self.behind2.geometry(str(win_wid + 8) + 'x' + str(win_hei + 8) + '+' + str(int(self.winfo_screenwidth(
            ) / 2 - (int(win_wid) / 2)) - 4) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 4))
            self.behind3 = Toplevel()
            self.behind3.overrideredirect(True)
            self.behind3.wm_attributes('-alpha', 0)
            self.behind3.wm_attributes('-topmost', True)
            Label(self.behind3, bg='black').place(relheight=1, relwidth=1)
            self.behind3.geometry(str(win_wid + 6) + 'x' + str(win_hei + 6) + '+' + str(int(self.winfo_screenwidth(
            ) / 2 - (int(win_wid) / 2)) - 3) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 3))
            self.behind4 = Toplevel()
            self.behind4.overrideredirect(True)
            self.behind4.wm_attributes('-alpha', 0)
            self.behind4.wm_attributes('-topmost', True)
            Label(self.behind4, bg='black').place(relheight=1, relwidth=1)
            self.behind4.geometry(str(win_wid + 4) + 'x' + str(win_hei + 4) + '+' + str(int(self.winfo_screenwidth(
            ) / 2 - (int(win_wid) / 2)) - 2) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 2))

            def yyclick(*event):
                self.wm_attributes('-topmost', 0)
                self.wm_attributes('-topmost', 1)
            self.behind.bind('<Button-1>', yyclick)
            self.behind2.bind('<Button-1>', yyclick)
            self.behind3.bind('<Button-1>', yyclick)
            self.behind4.bind('<Button-1>', yyclick)

        # 创建窗口

        def turn_red(event, num):
            self.button_list[num]['bg'] = button_color

        def turn_green(event, num):
            self.button_list[num]['bg'] = topbg

        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = topbg

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = topbg

        def zdh(*event):    # 最大化按钮函数
            if self.cksfzdh == 0:
                self.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif self.cksfzdh == 1:
                self.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            self.protocol('WM_DELETE_WINDOW', command[button.index('×')])
        else:
            command[command.index('<close>')] = self.destroy
            self.protocol('WM_DELETE_WINDOW', self.destroy)
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        self.title(title)
        self.wm_attributes('-alpha', 0)
        self.overrideredirect(True)
        self.geometry(str(win_wid) + 'x' + str(win_hei) + '+' + str(int(self.winfo_screenwidth() / 2 - (
            int(win_wid) / 2))) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30)))
        if topm:
            self.wm_attributes('-topmost', True)
        if win_bg_lj != '':
            if oimage == True:
                a = Image.open(win_bg_lj)
            else:
                a = win_bg_lj
            if '□' in button:
                a = a.resize((self.winfo_screenwidth(), self.winfo_screenwidth()))
            else:
                a = a.resize((win_wid, win_hei))
            p.b = ImageTk.PhotoImage(a)
            bg = Label(self, image=p.b)
            bg.place(relwidth=1, relheigh=1)
        # 窗口背景及属性设置

        self.update()

        def relxy(event):    # 拖动窗口函数，确定单击时的鼠标坐标
            self.mouse_relx = event.x_root - self.winfo_x()
            self.mouse_rely = event.y_root - self.winfo_y()
            self.window_relx = self.winfo_x()

        def top_click(event):    # 拖动窗口函数
            if event.y_root < self.winfo_screenheight() - 75 + self.mouse_rely:
                if self.cksfzdh == 1:
                    self.cksfzdh = 0
                    self.button_list[button.index('□')]['text'] = '□'
                    self.state("normal")

                if topm:
                    self.behind.geometry(str(self.winfo_width() + 10) + 'x' + str(self.winfo_height() + 10) + '+' + str(
                        event.x_root - self.mouse_relx - 5) + '+' + str(event.y_root - self.mouse_rely - 5))
                    self.behind2.geometry(str(self.winfo_width() + 8) + 'x' + str(self.winfo_height() + 8) + '+' + str(
                        event.x_root - self.mouse_relx - 4) + '+' + str(event.y_root - self.mouse_rely - 4))
                    self.behind3.geometry(str(self.winfo_width() + 6) + 'x' + str(self.winfo_height() + 6) + '+' + str(
                        event.x_root - self.mouse_relx - 3) + '+' + str(event.y_root - self.mouse_rely - 3))
                    self.behind4.geometry(str(self.winfo_width() + 4) + 'x' + str(self.winfo_height() + 4) + '+' + str(
                        event.x_root - self.mouse_relx - 2) + '+' + str(event.y_root - self.mouse_rely - 2))
                if self.mouse_relx - self.window_relx > self.winfo_width()-40*len(button):
                    self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                self.mouse_relx - self.winfo_width()-40*len(button)+1) + '+' + str(event.y_root - self.mouse_rely))
                else:
                    self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                self.mouse_relx) + '+' + str(event.y_root - self.mouse_rely))
            else:
                if self.mouse_relx - self.window_relx > self.winfo_width()-40*len(button):
                    self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                self.mouse_relx - self.winfo_width()-40*len(button)+1) + '+' + str(event.y_root - self.mouse_rely))
                else:
                    self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                self.mouse_relx) + '+' + str(event.y_root - self.mouse_rely))
                if topm:
                    self.behind.geometry(str(self.winfo_width() + 10) + 'x' + str(self.winfo_height() + 10) + '+' + str(
                        event.x_root - self.mouse_relx - 5) + '+' + str(self.winfo_screenheight() - 40 - self.mouse_rely - 5))
                    self.behind2.geometry(str(self.winfo_width() + 8) + 'x' + str(self.winfo_height() + 8) + '+' + str(
                        event.x_root - self.mouse_relx - 4) + '+' + str(self.winfo_screenheight() - 40 - self.mouse_rely - 4))
                    self.behind3.geometry(str(self.winfo_width() + 6) + 'x' + str(self.winfo_height() + 6) + '+' + str(
                        event.x_root - self.mouse_relx - 3) + '+' + str(self.winfo_screenheight() - 40 - self.mouse_rely - 3))
                    self.behind4.geometry(str(self.winfo_width() + 4) + 'x' + str(self.winfo_height() + 4) + '+' + str(
                        event.x_root - self.mouse_relx - 2) + '+' + str(self.winfo_screenheight() - 40 - self.mouse_rely - 2))

        top = Label(self, bg=topbg)
        top.place(relwidth=1, height=40, x=0, y=0)
        top.bind('<B1-Motion>', top_click)
        top.bind('<Button-1>', relxy)
        if '□' in button:
            top.bind('<Double-Button-1>', zdh)
        # 窗口上部绿色那一条

        self.wid = Label(self, highlightthickness=0, borderwidth=1, padx=0, pady=0,
                    compound='center', font='楷体', text=title, fg='white', bg=topbg, justify='left')
        self.wid.place(x=15, y=0, height=40)
        self.wid.bind('<B1-Motion>', top_click)
        self.wid.bind('<Button-1>', relxy)
        # 标题Label

        self.button_frame = Frame(self)
        self.button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        self.cksfzdh = 0

        self.button_list = []
        for i in range(len(button)):
            if isinstance(button[i], str):
                self.button_list.append(Button(self.button_frame, text=button[i], font=(
                    'Arail', 16), fg='white', bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            else:
                self.self.button_list.append(Button(self.button_frame, image=button[i], bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            if button[i] != '×':
                Tips(self.button_list[i], tips[i], self, enterf=lambda event, i=i:turn_red(event, i), leavef=lambda event, i=i:turn_green(event, i))
            else:
                Tips(self.button_list[i], '关闭', self, enterf=enter_red, leavef=enter_green)

        # 各个按钮

        separator = Frame(self, height=2, bd=1, relief="sunken")
        separator.place(relx=0.5, y=40, anchor=CENTER, relwidth=1)
        # 分割线

    def destroy(self, jy=True):    # 关闭按钮函数
        if jy:
            for i in range(51):
                if self.top:
                    self.behind.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                    self.behind2.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                    self.behind3.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                    self.behind4.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                self.wm_attributes('-alpha', 1 - i * 0.02)
                time.sleep(0.01)
                if self.top:
                    self.behind.update()
                    self.behind2.update()
                    self.behind3.update()
                    self.behind4.update()
                self.update()
        Toplevel.destroy(self)
        if self.top:
            self.behind.destroy()
            self.behind2.destroy()
            self.behind3.destroy()
            self.behind4.destroy()

    def mainloop(self, jy=True):
        '''
        参数：
        jy：是否渐隐显示窗口
        '''
        def set_appwindow(root):
            GWL_EXSTYLE = -20
            WS_EX_TOOLWINDOW = 0x00000080
            WS_EX_APPWINDOW = 0x00040000

            hwnd = windll.user32.GetParent(root.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            # re-assert the new window style
            root.wm_withdraw()
            root.after(10, lambda: root.wm_deiconify())

        self.after(0, lambda: set_appwindow(self))
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', i * 0.02)
                if self.top:
                    self.behind.wm_attributes('-alpha', i * 0.02*0.1)
                    self.behind2.wm_attributes('-alpha', i * 0.02*0.1)
                    self.behind3.wm_attributes('-alpha', i * 0.02*0.1)
                    self.behind4.wm_attributes('-alpha', i * 0.02*0.1)
                time.sleep(0.01)
                self.update()
                if self.top:
                    self.behind.update()
                    self.behind2.update()
                    self.behind3.update()
                    self.behind4.update()
        else:
            self.wm_attributes('-alpha', 1)
            if self.top:
                self.behind.wm_attributes('-alpha', 0.1)
                self.behind2.wm_attributes('-alpha', 0.1)
                self.behind3.wm_attributes('-alpha', 0.1)
                self.behind4.wm_attributes('-alpha', 0.1)

    def geometry(self, wz):
        qwz = wz[:wz.find('+')] if '+' in wz else wz
        Toplevel.geometry(self, wz)
        try:
            self.behind.geometry(str(int(qwz.split('x')[0])+10)+'x'+str(int(qwz.split('x')[1])+10))
            self.behind2.geometry(str(int(qwz.split('x')[0])+8)+'x'+str(int(qwz.split('x')[1])+8))
            self.behind3.geometry(str(int(qwz.split('x')[0])+6)+'x'+str(int(qwz.split('x')[1])+6))
            self.behind4.geometry(str(int(qwz.split('x')[0])+4)+'x'+str(int(qwz.split('x')[1])+4))
        except:
            pass

    def topmost(self, bool):
        if bool:
            try:
                self.behind.deiconify()
                self.behind2.deiconify()
                self.behind3.deiconify()
                self.behind4.deiconify()
            except:
                pass
            self.wm_attributes('-topmost', 1)
        else:
            try:
                self.behind.withdraw()
                self.behind2.withdraw()
                self.behind3.withdraw()
                self.behind4.withdraw()
            except:
                pass
            self.wm_attributes('-topmost', 0)

    def change_but(self, button=['□', '×'], abg=['<zdh-y>', '<close-y>'], command=['<zdh>', '<close>']):
        self.button_text = button
        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = self.topbg

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = self.topbg

        def zdh(*event):    # 最大化按钮函数
            if self.cksfzdh == 0:
                self.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif self.cksfzdh == 1:
                self.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            self.protocol('WM_DELETE_WINDOW', command[button.index('×')])
        else:
            command[command.index('<close>')] = self.destroy
            self.protocol('WM_DELETE_WINDOW', self.destroy)
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        self.button_frame.place_forget()
        self.button_frame = Frame(self)
        self.button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        self.button_list = []
        for i in range(len(button)):
            self.button_list.append(Button(self.button_frame, text=button[i], font=(
                'Arail', 16), fg='white', bg=self.topbg, command=command[i], relief='flat', activebackground=self.topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            if button[i] == '×':
                Tips(self.button_list[i], '关闭', self, enterf=abg[i][1], leavef=abg[i][0])
            elif button[i] == '□':
                Tips(self.button_list[i], '最大化/还原', self, enterf=abg[i][1], leavef=abg[i][0])
            else:
                self.button_list[i].bind('<Enter>', abg[i][1])
                self.button_list[i].bind('<Leave>', abg[i][0])

    def add_but(self, button, abg, command):
        '''
        abg为长度为二的元组，第0项是leave，1是enter
        '''
        self.button_text.insert(0, button)
        self.button_list.insert(0, Button(self.button_frame, text=button, font=(
                'Arail', 16), fg='white', bg=self.topbg, command=command, relief='flat', activebackground=self.topbg))
        self.button_list[0].bind('<Enter>', abg[1])
        self.button_list[0].bind('<Leave>', abg[0])
        for i in range(len(self.button_list)):
            self.button_list[i].place(
                relx=1 / len(self.button_list) * (i + 1), y=0, width=40, height=40, anchor=NE)
        self.button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * (len(self.button_list)), height=40)


class OFrame(Frame):
    def oframe(self, title='去框的窗口', button=['□', '×'], topbg='#66CDAA', abg=['<zdh-y>', '<close-y>'], command=['<zdh>', '<close>'], win_bg_lj=''):
        '''
        参数:
        title：标题，
        win_hei：窗口高度，
        win_wid：窗口长度，
        top：是否始终至于所有窗口顶层(True, False)，
        button：标题栏上的按钮，
        topbg：标题栏的背景颜色，
        abg：各个标题栏上的按钮碰到鼠标的两个颜色函数(，用元组扩起来，与button一一对应)，<zdh-y>代表最大化按钮的颜色函数，<close-y>代表关闭按钮的颜色函数
        command：各个按钮按下后执行的函数(<close>为关闭窗口，<zdh>为窗口最大化)
        win_bg_lj：窗口背景图片路径
        其他：
        窗口为对象名.window，
        按钮为对象名.button[x]，
        <zdh>的按钮必须为□，<zdh-y><close-y>必须分别为□×
        '''
        class V:
            pass
        v = V()
        # 创建窗口

        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = topbg

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = topbg

        def zdh(*event):    # 最大化按钮函数
            if v.cksfzdh == 0:
                v.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif v.cksfzdh == 1:
                v.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            pass
        else:
            command[command.index('<close>')] = self.place_forget
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        if win_bg_lj != '' and '\\':
            a = Image.open(win_bg_lj)
            a = a.resize((self.winfo_screenwidth(), self.winfo_screenwidth()))
            b = ImageTk.PhotoImage(a)
            bg = Label(self, image=b)
            bg.place(relwidth=1, relheigh=1)
        # 窗口背景及属性设置

        top = Label(self, bg=topbg)
        top.place(relwidth=1, height=40, x=0, y=0)
        # 窗口上部绿色那一条

        button_frame = Frame(self)
        button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        v.cksfzdh = 0

        self.button_list = []
        for i in range(len(button)):
            self.button_list.append(Button(button_frame, text=button[i], font=(
                'Arail', 16), fg='white', bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            self.button_list[i].bind('<Enter>', abg[i][1])
            self.button_list[i].bind('<Leave>', abg[i][0])

        wid = Label(self, highlightthickness=0, borderwidth=1, padx=0, pady=0,
                    compound='center', font='楷体', text=title, fg='white', bg=topbg)
        wid.place(x=10, y=0, height=40)
        # 标题Label

        separator = Frame(self, height=2, bd=1, relief="sunken")
        separator.place(relx=0.5, y=40, anchor=CENTER, relwidth=1)
        # 分割线


class PwWindow(Tk):
    def __init__(self, transfor, translate, title='数据加解密器', sign='', my=False, random=True):
        Tk.__init__(self)
        transfor = self.add_error(transfor)
        translate = self.add_error(translate)
        class V(object):
            pass

        v = V()
        self.title(title)
        self.minsize(250, 140)
        self.geometry('%dx%d+%d+%d' % (500, 280, (self.winfo_screenwidth() / 2) -
                                            (500 / 2), (self.winfo_screenheight() / 2) - (280 / 2) - 30))
        text1 = Text(self, font=('微软雅黑', 12))
        text1.place(relwidth=0.499, relheigh=1, relx=0, anchor=NW)
        text2 = Text(self, font=('微软雅黑', 12))
        text2.place(relwidth=0.499, relheigh=1, relx=1, anchor=NE)

        def clear1():
            text1.delete(1.0, 'end')

        clear1_b = Button(self, text='清空', command=clear1, relief='groove')
        clear1_b.place(anchor=S, relx=0.25, rely=1, relwidth=0.499)

        def copy2():
            pyperclip.copy(text2.get(1.0, 'end')[:-1])

        copy1_b = Button(self, text='复制', command=copy2, relief='groove')
        copy1_b.place(anchor=S, relx=0.75, rely=1, relwidth=0.499)

        v.mode = IntVar()
        v.mode.set(1)

        cd = Menu(self)
        edit = Menu(self, tearoff=0)
        cd.add_cascade(label='模式', menu=edit)

        def trans():
            if v.mode.get() == 1:
                nr = text1.get(1.0, 'end')[:-1]
                text2.delete(1.0, "end")
                sd = transfor(nr)
                if random:
                    for i in range(30):
                        hc = transfor(nr)
                        if len(hc) < len(sd):
                            sd = hc
                text2.insert('insert', sd)
            if v.mode.get() == 2:
                f = text1.get(1.0, 'end')[:-1]
                text2.delete(1.0, "end")
                text2.insert('insert', translate(f))

        def about():
            aboutk = ScWindow(sign, fs='b', tk=False, win_hei=200, win_wid=300, title='关于', disabled=True)

        def setmy():
            def qued(*event):
                self.miyao = miy.zjet[0].get()
                # print((ord(self.miyao) if len(str(ord(self.miyao))) <= 3 else int(str(ord(self.miyao))[:3])))
                miy.destroy()
            miy = SrWindow(qued, tk=False, title='更改秘钥', zj=['e'], name=['秘钥：'])
            miy.zjet[0].insert('insert', self.miyao)

        edit.add_radiobutton(label='转换为密码', variable=v.mode, value=1)
        edit.add_radiobutton(label='翻译成文字', variable=v.mode, value=2)
        if my:
            cd.add_command(label='秘钥', command=setmy)
        cd.add_command(label='转换', command=trans)
        if sign != '':
            cd.add_command(label='关于', command=about)
        self.config(menu=cd)

    def add_error(self, function):
        def jg(data):
            try:
                a = function(data)
            except:
                messagebox.showerror(title='提示', message='转换失败')
            else:
                return a
        return jg


    def destroy(self, jy=False):
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', 1 - i * 0.02)
                time.sleep(0.01)
                self.update()
        Tk.destroy(self)

    def mainloop(self, jy=False):
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', i * 0.02)
                time.sleep(0.01)
                self.update()
        Tk.mainloop(self)

    def ctgeometry(self, width, height):
        x = int(self.winfo_screenwidth() / 2 - width / 2)
        y = int(self.winfo_screenheight() / 2 - height / 2)
        self.geometry(str(width) + 'x' + str(height) +
                      '+' + str(x) + '+' + str(y))

    def givesign(self, nr='By:Bill', width=100):
        def close():
            self.destroy()
            tk = Tk()
            tk.wm_attributes('-topmost', 1)
            tk.geometry('%dx%d+%d+%d' % (width, 40, (tk.winfo_screenwidth() / 2) -
                                         (width / 2), (tk.winfo_screenheight() / 2) - (20 / 2)))
            tk.overrideredirect(True)
            Label(tk, text=nr, fg='black', font=(
                '华文新魏', 14), relief='ridge').place(relwidth=1, relheight=1)
            for i in range(101):
                tk.wm_attributes('-alpha', (i * 0.01))
                tk.update()
                time.sleep(0.01)
            tk.update()
            time.sleep(1)
            for i in range(101):
                tk.wm_attributes('-alpha', (1 - i * 0.01))
                tk.update()
                time.sleep(0.01)
            tk.destroy()
        self.protocol('WM_DELETE_WINDOW', close)


class KeySrScWindow(PwWindow):
    '''
    KeySrScWindow为实时的输入输出界面
    '''

    def __init__(self, **kw):
        '''
        参数：
            function：处理数据的函数
            width：窗口宽度
            height：窗口高度
            entrynum：输入框个数
            entryheight：输入框高度
            gapheight：间隙高度
            relSrwidth：输入界面相对宽度
            relScwidth：输出界面相对宽度
            titlestr：标题
            name：输入框名称，列表
        '''
        Tk.__init__(self)

        #self.setDefaultPara(['function', 'width', 'titlestr', 'relScwidth', 'relSrwidth', 'entryheight', 'gapheight', 'entrynum', 'height', 'name'],
        #                    ['self.defaultFunction', '400', "'输入与输出'", '0.5', '0.5', '30', '20', '2', 'self.gapheight*(self.entrynum+1)+self.entryheight*self.entrynum', "['数值1', '数值2']"], kw)
        self.function = kw['function'] if 'function' in kw else self.defaultFunction
        self.width = kw['width'] if 'width' in kw else 400
        self.titlestr = kw['titlestr'] if 'titlestr' in kw else '输入与输出'
        self.relScwidth = kw['relScwidth'] if 'relScwidth' in kw else 0.5
        self.relSrwidth = kw['relSrwidth'] if 'relSrwidth' in kw else 0.5
        self.entryheight = kw['entryheight'] if 'entryheight' in kw else 30
        self.gapheight = kw['gapheight'] if 'gapheight' in kw else 20
        self.entrynum = kw['entrynum'] if 'entrynum' in kw else 2
        self.height = kw['height'] if 'height' in kw else self.gapheight * \
            (self.entrynum + 1) + self.entryheight * self.entrynum
        self.name = kw['name'] if 'name' in kw else ['数值1', '数值2']

        self.ctgeometry(self.width, self.height)
        self.title(self.titlestr)

        self.srf = Frame(self)
        self.scf = Frame(self)
        self.separate = Frame(self, relief='sunken', bd=1)

        self.sctext = Text(self.scf, font=('微软雅黑', 10))
        self.sctext.place(height=self.height - 40,
                          relwidth=0.8, relx=0.5, y=self.gapheight, anchor=N)

        self.entrylist = []
        for i in range(self.entrynum):
            self.entrylist.append(PlaholEntry(
                self.srf, placeholder=self.name[i]))
            self.entrylist[i].place(anchor=N, relwidth=0.8, height=self.entryheight,
                                    relx=0.5, y=self.gapheight * (i + 1) + self.entryheight * i)
            self.entrylist[i].bind('<Key>', self.processedFunction)
            self.entrylist[i].bind('<Up>', lambda event, num=i: self.upwards(event, num))
            self.entrylist[i].bind('<Down>', lambda event, num=i: self.downwards(event, num))

        self.srf.place(relheight=1, relwidth=self.relSrwidth, x=0, y=0)
        self.scf.place(relheight=1, relwidth=self.relScwidth,
                       relx=1, y=0, anchor=NE)
        self.separate.place(relx=self.relSrwidth, y=0, relheight=1, width=2)

    def upwards(self, event, num):
        try:
            self.entrylist[num-1].focus_set()
        except:
            pass

    def downwards(self, event, num):
        try:
            self.entrylist[num+1].focus_set()
        except:
            pass

    def setDefaultPara(self, key, value, kw):
        '''
        key与value均为字符串列表
        '''
        if not len(key) == len(value):
            raise ValueError('key参数与value参数长度不一致')
        for i in range(len(key)):
            print("self.%s = kw['%s'] if '%s' in kw else %s" %
                  (key[i], key[i], key[i], value[i]))

    def defaultFunction(self, *nr):
        return ','.join(nr)

    def processedFunction(self, event):
        def thr():
            self.sctext.delete(1.0, END)
            a = [i.get() for i in self.entrylist]
            for i in range(len(a)):
                if a[i] == self.name[i]:
                    a[i] = ''
            if not '' in a:
                self.sctext.insert(END, str(
                    self.function(*a)))
        a = threading.Thread(target=thr)
        a.setDaemon(True)
        a.start()

    def ctgeometry(self, width, height):
        PwWindow.ctgeometry(self, width, height)
        self.width = width
        self.height = height
"""
class OBTk(Tk):
    '''
    使用如Tk一样，对象名=Otk(参数)

    参数:
    title：标题，
    win_hei：窗口高度，
    win_wid：窗口长度，
    top：是否始终至于所有窗口顶层(True, False)，
    button：标题栏上的按钮，
    topbg：标题栏的背景颜色，
    abg：各个标题栏上的按钮碰到鼠标的两个颜色函数(，用元组扩起来，与button一一对应)，<zdh-y>代表最大化按钮的颜色函数，<close-y>代表关闭按钮的颜色函数
    command：各个按钮按下后执行的函数(<close>为关闭窗口，<zdh>为窗口最大化)
    win_bg_lj：窗口背景图片路径
    其他：
    按钮为对象名.button[x]，
    <zdh>的按钮必须为□，<zdh-y><close-y>必须分别为□×
    '''

    def __init__(self, title='去框的窗口', win_hei=563, win_wid=1000, top=False, button=['□', '×'], topbg='#66CDAA', abg=['<zdh-y>', '<close-y>'], command=['<zdh>', '<close>'], win_bg_lj=''):
        Tk.__init__(self)
        self.behind = Toplevel()
        self.behind.overrideredirect(True)
        self.behind.wm_attributes('-alpha', 0.2)
        Label(self.behind, bg='black').place(relheight=1, relwidth=1)
        self.behind.geometry(str(win_wid + 10) + 'x' + str(win_hei + 10) + '+' + str(int(self.winfo_screenwidth(
        ) / 2 - (int(win_wid) / 2)) - 5) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 5))

        class V:
            pass
        v = V()
        # 创建窗口

        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = '#66CDAA'

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = '#66CDAA'

        def zdh(*event):    # 最大化按钮函数
            if v.cksfzdh == 0:
                v.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif v.cksfzdh == 1:
                v.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            pass
        else:
            command[command.index('<close>')] = self.destroy
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        self.title(title)
        self.wm_attributes('-alpha', 0)
        self.overrideredirect(True)
        self.geometry(str(win_wid) + 'x' + str(win_hei) + '+' + str(int(self.winfo_screenwidth() / 2 - (
            int(win_wid) / 2))) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30)))
        if top:
            self.wm_attributes('-topmost', True)
        if win_bg_lj != '' and '\\':
            a = Image.open(win_bg_lj)
            a = a.resize((self.winfo_screenwidth(), self.winfo_screenwidth()))
            b = ImageTk.PhotoImage(a)
            bg = Label(self, image=b)
            bg.place(relwidth=1, relheigh=1)
        # 窗口背景及属性设置

        self.update()

        def relxy(event):    # 拖动窗口函数，确定单击时的鼠标坐标
            v.mouse_relx = event.x_root - self.winfo_x()
            v.mouse_rely = event.y_root - self.winfo_y()
            v.window_relx = self.winfo_x()

        def top_click(event):    # 拖动窗口函数
            if event.y_root < self.winfo_screenheight() - 75 + v.mouse_rely:
                if v.cksfzdh == 1:
                    v.cksfzdh = 0
                    self.button_list[button.index('□')]['text'] = '□'
                    self.state("normal")

                self.behind.geometry(str(self.winfo_width() + 10) + 'x' + str(self.winfo_height() + 10) + '+' + str(
                    event.x_root - v.mouse_relx - 5) + '+' + str(event.y_root - v.mouse_rely - 5))
                self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(
                    event.x_root - v.mouse_relx) + '+' + str(event.y_root - v.mouse_rely))
            else:
                self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                                   v.mouse_relx) + '+' + str(self.winfo_screenheight() - 75))

        top = Label(self, bg=topbg)
        top.place(relwidth=1, height=40, x=0, y=0)
        top.bind('<B1-Motion>', top_click)
        top.bind('<Button-1>', relxy)
        if '□' in button:
            top.bind('<Double-Button-1>', zdh)
        # 窗口上部绿色那一条

        button_frame = Frame(self)
        button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        v.cksfzdh = 0

        self.button_list = []
        for i in range(len(button)):
            self.button_list.append(Button(button_frame, text=button[i], font=(
                'Arail', 16), fg='white', bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            self.button_list[i].bind('<Enter>', abg[i][1])
            self.button_list[i].bind('<Leave>', abg[i][0])

        wid = Label(self, highlightthickness=0, borderwidth=1, padx=0, pady=0,
                    compound='center', font='楷体', text=title, fg='white', bg=topbg)
        wid.place(x=15, y=0, height=40, width=90)
        wid.bind('<B1-Motion>', top_click)
        wid.bind('<Button-1>', relxy)
        # 标题Label

        separator = Frame(self, height=2, bd=1, relief="sunken")
        separator.place(relx=0.5, y=40, anchor=CENTER, relwidth=1)
        # 分割线

    def destroy(self, jy=True):    # 关闭按钮函数
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', 1 - i * 0.02)
                self.behind.wm_attributes('-alpha', (1 - i * 0.02) * 0.2)
                time.sleep(0.01)
                self.update()
                self.behind.update()
        Tk.destroy(self)

    def mainloop(self, jy=True):
        '''
        参数：
        jy：是否渐隐显示窗口
        '''
        def set_appwindow(root):
            GWL_EXSTYLE = -20
            WS_EX_TOOLWINDOW = 0x00000080
            WS_EX_APPWINDOW = 0x00040000

            hwnd = windll.user32.GetParent(root.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            # re-assert the new window style
            root.wm_withdraw()
            root.after(10, lambda: root.wm_deiconify())

        self.after(0, lambda: set_appwindow(self))
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', i * 0.02)
                time.sleep(0.01)
                self.update()
        Tk.mainloop(self)


class OBToplevel(Toplevel):
    '''
    使用如Toplevel一样，对象名=Otk(参数)

    参数:
    title：标题，
    win_hei：窗口高度，
    win_wid：窗口长度，
    top：是否始终至于所有窗口顶层(True, False)，
    button：标题栏上的按钮，
    topbg：标题栏的背景颜色，
    abg：各个标题栏上的按钮碰到鼠标的两个颜色函数(，用元组扩起来，与button一一对应)，<zdh-y>代表最大化按钮的颜色函数，<close-y>代表关闭按钮的颜色函数
    command：各个按钮按下后执行的函数(<close>为关闭窗口，<zdh>为窗口最大化)
    win_bg_lj：窗口背景图片路径
    其他：
    按钮为对象名.button[x]，
    <zdh>的按钮必须为□，<zdh-y><close-y>必须分别为□×
    '''

    def __init__(self, title='去框的窗口', win_hei=563, win_wid=1000, top=False, button=['□', '×'], topbg='#66CDAA', abg=['<zdh-y>', '<close-y>'], command=['<zdh>', '<close>'], win_bg_lj=''):
        Toplevel.__init__(self)
        self.behind = Toplevel()
        self.behind.overrideredirect(True)
        self.behind.wm_attributes('-alpha', 0)
        self.behind.wm_attributes('-topmost', True)
        Label(self.behind, bg='black').place(relheight=1, relwidth=1)
        self.behind.geometry(str(win_wid + 10) + 'x' + str(win_hei + 10) + '+' + str(int(self.winfo_screenwidth(
        ) / 2 - (int(win_wid) / 2)) - 5) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 5))
        self.behind2 = Toplevel()
        self.behind2.overrideredirect(True)
        self.behind2.wm_attributes('-alpha', 0)
        self.behind2.wm_attributes('-topmost', True)
        Label(self.behind2, bg='black').place(relheight=1, relwidth=1)
        self.behind2.geometry(str(win_wid + 8) + 'x' + str(win_hei + 8) + '+' + str(int(self.winfo_screenwidth(
        ) / 2 - (int(win_wid) / 2)) - 4) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 4))
        self.behind3 = Toplevel()
        self.behind3.overrideredirect(True)
        self.behind3.wm_attributes('-alpha', 0)
        self.behind3.wm_attributes('-topmost', True)
        Label(self.behind3, bg='black').place(relheight=1, relwidth=1)
        self.behind3.geometry(str(win_wid + 6) + 'x' + str(win_hei + 6) + '+' + str(int(self.winfo_screenwidth(
        ) / 2 - (int(win_wid) / 2)) - 3) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 3))
        self.behind4 = Toplevel()
        self.behind4.overrideredirect(True)
        self.behind4.wm_attributes('-alpha', 0)
        self.behind4.wm_attributes('-topmost', True)
        Label(self.behind4, bg='black').place(relheight=1, relwidth=1)
        self.behind4.geometry(str(win_wid + 4) + 'x' + str(win_hei + 4) + '+' + str(int(self.winfo_screenwidth(
        ) / 2 - (int(win_wid) / 2)) - 2) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30) - 2))

        class V:
            pass
        v = V()
        # 创建窗口

        def enter_red(event):
            self.button_list[button.index('×')]['bg'] = 'red'

        def enter_green(event):
            self.button_list[button.index('×')]['bg'] = '#66CDAA'

        def zdh_red(event):
            self.button_list[button.index('□')]['bg'] = '#40E0D0'

        def zdh_green(event):
            self.button_list[button.index('□')]['bg'] = '#66CDAA'

        def zdh(*event):    # 最大化按钮函数
            if v.cksfzdh == 0:
                v.cksfzdh = 1
                self.state("zoomed")
                self.button_list[button.index('□')]['text'] = '〼'
                self.button_list[button.index('□')]['font'] = ('Arail', 14)
            elif v.cksfzdh == 1:
                v.cksfzdh = 0
                self.button_list[button.index('□')]['text'] = '□'
                self.state("normal")

        try:
            command.index('<zdh>')
        except:
            pass
        else:
            command[command.index('<zdh>')] = zdh
        try:
            command.index('<close>')
        except:
            pass
        else:
            command[command.index('<close>')] = self.destroy
        try:
            abg.index('<zdh-y>')
        except:
            pass
        else:
            abg[abg.index('<zdh-y>')] = (zdh_green, zdh_red)
        try:
            abg.index('<close-y>')
        except:
            pass
        else:
            abg[abg.index('<close-y>')] = (enter_green, enter_red)

        self.title(title)
        self.wm_attributes('-alpha', 0)
        self.overrideredirect(True)
        self.geometry(str(win_wid) + 'x' + str(win_hei) + '+' + str(int(self.winfo_screenwidth() / 2 - (
            int(win_wid) / 2))) + '+' + str(int(self.winfo_screenheight() / 2 - (int(win_hei) / 2) - 30)))
        if top:
            self.wm_attributes('-topmost', True)
        if win_bg_lj != '' and '\\':
            a = Image.open(win_bg_lj)
            a = a.resize((self.winfo_screenwidth(), self.winfo_screenwidth()))
            b = ImageToplevel.PhotoImage(a)
            bg = Label(self, image=b)
            bg.place(relwidth=1, relheigh=1)
        # 窗口背景及属性设置

        self.update()

        def relxy(event):    # 拖动窗口函数，确定单击时的鼠标坐标
            v.mouse_relx = event.x_root - self.winfo_x()
            v.mouse_rely = event.y_root - self.winfo_y()
            v.window_relx = self.winfo_x()

        def top_click(event):    # 拖动窗口函数
            if event.y_root < self.winfo_screenheight() - 75 + v.mouse_rely:
                if v.cksfzdh == 1:
                    v.cksfzdh = 0
                    self.button_list[button.index('□')]['text'] = '□'
                    self.state("normal")

                self.behind.geometry(str(self.winfo_width() + 10) + 'x' + str(self.winfo_height() + 10) + '+' + str(
                    event.x_root - v.mouse_relx - 5) + '+' + str(event.y_root - v.mouse_rely - 5))
                self.behind2.geometry(str(self.winfo_width() + 8) + 'x' + str(self.winfo_height() + 8) + '+' + str(
                    event.x_root - v.mouse_relx - 4) + '+' + str(event.y_root - v.mouse_rely - 4))
                self.behind3.geometry(str(self.winfo_width() + 6) + 'x' + str(self.winfo_height() + 6) + '+' + str(
                    event.x_root - v.mouse_relx - 3) + '+' + str(event.y_root - v.mouse_rely - 3))
                self.behind4.geometry(str(self.winfo_width() + 4) + 'x' + str(self.winfo_height() + 4) + '+' + str(
                    event.x_root - v.mouse_relx - 2) + '+' + str(event.y_root - v.mouse_rely - 2))
                self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(
                    event.x_root - v.mouse_relx) + '+' + str(event.y_root - v.mouse_rely))
            else:
                self.geometry(str(self.winfo_width()) + 'x' + str(self.winfo_height()) + '+' + str(event.x_root -
                                                                                                   v.mouse_relx) + '+' + str(self.winfo_screenheight() - 75))

        top = Label(self, bg=topbg)
        top.place(relwidth=1, height=40, x=0, y=0)
        top.bind('<B1-Motion>', top_click)
        top.bind('<Button-1>', relxy)
        if '□' in button:
            top.bind('<Double-Button-1>', zdh)
        # 窗口上部绿色那一条

        button_frame = Frame(self)
        button_frame.place(relx=1, rely=0, anchor=NE,
                           width=40 * len(button), height=40)

        v.cksfzdh = 0

        self.button_list = []
        for i in range(len(button)):
            self.button_list.append(Button(button_frame, text=button[i], font=(
                'Arail', 16), fg='white', bg=topbg, command=command[i], relief='flat', activebackground=topbg))
            self.button_list[i].place(
                relx=1 / len(button) * (i + 1), y=0, width=40, height=40, anchor=NE)
            self.button_list[i].bind('<Enter>', abg[i][1])
            self.button_list[i].bind('<Leave>', abg[i][0])

        wid = Label(self, highlightthickness=0, borderwidth=1, padx=0, pady=0,
                    compound='center', font='楷体', text=title, fg='white', bg=topbg)
        wid.place(x=15, y=0, height=40, width=90)
        wid.bind('<B1-Motion>', top_click)
        wid.bind('<Button-1>', relxy)
        # 标题Label

        separator = Frame(self, height=2, bd=1, relief="sunken")
        separator.place(relx=0.5, y=40, anchor=CENTER, relwidth=1)
        # 分割线

    def destroy(self, jy=True):    # 关闭按钮函数
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', 1 - i * 0.02)
                self.behind.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                self.behind2.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                self.behind3.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                self.behind4.wm_attributes('-alpha', (1 - i * 0.02) * 0.1)
                time.sleep(0.01)
                self.update()
                self.behind.update()
                self.behind2.update()
                self.behind3.update()
                self.behind4.update()
        Toplevel.destroy(self)
        self.behind.destroy()
        self.behind2.destroy()
        self.behind3.destroy()
        self.behind4.destroy()

    def mainloop(self, jy=True):
        '''
        参数：
        jy：是否渐隐显示窗口
        '''
        def set_appwindow(root):
            GWL_EXSTYLE = -20
            WS_EX_TOOLWINDOW = 0x00000080
            WS_EX_APPWINDOW = 0x00040000

            hwnd = windll.user32.GetParent(root.winfo_id())
            style = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            style = style & ~WS_EX_TOOLWINDOW
            style = style | WS_EX_APPWINDOW
            res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
            # re-assert the new window style
            root.wm_withdraw()
            root.after(10, lambda: root.wm_deiconify())

        self.after(0, lambda: set_appwindow(self))
        if jy:
            for i in range(51):
                self.wm_attributes('-alpha', i * 0.02)
                self.behind.wm_attributes('-alpha', i * 0.02*0.1)
                self.behind2.wm_attributes('-alpha', i * 0.02*0.1)
                self.behind3.wm_attributes('-alpha', i * 0.02*0.1)
                self.behind4.wm_attributes('-alpha', i * 0.02*0.1)
                time.sleep(0.01)
                self.update()
                self.behind.update()
                self.behind2.update()
                self.behind3.update()
                self.behind4.update()
"""


if __name__ == '__main__':
    a = OTk(button=['□', '×'], abg=['<zdh-y>', '<close-y>'], command=[lambda:b.change_but(button=['□', '×'], abg=['<zdh-y>', '<close-y>'], command=['<zdh>', '<close>']), '<close>'])
    b = OToplevel(button=['×'], abg=['<close-y>'], command=['<close>'], title='test1', win_wid=300, win_hei=100, top=True)
    b.mainloop()
    a.mainloop()
