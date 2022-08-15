from tkinter import *
import time
from PIL import Image, ImageTk, ImageFilter, ImageDraw, ImageEnhance

class SideMenu(Frame):
    '''
    SideMenu为侧边的选择菜单
    '''
    def __init__(self, master=None, indheight=30, func=[print], text=['SideMenu'], bg='white', lg='blue', lgwidth=5, enleave='bg', abg='#DCDCDC', font=('微软雅黑', 12), width=200, height=400, **kw):
        '''
        参数：
            master：父容器
            indheight：每个选项组件的高度
            func：每个选项对应的函数
            text：每个选项对应的文字
            bg：背景颜色
            lg：被选中选项的颜色
            lgwidth：表示条宽度
            enleave：鼠标指针飘过选项时的强调样式，参数值必须为none，relief, bg, rebg。none代表鼠标指针飘过时不强调，relief代表飘过时改变relief，bg代表改变bg，rebg代表同时改变relief和bg
            abg：当enleave参数为bg或rebg时，表示强调所改变的组件背景颜色
            width, height：分别为宽度和高度，也可在布局管理器中调整
        实例变量：
            cho：当前被选中的选项序数，从0开始
            oplist：按钮对象列表
        注意：
            func与text的长度必须一致
        '''
        if len(func) != len(text):
            raise ValueError('func参数与text参数项数不一致')
        if not enleave in ('none', 'relief', 'bg', 'rebg'):
            raise ValueError('enleave参数值错误')

        Frame.__init__(self, master, bg=bg, width=width, height=height, **kw)

        def rfunc(f):
            if self.cho != f:
                self.cho = f
                chol.place(width=lgwidth, height=indheight, y=indheight*self.cho)
                func[f]()

        def touch(event, op, fs):
            if fs == 'rebg' or fs == 'bg':
                op['bg'] = abg
            if fs == 'rebg' or fs == 'relief':
                op['relief'] = 'groove'
        def leave(event, op, fs):
            if fs == 'rebg' or fs == 'bg':
                op['bg'] = bg
            if fs == 'rebg' or fs == 'relief':
                op['relief'] = 'flat'

        self.oplist = []
        lblist = []
        for i in range(len(text)):
            self.oplist.append(Button(self, text=text[i], bg=bg, relief='flat', font=font, command=lambda i=i: rfunc(i)))
            if enleave != 'none':
                self.oplist[i].bind('<Enter>', lambda event, i=i: touch(event, self.oplist[i], enleave))
                self.oplist[i].bind('<Leave>', lambda event, i=i: leave(event, self.oplist[i], enleave))
            self.oplist[i].place(relwidth=1, height=indheight, y=indheight*i)
        if enleave != 'relief' and enleave != 'rebg':
            for i in range(len(text)):
                Frame(self, relief='sunken', bd=1,).place(relx=0.5, anchor=CENTER, relwidth=1, height=2, y=indheight*(i+1))

        Frame(self, relief='sunken', bd=1,).place(relx=1, anchor=E, width=2, relheight=1, rely=0.5)
        self.cho = 0
        chol = Label(self, bg=lg)
        chol.place(width=lgwidth, height=indheight, y=indheight*self.cho)
        self.cho = -1
        rfunc(0)


