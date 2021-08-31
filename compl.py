#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--- importamos librerias ----------------------------------#
from tkinter import font
from tkinter import scrolledtext as st
import json
from getpass import getuser
import os
from tkinter.ttk import Style

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter import *
    from PIL import Image, ImageTk
    from tkinter import messagebox as mb
except ImportError:
    import Tkinter as Tk
    import ttk
#-----------------------------------------------------------#
user = getuser()
path = os.path.expanduser("~/")
path_Directory = path+"compliance/file/directory.json"
path_Account = path+"compliance/file/account.json"
path_Command = path+"compliance/file/command.json"
path_Service = path+"compliance/file/service.json"
path_icon = path+"compliance/image/"
path_modulo = path+"compliance/file/" #TODO variable de modulos

list_client = [
    "AFB",
    "ASISA",
    "CESCE",
    "CTTI",
    "ENEL",
    "EUROFRED",
    "FT",
    "INFRA",
    "IDISO",
    "LBK",
    "PLANETA",
    "SERVIHABITAT"
]  
list_issues = [
    "DESVIACIONES",
    "EXTRACIONES"
]
class Directory(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widgetsFiles()
        self.listServer.delete(0,END)
        self.srcRisk.delete('1.0',tk.END)
        self.srcImpact.delete('1.0',tk.END)
        self.cbxUser.delete(0,END)
    def cargar_files(self):
        #limpiando el arbol de vistas
        records = self.tree.get_children()
        for elemnt in records:
            self.tree.delete(elemnt)
        with open(path_Directory) as g:
                data = json.load(g)
                count = 0
                for md in data[clt]:
                    if count % 2 == 0:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['directory'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('evenrow'))
                    else:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['directory'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('oddrow'))
                    count += 1
    def selecionar_elemntFile(self, event):
        sel_valor = self.tree.focus()
        valor = self.tree.item(sel_valor, 'values')
        valFile = valor[0]
        with open(path_Directory) as g:
                data = json.load(g)
                for md in data[clt]:
                    if valFile == md['directory']:
                        #limpiar------------------------------------                      
                        self.listServer.delete(0,END)
                        self.srcRisk.delete('1.0',tk.END)
                        self.srcImpact.delete('1.0',tk.END)
                        self.cbxUser.delete(0,END)
                        #-------------------------------------------
                        self.listServer.insert(END,*md['servers'])
                        self.srcRisk.insert(END,md['risk'])
                        self.srcImpact.insert(END,md['impact'])
                        self.cbxUser['values']=md["user"]
        self.cbxUser.set('CONTACTOS')
    def widgetsFiles(self):
        self.vtn_files = Toplevel(self)
        self.vtn_files.config(background='#F1ECC3')
        self.vtn_files.geometry("860x585+345+65")
        self.vtn_files.resizable(0,0)
        self.vtn_files.title('FILES')
        
        self.textBuscar = ttk.Entry(self.vtn_files,
                                        justify='left',
                                        width=40,
                                        font=('Trajan', 12))
        self.textBuscar.grid(row=0, column=0, padx=10, pady=10, ipady=7, sticky='we')

        self.btnBuscar = ttk.Button(self.vtn_files, 
                                        text='Buscar FICHERO')
        self.btnBuscar.grid(row=0, column=1, pady=10, sticky='w')

        self.btnCerrar = ttk.Button(self.vtn_files, 
                                        text='Cerrar')
        self.btnCerrar.grid(row=0, column=2, padx=60, pady=10, sticky=E)

        self.labelframe1=ttk.LabelFrame(self.vtn_files, text="DATOS")
        self.labelframe1.grid(column=0, row=1, padx=10, pady=10, columnspan=3, sticky='nsew')
        self.tree_scrollbar=tk.Scrollbar(self.labelframe1, orient=tk.VERTICAL)
        self.tree_scrollbar.grid(column=1, row=0, sticky=N+S, pady=10)
        #creamos el treeview
        self.tree = ttk.Treeview(self.labelframe1, 
                                yscrollcommand=self.tree_scrollbar.set,
                                height=9)
        #configuramos el scroll al trieview
        self.tree_scrollbar.config(command=self.tree.yview)
        #creamos las columnas
        self.tree['columns'] = ("FILE","ACCOUNT","GECOS","OWNERGROUP","CODE")
        #formato a las columnas
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("FILE", anchor=W, width=140)
        self.tree.column("ACCOUNT", anchor=CENTER, width=200)
        self.tree.column("GECOS", anchor=CENTER, width=140)
        self.tree.column("OWNERGROUP", anchor=CENTER, width=200)
        self.tree.column("CODE", anchor=CENTER, width=140)
        #indicar cabecera
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("#1", text="FILE", anchor=W)
        self.tree.heading("#2", text="ACCOUNT", anchor=CENTER)
        self.tree.heading("#3", text="GECOS", anchor=CENTER)
        self.tree.heading("#4", text="OWNER GROUP", anchor=CENTER)
        self.tree.heading("#5", text="CODE", anchor=CENTER)

        self.tree.tag_configure('oddrow', background="light cyan", font=('Trajan', 12))
        self.tree.tag_configure('evenrow', background="LightCyan3", font=('Trajan', 12))
        self.tree.grid(column=0, row=0, pady=10)

        self.labelframe2=ttk.LabelFrame(self.vtn_files, text="OTROS DATOS")
        self.labelframe2.grid(column=0, row=2, padx=10, pady=10, columnspan=3, sticky='nsew')
        
        self.lbl1 = ttk.Label(self.labelframe2, text='SERVER')
        self.lbl1.grid(row=0, column=0, pady=5, padx=5)

        self.listServer = tk.Listbox(self.labelframe2, height=3)
        self.fr2_scroll1 = tk.Scrollbar(self.labelframe2, orient=tk.VERTICAL)
        self.listServer.config(foreground='blue',
                                    selectforeground='white', 
                                    selectbackground='#347083', 
                                    font=('Trajan', 12),
                                    height=8, width=20,
                                    yscrollcommand=self.fr2_scroll1.set)
        self.fr2_scroll1.config(command=self.listServer.yview)
        self.listServer.grid(column=0, row=1, padx=5, pady=5, sticky=N+E+S+W, rowspan=2)
        self.fr2_scroll1.grid(column=0, row=1, sticky='nse', pady=5, rowspan=2)

        self.lbl2 = ttk.Label(self.labelframe2, text='RISK')
        self.lbl2.grid(row=0, column=1, pady=5, padx=10, sticky='W')
        
        self.btnCpRisk = ttk.Button(self.labelframe2, 
                                        text='Copiar')
        self.btnCpRisk.grid(row=0, column=1, padx=10, pady=10, sticky=E)
        
        self.srcRisk = st.ScrolledText(self.labelframe2,
                                    wrap=tk.WORD,
                                    highlightcolor='#548CA8',
                                    borderwidth=0, 
                                    highlightthickness=3,)
        self.srcRisk.config(font=('Trajan', 12), 
                                    width=27,
                                    height=4,
                                    foreground='#334257', 
                                    selectforeground='#CDFFEB', 
                                    selectbackground='#476072')
        self.srcRisk.grid(row=1, column=1, pady=5, padx=10, sticky='n')

        self.lbl3 = ttk.Label(self.labelframe2, text='IMPACT')
        self.lbl3.grid(row=0, column=2, pady=10, padx=5, sticky='W')

        self.btnCpImp = ttk.Button(self.labelframe2, 
                                        text='Copiar')
        self.btnCpImp.grid(row=0, column=2, padx=5, pady=10, sticky=E)

        self.srcImpact = st.ScrolledText(self.labelframe2,
                                    wrap=tk.WORD,
                                    highlightcolor='#548CA8',
                                    borderwidth=0, 
                                    highlightthickness=3,)
        self.srcImpact.config(font=('Trajan', 12), 
                                    width=27,
                                    height=4,
                                    foreground='#334257', 
                                    selectforeground='#CDFFEB', 
                                    selectbackground='#476072')
        self.srcImpact.grid(row=1, column=2, pady=5, padx=5, sticky='n')
        self.cbxUser = ttk.Combobox(self.labelframe2, foreground='blue', width=14)
        self.cbxUser.config(font=('Trajan', 12), justify='center')
        self.cbxUser.set('CONTACTO')
        self.cbxUser.grid(column=1, row=2, pady=10, padx=10, sticky='nsew')
        self.tree.bind("<ButtonRelease-1>", self.selecionar_elemntFile)
        self.cargar_files()
class Desviacion(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.widgets_DESVIACION()
    def widgets_DESVIACION(self):
        # --- DEFINIMOS LOS FRAME, QUE CONTENDRAN LOS WIDGETS --------------------------#
        self.DESV_frame1=ttk.LabelFrame(self, 
                                        text="CLIENTE / MODULO", 
                                        border=1, 
                                        relief='sunken')
        self.DESV_frame1.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        self.DESV_frame2=ttk.LabelFrame(self, 
                                        text="SISTEMA OPERATIVO", 
                                        border=1, 
                                        relief='sunken')
        self.DESV_frame2.grid(column=1, row=0, padx=10, pady=10, sticky='nsew')
        self.DESV_frame3=ttk.LabelFrame(self, 
                                        text="EDITAR / EVIDENCIA", 
                                        border=1, 
                                        relief='sunken')
        self.DESV_frame3.grid(column=2, row=0, padx=10, pady=10, sticky='nsew')
        # -----------------------------------------------------------------------------#
        self.DESV_frame1.columnconfigure(0, weight=1)
        #self.DESV_frame1.columnconfigure(1, weight=1)

        self.DESV_frame2.columnconfigure(0, weight=1)
        self.DESV_frame3.columnconfigure(0, weight=1)
        #self.DESV_frame1.rowconfigure(0, weight=1)
        #self.DESV_frame1.rowconfigure(1, weight=1)
        self.DESV_frame1.rowconfigure(2, weight=5)

        self.DESV_frame2.rowconfigure(0, weight=1)
        self.DESV_frame3.rowconfigure(0, weight=1)
        # --- Variable del OptionMenu, lista de clientes ------------------------------#
        clientesVar = tk.StringVar(self)
        clientesVar.set('CLIENTES')
        # -----------------------------------------------------------------------------#
        ## ======================== FRAME 1 ========================================= ##
        # --- OptionMenu, lista de clientes ------------------------------ #
        self.DESfr1_optMn = ttk.OptionMenu(self.DESV_frame1, 
                                            clientesVar, 
                                            *list_client, 
                                            command=self.cargar_modulo)
        self.DESfr1_optMn["menu"].config(background='#3A6351',
                                            selectcolor='#082032',
                                            activebackground='#5F939A',
                                            foreground="#F2EDD7",
                                            font=('Source Sans Pro', 13, font.BOLD))
        self.DESfr1_optMn.grid(row=0, column=0, padx=5, pady=5, sticky='new', columnspan=2)
        # -----------------------------------------------------------------------------#
        # --- widgets para buscar -----------------------------------------------------#
        self.DESfr1_entry = ttk.Entry(self.DESV_frame1, width=25)
        self.DESfr1_entry.config(foreground="black",
                                    font=('Source Sans Pro', 15, font.BOLD))
        self.DESfr1_entry.grid(row=1, column=0, pady=5, padx=5, ipady=8, sticky='nsew',columnspan=2)
        self.DESfr1_button = ttk.Button(self.DESV_frame1, text='H', width=5)
        self.DESfr1_button.grid(row=1, column=0, pady=5, padx=5, ipady=8, sticky='e',columnspan=2)
        # -----------------------------------------------------------------------------#
        self.yScroll = tk.Scrollbar(self.DESV_frame1, orient=tk.VERTICAL)
        self.yScroll.grid(row=2, column=1, pady=5, sticky='nse')
        self.xScroll = tk.Scrollbar(self.DESV_frame1, orient=tk.HORIZONTAL)
        self.xScroll.grid(row=3, column=0, padx=5, sticky='ew', columnspan=2)
        self.listbox = tk.Listbox(self.DESV_frame1, xscrollcommand=self.xScroll.set, yscrollcommand=self.yScroll.set)
        self.listbox.grid(row=2, column=0, pady=5, padx=5, sticky='nsew')
        cities = ('CASTELL DE L''ARENY',
             'CASTELLADRAL',
             'CASTELLAR',
             'CASTELLAR DE N''HUG',
             'CASTELLAR DEL RIU',
             'CASTELLBELL I VILLAR',
             'CASTELLBISBAL',
             'CASTELLCIR',
             'CASTELLDEFELS',
             'CASTELLET',
             'CASTELLFOLLIT DE RIUBREGOS',
             'CASTELLFOLLIT DEL BOIX',
             'CASTELLGALI',
             'CASTELLNOU DE BAGES',
             'CASTELLOLI',
             'CASTELLTALLAT',
             'CASTELLTERÇOL',
             'CASTELLVI DE LA MARCA',
             'CASTELLVI DE ROSANES',
             'CENTELLES')    
        self.listbox.insert(tk.END,*cities)
        self.xScroll['command'] = self.listbox.xview
        self.yScroll['command'] = self.listbox.yview
        ## ======================== FRAME 2 ========================================= ##
        self.DESfr2_lblModulo = ttk.Label(self.DESV_frame2, text='MODULO')
        self.DESfr2_lblModulo.grid(row=0, column=0, padx=5, pady=5, sticky='new')
        ## ======================== FRAME 3 ========================================= ##
        self.DESfr3_lblModulo = ttk.Label(self.DESV_frame3, text='EDITAR')
        self.DESfr3_lblModulo.grid(row=0, column=0, padx=5, pady=5, sticky='new')
    def abrir_file(self):
        global Directory
        files = Directory(self)
    def callback(*args):
        id_tab = app.cuaderno.index(app.cuaderno.select())
        app.cuaderno.tab(id_tab, text='DESVIACIONES : '+clt)
    def cargar_modulo(self, *args):
        global clt
        clt = clientesVar.get()
        print('cliente al cargar modulo : ',clt)
        self.callback(clt)
class ButtonNotebook(ttk.Notebook):
    _initialized = False
    def __init__(self, parent, *args, **kwargs):
        if not self._initialized:
            self._initialize()
            self._inititialized = True
        kwargs["style"] = "ButtonNotebook"
        super().__init__(*args, **kwargs)
        self._active = None
        self.bind("<ButtonPress-1>", self.on_tab_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_tab_close_release)
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
        self.style.layout("ButtonNotebook", [("ButtonNotebook.client", {"sticky": "nswe"})])
        self.style.layout("ButtonNotebook.Tab", [
            ("ButtonNotebook.tab", {
                "sticky": "nswe", 
                "children": [
                    ("ButtonNotebook.padding", {
                        "side": "top", 
                        "sticky": "nswe",
                        "children": [
                            ("ButtonNotebook.focus", {
                                "side": "top", 
                                "sticky": "nswe",
                                "children": [
                                    ("ButtonNotebook.label", {"side": "left", "sticky": ''}),
                                    ("ButtonNotebook.tab_btn_close", {"side": "left", "sticky": ''}),
                                ]
                            })
                        ]
                    })
                ]
            })
        ])
        self.style.configure("ButtonNotebook.Tab",
            background='#FDD2BF',
            foreground='#012443',
            padding=[20, 10],
        )         
        self.style.map('ButtonNotebook.Tab', background = [("selected", "#B61919"),
                                                      ("active", "#FF6B6B")],
                                        foreground = [("selected", "#ffffff"),
                                                      ("active", "#012443")]
                 ) 
class Aplicacion():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CONTINOUS COMPLIANCE")
        self.root.geometry("1028x768")
        #self.root.resizable(0,0)
        self.cuaderno = ButtonNotebook(self.root)
        self.contenedor = ttk.Frame(self.cuaderno)
        self.contenedor.columnconfigure(1, weight=1)
        self.contenedor.rowconfigure(1, weight=1)
        self.cuaderno.add(self.contenedor, text='WorkSpace')
        self.cuaderno.pack(expand=1, fill='both')
        self.iconos()
        self.widgets_APP()
        self.estilos()
    def estilos(self):
        self.style = Style()
        self.style.configure('.',
                            font=('Source Sans Pro',12, font.BOLD),)
        self.style.configure('TFrame',
                            background='#f1ecc3',
        )
        self.style.configure('TLabelframe',
                            background='#f1ecc3',
        )
        self.style.configure('TLabelframe.Label',
                            background='#1A1C20',
                            foreground='#F0A500',
        )
        self.style.configure('ButtonNotebook',
                            background='#082032'
        )
        self.style.configure('APP.TButton',
                            background = "#297F87",
                            foreground = "#FFF7AE",
                            font=('Source Sans Pro',14,font.BOLD),
                            padding=20,
                            relief='sunke',
                            borderwidth=5,
                            )
        self.style.map('APP.TButton',
                            background = [('active',"#F6D167"),('pressed','red')],
                            foreground = [('active',"#DF2E2E"),('pressed','red')],
                            padding=[('active',20),('pressed',100)],
                            relief=[('active','ridge'),('pressed','groove')],
                            borderwidth=[('active',5)],
                            )
        self.style.configure('APP.TLabel',
                            background = "#082032",
                            foreground = "#CDFFEB",
                            font=('Source Sans Pro',20,font.BOLD))
        self.style.configure('TMenubutton',
                            background = "#5F939A",
                            foreground = "#F2EDD7",
                            padding = 5,
                            font=('Source Sans Pro',15,font.BOLD))
        self.style.map('TMenubutton',
                            background = [('active',"#3A6351")],
                            foreground = [('active',"#A0937D")],
                            relief=[('active','ridge'),('pressed','groove')],
                            borderwidth=[('active',1)],
                            )
    def iconos(self):
        self.Desviaciones_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"openDesviaciones.png").resize((80, 80)))
        self.Extracion_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"openExtraciones.png").resize((80, 80)))
        self.Abrir_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"abrir.png").resize((30, 30)))
        self.Client_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"clientes.png").resize((30, 30)))
        self.Salir_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"salir.png").resize((30, 30)))
        self.CopiarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"copiarBarra.png").resize((30, 30)))
        self.PegarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"pegarBarra.png").resize((30, 30)))
        self.Ayuda_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"ayuda.png").resize((30, 30)))
        self.AcercaDe_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"acercaDe.png").resize((30, 30)))
    def abrir_issuesDesviacion(self):
        global desviacion
        desviacion = Desviacion(self)
        self.cuaderno.add(desviacion, text='Issues DESVIACIONES')
        self.cuaderno.select(desviacion)
    def widgets_APP(self):
        self.menuBar = tk.Menu(self.root, relief=FLAT, border=0)
        self.root.config(menu=self.menuBar)
        self.menuBar.config(background='#1A1C20',
                            foreground='#CF7500',
                            font=('Sans serif',12,font.BOLD),
                            activebackground='#003638',
                            activeforeground='#53B8BB',
                            )
        
        self.fileMenu = Menu(self.menuBar, tearoff=0)
        self.fileMenu.config(background='#003638',
                            foreground='#F3F2C9',
                            font=('Sans serifo',12,font.BOLD),
                            activebackground='#003638',
                            activeforeground='#53B8BB',
                            )

        # --- INICIAMOS SUB MENU -------------------------- #
        self.clientMenu = Menu(self.fileMenu, tearoff=0)
        self.issuesMenu = Menu(self.fileMenu, tearoff=0)
        # -------------------------------------------------- #

        self.issuesMenu.config(background='#003638',
                            foreground='#F3F2C9',
                            font=('Sans serifo',12,font.BOLD),
                            activebackground='#003638',
                            activeforeground='#53B8BB',
                            selectcolor='#CF7500'
                            )
        self.clientMenu.config(background='#003638',
                            foreground='#F3F2C9',
                            font=('Sans serifo',12,font.BOLD),
                            activebackground='#003638',
                            activeforeground='#53B8BB',
                            selectcolor='#CF7500'
                            )

        self.fileMenu.add_cascade(label="  Abrir",
                                    compound=LEFT,
                                    image=self.Abrir_icon,
                                    menu = self.issuesMenu)

        self.fileMenu.add_cascade(label="  Clientes",
                                    image=self.Client_icon,
                                    compound=LEFT,
                                    menu=self.clientMenu)

        self.fileMenu.add_separator()

        self.fileMenu.add_command(label="  Salir",
                                    image=self.Salir_icon,
                                    compound=LEFT,
                                    command=self.root.quit)

        self.ClientVar = tk.IntVar()
        for i, m in enumerate(list_client):
            self.clientMenu.add_radiobutton(label=m,
                                            variable=self.ClientVar,
                                            value=i,
                                            )

        self.IssuesVar = tk.IntVar()
        for i, m in enumerate(list_issues):
            self.issuesMenu.add_radiobutton(label=m,
                                            variable=self.IssuesVar,
                                            value=i,
                                            )

        self.editMenu = Menu(self.menuBar, tearoff=0)
        self.editMenu.config(background='#003638',
                            foreground='#F3F2C9',
                            font=('Sans serif',12,font.BOLD),
                            activebackground='#003638',
                            activeforeground='#53B8BB',
                            )
        self.editMenu.add_command(label="  Copiar",
                                    image=self.CopiarBar_icon,
                                    compound=LEFT)
        self.editMenu.add_command(label="  Pegar",
                                    image=self.PegarBar_icon,
                                    compound=LEFT)

        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu.config(background='#003638',
                            foreground='#F3F2C9',
                            font=('Sans serif',12,font.BOLD),
                            activebackground='#003638',
                            activeforeground='#53B8BB',
                            )
        self.helpMenu.add_command(label="  Ayuda",
                                    image=self.Ayuda_icon,
                                    compound=LEFT,)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(label="  Acerca de...",
                                    image=self.AcercaDe_icon,
                                    compound=LEFT,)

        self.menuBar.add_cascade(label=" Archivo ", menu=self.fileMenu)
        self.menuBar.add_cascade(label=" Editar ", menu=self.editMenu)
        self.menuBar.add_cascade(label=" Ayuda ", menu=self.helpMenu)

        self.btn_AbrirDesv = ttk.Button(self.contenedor, text='DESVIACIONES',
                                    width=15,
                                    style='APP.TButton',
                                    image=self.Desviaciones_icon,
                                    compound='top',
                                    command=self.abrir_issuesDesviacion)
        self.btn_AbrirDesv.grid(padx=30, 
                                    pady=30, 
                                    row=0, 
                                    column=0, 
                                    ipady=20, 
                                    sticky='wn')
        self.btn_AbrirExt = ttk.Button(self.contenedor, text='EXTRACIONES',
                                    width=15,
                                    style='APP.TButton',
                                    image=self.Extracion_icon,
                                    compound='top',
                                    command=self.abrir_issuesDesviacion)
        self.btn_AbrirExt.grid(
                                    pady=30,
                                    row=0, 
                                    column=1, 
                                    ipady=20, 
                                    sticky='wn')
        self.lbl_Bienvenido = ttk.Label(self.contenedor,
                                            style='APP.TLabel',
                                            text='Bienvenido : '+user,
                                            anchor='center')
        self.lbl_Bienvenido.grid(row=1, 
                                    column=0, 
                                    columnspan=3,
                                    sticky='sew')
    def mainloop(self):
        self.root.mainloop()
if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()