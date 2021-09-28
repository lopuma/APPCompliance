#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import Button, ttk
from tkinter.constants import W
from PIL import Image, ImageTk
from tkinter import scrolledtext as st
from os import listdir, path, sep
from os.path import isdir, join, abspath
from tkinter import font
from tkinter.ttk import Style
class Extracione(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args)
        self = self
        self.configure(background="gold")
        self.navIcon = ImageTk.PhotoImage(Image.open(
            "/home/esy9d7l1/compliance/image/menu.png").resize((25, 25)))
        self.closeIcon = ImageTk.PhotoImage(Image.open(
            "/home/esy9d7l1/compliance/image/close.png").resize((25, 25)))
        self.menu()
        self.text()
        self.bind("<Control-l>", lambda x: self.hide())
        self.hidden = 0
        # self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.rowconfigure(0, weight=1)
        #self.lb.bind('<<ListboxSelect>>', self.seleccionar_plantilla)

    def seleccionar_plantilla(self, event):
        print("abrir")
        nombre = "SSH_Aix_FT_CSD_PREG:267"
        with open("/home/esy9d7l1/compliance/extracion/{}".format(nombre), "r", encoding="utf-8") as g:
            data = g.read()
            self.txt.delete('1.0',tk.END)
            for md in data:
                self.txt.insert(tk.END, md)

        # if modulo_selecionado in md['modulo']:
        #     ## --- LIMPIAR ------------------------------------- ##
        #     self.limpiar_Widgets()
        #     ## ------------------------------------------------- ##
        #     self.asignarValor_aWidgets(md)

    def menu(self):
        
        self.frame1 = tk.Frame(
            self,
            background="gold",
            width=300
        )

        # self.frame1.pack(side="left", fill=tk.BOTH, expand=1)
        self.frame1.grid_propagate(False)
        self.frame1.grid(row=0, column=0, sticky="nsew")
        self.frame1.columnconfigure(0, weight=1)
        self.frame1.rowconfigure(1, weight=1)
        # self.frame1.rowconfigure(0, weight=1)
        self.btn_nav = Button(self,
                              background="#39A2DB",
                              border=0,
                              borderwidth=0,
                              highlightthickness=0,
                              relief='flat',
                              image=self.navIcon,
                              command=self.show_btn_nav,
                              )

        # self.btn_nav.grid(row=0, column=0, sticky="nw")
        #self.frame1.columnconfigure(1, weight=1)
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
        # self.btn.pack(side="top", fill=tk.X)
        self.btn_close.grid(row=0, column=0, sticky="e")
        # self.btn_nav.grid_forget()
        self.tree = Treeview(self.frame1)
        
        self.tree.rowconfigure(1, weight=1)
        self.tree.columnconfigure(0, weight=1)
        #+-------------------------------------------+
        # self.lb = tk.Listbox(self.frame1)
        # self.lb['bg'] = "white"
        # self.lb['fg'] = "blue"
        # self.lb['font'] = "Consolas", 13
        self.tree.grid(row=1, column=0, sticky="nsew")
        # # self.lb.pack(side="left", fill=tk.BOTH, expand=1)
        # self.lb.insert(tk.END, "Plantilla 1")
        # # for file in glob.glob("extracion/*"):
        # # 	self.lb.insert(tk.END, file)
        #+-------------------------------------------+

    def text(self):
        self.frame2 = tk.Frame(self)
        # self.frame2.pack(side="left", fill=tk.BOTH, expand=1)
        self.frame2.grid(row=0, column=1, sticky="nsew")
        self.frame2.columnconfigure(0, weight=1)
        self.frame2.rowconfigure(0, weight=1)
        self.txt = st.ScrolledText(
            self.frame2,
            font=("Consolas", 14),
        )
        # self.txt.config(state='disabled')
        self.txt['bg'] = 'white'
        # self.txt.pack(fill=tk.BOTH, expand=1)
        self.txt.grid(row=0, column=0, sticky="nsew")

    def hide(self):
        if self.hidden == 0:
            self.frame1.destroy()
            self.hidden = 1
            self.btn_nav.grid(row=0, column=0, sticky="nw")
            print("Hidden", self.hidden)
        else:
            # self.frame2.destroy()
            self.menu()
            # self.text()
            self.hidden = 0
            self.btn_nav.grid_forget()
            print("Hidden", self.hidden)

    def hide_btn_nav(self):
        if self.hidden == 0:
            self.frame1.destroy()
            self.hidden = 1
            self.btn_nav.grid(row=0, column=0, sticky="nw")
            print("Hidden", self.hidden)

    def show_btn_nav(self):
        if self.hidden == 1:
            #self.frame2.destroy()
            self.menu()
            #self.text()
            self.hidden = 0
            self.btn_nav.grid_forget()
            print("Hidden", self.hidden)
class Treeview(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args)
        self.text_font = font.Font(family='Consolas', size=16)
        #self = self
        #self.title("Explorador de archivos y carpetas")
        self.estilos()
        self.treeview = ttk.Treeview(self)
        #self.treeview.rowconfigure(1, weight=1)
        #self.treeview.columnconfigure(0, weight=1)
        #self.treeview.tag_configure('oddrow', background="#CEE5D0", font=self.text_font)
        #self.treeview.tag_configure('evenrow', background="#F3F0D7", font=self.text_font)
        self.treeview.heading("#0", text="EXTRACIONES", anchor="center")
        self.treeview.grid(row=1, column=0, sticky="nsew")
        
        # Asociar el evento de expansión de un elemento con la
        # función correspondiente.
        self.treeview.tag_bind(
            "fstag", "<<TreeviewOpen>>", self.item_opened
        )
        self.treeview.bind(
            "<<TreeviewSelect>>", lambda e :self.select_extraction(e)
        )
        
        # Expandir automáticamente.
        # for w in (self, self):
       
        #self.grid(row=1, column=0, sticky="nsew")
        
        # Este diccionario conecta los IDs de los ítems de Tk con
        # su correspondiente archivo o carpeta.
        self.fsobjects = {}
        
        self.file_image = tk.PhotoImage(file="/home/esy9d7l1/compliance/image/files.png")
        self.folder_image = tk.PhotoImage(file="/home/esy9d7l1/compliance/image/folder.png")
        
        # Cargar el directorio raíz.
        self.load_tree(abspath("/home/esy9d7l1/compliance/extracion"))
    
    def estilos(self):
        self.style = Style()
        self.style.configure(
            'Treeview',
            fieldbackground= '#CEE5D0',
            background='#CEE5D0',
            selectbackground="#FF7878",
            selectforeground="#E0C097",
            font=('Calibra',14)
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
            print("No tienes suficientes permisos para acceder a",
                  path)
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
            parent, tk.END, text=name, tags=("fstag",),
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
    
    def select_extraction(self, event):
        tree_event = event.widget
        item_id = tree_event.selection()[0]
        ## ---Obtener el index
        index = tree_event.index(item_id)
        ## -----------------------------------
        dir_selecionado = tree_event.item(item_id, option="text")
        print(dir_selecionado)