class SliButton(Canvas):
    '''
    SliButton为更加美观且可拖动的滑动条
    建议将窗口overrideredirect，否则就给定thick以窗口边框厚度的值，win7的貌似为8
    '''
    def __init__(self, window, x, width, master=None, state='normal', lwidth=10, bg='#dcdcdc', lg='yellow', image=None, thick=0, sliburlf='flat', **kw):
        '''
        参数：
            window：窗口
            x：该控件相对于窗口的横坐标（注意：是窗口而不是父容器）
            width：该容器的长度
            master：父容器
            state：控件样式，默认为normal，还可disabled
            lwidth：slibu的长，当state为disabled时无效
            bg：背景颜色
            lg：滑动条颜色
            image：整个控件的背景图片(常用于透明)，设置后bg参数无效
            thick：窗口边框厚度
            sliburlf：拖动按钮的样式，必须为raised或flat
        实例变量：
            value, x, width, window, thick, slibu, ismove
        '''
        if not sliburlf in ('raised', 'flat'):
            raise ValueError('sliburlf参数错误')
        
        Canvas.__init__(self, master, bg=bg, width=width+lwidth/2, height=4, highlightthickness=0, **kw)
        if image != None:
            self.create_image(0, 0, image=image, anchor=NW)
        
        self.value = 0.50
        self.window = window
        self.x = x
        self.width = width
        self.thick = thick
        self.ismove = False
        self.state = state
        self.lwidth = lwidth

        self.__progr = Label(self, bg=lg)
        self.__progr.place(width=self.value*self.width, relheight=1, x=0, y=0)
        if self.state == 'normal':
            self.slibu = Label(self, relief=sliburlf, highlightthickness=0, bg='white')
            self.slibu.place(anchor=N, relheight=1, width=self.lwidth, x=self.value*self.width, y=0)
            self.slibu.bind('<B1-Motion>', self.__move)
            self.slibu.bind('<Button-1>', self.__gselx)
            self.slibu.bind('<ButtonRelease-1>', self.__notmove)
            self.bind('<Button-1>', self.__clickto)
            self.__progr.bind('<Button-1>', self.__clickto)
            if sliburlf == 'flat':
                pass # slibu前后加两条杠
            def touch(*event):
                if sliburlf == 'raised':
                    self.slibu['relief'] = 'sunken'
                elif sliburlf == 'flat':
                    self.slibu['bg'] = 'grey'
            def leave(*event):
                if not self.ismove:
                    if sliburlf == 'raised':
                        self.slibu['relief'] = 'raised'
                    elif sliburlf == 'flat':
                        self.slibu['bg'] = 'white'
            self.slibu.bind('<Enter>', touch)
            self.slibu.bind('<Leave>', leave)
        

    def get_value(self):
        '''
        用于获取value属性值，相当于直接读取self.value
        '''
        return self.value

    def set_value(self, num):
        '''
        用于设置value属性值并刷新进度条
        参数：
            num：value属性值，范围为0到1
        '''
        self.value = num
        self.__progr.place(width=self.value*self.width, relheight=1, x=0, y=0)
        if self.state == 'normal':
            self.slibu.place(anchor=N, relheight=1, width=self.lwidth, x=self.value*self.width, y=0)

    def __gselx(self, event):
        # 按下
        self.ismove = True
        self.__selx = event.x_root-self.window.winfo_x()-self.x - self.value*self.width - self.thick

    def __notmove(self, event):
        # 松开
        self.ismove = False

    def __move(self, *event):
        # 拖动
        print(event[0].x)
        if event[0].x_root-self.window.winfo_x()-self.x-self.__selx - self.thick <= 0:
            self.value = 0.00
        elif event[0].x_root-self.window.winfo_x()-self.x-self.__selx - self.thick >= self.width:
            self.value = 1.00
        else:
            self.value = (event[0].x_root-self.window.winfo_x()-self.x-self.__selx - self.thick)/self.width
        self.__progr.place(width=self.value*self.width, relheight=1, x=0, y=0)
        self.slibu.place(anchor=N, relheight=1, width=self.lwidth, x=self.value*self.width, y=0)

    def __clickto(self, *event):
        self.value = (event[0].x_root-self.window.winfo_x()-self.x- self.thick)/self.width
        self.__progr.place(width=self.value*self.width, relheight=1, x=0, y=0)
        self.slibu.place(relheight=1, width=self.lwidth, x=self.value*self.width, y=0)

    def auto_move(self, boo, whole=10000, each=1000, mode='after'):
        '''
        用于设置进度条自动播放
        参数：
            boo：True或False，可用False表示暂停
            whole：播放完一共所需的时间，以微秒为单位
            each：每次播放所间隔的时间，以微秒为单位
            mode：默认为after，即使用window.after，还可设置为sleep，即使用time.sleep
        '''          
        self.auto = boo
        self.speed = each/whole
        self.mode = mode
        if boo:
            if mode == 'after':
                def amo():
                    if self.ismove == False and int(self.value) != 1 and self.auto:
                        self.value = self.value +each/whole
                        if self.value>1:
                            self.value =1.00
                        self.__progr.place(width=self.value*self.width, relheight=1, x=0, y=0)
                        if self.state == 'normal':
                            self.slibu.place(anchor=N, relheight=1, width=self.lwidth, x=self.value*self.width, y=0)
                        self.window.update()
                    if self.auto and self.speed == each/whole and self.mode == mode:
                        self.window.after(each, bmo)
                def bmo():
                    if self.ismove == False and int(self.value) != 1 and self.auto:
                        self.value = self.value +each/whole
                        if self.value>1:
                            self.value =1.00
                        self.__progr.place(width=self.value*self.width, relheight=1, x=0, y=0)
                        if self.state == 'normal':
                            self.slibu.place(anchor=N, relheight=1, width=self.lwidth, x=self.value*self.width, y=0)
                        self.window.update()
                    if self.auto and self.speed == each/whole and self.mode == mode:
                        self.window.after(each, amo)
                self.window.after(each, amo)
            elif mode == 'sleep':
                time.sleep(each/1000)
                while self.auto and self.speed == each/whole and self.mode == mode and int(self.value) != 1 :
                    if self.ismove == False and self.auto:
                        self.value = self.value +each/whole
                        if self.value>1:
                            self.value =1.00
                        self.__progr.place(width=self.value*self.width, relheight=1, x=0, y=0)
                        if self.state == 'normal':
                            self.slibu.place(anchor=N, relheight=1, width=self.lwidth, x=self.value*self.width, y=0)
                        self.window.update()
                    time.sleep(each/1000)
            else:
                raise ValueError('mode参数错误')

    def place(self, cnf={}, **kw):
        '''
        重写了Canvas的place_configure以适应SliButton，除了relwidth之外所有参数均一样，可不输入width参数
        '''
        if 'relwidth' in kw:
            raise ValueError('SliButton的place不支持relwidth参数')
        kw['width'] = self.width + self.lwidth/2
        Canvas.place(self, cnf, **kw)


