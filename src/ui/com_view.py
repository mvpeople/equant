import os
import sys
sys.path.append("..")

from threading import Lock
import tkinter as tk
import tkinter.ttk as ttk

from utils.utils import *
from utils.language import Language
from .language import Language

from report.windowconfig import center_window


class QuantFrame(object):
    '''通用方法类'''
    def __init__(self):
        pass
        
    def addScroll(self, frame, widgets, xscroll=True, yscroll=True):
        xsb,ysb = None, None

        if xscroll:
            xsb = tk.Scrollbar(frame, orient="horizontal")
            widgets.config(xscrollcommand=xsb.set)
            xsb.config(command=widgets.xview, bg=rgb_to_hex(255,0,0))
            xsb.pack(fill=tk.X, side=tk.BOTTOM)

        if yscroll:
            ysb = tk.Scrollbar(frame, orient="vertical")
            widgets.config(yscrollcommand=ysb.set)
            ysb.config(command=widgets.yview, bg=rgb_to_hex(255,0,0))
            ysb.pack(fill=tk.Y, side=tk.RIGHT)

        return xsb, ysb

    def testDigit(self, content):
        """判断Entry中内容"""
        if content.isdigit() or content == "":
            return True
        return False

    def testFloat(self, content):
        """判断Entry中是否为浮点数"""
        try:
            if content == "" or isinstance(float(content), float):
                return True
        except:
            return False

    def handlerAdaptor(self, fun, **kwargs):
        """回调适配器"""
        return lambda event, fun=fun, kwargs=kwargs: fun(event, **kwargs)


class QuantToplevel(tk.Toplevel):
    def __init__(self, master=None):
        tk.Toplevel.__init__(self, master)
        self._master = master
        self.language = Language("EquantMainFrame")
        self.setPos()
        #图标
        self.iconbitmap(bitmap=r"./icon/epolestar ix2.ico")

    def setPos(self):
        # 获取主窗口大小和位置，根据主窗口调整输入框位置
        ws = self._master.winfo_width()
        hs = self._master.winfo_height()
        wx = self._master.winfo_x()
        wy = self._master.winfo_y()

        #计算窗口位置
        w, h = 400, 120
        x = (wx + ws/2) - w/2
        y = (wy + hs/2) - h/2

        #弹出输入窗口，输入文件名称
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.minsize(200, 120)

    def display(self):
        """显示并设置模态窗口"""
        self.update()
        self.deiconify()
        self.grab_set()
        self.focus_set()
        self.wait_window()


class NewFileToplevel(QuantToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.attributes("-toolwindow", 1)
        self.title("新建文件")
        self.createWidgets()

    def createWidgets(self):
        f1, f2, f3 = tk.Frame(self), tk.Frame(self), tk.Frame(self)
        f1.pack(side=tk.TOP, fill=tk.X, pady=5)
        f2.pack(side=tk.TOP, fill=tk.X)
        f3.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        name_label = tk.Label(f1, text=self.language.get_text(14), width=10)
        self.nameEntry = tk.Entry(f1, width=23)
        type_label = tk.Label(f2, text=self.language.get_text(15), width=10)
        self.type_chosen = ttk.Combobox(f2, state="readonly", width=20)
        self.type_chosen["values"] = [".py"]
        self.type_chosen.current(0)

        self.saveBtn = tk.Button(f3, text=self.language.get_text(19))
        self.cancelBtn = tk.Button(f3, text=self.language.get_text(20))
        name_label.pack(side=tk.LEFT, expand=tk.NO)
        self.nameEntry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=15)
        type_label.pack(side=tk.LEFT, expand=tk.NO)
        self.type_chosen.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=15)
        self.cancelBtn.pack(side=tk.RIGHT, expand=tk.NO, padx=20)
        self.saveBtn.pack(side=tk.RIGHT, expand=tk.NO)

    def display(self):
        self.update()
        self.deiconify()
        self.grab_set()
        self.focus_set()
        self.nameEntry.focus_set()
        self.wait_window()


