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
            self.bottomTab.pack(side=LEFT, ipady=12)

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
            tk.PhotoImage("im1", data='''
                        R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2f///////////////yH5
                        BAEKAAIALAAAAAAIAAgAAAMUCCAsCmO5OBVl8OKhoV3e9jQOkAAAOw==
                        '''),
            tk.PhotoImage("im2", data='''
                        R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2f///////////////yH5
                        BAEKAAMALAAAAAAIAAgAAAMPCDA8+gw+GGlVbWKqmwMJADs=
                        ''' ),
            tk.PhotoImage("im3", data='''
                        R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2f///////////////yH5B
                        AEKAAMALAAAAAAIAAgAAAMPGDE8+gw+GGlVbWKqmwsJADs=
                        ''')
        )
        self.style.element_create("tab_btn_close", "image", "im1",
                            ("active", "pressed", "!disabled", "im2"),
                            ("active", "!disabled", "im3"), border=8, sticky='')
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
                                    ("ScrollableNotebook.label", {"side": "left", "sticky": ''}),
                                    ("ScrollableNotebook.tab_btn_close", {"side": "left", "sticky": ''}),
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
            padding=[20, 10],
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
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            count -= 1
            Thread(target=self._leftSlide, daemon=True).start()
            #self._rightSlide()
        if event.num == 4 or event.delta == 120:
            count += 1
            Thread(target=self._rightSlide, daemon=True).start()
            #self._leftSlide()
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
        print('sube')
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