class CheckPic(Frame):
    def __init__(self, master=None, bl=False, image='', picname='', cnf={}, **kw):
        Frame.__init__(self, master, cnf, **kw)
        picl = Label(self, image=image)
        picl.place(relwidth=1, relheight=1, x=0, y=0)
        self.var = IntVar()
        self.checkbuton = Checkbutton(self, width=15, height=15, variable=self.var, onvalue=1, offvalue=0)
        if bl:
            self.checkbuton.select()
        else:
            self.checkbuton.deselect()
        def click(event):
            if self.var.get() == 1:
                self.checkbuton.deselect()
            else:
                self.checkbuton.select()
        picl.bind('<Button-1>', click)
        self.checkbuton.place(x=0, y=0, width=15, height=14)
        self.pic_name = picname
    def get(self):
        return self.var.get()
    def set(self, num):
        self.var.set(num)


class CheckLabel(Frame):
    def __init__(self, master=None, win=0, bl=False, text='', labelfont=('楷体', 12), labelname='', cbx=0, cby=9, cnf={}, **kw):
        Frame.__init__(self, master, cnf, **kw)
        lab = Label(self, text='  '+text, font=labelfont, anchor=W)
        lab.place(relwidth=1, relheight=1, x=0, y=0)
        if win != 0:
            Tips(lab, text.lstrip(), win)
        self.var = IntVar()
        self.checkbuton = Checkbutton(self, width=15, height=15, variable=self.var, onvalue=1, offvalue=0)
        if bl:
            self.checkbuton.select()
        else:
            self.checkbuton.deselect()
            
        self.checkbuton.place(x=cbx, y=cby, width=15, height=14)
        
        self.labelname = labelname
    def get(self):
        return self.var
    def set(self, num):
        self.var = num


class Tips(object):
    '''
    给组件设置当鼠标碰到组件时的提示
    '''
    def __none(self):
        pass
    def __init__(self, exam, text, wind, tim=500, enterf=__none, leavef=__none, motionf=__none, clickf=__none):
        '''
        参数：
            exam：组件对象
            text：显示文本
            wind：窗口对象
            tim：触发时间
            enterf：<Enter>绑定的其他函数
            leavef：<Leave>绑定的其他函数
            motionf：<Motion>绑定的其他函数
        '''
        self.win = []
        self.iin = False
        self.wz = False
        self.isclick = False
        self.exam = exam
        self.text = text
        self.wind = wind
        self.tim = tim
        self.enterf = enterf
        self.leavef = leavef
        self.motionf = motionf
        self.clickf = clickf
        self.exam.bind('<Enter>', self.enter)
        self.exam.bind('<Leave>', self.leave)
        self.exam.bind('<Motion>', self.motion)
        self.exam.bind('<Button-1>', self.click)
    def enter(self, *event):
        '''
        给组件<Enter>绑定的方法，如需自定义请按照以下语句或更改enterf参数：
            def 函数名(*event):
                Tips.enter(对象名, event)
                <自定义内容>
            对象名.enter = 函数名
        '''
        self.enterf(event)
        self.iin = True
        def showtip():
            if self.iin and self.wz != False and self.isclick == False:
                self.win.append(Toplevel())
                self.win[-1].overrideredirect(True)
                self.win[-1].wm_attributes('-topmost', 1)
                Label(self.win[-1], text=self.text, relief='solid', bd=1, bg='white').pack()
                self.win[-1].geometry('+'+str(self.wz[0]+10)+'+'+str(self.wz[1]+10))
                self.win[-1].update()
        if self.iin:
            self.wind.after(self.tim, showtip)
    def leave(self, *event):
        '''
        给组件<Leave>绑定的方法，如需自定义请按照以下语句或更改leavef参数：
            def 函数名(*event):
                Tips.leave(对象名, event)
                <自定义内容>
            对象名.leave = 函数名
        '''
        self.leavef(event)
        self.iin = False
        self.isclick = False
        for i in self.win:
            try:
                i.destroy()
            except:
                pass
        self.win = []
    def motion(self, *event):
        '''
        给组件<Motion>绑定的方法，如需自定义请按照以下语句或更改motionf参数：
            def 函数名(*event):
                Tips.motion(对象名, event)
                <自定义内容>
            对象名.motion = 函数名
        '''
        self.motionf(event)
        self.wz = (event[0].x_root, event[0].y_root)
        for i in self.win:
            try:
                i.destroy()
            except:
                pass
        self.win = []
        self.enter(0)
    def click(self, *event):
        self.clickf(event)
        self.isclick = True
        for i in self.win:
            try:
                i.destroy()
            except:
                pass
        self.win = []