class NewDirToplevel(QuantToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.attributes("-toolwindow", 1)
        self.title("新建文件夹")
        self.createWidget()

    def createWidget(self):
        f1, f2, f3 = tk.Frame(self), tk.Frame(self), tk.Frame(self)
        f4, f5 = tk.Frame(f3), tk.Frame(f3)

        f1.pack(side=tk.TOP, fill=tk.X, pady=5)
        f2.pack(side=tk.TOP, fill=tk.X)
        f3.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        f4.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        f5.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)

        nameLabel = tk.Label(f1, text="输入分组名称：")
        self.nameEntry = tk.Entry(f2)
        self.saveBtn = tk.Button(f4, text="保存")
        self.cancelBtn = tk.Button(f5, text="取消")

        nameLabel.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO, padx=15)
        self.nameEntry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=15)
        self.saveBtn.pack(side=tk.RIGHT, expand=tk.NO, padx=10)
        self.cancelBtn.pack(side=tk.LEFT, expand=tk.NO, padx=10)

    def display(self):
        self.update()
        self.deiconify()
        self.grab_set()
        self.focus_set()
        self.nameEntry.focus_set()
        self.wait_window()


class RenameToplevel(QuantToplevel):
    def __init__(self, path, master=None):
        super().__init__(master)
        self.path = path
        self.attributes("-toolwindow", 1)
        self.title("重命名")
        self.createWidget()

    def createWidget(self):
        f1, f2 = tk.Frame(self), tk.Frame(self)
        f1.pack(side=tk.TOP, fill=tk.X, pady=15)
        f2.pack(side=tk.BOTTOM, fill=tk.X)

        if os.path.isfile(self.path):
            newLabel = tk.Label(f1, text=self.language.get_text(28))
            self.newEntry = tk.Entry(f1, width=15)
            self.newEntry.insert(tk.END, os.path.basename(self.path))

            self.saveBtn = tk.Button(f2, text="确定")
            self.cancelBtn = tk.Button(f2, text="取消")

            newLabel.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO, padx=15)
            self.newEntry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=15)

            self.cancelBtn.pack(side=tk.RIGHT, expand=tk.NO, ipadx=5, padx=15, pady=10)
            self.saveBtn.pack(side=tk.RIGHT, expand=tk.NO, ipadx=5, padx=15, pady=10)

        if os.path.isdir(self.path):
            newLabel = tk.Label(f1, text=self.language.get_text(30))
            self.newEntry = tk.Entry(f1, width=15)
            self.newEntry.insert(tk.END, os.path.basename(self.path))

            self.saveBtn = tk.Button(f2, text="确定", bd=0)
            self.cancelBtn = tk.Button(f2, text="取消", bd=0)

            newLabel.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO, padx=15)
            self.newEntry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES, padx=15)

            self.cancelBtn.pack(side=tk.RIGHT, expand=tk.NO, ipadx=5, padx=15, pady=10)
            self.saveBtn.pack(side=tk.RIGHT, expand=tk.NO, ipadx=5, padx=15, pady=10)

    def display(self):
        self.update()
        self.deiconify()
        self.grab_set()
        self.focus_set()
        self.newEntry.focus_set()
        self.wait_window()


class DeleteToplevel(QuantToplevel):
    def __init__(self, path, master=None):
        super().__init__(master)
        self.path = path
        self.attributes("-toolwindow", 1)
        # self.wm_attributes("-topmost", 1)
        self.title("删除")
        self.createWidget()

    def createWidget(self):
        f1, f2 = tk.Frame(self), tk.Frame(self)
        f1.pack(side=tk.TOP, fill=tk.X, pady=5)
        f2.pack(side=tk.BOTTOM, fill=tk.X)
        label = tk.Label(f1)
        label["text"] = self.language.get_text(34)
        path = self.path
        if len(self.path) > 1:
            label["text"] = "即将删除被选中项"
        else:
            if os.path.isdir(self.path[0]):
                label["text"] = self.language.get_text(35) + os.path.basename(self.path[0]) + "?"
            if os.path.isfile(self.path[0]):
                label["text"] = self.language.get_text(34) + \
                                os.path.join(os.path.basename(os.path.dirname(self.path[0])),
                                             os.path.basename(self.path[0])) + "?"

        self.saveBtn = tk.Button(f2, text=self.language.get_text(33))
        self.cancelBtn = tk.Button(f2, text=self.language.get_text(20))

        label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO, padx=15, pady=15)
        self.cancelBtn.pack(side=tk.RIGHT, expand=tk.NO, ipadx=5, padx=15, pady=10)
        self.saveBtn.pack(side=tk.RIGHT, expand=tk.NO, ipadx=5, padx=15, pady=10)


