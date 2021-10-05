# -*- coding: utf-8 -*-
import os
import tkinter as tk
from os import listdir, path, sep
from os.path import isdir, join, abspath
from getpass import getuser
from tkinter import *
from tkinter import Button, ttk
from tkinter import scrolledtext as st
from tkinter import messagebox as mb
from tkinter import font
from PIL import Image, ImageTk
from tkinter.ttk import Style
from threading import Thread
import time
user = getuser()
mypath = os.path.expanduser("~/")
path_extracion = mypath+"Compliance/extracion/"
path_icon = mypath+"Compliance/image/"

parar = False
class Extracion(ttk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent, *args)
        self.navIcon = ImageTk.PhotoImage(Image.open(
            path_icon+r"menu.png").resize((25, 25)))
        self.closeIcon = ImageTk.PhotoImage(Image.open(
            path_icon+r"close.png").resize((25, 25)))
        self.wd = 300
        self.menu()
        #self.ampliador()
        self.text()
        self.hidden = 0
        #self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=5)
        self.rowconfigure(0, weight=1)

    def menu(self):
        self.text_font = font.Font(family='Consolas', size=16, weight="bold")
        self.frame1 = tk.Frame(
            self,
            background="gold",
            width=self.wd
        )
        self.frame1.grid_propagate(False)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=1)
        self.btn_nav = Button(
            self,
            background="#39A2DB",
            border=0,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            image=self.navIcon,
            command=self.show_btn_nav,
        )
        self.btn_close = tk.Button(
            self.frame1,
            background="#39A2DB",
            border=0,
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            image=self.closeIcon,
            command=self.hide_btn_nav,
        )
        self.btn_close.grid(row=0, column=0, sticky="e")
        self.treeview = ttk.Treeview(
            self.frame1,
            style="myTREE.Treeview",
        )
        self.treeview.tag_configure(
            "folder",
            font=self.text_font,
        )
        self.treeview.heading("#0", text="EXTRACIONES", anchor="center")
        self.treeview.grid(row=1, column=0, sticky="nsew")

        self.treeview.tag_bind(
            "fstag", "<<TreeviewOpen>>", self.item_opened
        )
        self.treeview.tag_bind(
            "fstag", "<<TreeviewClose>>", self.item_closed
        )
        self.treeview.bind(
            "<<TreeviewSelect>>", lambda e :self.select_extraction(e)
        )
        self.fsobjects = {}
        
        self.file_image = tk.PhotoImage(file=path_icon+r"files.png")
        self.folder_image = tk.PhotoImage(file=path_icon+r"folder.png")

        self.max = ttk.Button(
            self.frame1,
            text="+",
        )
        self.max.grid(row=2, column=0, sticky="e")

        self.min = ttk.Button(
            self.frame1,
            text="-",
        )
        self.min.grid(row=2, column=0, sticky="w")
                
        # Cargar el directorio raíz.
        self.load_tree(abspath(path_extracion))
        self.max.bind("<Button-1>",lambda e: Thread(target=self.ampliar, daemon=True).start())
        self.max.bind("<ButtonRelease-1>", self._parar_)
        self.min.bind("<Button-1>",lambda e: Thread(target=self.reducir, daemon=True).start())
        self.min.bind("<ButtonRelease-1>", self._parar_)

    def ampliar(self):
        global parar
        parar = False
        while not parar:
            time.sleep(0.01)
            if self.wd < 1250:
                self.wd += 3
                self.frame1.config(width=self.wd)
            else:
                self._parar_(event=None)
        print(self.wd)

    def _parar_(self, event):
        global parar
        parar = True
    
    def reducir(self):
        global parar
        parar = False
        while not parar:
            time.sleep(0.01)
            if self.wd > 180:
                self.wd -= 3
                self.frame1.config(width=self.wd)
            else:
                self._parar_(event=None)
    
    def seleccionar_plantilla(self, plantilla):
        self.plantilla = plantilla
        print(self.plantilla)
        with open(plantilla) as g:
            data = g.read()
            self.txt.delete('1.0',tk.END)
            for md in data:
                self.txt.insert(tk.END, md)

    def estilos(self):
        self.style = Style()
        self.style.configure(
            'myTREE.Treeview',
            fieldbackground= '#CEE5D0',
            background='#CEE5D0',
            selectbackground="#FF7878",
            selectforeground="#E0C097",
            padding=0, 
        )
        # self.style.map('Treeview',
        #     background=[
        #         ("active","red")
        #     ]
        # )
    
    def listdir(self, path):
        try:
            return listdir(path)
        except PermissionError:
            print("No tienes suficientes permisos para acceder a", path)
            return []
    
    def get_icon(self, path):
        """
        Retorna la imagen correspondiente según se especifique
        un archivo o un directorio.
        """
        return self.folder_image if isdir(path) else self.file_image
    
    def insert_item(self, name, path, parent=""):
        """
        Añade un archivo o carpeta a la lista y retorna el identificador
        del ítem.
        """
        iid = self.treeview.insert(
            parent, tk.END, text=name, tags=("fstag",)+(("folder",)if isdir(path) else ()),
            image=self.get_icon(path))
        self.fsobjects[iid] = path
        return iid
    
    def load_tree(self, path, parent=""):
        """
        Carga el contenido del directorio especificado y lo añade
        a la lista como ítemes hijos del ítem "parent".
        """
        for fsobj in self.listdir(path):
            fullpath = join(path, fsobj)
            child = self.insert_item(fsobj, fullpath, parent)
            if isdir(fullpath):
                for sub_fsobj in self.listdir(fullpath):
                    self.insert_item(sub_fsobj, join(fullpath, sub_fsobj),
                                    child)

    def load_subitems(self, iid):
        """
        Cargar el contenido de todas las carpetas hijas del directorio
        que se corresponde con el ítem especificado.
        """

        for child_iid in self.treeview.get_children(iid):
            if isdir(self.fsobjects[child_iid]):
                self.load_tree(self.fsobjects[child_iid],
                            parent=child_iid)
    
    def item_opened(self, event):
        """
        Evento invocado cuando el contenido de una carpeta es abierto.
        """
        iid = self.treeview.selection()[0]
        self.load_subitems(iid)
    
    def item_closed(self, event):
        """
        Evento invocado cuando el contenido de una carpeta es abierto.
        """
        iid = self.treeview.selection()[0]
        records = self.treeview.get_children(iid)
        self.treeview.delete(*self.treeview.get_children())
        self.load_tree(abspath(path_extracion))

        #self.listdir(path)
        # for elemnts in records:
        #     self.treeview.delete(elemnts)
        #     self.load_tree(self.fsobjects[elemnts],
        #                         parent=elemnts)
        # for child_iid in self.treeview.get_children(iid):
        #     if isdir(self.fsobjects[child_iid]):
        #             self.load_tree(self.fsobjects[child_iid],
        #                         parent=child_iid)
        #self.load_subitems(iid)

    def select_extraction(self, event):
        iid = self.treeview.selection()[0]
        plantilla = self.treeview.item(iid, option="text")
        path = ''
        for root, _, files in os.walk(path_extracion):
            if plantilla in files:
                path = os.path.join(root, plantilla)
                break
        if len(path) != 0:
            self.seleccionar_plantilla(path)

    def ampliador(self):
        self.frame3 = tk.Frame(
            self
        )
        self.frame3.config(
            border=0,
            background="blue",
            width=1
        )
        #self.frame3.grid(row=0, column=1, sticky="nsew")
    def text(self):
        self.frame2 = tk.Frame(self)
        self.frame2.grid(row=0, column=2, sticky="nsew")
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.rowconfigure(0, weight=1)
        self.txt = st.ScrolledText(
            self.frame2,
            font=("Consolas", 14),
        )
        self.txt.config(
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=2,
            insertbackground='#297F87',
            selectbackground='lightblue',
            state='normal'
        )
        self.txt.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        global parar
        if self.hidden == 0:
            self.frame1.destroy()
            self.hidden = 1
            self.btn_nav.grid(row=0, column=0, sticky="nw")
            parar = False
        else:
            self.menu()
            self.hidden = 0
            self.btn_nav.grid_forget()
            parar = False

    def hide_btn_nav(self):
        global parar
        if self.hidden == 0:
            self.frame1.destroy()
            self.hidden = 1
            self.btn_nav.grid(row=0, column=0, sticky="nw")
        parar = False
        print(self.wd)        

    def show_btn_nav(self):
        global parar
        if self.hidden == 1:
            self.menu()
            self.hidden = 0
            self.btn_nav.grid_forget()
        parar = False
        print(self.wd)