class Tipsf(object):
    '''
    给组件设置当鼠标碰到组件时的提示(Frame)
    *父容器必须全屏(fullscreen)
    '''
    def __none(self):
        pass
    def __init__(self, exam, text, wind, tim=500, enterf=__none, leavef=__none, motionf=__none, clickf=__none):
        '''
        参数：
            exam：组件对象
            text：显示文本
            wind：窗口对象
            tim：触发时间
            enterf：<Enter>绑定的其他函数
            leavef：<Leave>绑定的其他函数
            motionf：<Motion>绑定的其他函数
        '''
        self.win = []
        self.iin = False
        self.wz = False
        self.exam = exam
        self.text = text
        self.wind = wind
        self.tim = tim
        self.enterf = enterf
        self.leavef = leavef
        self.motionf = motionf
        self.clickf = clickf
        self.exam.bind('<Enter>', self.enter)
        self.exam.bind('<Leave>', self.leave)
        self.exam.bind('<Motion>', self.motion)
        self.exam.bind('<Button-1>', self.click)
    def enter(self, *event):
        '''
        给组件<Enter>绑定的方法，如需自定义请按照以下语句或更改enterf参数：
            def 函数名(*event):
                Tips.enter(对象名, event)
                <自定义内容>
            对象名.enter = 函数名
        '''
        self.enterf(event)
        self.iin = True
        def showtip():
            if self.iin and self.wz != False:
                self.win.append(Frame(self.wind))
                Label(self.win[-1], text=self.text, relief='solid', bd=1, bg='white').pack()
                self.win[-1].place(x=self.wz[0]+10, y=self.wz[1]+10)
        if self.iin:
            self.wind.after(self.tim, showtip)
    def leave(self, *event):
        '''
        给组件<Leave>绑定的方法，如需自定义请按照以下语句或更改leavef参数：
            def 函数名(*event):
                Tips.leave(对象名, event)
                <自定义内容>
            对象名.leave = 函数名
        '''
        self.leavef(event)
        self.iin = False
        for i in self.win:
            try:
                i.place_forget()
            except:
                pass
        self.win = []
    def motion(self, *event):
        '''
        给组件<Motion>绑定的方法，如需自定义请按照以下语句或更改motionf参数：
            def 函数名(*event):
                Tips.motion(对象名, event)
                <自定义内容>
            对象名.motion = 函数名
        '''
        self.motionf(event)
        self.wz = (event[0].x_root, event[0].y_root)
        for i in self.win:
            try:
                i.destroy()
            except:
                pass
        self.win = []
        self.enter(0)
    def click(self, *event):
        self.clickf(event)
        for i in self.win:
            try:
                i.place_forget()
            except:
                pass
        self.win = []


class SupListbox(Frame):
    '''
    SupListbox为具有自带滚动条, 可以移动各选项的Listbox
    '''
    def __init__(self, master=None, text=['line1','line2'], DoubleCommand=None, cnf={}, **kw):
        '''
        参数:
            master: 父容器
            text: Listbox里的内容
            DoubleCommand: 双击某个选项触发的函数
            
        注意事项:
            DoubleCommand的函数的第一个参数必须是self
        '''
        
        Frame.__init__(self, master, cnf, **kw)

        lb_scr = Scrollbar(self)
        lb_scr.pack(side=RIGHT, fill=Y)

        lb = Listbox(self, yscrollcommand=lb_scr.set)

        self.lb = lb

        for i in text:
            lb.insert(END, i)

        lb.pack(side=LEFT, fill=BOTH, expand=True)
        lb_scr.config(command=lb.yview)
        
        lb.bind('<Double-Button-1>', DoubleCommand)

        lb.bind('<Button-1>', self.getIndex)
        lb.bind('<B1-Motion>', self.Td)

    def getIndex(self, event):
        self.lb.index = self.lb.nearest(event.y)

    def Td(self, event):
        '''
        本函数用于移动各选项
        '''
        newIndex = self.lb.nearest(event.y)

        if newIndex < self.lb.index:
            x = self.lb.get(newIndex)
            self.lb.delete(newIndex)
            self.lb.insert(newIndex + 1, x)
            self.lb.index = newIndex
        
        elif newIndex > self.lb.index:
            x = self.lb.get(newIndex)
            self.lb.delete(newIndex)
            self.lb.insert(newIndex - 1, x)
            self.lb.index = newIndex


    def getNow(self):
        return self.lb.get('active')
        