"""
class MoveToplevel(QuantToplevel):

    def __init__(self, master=None):
        super().__init__(master)
        self.attributes("-toolwindow", 1)
        self.title("移动")
        self.createWidget()

    def createWidget(self):
        group_label = tk.Label(self, text=self.language.get_text(25))
        group_entry = tk.Label(self)
        group_entry["text"] = "自编"
        name_label = tk.Label(self, text=self.language.get_text(26))
        name_entry = tk.Label(self)
        name_entry["text"] = "基于平移布林通道的系统.py"

        move_label = tk.Label(self, text=self.language.get_text(27))
        move_chosen = ttk.Combobox(self)

        save_button = tk.Button(self, text=self.language.get_text(19))
        cancal_button = tk.Button(self, text=self.language.get_text(20))

        group_label.grid(row=0, column=0, sticky=tk.W)
        group_entry.grid(row=0, column=1, sticky=tk.W)
        name_label.grid(row=1, column=0, sticky=tk.W)
        name_entry.grid(row=1, column=1, sticky=tk.W)
        move_label.grid(row=2, column=0, sticky=tk.W)
        move_chosen.grid(row=2, column=1, sticky=tk.W)
        save_button.grid(row=3, column=0, sticky=tk.E)
        cancal_button.grid(row=3, column=1, sticky=tk.E)

    def display(self):
        self.update()
        self.deiconify()
        self.grab_set()
        self.focus_set()
        # self.newEntry.focus_set()
        self.wait_window()
"""


def Singleton(cls):
    # 单例模式
    _instance = {}

    def __singleton(*args, **kw):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kw)
        return _instance[cls]

    return __singleton


# @Singleton
class HistoryToplevel(QuantToplevel):
    def __init__(self, view, master=None):
        super().__init__(master)
        # self.withdraw()
        self.wm_attributes("-topmost", 0)  # 窗口置顶
        self._view = view
        self._master = master
        self.set_config()
        self.withdraw()

    def set_config(self):
        self.title('回测报告')
        center_window(self, 1000, 600)
        self.minsize(1000, 600)

    def display_(self):
        self.update()
        self.deiconify()


class AlarmToplevel(tk.Toplevel):
    def __init__(self, text, master=None):
        super().__init__(master)
        self.attributes("-toolwindow", 1)
        self.dspText = text

        self.title("下单提醒")
        self.createWidget(self.dspText)

    def createWidget(self, text):
        f1 = tk.Frame(self, width=30, height=10)
        f1.pack(side=tk.TOP, fill=tk.X, pady=5)

        textWgt = tk.Text(f1, width=60, height=20)

        textWgt.insert(tk.END, text)
        textWgt.see(tk.END)
        textWgt.config(state="disabled")
        textWgt.pack()

    def setPos(self):
        # 获取主窗口大小和位置，根据主窗口调整输入框位置
        ws = self._master.winfo_width()
        hs = self._master.winfo_height()
        wx = self._master.winfo_x()
        wy = self._master.winfo_y()

        #计算窗口位置
        w, h = 350, 260
        x = (wx + ws/2) - w/2
        y = (wy + hs/2) - h/2

        #弹出输入窗口，输入文件名称
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.minsize(200, 120)


