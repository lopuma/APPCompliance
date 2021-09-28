# -*- coding: utf-8 -*-
# Copyright (c) Muhammet Emin TURGUT 2020
# For license see LICENSE
import tkinter as tk
import tkinter.font as tkFont
from tkinter import font
import os
import time
from tkinter import *
from tkinter import ttk
from threading import Thread
from PIL import Image, ImageTk
release = True
path = os.path.expanduser("~/")
path_icon = path+"compliance/image/"
count = 0
class ScrollableNotebook(ttk.Frame):
    _initialized = False
    def __init__(self,parent,wheelscroll=False,tabmenu=False,*args,**kwargs):
        ttk.Frame.__init__(self, parent, *args)
        if not self._initialized:
            self._initialize()
            self._inititialized = True
        kwargs["style"] = "ScrollableNotebook"
        self._active = None
        self.xLocation = 0
        self.WorkSpac_icon = ImageTk.PhotoImage(Image.open(path_icon+r"workspace.png").resize((20, 20)))
        self.notebookContent = ttk.Notebook(self,**kwargs)
        self.notebookContent.pack(fill="both", expand=True)
        self.notebookTab = ttk.Notebook(self,**kwargs)
        self.notebookTab.bind("<<NotebookTabChanged>>",lambda e:self._tabChanger(e))
        if wheelscroll==True: 
            self.notebookTab.bind("<MouseWheel>", self._wheelscroll)
            self.notebookTab.bind("<Button-4>", self._wheelscroll)
            self.notebookTab.bind("<Button-5>", self._wheelscroll)
        slideFrame = ttk.Frame(self)
        slideFrame.place(relx=1.0, x=0, y=1, anchor=NE)
        self.menuSpace=30
        if tabmenu==True:
            self.menuSpace=50
            self.bottomTab = ttk.Label(slideFrame, 
                                text="  \u2630  ", 
                                width=5,
                                anchor='center',
                                background='#DF2E2E',
                                foreground='#F6D167'
                                )
            self.bottomTab.bind("<1>",self._bottomMenu)
            self.bottomTab.pack(side=RIGHT, ipady=14)

        self.leftArrow = ttk.Label(slideFrame, 
                                text=" \u276E ",
                                foreground="#297F87",
                                )
        self.leftArrow.bind("<Button-1>",lambda e: Thread(target=self._leftSlide, daemon=True).start())
        self.leftArrow.bind("<ButtonRelease-1>", self._release_callback)
        self.leftArrow.pack(side=LEFT)
        self.rightArrow = ttk.Label(slideFrame, 
                                text=" \u276F ",
                                foreground="#297F87",
                                )
        #rightArrow.bind("<1>",self._rightSlide)
        self.rightArrow.bind("<Button-1>",lambda e: Thread(target=self._rightSlide, daemon=True).start())
        self.rightArrow.bind("<ButtonRelease-1>", self._release_callback)
        self.rightArrow.pack(side=RIGHT)

        self.notebookContent.bind("<Configure>", self._resetSlide)
        self.notebookTab.bind("<ButtonPress-1>", self.on_tab_close_press, True)
        self.notebookTab.bind("<ButtonRelease-1>", self.on_tab_close_release)
        self.notebookContent.bind("<ButtonPress-1>", self.on_tab_close_press, True)
        self.notebookContent.bind("<ButtonRelease-1>", self.on_tab_close_release)
    
    def _release_callback(self, e):
        global release
        release = True
        self.rightArrow.configure(foreground='#297F87')
        self.leftArrow.configure(foreground='#297F87')
    
    def on_tab_close_press(self, event):
        name = self.identify(event.x, event.y)  
        if name == "tab_btn_close":
            index = self.index("@%d,%d" % (event.x, event.y))
            self.state(['pressed'])
            self._active = index
    
    def on_tab_close_release(self, event):
        if not self.instate(['pressed']):
            return None
        name =  self.identify(event.x, event.y)
        if name == "tab_btn_close":
            index = self.index("@%d,%d" % (event.x, event.y))
            if index != 0:
                if self._active == index:
                    self.forget(index)
                    self.notebookContent.forget(index)
                    self.event_generate("<<NotebookTabClosed>>")
        self.state(["!pressed"])
        self._active = None
    
    def _initialize(self):
        self.style = ttk.Style()
        self.images = (
        #     tk.PhotoImage("img1", data='''
        #     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
        # ''' ),
        #     tk.PhotoImage("img2", data="""
        #     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
        # """),
        #     tk.PhotoImage("img3", data="""
        #     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
        # """)
        tk.PhotoImage("img1", data='''
            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
        ''' ),
            tk.PhotoImage("img3", data="""
            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
        """)
        )
        self.style.element_create("tab_btn_close", "image", "img1",
                            #("active", "pressed", "!disabled", "img2"), 
                            ("active", "!disabled", "img3"), border=15, sticky=''
        )
        self.style.layout("ScrollableNotebook", [("ScrollableNotebook.client", {"sticky": "nswe"})])
        self.style.layout("ScrollableNotebook.Tab", [
            ("ScrollableNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("ScrollableNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("ScrollableNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("ScrollableNotebook.label", {"side": "left", "sticky": 'se'}),
                                    ("ScrollableNotebook.tab_btn_close", {"side": "left", "sticky": 'nw'}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])
        self.style.configure('ScrollableNotebook',
                            background='#082032',
        )
        self.style.configure("ScrollableNotebook.Tab",
            background='#FDD2BF',
            foreground='#012443',
            padding=[5, 8],
            anchor="center",
            justify="center",
            font=('Courier', 17, font.BOLD)
        )         
        self.style.map('ScrollableNotebook.Tab', background = [("selected", "#B61919"),
                                                    ("active", "#FF6B6B")],
                                        foreground = [("selected", "#ffffff"),
                                                    ("active", "#012443")]
                                                    )
        self.style.configure('TLabel',
                            background="red"
        )
        self.style.map('TLabel',
                            background = [("selected", "#B61919")]
        )
    
    def _wheelscroll(self, event):
        # if event.delta > 0:
        #     Thread(target=self._leftSlide, daemon=True).start()
        # else:
        #     Thread(target=self._rightSlide, daemon=True).start()
        global count
        # # respond to Linux or Windows wheel event
        # if event.num == 5 or event.delta == -120:
        #     count -= 1
        #     Thread(target=self._leftSlide, daemon=True).start()
        #     #self._rightSlide()
        # if event.num == 4 or event.delta == 120:
        #     count += 1
        #     Thread(target=self._rightSlide, daemon=True).start()
        #     #self._leftSlide()
        print(count)

    def _bottomMenu(self,event):
        self.text_font = tkFont.Font(family='Consolas', size=13)
        tabListMenu = Menu(self, tearoff = 0)
        for tab in self.notebookTab.tabs():
            tabListMenu.add_command(label=self.notebookTab.tab(tab, option="text"),
                                    command= lambda temp=tab: self.select(temp),
                                    background='#ccffff', 
                                    foreground='blue',
                                    font=self.text_font,
                                    activebackground='#004c99',
                                    activeforeground='white')
        tabListMenu.entryconfig('WorkSpace  ', 
                                accelerator="ALT+W",
                                image=self.WorkSpac_icon, 
                                compound='left', 
                                label='  WorkSpace')
        try: 
            tabListMenu.tk_popup(event.x_root, event.y_root)
            # self.bottomTab.configure(background='black',
            #                     foreground='#F6D167')
        except:
            self.bottomTab.configure(background='#DF2E2E',
                                foreground='#F6D167')

    def _tabChanger(self,event):
        if event.state == 0:
            self._resetSlide(event=None)
        try:
            self.notebookContent.select(self.notebookTab.index("current"))
        except: pass

    def _rightSlide(self):
        global release
        release = False
        self.rightArrow.configure(foreground='#DF2E2E')
        while not release:
            time.sleep(0.01)
            if self.notebookTab.winfo_width()>self.notebookContent.winfo_width()-self.menuSpace:
                if (self.notebookContent.winfo_width()-(self.notebookTab.winfo_width()+self.notebookTab.winfo_x()))<=self.menuSpace+5:
                    self.xLocation-=20
                    self.notebookTab.place(x=self.xLocation,y=0)
                else:
                    self._release_callback(e=None)
    
    def _leftSlide(self):
        global release
        release = False
        self.leftArrow.configure(foreground='#DF2E2E')
        while not release:
            time.sleep(0.01)
            if not self.notebookTab.winfo_x()== 0:
                self.xLocation+=20
                self.notebookTab.place(x=self.xLocation,y=0)
            else:
                    self._release_callback(e=None)

    def _resetSlide(self, event):
        self.notebookTab.place(x=0,y=0)
        self.xLocation = 0

    def add(self,frame,**kwargs):
        named = kwargs['text']
        if len(self.notebookTab.winfo_children())!=0:
            self.notebookContent.add(frame, text=named,state="hidden")
        else:
            self.notebookContent.add(frame, text=named,state="hidden")
        self.notebookTab.add(ttk.Frame(self.notebookTab),**kwargs)
        id_tab = self.tabs()[-1]
        self.notebookTab.select(id_tab)

    def forget(self,tab_id):
        #self.notebookContent.forget(self.__ContentTabID(tab_id))
        self.notebookTab.forget(tab_id)

    def hide(self,tab_id):
        #self.notebookContent.hide(self.__ContentTabID(tab_id))
        self.notebookTab.hide(tab_id)

    def identify(self,x, y):
        return self.notebookTab.identify(x,y)

    def index(self,tab_id):
        return self.notebookTab.index(tab_id)
        #return self.notebookTab.index(self.notebookTab.select('current'))

    def __ContentTabID(self,tab_id):
        return self.notebookContent.tabs()[self.notebookTab.tabs().index(tab_id)]

    def insert(self,pos,frame, **kwargs):
        #self.notebookContent.insert(pos,frame, **kwargs)
        self.notebookTab.insert(pos,frame,**kwargs)

    def select(self,tab_id):
        self.notebookTab.select(tab_id)
        print(tab_id)
        if tab_id == '.!scrollablenotebook.!notebook2.!frame':
            self._resetSlide(event=None)
            self._release_callback(e=None)
        elif tab_id == '.!scrollablenotebook.!notebook2.!frame2' or tab_id == '.!scrollablenotebook.!notebook2.!frame3' or tab_id == '.!scrollablenotebook.!notebook2.!frame4':
            Thread(target=self._leftSlide, daemon=True).start()
            self.rightArrow.configure(foreground='#297F87')
        else:
            Thread(target=self._rightSlide, daemon=True).start()
            self.leftArrow.configure(foreground='#297F87')

    def tab(self,tab_id, option=None, **kwargs):
        kwargs_Content = kwargs.copy()
        kwargs_Content["text"] = "" # important
        #self.notebookContent.tab(self.__ContentTabID(tab_id), option=None, **kwargs_Content)
        return self.notebookTab.tab(tab_id, option=None, **kwargs)

    def tabs(self):
        #return self.notebookContent.tabs()
        return self.notebookTab.tabs()

    def enable_traversal(self):
        self.notebookContent.enable_traversal()
        self.notebookTab.enable_traversal()