class Slibar(Canvas):  # 进度条
    def __init__(self, parent, length, alcor, cmcor, bkpic, **options):
        '''
        参数:
            length: 长度
            alcor: 已经过的颜色
            cmcor: 未经过的颜色
            bkpic: 进度条按钮的图片
        '''
        Canvas.__init__(self, parent, options)

        self.length = length
        self.alcor = alcor
        self.cmcor = cmcor
        self.bkpic = bkpic

        self.create_rectangle(0, 2.5, self.length, 7.5, fill=self.cmcor, width=0)
        self.rectangle = self.create_rectangle(0, 0, 0, 0, fill=self.alcor, width=0)

        self.slibar_block_pic = ImageTk.PhotoImage(Image.open(self.bkpic))

        self.slibar_block = self.create_image(0, 5, image=self.slibar_block_pic)
        self.bind_mouse_button()

    def bind_mouse_button(self):
        self.bind('<Button-1>', self.on_slibar_clicked)
        self.bind('<B1-Motion>', self.on_slibar_clicked)
        self.tag_bind(self.rectangle, '<B1-Motion>', self.on_slibar_clicked)
        self.tag_bind(self.slibar_block, '<B1-Motion>', self.on_slibar_clicked)

    def on_slibar_clicked(self, event):
        if event.x > 0 and event.x < self.length:
            self.move_to_position(event.x)
            self.event_generate('<<slibarPositionChanged>>', x=event.x)

    def move_to_position(self, new_position):
        new_position = round(new_position, 1)
        self.coords(self.rectangle, 0, 2.5, new_position, 7.5)
        self.coords(self.slibar_block, new_position, 5)

class SlibarD(Canvas):  # 进度条
    def __init__(self, parent, length, alcor, cmcor, **options):
        '''
        参数:
            length: 长度
            alcor: 已经过的颜色
            cmcor: 未经过的颜色
        '''
        Canvas.__init__(self, parent, options)

        self.length = length
        self.alcor = alcor
        self.cmcor = cmcor

        self.create_rectangle(0, 0, self.length, 8, fill=self.cmcor, width=0)
        self.rectangle = self.create_rectangle(0, 0, 0, 0, fill=self.alcor, width=0)

    def move_to_position(self, new_position):
        new_position = round(new_position, 1)
        self.coords(self.rectangle, 0, 0, new_position, 8)



class RoundedSliButton(object):
    """圆角进度条"""
    def __init__(self, master, x, y, width, height, **kw):
        '''
        参数：
            master：父容器，必须是Canvas
            x：横坐标
            y：纵坐标
            width：长度
            height：高度
            bg：背景色
            fg：进度条颜色
        '''
        if not 'bg' in kw:
            kw['bg'] = '#b3b3b3'
        if not 'fg' in kw:
            kw['fg'] = 'black'
        self.back = master.create_line(x, y, x+width, y, width=height, capstyle='round', fill=kw['bg'])
        self.front = master.create_line(x, y, x, y, width=height, capstyle='round', fill=kw['fg'])
        self.value = 0
        self.width = width
        self.x = x
        self.y = y
        self.master = master
    def moveto(self, posi):
        self.value = posi
        self.master.coords(self.front, self.x, self.y, self.x+self.width*posi, self.y)
    def changewidth(self, width):
        self.width = width
        self.master.coords(self.back, self.x, self.y, self.x+self.width, self.y)
        self.master.coords(self.front, self.x, self.y, self.x+self.width*self.value, self.y)
    def hide(self):
        self.master.itemconfig(self.back, state='hidden')
        self.master.itemconfig(self.front, state='hidden')  
        