class AlarmWin(tk.Toplevel):
    _instance_lock = Lock()
    __instance = None
    __has_initialization = False

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if not cls.__instance:
                cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, text, master):
        if not AlarmWin.__has_initialization:
            super().__init__(master)
            self._master = master
            self._textWgt = None
            self._textList = []
            self._onPage = 1
            self._pages = 1
            self._autoPages = True

            self._initImage()
            self._setPos()
            self._createFrames()
            AlarmWin.__has_initialization = True
            self.protocol("WM_DELETE_WINDOW", self.closeWin)
        self.updateTextList(text)

        if self._autoPages:
            self.updateOnPage()
            self.insertSpecificPageText(text)
        self.updatePages()
        self.updatePagesLabel()

    def closeWin(self):
        self.rebuild()
        self.destroy()

    def _initImage(self):
        self.topImage1 = r'./icon/top1.gif'
        self.btmImage1 = r'./icon/bottom1.gif'
        self.befImage1 = r'./icon/before1.gif'
        self.nxtImage1 = r'./icon/next1.gif'

        self.topImage2 = r'./icon/top2.gif'
        self.btmImage2 = r'./icon/bottom2.gif'
        self.befImage2 = r'./icon/before2.gif'
        self.nxtImage2 = r'./icon/next2.gif'

    def _setPos(self):
        self.title("下单提醒")
        self.attributes("-toolwindow", 1)
        self.wm_attributes("-topmost", 1)
        self.wm_resizable(0, 0)

        ws = self._master.winfo_width()
        hs = self._master.winfo_height()
        wx = self._master.winfo_x()
        wy = self._master.winfo_y()

        #计算窗口位置
        w, h = 400, 400
        x = (wx + ws/2) - w/2
        y = (wy + hs/2) - h/2

        #弹出输入窗口，输入文件名称
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        # self.minsize(400, 400)


    def _createFrames(self):
        textFrame = tk.Frame(self, width=400, height=370)
        textFrame.pack(side=tk.TOP, padx=1)
        textFrame.pack_propagate(False)
        btnFrame = tk.Frame(self, width=400, height=30, padx=1)
        btnFrame.pack(side=tk.TOP, padx=1)
        textFrame.pack_propagate(False)
        self._createTextWgt(textFrame)
        self._createBtn(btnFrame)

    def _createTextWgt(self, frame):
        self.textWgt = tk.Text(frame, bg="black")
        self.textWgt.config(state="disabled", font=("Consolas", 16), fg="white")
        self.textWgt.pack(fill=tk.BOTH, expand=tk.YES)

    def insertSpecificPageText(self, text):
        self.textWgt.config(state="normal")
        self.textWgt.delete(0.0, "end" + "-1c")
        self.textWgt.insert(tk.END, text)
        self.textWgt.see(tk.END)
        self.textWgt.config(state="disabled")

    def _createBtn(self, frame):
        topImage1 = tk.PhotoImage(file=self.topImage1)
        btmImage1 = tk.PhotoImage(file=self.btmImage1)
        befImage1 = tk.PhotoImage(file=self.befImage1)
        nxtImage1 = tk.PhotoImage(file=self.nxtImage1)

        self.topBtn = tk.Label(frame, text="top", image=topImage1)
        self.btmBtn = tk.Label(frame, text="bottom", image=btmImage1)
        self.befBtn = tk.Label(frame, text="before", image=befImage1)
        self.nxtBtn = tk.Label(frame, text="next", image=nxtImage1)
        self.pageLabel = tk.Label(frame, text="%d/%d" % (self._onPage, self._pages))

        self.topBtn.pack(side=tk.LEFT, padx=4, pady=4)
        self.befBtn.pack(side=tk.LEFT, padx=4, pady=4)
        self.pageLabel.pack(side=tk.LEFT, padx=4, pady=4)
        self.nxtBtn.pack(side=tk.LEFT, padx=4, pady=4)
        self.btmBtn.pack(side=tk.LEFT, padx=4, pady=4)

        self.topBtn.bind("<Button-1>", self.toTop)
        self.btmBtn.bind("<Button-1>", self.toBottom)
        self.befBtn.bind("<Button-1>", self.toBefore)
        self.nxtBtn.bind("<Button-1>", self.toNext)

        self.topBtn.image = topImage1
        self.btmBtn.image = btmImage1
        self.befBtn.image = befImage1
        self.nxtBtn.image = nxtImage1

    def updatePagesLabel(self):
        self.pageLabel.config(text="%d/%d" % (self._onPage, self._pages))

    def updateOnPage(self):
        self._onPage = len(self._textList)

    def updateTextList(self, text):
        self._textList.append(text)

    def updatePages(self):
        self._pages = len(self._textList)
        if self._onPage == self._pages:
            for wgt, image in zip([self.nxtBtn, self.btmBtn], [self.nxtImage2, self.btmImage2]):
                self.setBtnImage(wgt, image)
            if self._onPage == 1:
                for wgt, image in zip([self.topBtn, self.befBtn], [self.topImage2, self.befImage2]):
                    self.setBtnImage(wgt, image)
            else:
                for wgt, image in zip([self.topBtn, self.befBtn], [self.topImage1, self.befImage1]):
                    self.setBtnImage(wgt, image)
        else:
            for wgt, image in zip([self.nxtBtn, self.btmBtn], [self.nxtImage1, self.btmImage1]):
                self.setBtnImage(wgt, image)

    def toTop(self, event):
        self._onPage = 1
        self._autoPages = False
        for wgt, image in zip([self.topBtn, self.befBtn], [self.topImage2, self.befImage2]):
            self.setBtnImage(wgt, image)
        if self._onPage != self._pages:
            for wgt, image in zip([self.nxtBtn, self.btmBtn], [self.nxtImage1, self.btmImage1]):
                self.setBtnImage(wgt, image)

        self.updatePagesLabel()
        self.insertSpecificPageText(self._textList[self._onPage-1])

    def toBottom(self, event):
        self._autoPages = True
        self._onPage = len(self._textList)
        # self.setBtnDisabeldImage(self.btmBtn)
        if self._onPage != self._onPage:
            for wgt, image in zip([self.topBtn, self.befBtn], [self.topImage1, self.befImage1]):
                self.setBtnImage(wgt, image)

        for wgt, image in zip([self.nxtBtn, self.btmBtn], [self.nxtImage2, self.btmImage2]):
            self.setBtnImage(wgt, image)
        self.updatePagesLabel()
        self.insertSpecificPageText(self._textList[self._onPage-1])

    def toBefore(self, event):
        # 在最左侧的情况
        self._autoPages = False
        # self._onPage -= 1
        if self._onPage != 1:
            self._onPage -= 1
        if self._onPage == 1:
            for wgt, image in zip([self.befBtn, self.topBtn], [self.befImage2, self.topImage2]):
                self.setBtnImage(wgt, image)
        if self._pages != 1:
            for wgt, image in zip([self.nxtBtn, self.btmBtn], [self.nxtImage1, self.btmImage1]):
                self.setBtnImage(wgt, image)

        self.updatePagesLabel()
        self.insertSpecificPageText(self._textList[self._onPage-1])

    def toNext(self, event):
        if self._onPage != self._pages:
            self._onPage += 1
        if self._onPage == self._pages:
            for wgt, image in zip([self.nxtBtn, self.btmBtn], [self.nxtImage2, self.btmImage2]):
                self.setBtnImage(wgt, image)
        if self._pages != self._onPage:
            for wgt, image in zip([self.befBtn, self.topBtn], [self.befImage1, self.topImage1]):
                self.setBtnImage(wgt, image)

        self.updatePagesLabel()
        self.insertSpecificPageText(self._textList[self._onPage-1])

    def setBtnImage(self, widget, image):
        iimage = tk.PhotoImage(file=image)
        widget.config(image=iimage)
        widget.image = iimage

    @classmethod
    def rebuild(cls):
        cls.__instance = None
        cls.__has_initialization = False


