# -*- coding: utf-8 -*-
# Copyright (c) Muhammet Emin TURGUT 2020
# For license see LICENSE
from posixpath import commonpath
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
path_icon = path+"Compliance/image/"
count = 0
class ScrollableNotebook(ttk.Frame):
    _initialized = False
    def __init__(self,parent,wheelscroll=False,tabmenu=False, application=None,*args,**kwargs):
        ttk.Frame.__init__(self, parent, *args)
        if not self._initialized:
            self._initialize()
            self._inititialized = True
        kwargs["style"] = "ScrollableNotebook"
        self._active = None
        self.xLocation = 0
        self._application = application
        self.WorkSpac_icon = ImageTk.PhotoImage(Image.open(path_icon+r"workspace.png").resize((20, 20)))
        self.novo = ImageTk.PhotoImage(Image.open(path_icon+r"novo.png").resize((25, 25)))
        self.notebookContent = ttk.Notebook(self,**kwargs)
        self.notebookContent.pack(fill="both", expand=True)
        self.notebookTab = ttk.Notebook(self,**kwargs)
        self.notebookTab.bind("<<NotebookTabChanged>>",lambda e:self._tabChanger(e))
        if wheelscroll==True: 
            self.notebookTab.bind("<MouseWheel>", self._wheelscroll)
            self.notebookTab.bind("<Button-4>", self._wheelscroll)
            self.notebookTab.bind("<Button-5>", self._wheelscroll)
        slideFrame = ttk.Frame(self)
        slideFrame.place(relx=1.0, x=0, y=0, anchor=NE)
        self.menuSpace=30
        if tabmenu==True:
            self.menuSpace=50
            self.bottomTab = ttk.Label(slideFrame, 
                                text="  \u2630  ", 
                                background='#DF2E2E',
                                foreground='#F6D167',
                                width=5, 
                                anchor="center"
                                )
            self.bottomTab.bind("<1>",self._bottomMenu)
            self.bottomTab.pack(side=RIGHT, ipady=12)
        self.bottomTab_novo = ttk.Label(slideFrame, 
                                image=self.novo,
                                text="Abrir",
                                #width=5,
                                padding=(10,0),
                                background="#082032",
                                foreground="white",
                                )
        self.bottomTab_novo.bind("<1>",self._bottomMenu_novo)
        self.bottomTab_novo.pack(side=LEFT, ipady=8)

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
                                    ("ScrollableNotebook.label", {"side": "left", "sticky": 'nsew'}),
                                    ("ScrollableNotebook.tab_btn_close", {"side": "left", "sticky": 'nsew'}),
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
            padding=[2, 2],
            anchor="center",
            justify="center",
            font=('Sans-Serif', 12, font.BOLD)
        )         
        self.style.map('ScrollableNotebook.Tab', background = [("selected", "#B61919"),
                                                    ("active", "#FF6B6B")],
                                        foreground = [("selected", "#ffffff"),
                                                    ("active", "#012443")]
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
        except:
            self.bottomTab.configure(background='#DF2E2E',
                                foreground='#F6D167')

    def _bottomMenu_novo(self,event):
        self.text_font = tkFont.Font(family='Consolas', size=13)
        self.tabListMenu = Menu(self, tearoff = 0)
        self.tabListMenu.add_command(
            label="  Desviaciones", 
            #accelerator='Ctrl+F',
            command=self._abrir_issuesDESV,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
        )
        self.tabListMenu.add_command(
            label="  Extraciones", 
            #accelerator='Ctrl+F',
            command=self._abrir_issuesEXT,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
        )
        self.tabListMenu.tk_popup(event.x_root, event.y_root)
    
    def _abrir_issuesEXT(self):
        self._application.abrir_issuesExtracion()
        Thread(target=self._rightSlide, daemon=True).start()
        self.leftArrow.configure(foreground='#297F87')

    def _abrir_issuesDESV(self):
        self._application.abrir_issuesDesviacion()
        Thread(target=self._rightSlide, daemon=True).start()
        self.leftArrow.configure(foreground='#297F87')

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