class PlaholEntry(Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', cnf={}, **kw):
        super().__init__(master, cnf, **kw)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['foreground']
        self['insertwidth'] = 1

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['foreground'] = self.placeholder_color

    def foc_in(self, *args):
        if self['foreground'] == self.placeholder_color:
           self.delete('0', 'end')
           self['foreground'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
           self.put_placeholder()


class _Tp(object):
    def transparentbg(self, bg, start_x=0, start_y=0, zj_wid=0, zj_hei=0, anchor='nw', opened=False, Tked=True):
        """
        参数：
        bg:将用于裁切的底图文件路径
        start_x:相对于底图来说开始的横坐标
        start_y:相对于底图来说开始的纵坐标
        zj_wid:组件的宽度
        zj_hei:组件的高度
        anchor:组件place时的anchor参数，默认为nw
        opened：bg参数是否是已经open过的图片，默认为否(是的话就得是图片路径)
        """
        if anchor == 'nw' or anchor == NW:
            region = (start_x, start_y, start_x + zj_wid, start_y + zj_hei)
        elif anchor == 'center' or anchor == CENTER:
            region = (start_x - (zj_wid / 2), start_y - (zj_hei / 2), start_x + (zj_wid / 2), start_y + (zj_hei / 2))
        elif anchor == 'ne' or anchor == NE:
            region = (start_x - zj_wid, start_y, start_x, start_y + zj_hei)
        elif anchor == 'sw' or anchor == SW:
            region = (start_x, start_y - zj_hei, start_x + zj_wid, start_y)
        elif anchor == 'se' or anchor == SE:
            region = (start_x - zj_wid, start_y - zj_hei, start_x, start_y)
        elif anchor == 'n' or anchor == N:
            region = (start_x - (zj_wid / 2), start_y, start_x + (zj_wid / 2), start_y + zj_hei)
        elif anchor == 's' or anchor == S:
            region = (start_x - (zj_wid / 2), start_y - zj_hei, start_x + (zj_wid / 2), start_y)
        elif anchor == 'w' or anchor == W:
            region = (start_x, start_y - (zj_hei / 2), start_x + zj_wid, start_y + (zj_hei / 2))
        elif anchor == 'e' or anchor == E:
            region = (start_x - zj_wid, start_y - (zj_hei / 2), start_x, start_y + (zj_hei / 2))
        im = Image.open(bg) if not opened else bg
        cropped = im.crop(region)
        tkimage = ImageTk.PhotoImage(cropped)
        return tkimage if Tked else cropped

    def bgcrop(self, **kw):
        self.master.update()
        if 'relwidth' in kw:
            w = self.master.winfo_width()*kw['relwidth']
        elif 'width' in kw:
            w = kw['width']
        else:
            w = self.winfo_width()
        if 'relheight' in kw:
            h = self.master.winfo_height()*kw['relheight']
        elif 'height' in kw:
            h = kw['height']
        else:
            h = self.winfo_height()
        if 'relx' in kw:
            sx = self.master.winfo_width()*kw['relx']
        elif 'x' in kw:
            sx = kw['x']
        else:
            sx = self.winfo_x()
        if 'rely' in kw:
            sy = self.master.winfo_height()*kw['rely']
        elif 'y' in kw:
            sy = kw['y']
        else:
            sy = self.winfo_y()
        if not 'anchor' in kw:
            kw['anchor'] = 'nw'
        self.backp = self.transparentbg(self.backpic, sx, sy, w, h, kw['anchor'], opened=True, Tked=False)
        self.forep = self.backp
        if self.brighter != 1:
            self.forep = self.brightness(self.forep, self.brighter)
        if isinstance(self.blur, int):
            self.forep = self.forep.filter(ImageFilter.BoxBlur(self.blur))
        if self.rounded != 0:
            forepic = self.circle_corner(self.forep, self.rounded)
            w,h=forepic.size
            self.backp.paste(forepic, (0,0, w,h))# TODO!!!
            self.backp = ImageTk.PhotoImage(self.backp)
        else:
            self.backp = ImageTk.PhotoImage(self.forep)
        self['image'] = self.backp
        self['compound'] = 'center'

    def circle_corner(self, img, radii):
       # 画圆（用于分离4个角）
       circle = Image.new('L', (radii * 2, radii * 2), 0)  # 创建黑色方形
       # circle.save('1.jpg','JPEG',qulity=100)
       draw = ImageDraw.Draw(circle)
       draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)  # 黑色方形内切白色圆形
       # circle.save('2.jpg','JPEG',qulity=100)

       img = img.convert("RGBA")
       w, h = img.size

       alpha = Image.new('L', img.size, 255)
       alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
       alpha.paste(circle.crop((radii, 0, radii * 2, radii)),
                   (w - radii, 0))  # 右上角
       alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)),
                   (w - radii, h - radii))  # 右下角
       alpha.paste(circle.crop((0, radii, radii, radii * 2)),
                   (0, h - radii))  # 左下角

       img.putalpha(alpha)    # 白色区域透明可见，黑色区域不可见

       return img

    def brightness(self, img, num):
        return ImageEnhance.Brightness(img).enhance(num)


class TpButton(Button, _Tp):
    '''
    TpButton为可背景透明的Button控件
    '''
    def __init__(self, master=None, backpic=None, blur=False, rounded=0, brighter=1, **kw):
        '''
        参数：
        master：父容器
        backpic：背景底图(例如整个窗口放了一整张图，那么将此图传入这个参数，会自动根据place时的位置裁切)
        blur：背景模糊程度，建议值为5-10
        rounded：圆角程度，建议值为5-10
        brighter：亮度加强，1为原亮度
        其他参数如relief，command，text与原Button控件相同

        注：
        控件放置时只能使用place
        TpButton的圆角暂时无效，建议使用TpCanvas
        '''
        if 'image' in kw:
            raise ValueError('TpButton不支持image参数')
        Button.__init__(self, master, **kw)
        self.master = master
        self.blur = blur
        self.backpic = backpic
        self.rounded = rounded
        self.brighter = brighter

    def place(self, **kw):
        self.bgcrop(**kw)
        Button.place(self, kw)


class TpLabel(Label, _Tp):
    '''
    TpLabel为可背景透明的Label控件
    '''
    def __init__(self, master=None, backpic=None, blur=False, rounded=0, brighter=1, **kw):
        '''
        参数：
        master：父容器
        backpic：背景底图(例如整个窗口放了一整张图，那么将此图传入这个参数，会自动根据place时的位置裁切)
        blur：背景模糊程度，建议值为5-10
        rounded：圆角程度，建议值为5-10
        brighter：亮度加强，1为原亮度
        其他参数如relief，text与原Button控件相同

        注：
        控件放置时只能使用place
        TpLabel的圆角暂时无效，建议使用TpCanvas
        '''
        if 'image' in kw:
            raise ValueError('TpLabel不支持image参数')
        Label.__init__(self, master, **kw)
        self.master = master
        self.backpic = backpic
        self.blur = blur
        self.rounded = rounded
        self.brighter = brighter

    def place(self, **kw):
        self.bgcrop(**kw)
        Label.place(self, kw)