"""
class AlarmWin(tk.Toplevel):
    _instance_lock = Lock()
    __instance = None
    __has_initialization = False

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if not cls.__instance:
                cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, text, master=None):
        if not AlarmWin.__has_initialization:
            super().__init__(master)
            self._master = master
            self._textWgt = None
            self._textList = []
            self._onPage = 1
            self._pages = 1
            self._autoPages = True
            self.setPos()
            self.createFrames()
            AlarmWin.__has_initialization = True
        self.updateTextList(text)

        if self._autoPages:
            self.updateOnPage()
            self.insertSpecificPageText(text)
        self.updatePages()
        self.updatePagesLabel()

    def setPos(self):
        self.title("下单提醒")
        self.attributes("-toolwindow", 1)
        self.wm_attributes("-topmost", 1)

        ws = self._master.winfo_width()
        hs = self._master.winfo_height()
        wx = self._master.winfo_x()
        wy = self._master.winfo_y()

        #计算窗口位置
        w, h = 400, 400
        x = (wx + ws/2) - w/2
        y = (wy + hs/2) - h/2

        #弹出输入窗口，输入文件名称
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.minsize(400, 400)

    def createFrames(self):
        textFrame = tk.Frame(self, width=400, height=360)
        textFrame.pack(side=tk.TOP, padx=1)
        textFrame.pack_propagate(False)
        btnFrame = tk.Frame(self, padx=1)
        btnFrame.pack(side=tk.TOP, fill=tk.X)
        self.createTextWgt(textFrame)
        self.createBtn(btnFrame)

    def createTextWgt(self, frame):
        self.textWgt = tk.Text(frame, bg="black")
        self.textWgt.config(state="disabled", font=("Consolas", 16), fg="white")
        self.textWgt.pack(fill=tk.BOTH, expand=tk.YES)

    def insertSpecificPageText(self, text):
        self.textWgt.config(state="normal")
        self.textWgt.delete(0.0, "end" + "-1c")
        self.textWgt.insert(tk.END, text)
        self.textWgt.see(tk.END)
        self.textWgt.config(state="disabled")

    def createBtn(self, frame):
        self.topBtn = tk.Button(frame, text="top", command=self.toTop)
        self.btmBtn = tk.Button(frame, text="bottom", command=self.toBottom)
        self.befBtn = tk.Button(frame, text="before", command=self.toBefore)
        self.nxtBtn = tk.Button(frame, text="next", command=self.toNext)
        self.pageLabel = tk.Label(frame, text="%d/%d" % (self._onPage, self._pages))

        self.topBtn.pack(side=tk.LEFT)
        self.befBtn.pack(side=tk.LEFT)
        self.pageLabel.pack(side=tk.LEFT)
        self.nxtBtn.pack(side=tk.LEFT)
        self.btmBtn.pack(side=tk.LEFT)

    def updatePagesLabel(self):
        print("11111111: ", self.pageLabel)
        self.pageLabel.config(text="%d/%d" % (self._onPage, self._pages))

    def updateTextList(self, text):
        self._textList.append(text)

    def updatePages(self):
        self._pages = len(self._textList)
        if self._onPage == self._pages:
            for wgt in [self.nxtBtn, self.btmBtn]:
                self.setBtnDisabeld(wgt)
            if self._onPage == 1:
                for wgt in [self.topBtn, self.befBtn]:
                    self.setBtnDisabeld(wgt)
            else:
                for wgt in [self.topBtn, self.befBtn]:
                    self.setBtnNormal(wgt)
        else:
            for wgt in [self.nxtBtn, self.btmBtn]:
                self.setBtnNormal(wgt)

    def updateOnPage(self):
        self._onPage = len(self._textList)

    def toTop(self):
        self._onPage = 1
        self._autoPages = False
        for wgt in [self.topBtn, self.befBtn]:
            self.setBtnDisabeld(wgt)

        for wgt in [self.nxtBtn, self.btmBtn]:
            self.setBtnNormal(wgt)

        self.updatePagesLabel()
        self.insertSpecificPageText(self._textList[self._onPage-1])

    def toBottom(self):
        self._autoPages = True
        self._onPage = len(self._textList)
        self.setBtnDisabeld(self.btmBtn)
        for wgt in [self.topBtn, self.befBtn]:
            self.setBtnNormal(wgt)

        for wgt in [self.nxtBtn, self.btmBtn]:
            self.setBtnDisabeld(wgt)
        self.updatePagesLabel()
        self.insertSpecificPageText(self._textList[self._onPage-1])

    def toBefore(self):
        # 在最左侧的情况
        self._autoPages = False
        self._onPage -= 1
        if self._onPage == 1:
            for wgt in [self.befBtn, self.topBtn]:
                self.setBtnDisabeld(wgt)
        for wgt in [self.nxtBtn, self.btmBtn]:
            self.setBtnNormal(wgt)

        self.updatePagesLabel()
        self.insertSpecificPageText(self._textList[self._onPage-1])

    def toNext(self):
        self._onPage += 1
        if self._onPage == self._pages:
            #self._autoPages = True
            for wgt in [self.nxtBtn, self.btmBtn]:
                self.setBtnDisabeld(wgt)
        for wgt in [self.befBtn, self.topBtn]:
            self.setBtnNormal(wgt)

        self.updatePagesLabel()
        self.insertSpecificPageText(self._textList[self._onPage-1])

    def setBtnNormal(self, widget):
        widget.config(state="normal")

    def setBtnDisabeld(self, widget):
        widget.config(state="disabled")

    @classmethod
    def rebuild(cls):
        cls.__instance = None
        cls.__has_initialization = False
"""