class TpCanvas(Canvas, _Tp):
    def __init__(self, master=None, backpic=None, forepic=None, activepic=None, text='', blur=False, rounded=0, brighter=1, **kw):
        '''
        参数：
        master：父容器
        backpic：背景底图(例如整个窗口放了一整张图，那么将此图传入这个参数，会自动根据place时的位置裁切)
        forepic：控件图片
        activepic：鼠标略过时显示的图片
        text：显示的文字内容
        blur：背景模糊程度，建议值为5-10
        rounded：圆角程度，建议值为5-10
        brighter：亮度加强，1为原亮度
        其他参数如relief，command与原Button控件相同

        注：
        控件放置时只能使用place
        如要实现Button的触发功能，则bind绑定即可
        '''
        self.textkw = {}
        if 'fg' in kw:
            self.textkw['fill'] = kw['fg']
            del kw['fg']
        if 'fill' in kw:
            self.textkw['fill'] = kw['fill']
            del kw['fg']
        if 'font' in kw:
            self.textkw['font'] = kw['font']
            del kw['font']
        kw['highlightthickness'] = 0 if 'highlightthickness' not in kw else kw['highlightthickness']
        Canvas.__init__(self, master, **kw)

        self.forep = ImageTk.PhotoImage(forepic) if forepic != None else None
        self.activep = ImageTk.PhotoImage(activepic) if activepic != None else None
        self.master = master
        self.backpic = backpic
        self.blur = blur
        self.text = text
        self.rounded = rounded
        self.brighter = brighter

    def place(self, **kw):
        self.master.update()
        if 'relwidth' in kw:
            w = self.master.winfo_width()*kw['relwidth']
        elif 'width' in kw:
            w = kw['width']
        else:
            w = self.winfo_width()
        if 'relheight' in kw:
            h = self.master.winfo_height()*kw['relheight']
        elif 'height' in kw:
            h = kw['height']
        else:
            h = self.winfo_height()
        if 'relx' in kw:
            sx = self.master.winfo_width()*kw['relx']
        elif 'x' in kw:
            sx = kw['x']
        else:
            sx = self.winfo_x()
        if 'rely' in kw:
            sy = self.master.winfo_height()*kw['rely']
        elif 'y' in kw:
            sy = kw['y']
        else:
            sy = self.winfo_y()
        if not 'anchor' in kw:
            kw['anchor'] = 'nw'
        self.backp = self.transparentbg(self.backpic, sx, sy, w, h, kw['anchor'], opened=True, Tked=False)
        self.forepi = self.backp
        if self.brighter != 1:
            self.forepi = self.brightness(self.forepi, self.brighter)
        if isinstance(self.blur, int):
            self.forepi = self.forepi.filter(ImageFilter.BoxBlur(self.blur))
        if self.rounded != 0:
            forepic = self.circle_corner(self.forepi, self.rounded)
            self.backp = ImageTk.PhotoImage(self.backp)
            self.forepi = ImageTk.PhotoImage(forepic)
            self.back = self.create_image(0, 0, anchor=NW, image=self.backp)
            self.fore = self.create_image(0, 0, anchor=NW, image=self.forepi)
        else:
            self.backp = ImageTk.PhotoImage(self.forepi)
            self.back = self.create_image(0, 0, anchor=NW, image=self.backp)
        self.create_image(w/2, h/2, image=self.forep, activeimage=self.activep, anchor=CENTER)
        self.create_text(w/2, h/2, text=self.text, anchor=CENTER, **self.textkw)
        self.lower(self.back)
        Canvas.place(self, kw)


class TpBarChart(TpCanvas):
    """
    TpBarChart为背景透明的条形图
    """
    def __init__(self, master=None, backpic=None, direction='horizontal', color='blue', barwidth=30, blur=False, rounded=0, brighter=1, **kw):
        """
        参数：
        backpic：父容器背景图
        direction：条形图方向
        color：条颜色
        blur：背景虚化，类型为int
        rounded：圆角，类型为int
        brighter：亮度加强，类型为int
        """
        TpCanvas.__init__(self, master=master, backpic=backpic, forepic=None, text='', activepic=None, blur=blur, rounded=rounded, brighter=brighter, **kw)
        self.direction = direction
        self.color = color
        self.barwidth = barwidth

        self.bar = []

    def add_bar(self, name, num):
        self.bar.append((name, num))

    def update_bar(self):
        self.place(x=self.winfo_x(), y=self.winfo_y(), width=self.winfo_width(), height=self.winfo_height())

    def place(self, **kw):
        TpCanvas.place(self, **kw)
        self.update()

        if len(self.bar) != 0:
            # TODO:加入竖向
            Label(self, bg='#c0c0c0').place(relwidth=1, height=1, x=0, y=self.winfo_height()-20)
            
            self.barins = []
            self.maxnum = max([x[1] for x in self.bar])
            self.maxbarheight = self.winfo_height()-40
            bottom = self.winfo_height()-20
            self.bottom = bottom
            for i in range(len(self.bar)):
                b = self.bar[i]
                rec = self.create_rectangle(10+(self.barwidth+10)*i, bottom-b[1]/self.maxnum*self.maxbarheight, 10+(self.barwidth+10)*i+self.barwidth, bottom, fill=self.color, width=1, outline='white')
                num = self.create_text(10+(self.barwidth+10)*i+self.barwidth/2, bottom-b[1]/self.maxnum*self.maxbarheight-10, text=str(b[1]), fill='white')
                name = self.create_text(10+(self.barwidth+10)*i+self.barwidth/2, bottom+10, text=b[0], fill='white')
                self.barins.append((rec, num, name))
                self.tag_bind(self.barins[-1][0], '<Button-1>', self.relxy)
                self.tag_bind(self.barins[-1][0], '<B1-Motion>', self.move)
            self.nowpositionx = 10
            self.lastpositionx = 0
            self.horizon = (10, self.winfo_width()-10-self.barwidth)
        else:
            bottom = self.winfo_height()-20
            self.bottom = bottom
            self.create_text(self.winfo_width()/2, self.winfo_height()/2, anchor=CENTER, text='无数据', fill='white', font=('华文新魏', 16))

    def relxy(self, event):
        self.nowpositionx = self.lastpositionx+self.nowpositionx
        self.mouse_x = event.x

    def move(self, event):
        bottom = self.bottom
        if (event.x-self.mouse_x)+self.nowpositionx <= self.horizon[0] and (event.x-self.mouse_x)+self.nowpositionx+(self.barwidth+10)*(len(self.bar)-1) >= self.horizon[1]:
            for i in range(len(self.barins)):
                b = self.bar[i]
                self.coords(self.barins[i][0], (event.x-self.mouse_x)+self.nowpositionx+(self.barwidth+10)*i, bottom-b[1]/self.maxnum*self.maxbarheight, (event.x-self.mouse_x)+self.nowpositionx+(self.barwidth+10)*i+self.barwidth, bottom)
                self.coords(self.barins[i][1], (event.x-self.mouse_x)+self.nowpositionx+(self.barwidth+10)*i+self.barwidth/2, bottom-b[1]/self.maxnum*self.maxbarheight-10)
                self.coords(self.barins[i][2], (event.x-self.mouse_x)+self.nowpositionx+(self.barwidth+10)*i+self.barwidth/2, bottom+10)
            self.lastpositionx = event.x-self.mouse_x

    def setposition(self, num):
        if len(self.bar) != 0:
            bottom = self.bottom
            if -(self.barwidth+10)*(num-1)+9 <= self.horizon[0] and (self.barwidth+10)*(len(self.bar)-1)-(self.barwidth+10)*(num-1)+9 >= self.horizon[1]:
                for i in range(len(self.barins)):
                    b = self.bar[i]
                    self.coords(self.barins[i][0], -(self.barwidth+10)*(num-1)+9+(self.barwidth+10)*i, bottom-b[1]/self.maxnum*self.maxbarheight, -(self.barwidth+10)*(num-1)+9+(self.barwidth+10)*i+self.barwidth, bottom)
                    self.coords(self.barins[i][1], -(self.barwidth+10)*(num-1)+9+(self.barwidth+10)*i+self.barwidth/2, bottom-b[1]/self.maxnum*self.maxbarheight-10)
                    self.coords(self.barins[i][2], -(self.barwidth+10)*(num-1)+9+(self.barwidth+10)*i+self.barwidth/2, bottom+10)
                self.nowpositionx = -(self.barwidth+10)*(num-1)+9
                self.lastpositionx = 0

if __name__ == '__main__':
    class V:
        pass
    v = V()
    a = Tk()
    a.geometry('600x400+500+200')
    def notsli():
        try:
            v.sbf.place_forget()
        except:
            pass
    def plasli():
        v.sbf.place(width=350, height=100, x=250, y=100)

    def pla_sbl():
        v.re.place(width=350, height=100, x=250, y=100)
        
    v.sbf = Frame(a)
    v.re = Frame(a)
    v.sb = SliButton(a, 250, 300, master=v.sbf, thick=8, sliburlf='flat', lwidth=4)
    v.sb.place()
    v.sb.set_value(0.2)
       
    sm = SideMenu(a, func=[notsli, notsli, notsli, plasli, pla_sbl], text=['side', 'menu', 'shell', 'slibutton', 'SupListbox'], lg='red', relief='ridge', bd=10)
    sm.place(height=400, width=200)
    Tips(sm, '234234', a)
    
    #a.overrideredirect(True)


    def jil(self):
        print(Slb.getNow())
        
    Slb = SupListbox(v.re, DoubleCommand=jil)
    Slb.place(width=300, height=200, x=10, y=30)
    
    v.sb.auto_move(True, 100000, 10, mode='sleep')
    v.sb['bg'] = 'blue'
    a.mainloop()

