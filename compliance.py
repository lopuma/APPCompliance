import tkinter as tk
import tkinter.font as tkFont
import json
import os
import subprocess
import time
from tkinter import *
from tkinter import ttk
from ScrollableNotebook  import *
from getpass import getuser
from tkinter import scrolledtext as st
from tkinter import messagebox as mb
from tkinter import font
from PIL import Image, ImageTk
from tkinter.ttk import Style
from threading import Thread
from Extracion import *
#-----------------------------------------------------------#
user = getuser()
path = os.path.expanduser("~/")
path_Directory = path+"compliance/file/directory.json"
path_Account = path+"compliance/file/account.json"
path_Command = path+"compliance/file/command.json"
path_Service = path+"compliance/file/service.json"
path_icon = path+"compliance/image/"
clt = ''
path_modulo = path+"compliance/file/desviaciones_{}.json"
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
list_issues = (
    "DESVIACIONES",
    "EXTRACIONES"
)
# --- VARIABLE GLOBAL ---
asigne_Ciente = ""
idOpenTab = 0
listModulo = []
listClave = []
data = []
txtWidget_focus = False
txtWidget = ""
tittleExpand = ""
top_active_LBK = False
class Directory(ttk.Frame):
    def __init__(self, parent, customer, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.customer = customer
        print(self.parent)
        self.vtn_directory = Toplevel(self)
        self.vtn_directory.config(background='#F9F3DF')
        self.vtn_directory.geometry("1000x650+345+65")
        #self.vtn_directory.resizable(0,0)
        self.vtn_directory.title('DIRECTORY for client {}'.format(self.customer))
        #self.vtn_directory.transient(self)
        #self.vtn_directory.grab_set()
        self.vtn_directory.columnconfigure(0, weight=1)
        #self.vtn_directory.rowconfigure(1, weight=1)
        self.vtn_directory.rowconfigure(2, weight=5)
        self.text_font = tkFont.Font(family='Consolas', size=13) 
        self.iconos()
        self.menu_clickDerecho()
        self.menuList_clickDerecho()
        self.widgets_DIRECTORY()
        self.cargar_directory()
        self.tree.bind("<ButtonRelease-1>", self.selecionar_elemntFile)
        self.tree.bind("<Key>", lambda e: desviacion.widgets_SoloLectura(e))
        self.srcRisk.bind("<Key>", lambda e: desviacion.widgets_SoloLectura(e))
        self.srcImpact.bind("<Key>", lambda e: desviacion.widgets_SoloLectura(e))
        self.srcVariable.bind("<Key>", lambda e: desviacion.widgets_SoloLectura(e))
        self.cbxUser.bind("<Key>", lambda e: desviacion.widgets_SoloLectura(e))
        self.textBuscar.bind("<Return>", lambda event=None: self.buscar(self.textBuscar.get()))
        #self.vtn_directory.bind("<Motion>", lambda e:desviacion.activar_Focus(e))
        self.srcImpact.bind("<Button-3>", self.display_menu_clickDerecho)
        self.srcRisk.bind("<Button-3>", self.display_menu_clickDerecho)
        self.srcVariable.bind("<Button-3>", self.display_menu_clickDerecho)
        self.textBuscar.bind("<Button-3>", self.display_menu_clickDerecho)
        self.listServer.bind("<Button-3>", self.display_menuLis_clickDerecho)
        self.textBuscar.bind("<Motion>", lambda x :self.act_elemt_text(x))
        self.srcImpact.bind("<Motion>", lambda x :self.act_elemt_src(x))
        self.srcRisk.bind("<Motion>", lambda x :self.act_elemt_src(x))
        self.srcVariable.bind("<Motion>", lambda x :self.act_elemt_src(x))
        self.listServer.bind("<Motion>", lambda x :self.act_elemt_list(x))
    def iconos(self):
        self.buscar_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"buscar.png").resize((25, 25)))
        self.cerrar_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"reduce.png").resize((25, 25)))
        self.copiar_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"copiarALL.png").resize((20, 20)))
    def cerrar_vtn(self):
        self.vtn_directory.destroy()
    def buscar(self, event=None):
        valor_aBuscar = event
        valor_Buscado = [n for n in self.directory if valor_aBuscar.strip() in n]
        if valor_aBuscar == "":
            mb.showerror(
            "ERROR", "Esta vacio o no existe el directorio/file.\nPrueba a buscar de nuevo...", parent=self.vtn_directory
            )            
            self.cargar_directory()
            self.limpiar_widgets()
        else:
            if len(valor_Buscado) == 0:
                mb.showerror(
                "ERROR", "Esta vacio o no existe el directorio/file.\nPrueba a buscar de nuevo...", parent=self.vtn_directory
                )                 
                self.cargar_directory()
                self.limpiar_widgets()
            else:
                self.limpiar_tree()
                with open(path_Directory) as g:
                    data = json.load(g)
                    count = 0
                    for md in data[self.customer]:
                        for vb in valor_Buscado:
                            if vb == md['directory']:
                                if count % 2 == 0:
                                    self.tree.insert(parent='', index='end', iid=count, text='', value=(md['directory'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('evenrow'))
                                else:
                                    self.tree.insert(parent='', index='end', iid=count, text='', value=(md['directory'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('oddrow'))
                                count += 1
                        self.limpiar_widgets()
    def cargar_directory(self):
        self.directory = []
        #limpiando el arbol de vistas
        self.limpiar_tree()
        with open(path_Directory) as g:
                data = json.load(g)
                count = 0
                for md in data[self.customer]:
                    self.directory.append(md['directory'])
                    if count % 2 == 0:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['directory'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('evenrow'))
                    else:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['directory'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('oddrow'))
                    count += 1
    def limpiar_tree(self):
        records = self.tree.get_children()
        for elemnt in records:
            self.tree.delete(elemnt)
    def selecionar_elemntFile(self, event):
        sel_valor = self.tree.focus()
        valor = self.tree.item(sel_valor, 'values')
        valFile = valor[0]
        with open(path_Directory) as g:
                data = json.load(g)
                for md in data[self.customer]:
                    if valFile == md['directory']:
                        #limpiar------------------------------------                      
                        self.limpiar_widgets()
                        #-------------------------------------------
                        self.listServer.insert(END,*md['servers'])
                        self.srcRisk.insert(END,md['risk'])
                        self.srcImpact.insert(END,md['impact'])
                        self.cbxUser['values'] = md["user"]
                        variables = str(md['variable'])
                        variables = variables.replace("[","").replace("]","").replace("'","").replace(",",";")
                        self.srcVariable.insert(END,variables)
                        self.lbl_SO['text'] = md['SO']
        self.textBuscar.focus()
        self.cbxUser.set('CONTACTOS')
    def limpiar_widgets(self):
        self.lbl_SO['text'] = "SISTEMA OPERATIVO"
        self.listServer.delete(0,END)
        self.srcRisk.delete('1.0',tk.END)
        self.srcImpact.delete('1.0',tk.END)
        self.cbxUser.option_clear()
        self.srcVariable.delete('1.0',tk.END)
    ## --- MENU CONTEXTUAL
    def act_elemt_text(self, event):
        event.widget.focus()
        if event.widget:
            self.menu_Contextual.entryconfig("  Buscar", state="disabled")
            self.menu_Contextual.entryconfig("  Pegar", state="normal")
            self.menu_Contextual.entryconfig("  Copiar", state="disabled")
            self.menu_Contextual.entryconfig("  Seleccionar todo", state="disabled")
            self.menu_Contextual.entryconfig("  Limpiar", state="normal")
            """ data = {
                'label':'Limpiand',
                'accelerator' : 'Ctrl+X',
                'background':'#ccffff', 
                'foreground':'black',
                'activebackground':'#004c99',
                'activeforeground':'white',
                'font':'self.text_font',
                'command':'self.seleccionar_todo',
                'state':'normal'
            }
            self.menu_Contextual.insert_command(8, **data) """
    def act_elemt_list(self, event):
        event.widget.focus()
    def act_elemt_src(self, event):
        event.widget.focus()
        if event.widget:
            self.menu_Contextual.entryconfig("  Buscar", state="normal")
            self.menu_Contextual.entryconfig("  Pegar", state="disabled")
            self.menu_Contextual.entryconfig("  Copiar", state="normal")
            self.menu_Contextual.entryconfig("  Seleccionar todo", state="normal")
            self.menu_Contextual.entryconfig("  Limpiar", state="disabled")
    def act_buscar(self):
        self.textBuscar.focus()
    def seleccionar_todo(self):
        self.srcEvent.tag_add("sel","1.0","end")
        return 'break'
    def copiar(self):
        seleccion = self.srcEvent.tag_ranges(tk.SEL)
        if seleccion:
            app.root.clipboard_clear()
            app.root.clipboard_append(self.srcEvent.get(*seleccion).strip())
            self.srcEvent.tag_remove("sel","1.0","end")
            return 'break'
    def pegar(self):
        self.srcEvent.event_generate("<<Paste>>")
        return 'break'
    def menu_clickDerecho(self):
        self.text_font = tkFont.Font(family='Consolas', size=13)   
        self.menu_Contextual = Menu(self, tearoff=0)
        self.menu_Contextual.add_command(label="  Buscar", 
                                accelerator='Ctrl+F',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.act_buscar,
                                )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(label="  Copiar", 
                                accelerator='Ctrl+C',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.copiar,
                                state='normal',
                                )
        self.menu_Contextual.add_command(label="  Pegar", 
                                accelerator='Ctrl+V',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command= self.pegar,
                                )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=self.seleccionar_todo,
            state='normal',
        )
        self.menu_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=self.seleccionar_todo,
            state='normal',
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(label="  Cerrar pestaña", 
                                #image=self.cerrar_icon,
                                compound=LEFT,
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.cerrar_vtn
                                )
    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
        self.srcEvent = event.widget
        self.srcEvent.focus()
    def menuList_clickDerecho(self):
        self.text_font = tkFont.Font(family='Consolas', size=13)   
        self.menuLis_Contextual = Menu(self, tearoff=0)
        self.menuLis_Contextual.add_command(label="  Buscar", 
                                accelerator='Ctrl+F',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.act_buscar,
                                )
        self.menuLis_Contextual.add_separator(background='#ccffff')
        self.menuLis_Contextual.add_command(label="  Copiar", 
                                accelerator='Ctrl+C',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.copiar,
                                state='normal',
                                )
        self.menuLis_Contextual.add_command(label="  Pegar", 
                                accelerator='Ctrl+V',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command= self.pegar,
                                state='disabled',
                                )
        self.menuLis_Contextual.add_separator(background='#ccffff')
        self.menuLis_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=self.seleccionar_todo,
            state='normal',
        )
        self.menuLis_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=self.seleccionar_todo,
            state='disabled',
        )
        self.menuLis_Contextual.add_separator(background='#ccffff')
        self.menuLis_Contextual.add_command(label="  Cerrar pestaña", 
                                #image=self.cerrar_icon,
                                compound=LEFT,
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.cerrar_vtn
                                )
    def display_menuLis_clickDerecho(self, event):
        self.menuLis_Contextual.tk_popup(event.x_root, event.y_root)
        self.srcEvent = event.widget
        self.srcEvent.focus()
    ## =============================================
    def widgets_DIRECTORY(self):
        self.textBuscar = tk.Entry(
            self.vtn_directory,
            justify='left',
            width=40,
            font=self.text_font,
            borderwidth=2,
            highlightthickness=3,
            highlightcolor='#316B83'
        )
        self.textBuscar.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        self.btnBuscar = ttk.Button(
            self.vtn_directory,
            text='Buscar',
            style='TOP1.TButton',
            image=self.buscar_icon,
            command= lambda: self.buscar(self.textBuscar.get())
        )
        self.btnBuscar.grid(row=0, column=1, sticky=W)

        self.btnCerrar = ttk.Button(
            self.vtn_directory, 
            text='Cerrar',
            style='TOP1.TButton',
            image=self.cerrar_icon,
            command=self.cerrar_vtn
        )
        self.btnCerrar.grid(row=0, column=2, padx=10, pady=5, sticky=E)
        
        ## ====================================================================================
        ## --- CREAMOS EL PRIMER LABEL FRAME
        self.labelframe1=ttk.LabelFrame(
            self.vtn_directory, 
            text="DATOS",
            style='TOP.TLabelframe'
        )
        self.labelframe1.grid(column=0, row=1, padx=10, pady=5, columnspan=3, sticky='nsew')
        self.labelframe1.columnconfigure(0, weight=1)
        
        ## --- creamos el scrollbar
        self.tree_scrollbar=tk.Scrollbar(self.labelframe1, orient=tk.VERTICAL)
        self.tree_scrollbar.grid(column=1, row=0, sticky=N+S,padx=(0,5), pady=10)
        
        ## ---creamos el treeview
        self.tree = ttk.Treeview(
            self.labelframe1, 
            yscrollcommand=self.tree_scrollbar.set,
            height=10,
        )
        ## ---configuramos el scroll al trieview
        self.tree_scrollbar.config(command=self.tree.yview)
        ## ---creamos las columnas
        self.tree['columns'] = ("FILE","ACCOUNT","GECOS","OWNERGROUP","CODE")
        ## --- formato a las columnas
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.column("FILE", anchor=W, width=300)
        self.tree.column("ACCOUNT", anchor=CENTER, width=100)
        self.tree.column("GECOS", anchor=CENTER, width=100)
        self.tree.column("OWNERGROUP", anchor=CENTER, width=150)
        self.tree.column("CODE", anchor=CENTER, width=100)
        ## --- indicar cabecera
        self.tree.heading("#0", text="", anchor=W)
        self.tree.heading("#1", text="FILE", anchor=W)
        self.tree.heading("#2", text="ACCOUNT", anchor=CENTER)
        self.tree.heading("#3", text="GECOS", anchor=CENTER)
        self.tree.heading("#4", text="OWNER GROUP", anchor=CENTER)
        self.tree.heading("#5", text="CODE", anchor=CENTER)
        self.tree.tag_configure('oddrow', background="#CEE5D0", font=self.text_font)
        self.tree.tag_configure('evenrow', background="#F3F0D7", font=self.text_font)
        self.tree.grid(column=0, row=0, pady=10, padx=(5,0), sticky=E+W)

        ## ====================================================================================
        ## --- CREAMOS EL SEGUNDO LABEL FRAME
        self.labelframe2=ttk.LabelFrame(
            self.vtn_directory, 
            text="OTROS DATOS",
            style='TOP.TLabelframe'
        )
        self.labelframe2.grid(column=0, row=2, padx=10, pady=5, columnspan=3, sticky='nsew')
        self.labelframe2.rowconfigure(1, weight=1)
        self.labelframe2.rowconfigure(3, weight=1)
        self.labelframe2.columnconfigure(2, weight=1)
        self.labelframe2.columnconfigure(4, weight=1)

        ## --- SERVERs
        self.lbl1 = ttk.Label(
            self.labelframe2,
            text='SERVER',
            style='TOP.TLabel',
        )
        self.lbl1.grid(row=0, column=0, pady=5, padx=5, columnspan=2)
        
        self.listServer = tk.Listbox(self.labelframe2, height=3)
        self.fr2_scroll1 = tk.Scrollbar(self.labelframe2, orient=tk.VERTICAL)
        self.listServer.config(
            foreground='#334257',
            selectforeground='#CDFFEB', 
            selectbackground='#476072', 
            font=self.text_font,
            highlightcolor='#548CA8',
            borderwidth=0, 
            highlightthickness=3,
            height=8,
            width=15,
            yscrollcommand=self.fr2_scroll1.set
        )
        self.fr2_scroll1.config(command=self.listServer.yview)
        self.listServer.grid(column=0, row=1, padx=(5,0), pady=5, sticky="nsw", rowspan=3)
        self.fr2_scroll1.grid(column=1, row=1, sticky='ns', pady=5, rowspan=3)
        
        ## --- RISK
        self.lbl2 = ttk.Label(
            self.labelframe2, 
            text='RISK',
            style='TOP.TLabel',
        )
        self.lbl2.grid(row=0, column=2, pady=5, padx=5, sticky='W')
        
        self.btnCpRisk = ttk.Button(
            self.labelframe2, 
            text='Copiar',
            style='TOP.TButton',
            image=self.copiar_icon,
        )
        self.btnCpRisk.grid(row=0, column=3, padx=20, pady=5, sticky=E)
        
        self.srcRisk = st.ScrolledText(
            self.labelframe2,
            wrap=tk.WORD,
            highlightcolor='#548CA8',
            borderwidth=0, 
            highlightthickness=3,
        )
        self.srcRisk.config(
            font=self.text_font, 
            height=6,
            foreground='#334257', 
            selectforeground='#CDFFEB', 
            selectbackground='#476072'
        )
        self.srcRisk.grid(row=1, column=2, pady=5, padx=5, sticky='new', columnspan=2)
        
        ## --- IMPACT
        self.lbl3 = ttk.Label(
            self.labelframe2,
            text='IMPACT',
            style='TOP.TLabel',
        )
        self.lbl3.grid(row=0, column=4, pady=5, padx=5, sticky='W')
        
        self.btnCpImp = ttk.Button(
            self.labelframe2,
            text='Copiar',
            style='TOP.TButton',                
            image=self.copiar_icon,
        )
        self.btnCpImp.grid(row=0, column=5, padx=20, pady=5, sticky=E)   
        
        self.srcImpact = st.ScrolledText(
            self.labelframe2,
            wrap=tk.WORD,
            highlightcolor='#548CA8',
            borderwidth=0, 
            highlightthickness=3,
        )
        self.srcImpact.config(
            font=self.text_font, 
            height=6,
            foreground='#334257', 
            selectforeground='#CDFFEB', 
            selectbackground='#476072'
        )
        self.srcImpact.grid(row=1, column=4, pady=5, padx=5, sticky='new', columnspan=2)
        
        ## --- SO
        self.lbl_SO = ttk.Label(
            self.labelframe2,
            text='SISTEMAS OPERATIVO',
            font=("Consolas",15, font.BOLD),
            style='TOP.TLabelframe.Label',
            justify='center',
        )
        self.lbl_SO.grid(row=2, column=2, pady=5, padx=10, sticky='w')
        
        ## --- USER
        self.cbxUser = ttk.Combobox(
            self.labelframe2,
        )
        self.cbxUser.config(
            font=("Consolas",14,font.BOLD), 
            justify='center',
        )
        self.cbxUser.set('CONTACTOS')
        self.cbxUser.grid(row=3, column=2, padx=5, pady=5, ipady=7, sticky='nsew')

        ## --- VARIABLE
        self.lbl4 = ttk.Label(
            self.labelframe2,
            text='VARIABLE',
            style='TOP.TLabel',
        )
        self.lbl4.grid(row=2, column=3, pady=5, padx=5, sticky='W')
        
        self.btnCpVariable = ttk.Button(
            self.labelframe2, 
            text='Copiar',
            style='TOP.TButton',                
            image=self.copiar_icon,
        )
        self.btnCpVariable.grid(row=2, column=5, padx=20, pady=5, sticky=E)

        self.srcVariable = st.ScrolledText(
            self.labelframe2,
            wrap=tk.WORD,
            highlightcolor='#548CA8',
            borderwidth=0, 
            highlightthickness=3,
        )
        self.srcVariable.config(
            font=self.text_font, 
            height=4,
            foreground='#334257', 
            selectforeground='#CDFFEB', 
            selectbackground='#476072'
        )
        self.srcVariable.grid(row=3, column=3, pady=5, padx=5, sticky='new', columnspan=3)
class Expandir(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        self.parent = parent
        super().__init__(*args, **kwargs)
        self.vtn_expandir = Toplevel(self)
        self.vtn_expandir.config(background='#F1ECC3')
        self.vtn_expandir.geometry("1005x600+345+65")
        self.vtn_expandir.transient(self.parent)
        #self.vtn_expandir.resizable(0,0)
        self.vtn_expandir.title("DESVIACIONES : {}".format(asigne_Ciente))
        self.vtn_expandir.columnconfigure(0, weight=1)
        self.vtn_expandir.rowconfigure(1, weight=1)
        self.text_font = tkFont.Font(family='Consolas', size=13)
        self.menu_clickDerecho()
        self.widgets_EXPANDIR()
        self.EXP_srcExpandir.bind("<Button-3><ButtonRelease-3>", self.display_menu_clickDerecho)
        self.EXP_srcExpandir.bind("<Motion>", lambda e:desviacion.activar_Focus(e))
        self.EXP_srcExpandir.bind("<Key>", lambda e: desviacion.widgets_SoloLectura(e))
    ## --- MENU CONTEXTUAL --------------------------- ##
    def cerrar_vtn_expandir(self):
        if txtWidget_focus:
            self.vtn_expandir.destroy()
    def menu_clickDerecho(self):
        self.menu_Contextual = Menu(self.vtn_expandir, tearoff=0)
        self.menu_Contextual.add_command(label="  Copiar", 
                                #image=self.copy2_icon,
                                compound=LEFT,
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command= app.copiar_texto_seleccionado,
                                )
        self.menu_Contextual.add_command(label="  Seleccionar todo", 
                                #image=self.copy2_icon,
                                compound=LEFT,
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=lambda : app.seleccionar_todo(event=None),
                                )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(label="  Cerrar pestaña", 
                                #image=self.cerrar_icon,
                                compound=LEFT,
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.cerrar_vtn_expandir
                                )
    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
    ## ----------------------------------------------- ##
    def widgets_EXPANDIR(self):
        self.EXP_lblWidget = ttk.Label(self.vtn_expandir, 
                                        text=tittleExpand,
                                        foreground='blue',
                                        font=('Source Sans Pro', 16, font.BOLD),
                                        )
        self.EXP_lblWidget.grid(row=0, column=0, padx=5, pady=5,sticky='w')
        self.EXP_btnCopyALL = ttk.Button(self.vtn_expandir,
                                            image=desviacion.CopyALL1_icon,
                                            #command=self.seleccionar_todo,
                                            style='DESV.TButton',
                                            )
        self.EXP_btnCopyALL.grid(row=0, column=1, padx=20, pady=5, sticky='ne')
        self.EXP_btnScreamEvidencia = ttk.Button(self.vtn_expandir,
                                            image=desviacion.Captura1_icon,
                                            command=desviacion.ScreamEvidencia,
                                            style='DESV.TButton',
                                            )
        self.EXP_btnScreamEvidencia.grid(row=0, column=2, pady=5, sticky='ne')
        self.EXP_btnReducir = ttk.Button(self.vtn_expandir,
                                            image=desviacion.Reducir_icon,
                                            command=self.cerrar_vtn_expandir,
                                            style='DESV.TButton',
                                            )
        self.EXP_btnReducir.grid(row=0, column=3, padx=20, pady=5, sticky='ne')
        self.EXP_srcExpandir = st.ScrolledText(self.vtn_expandir,
                                            wrap='word',
                                            font=('Consolas', 15), 
                                            selectbackground='lightblue',
                                            highlightbackground='gray88',
                                            highlightthickness=2,
                                            highlightcolor='#297F87',)
        self.EXP_srcExpandir.grid(row=1, column=0, padx=5, pady=5, sticky='nsew', columnspan=4)
class Extracion(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent,*args)
        text = StringVar()
        button = Button(
            self, 
            textvariable=text,
            font=('Courier',14),
            bg="#00a8e8",
            fg="white"
        ).pack(
            expand=True, 
            fill=BOTH)
        text.set('Click Me!')
class Desviacion(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent,*args)
        self.parent = parent
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.iconos()
        self.widgets_DESVIACION()
        ## --- SELECCIONAR ELEMENTO DEL LISTBOX. --- #
        self.DESVfr1_listbox.bind('<<ListboxSelect>>',self.selecionar_Modulos)
        ## --- ADJUTAR EL TEXT DE LOS LABEL --- #
        self.DESVfr2_lblModulo.bind("<Configure>", self.label_resize)
        self.DESVfr2_lblDescripcion.bind("<Configure>", self.label_resize)
        ## --- ACTIVAR WIDGET. --- #
        self.DESVfr2_srcComprobacion.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr2_srcBackup.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcEditar.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcRefrescar.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcEvidencia.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr1_listbox.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr1_entModulo.bind("<Motion>",lambda e:self.activar_Focus(e))
        app.cuaderno.bind("<Motion>",lambda e:self.activar_Focus(e))
        ## --- MOSTRAR MENU DERECHO  --- ##
        app.root.bind("<Button-3><ButtonRelease-3>", app.display_menu_clickDerecho)
        ## --- ACTIVAR MODO SOLO LECTURA --- ##
        self.DESVfr2_srcComprobacion.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr2_srcBackup.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcEditar.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcRefrescar.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcEvidencia.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        ## --- SELECCIONAR TOD --- ##
        self.DESVfr2_srcComprobacion.bind('<Control-a>', lambda e: app.seleccionar_todo(e))
        self.DESVfr2_srcBackup.bind('<Control-a>', lambda e: app.seleccionar_todo(e))
        self.DESVfr3_srcEditar.bind('<Control-a>', lambda e: app.seleccionar_todo(e))
        self.DESVfr3_srcRefrescar.bind('<Control-a>', lambda e: app.seleccionar_todo(e))
        self.DESVfr3_srcEvidencia.bind('<Control-a>', lambda e: app.seleccionar_todo(e))
        ## --- BUSCAR --- ##
        self.DESVfr1_entModulo.bind("<Return>", lambda event=None: self.buscar_Modulos(self.DESVfr1_entModulo.get()))
        self.DESVfr1_entModulo.bind("<KeyPress>", lambda e: self.limpiar_busqueda(e))
        self.DESVfr1_listbox.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr2_srcComprobacion.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr2_srcBackup.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr3_srcEditar.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr3_srcRefrescar.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr3_srcEvidencia.bind('<Control-f>', lambda e : self.buscar(e))
        app.editMenu.bind_all('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr1_listbox.bind_all("<Down>", self.ListDown)
        self.DESVfr1_listbox.bind_all("<Up>", self.ListUp)
        ## --- --- ##
    def iconos(self): #TODO ICONOS DE VENTANA DESVIACION
        self.BuscarModulo_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"buscar.png").resize((25, 25)))
        self.LimpiarModulo_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"limpiar.png").resize((25, 25)))
        self.Expandir_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"expandir.png").resize((20, 20)))
        self.Captura_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"captura.png").resize((20, 20)))
        self.Captura1_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"captura.png").resize((30, 30)))
        self.Reducir_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"reduce.png").resize((30, 30)))
        self.CopyALL_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"copiarALL.png").resize((20, 20)))
        self.CopyALL1_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"copiarALL.png").resize((30, 30)))
    ## --- ADJUTAR EL TEXT DE LOS LABEL -------------------------- ##
    def label_resize(self, event):
        event.widget['wraplength'] = event.width
    ## --- ACTIVAR MODO SOLO LECTURA ----------------------------- ##
    def widgets_SoloLectura(self, event):
        print(event.state)
        if(20==event.state and event.keysym=='c' or event.keysym=='Down' or event.keysym=='Up' or 20==event.state and event.keysym=='f' or 20==event.state and event.keysym=='a'):
            return
        else:
            return "break"
    ## --- ACTIVAR WIDGET ---------------------------------------- ##
    def activar_Focus(self, event):
        global txtWidget
        global txtWidget_focus
        txtWidget = event.widget
        #print(txtWidget)
        if str(txtWidget) == ".!buttonnotebook":
            txtWidget.focus()
            app.menu_Contextual.entryconfig('  Copiar', state='disabled')
            app.menu_Contextual.entryconfig('  Pegar', state='disabled')
            app.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr1_listbox:
            app.menu_Contextual.entryconfig('  Copiar', state='disabled')
            app.menu_Contextual.entryconfig('  Pegar', state='disabled')
            app.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            txtWidget.focus()
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr1_entModulo:
            app.menu_Contextual.entryconfig('  Copiar', state='disabled')
            app.menu_Contextual.entryconfig('  Pegar', state='normal')
            app.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            txtWidget.focus()
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        else:
            app.menu_Contextual.entryconfig('  Copiar', state='normal')
            app.menu_Contextual.entryconfig('  Buscar', state='normal')
            app.menu_Contextual.entryconfig('  Pegar', state='disabled')
            app.menu_Contextual.entryconfig('  Seleccionar todo', state='normal')
            txtWidget.focus()
            txtWidget_focus = True
        if txtWidget == self.DESVfr2_srcComprobacion:
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr2_srcBackup:
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr3_srcEditar:
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr3_srcRefrescar:
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr3_srcEvidencia:
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
    ## ------ VENTANAS TOP EXPANDIR ------------------------------ ##
    def expandir1(self):
        global tittleExpand
        tittleExpand = "COMPROBACION"
        self.DESVfr2_srcComprobacion.focus()
        expandir = Expandir(self)
        if self.DESVfr2_srcComprobacion:
            text_aExpandir = self.DESVfr2_srcComprobacion.get('1.0', tk.END)
            expandir.EXP_srcExpandir.insert('1.0',text_aExpandir)
    def expandir2(self):
        global tittleExpand
        tittleExpand = "BACKUP"
        self.DESVfr2_srcBackup.focus()        
        expandir = Expandir(self)
        if self.DESVfr2_srcBackup:
            text_aExpandir = self.DESVfr2_srcBackup.get('1.0', tk.END)
            expandir.EXP_srcExpandir.insert('1.0',text_aExpandir)
    def expandir3(self):
        global tittleExpand
        tittleExpand = "EDITAR"
        self.DESVfr3_srcEditar.focus()        
        expandir = Expandir(self)
        if self.DESVfr3_srcEditar:
            text_aExpandir = self.DESVfr3_srcEditar.get('1.0', tk.END)
            expandir.EXP_srcExpandir.insert('1.0',text_aExpandir)
    def expandir4(self):
        global tittleExpand
        tittleExpand = "REFRESCAR"
        self.DESVfr3_srcRefrescar.focus()        
        expandir = Expandir(self)
        if self.DESVfr3_srcRefrescar:
            text_aExpandir = self.DESVfr3_srcRefrescar.get('1.0', tk.END)
            expandir.EXP_srcExpandir.insert('1.0',text_aExpandir)
    def expandir5(self):
        global tittleExpand
        tittleExpand = "EVIDENCIA"
        self.DESVfr3_srcEvidencia.focus()        
        expandir = Expandir(self)
        if self.DESVfr3_srcEvidencia:
            text_aExpandir = self.DESVfr3_srcEvidencia.get('1.0', tk.END)
            expandir.EXP_srcExpandir.insert('1.0',text_aExpandir)
    ## --- FUNCIONES AL SELECIONAR MODULO, O BUSCAR MODULO ------- ##
    def asignarValor_aWidgets(self, md):
        self.DESV_frame2['text'] = md['SO']
        self.DESVfr2_lblModulo['text'] = md['modulo']
        self.DESVfr2_lblDescripcion['text'] = md['descripcion']
        self.DESVfr2_srcComprobacion.insert(END,md['comprobacion'])
        self.DESVfr2_srcBackup.insert(END,md['copia'])
        self.DESVfr3_srcEditar.insert(END,md['editar'])
        self.DESVfr3_srcRefrescar.insert(END,md['refrescar'])
        self.DESVfr3_srcEvidencia.insert(END,md['evidencia'])
    def limpiar_Widgets(self):
        self.DESV_frame2['text'] = 'SISTEMA OPERATIVO SI'
        self.DESVfr2_lblModulo['text'] = 'MODULO'
        self.DESVfr2_lblDescripcion['text'] = ''
        self.DESVfr2_srcComprobacion.delete('1.0',END)
        self.DESVfr2_srcBackup.delete('1.0',END)
        self.DESVfr3_srcEditar.delete('1.0',END)
        self.DESVfr3_srcRefrescar.delete('1.0',END)
        self.DESVfr3_srcEvidencia.delete('1.0',END)
        self.limpiar_busqueda2()
    def selecionar_Modulos(self, event):
        modulo_selecionado = event.widget.get(ANCHOR)
        with open(path_modulo.format(asigne_Ciente)) as g:
            data = json.load(g)
            for md in data:
                if modulo_selecionado in md['modulo']:
                    ## --- LIMPIAR ------------------------------------- ##                      
                    self.limpiar_Widgets()
                    ## ------------------------------------------------- ##
                    self.asignarValor_aWidgets(md)
    def buscar(self, event):
        self.DESVfr1_entModulo.focus()
    def buscar_Modulos(self, event=None):
        try:
            valor_aBuscar = event
            print('valor a buscar --> ', valor_aBuscar)
            print('========== LISTAS ==========')
            print(listClave)
            print('\n\n')
            print(listModulo)
            print('============================')
            clave_Buscado = [n for n in listClave if valor_aBuscar.upper().strip() in n]
            modulo_Buscado = [n for n in listModulo if valor_aBuscar.strip().replace("\\","/") in n]
            if len(clave_Buscado) <= 1:
                clave_Buscado = str(clave_Buscado).replace("[","").replace("]","").replace("'","")
            else:
                clave_Buscado = ""
            if len(modulo_Buscado) <= 1:
                modulo_Buscado = str(modulo_Buscado).replace("[","").replace("]","").replace("'","")
            else:
                modulo_Buscado = ""
            print('--------------------------------------')
            print('clave buscado --> ', clave_Buscado)
            print('modulo buscado --> ', modulo_Buscado)
            print('--------------------------------------')
            # ## --------- OBTENER MODULO POR CLAVE O MODULO -------------- ## //TODO "definir si buscar por clave o modulo"
            if len(clave_Buscado) == 0 and len(modulo_Buscado) == 0:
                self.limpiar_Widgets()
                self.DESVfr1_listbox.select_clear(ANCHOR)
                mb.showerror("ERROR","Esta vacio o no existe el modulo.\nPrueba a buscar por CLAVE o el MODULO completo")
                self.DESVfr1_entModulo.focus()
            elif len(clave_Buscado) != 0:
                with open(path_modulo.format(asigne_Ciente)) as g:
                    data = []
                    data = json.load(g)
                    for md in data:
                        if clave_Buscado in md['clave']:
                            modulo_Encontrado = md['modulo']
                            ## --- LIMPIAR ------------------------------------- ##                      
                            self.limpiar_Widgets()
                            ## ------------------------------------------------- ##
                            self.asignarValor_aWidgets(md)
                    self.DESVfr1_listbox.selection_clear(0, tk.END)        
                    modulo_ListBox = self.DESVfr1_listbox.get(0, tk.END)
                    indice = modulo_ListBox.index(modulo_Encontrado)
                    self.DESVfr1_listbox.selection_set(indice)
                    print('MODULO ENCONTRADO : << {} >> '.format(modulo_Encontrado))
                    # self.DESVfr1_btnBuscar.grid_forget()
                    # self.DESVfr1_btnLimpiar.grid(row=1, column=0, pady=5, padx=5, sticky='nse',columnspan=2)
            else:
                data = []
                with open(path_modulo.format(asigne_Ciente)) as g:
                    data = json.load(g)
                    for md in data:
                        if modulo_Buscado in md['modulo']:
                            modulo_Encontrado = md['modulo']
                            ## --- LIMPIAR ------------------------------------- ##                      
                            self.limpiar_Widgets()
                            ## ------------------------------------------------- ##
                            self.asignarValor_aWidgets(md)
                    self.DESVfr1_listbox.selection_clear(0, tk.END)
                    modulo_ListBox = self.DESVfr1_listbox.get(0, tk.END)
                    indice = modulo_ListBox.index(modulo_Encontrado)
                    self.DESVfr1_listbox.selection_set(indice)
                    print('MODULO ENCONTRADO : << {} >> '.format(modulo_Encontrado))
            self.DESVfr1_btnBuscar.grid_forget()
            self.DESVfr1_btnLimpiar.grid(row=1, column=0, pady=5, padx=5, sticky='nse',columnspan=2)    
        except:
            self.DESVfr1_listbox.select_clear(ANCHOR)
            mb.showerror("ERROR","Esta vacio o no existe el modulo.\nPrueba a buscar por CLAVE o el MODULO completo")
            self.limpiar_Widgets()
            self.DESVfr1_entModulo.focus()    
    def limpiar_busqueda(self, event=None):
        long_entry = self.DESVfr1_entModulo.get()
        if len(long_entry) <= 1:
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=0, pady=5, padx=5, sticky='nse',columnspan=2)
            self.DESVfr1_entModulo.focus()
    def limpiar_busqueda2(self):
        self.DESVfr1_entModulo.delete(0,"end")
        self.DESVfr1_btnLimpiar.grid_forget()
        self.DESVfr1_btnBuscar.grid(row=1, column=0, pady=5, padx=5, sticky='nse',columnspan=2)
        self.DESVfr1_entModulo.focus()
    def ListDown(self, event):
        widget_Focus = event.widget
        listBox = self.DESVfr1_listbox
        print('<<1>>',widget_Focus)
        print('<<2>>',listBox)
        if widget_Focus:
            print('si esta activo LIS')
            event.widget.yview_scroll(1,"units")
            selecion = event.widget.curselection()
            modulo_selecionado = event.widget.get(selecion)
            print('<<3>>',modulo_selecionado)
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if modulo_selecionado in md['modulo']:
                        ## --- LIMPIAR ------------------------------------- ##                      
                        self.limpiar_Widgets()
                        ## ------------------------------------------------- ##
                        self.asignarValor_aWidgets(md)
        #
    def ListUp(self, event):
        widget_Focus = event.widget
        listBox = self.DESVfr1_listbox
        if widget_Focus == listBox:
            self.DESVfr1_listbox.yview_scroll(-1,"units")
            selecion = self.DESVfr1_listbox.curselection()
            modulo_selecionado = event.widget.get(selecion)
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if modulo_selecionado in md['modulo']:
                        ## --- LIMPIAR ------------------------------------- ##                      
                        self.limpiar_Widgets()
                        ## ------------------------------------------------- ##
                        self.asignarValor_aWidgets(md)
        else:
            pass
    def enabled_Widgets(self):
        self.DESVfr1_listbox.config(state="normal")
        self.DESVfr1_entModulo.config(state="normal")
        self.DESVfr1_entModulo.focus()
        self.DESVfr1_btnBuscar.config(state="normal")
        self.DESVfr2_srcComprobacion.config(state="normal")
        self.DESVfr2_srcBackup.config(state="normal")
        self.DESVfr3_srcEditar.config(state="normal")
        self.DESVfr3_srcRefrescar.config(state="normal")
        self.DESVfr3_srcEvidencia.config(state="normal")
        self.DESV_btn1Expandir.config(state='normal')
        self.DESV_btn2Expandir.config(state='normal')
        self.DESV_btn3Expandir.config(state='normal')
        self.DESV_btn4Expandir.config(state='normal')
        self.DESV_btn5Expandir.config(state='normal')
        self.DESV_btnScreamEvidencia.config(state='normal')
        self.DESV_btnCopyALL.config(state='normal')
        self.DESV_btnDirectory.config(state='normal')
    def cargar_Modulos(self, *args):
        self.enabled_Widgets()
        global asigne_Ciente
        global listModulo
        global listClave
        customer = self.clientesVar.get()
        ## --- LIMPIAR -----------------------------
        self.DESVfr1_listbox.delete(0,END)
        self.limpiar_Widgets()
        ## ----------------------------------------- ##
        asigne_Ciente = customer       
        with open(path_modulo.format(customer)) as g:
            data = json.load(g)
            listModulo = []
            listClave = []
            for md in data:
                listModulo.append(md['modulo'])
                listClave.append(md['clave'])
        listModulo.sort()
        self.DESVfr1_listbox.insert(END,*listModulo)
        self.cambiar_NamePestaña(customer)
    def ScreamEvidencia(self):
        app.root.withdraw()
        code = subprocess.call(["./scream.sh"])
        time.sleep(5)
        mb.showinfo("INFO","Informacion")
        app.root.deiconify()
    def copiarALL(self):
        self.DESVfr3_srcEvidencia.focus()
        if self.DESVfr3_srcEvidencia:
            self.DESVfr3_srcEvidencia.tag_add("sel","1.0","end")
            seleccion = self.DESVfr3_srcEvidencia.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(self.DESVfr3_srcEvidencia.get(*seleccion).strip())
        else:
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
    def widgets_DESVIACION(self):
        self.text_font = tkFont.Font(family='Consolas', size=13)
        # --- DEFINIMOS LOS LABEL FRAMEs, QUE CONTENDRAN LOS WIDGETS --------------------------#
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
        self.DESV_frame2.columnconfigure(0, weight=1)
        self.DESV_frame3.columnconfigure(0, weight=1)
        self.DESV_frame1.rowconfigure(2, weight=5)
        self.DESV_frame2.rowconfigure(3, weight=1)
        self.DESV_frame2.rowconfigure(5, weight=1)
        self.DESV_frame3.rowconfigure(1, weight=1)
        self.DESV_frame3.rowconfigure(3, weight=1)
        self.DESV_frame3.rowconfigure(5, weight=1)
        # --- Variable del OptionMenu, lista de clientes ------------------------------#
        self.clientesVar = tk.StringVar(self)
        self.clientesVar.set('CLIENTES')
        # -----------------------------------------------------------------------------#
        ## ======================== FRAME 1 ========================================= ##
        # ---------------- OptionMenu, lista de clientes ---------------------------- ##
        self.DESVfr1_optMn = tk.OptionMenu(self.DESV_frame1, 
                                            self.clientesVar, 
                                            *list_client, 
                                            command=self.cargar_Modulos,
                                            )
        self.DESVfr1_optMn.config(background = "#5F939A",
                                    foreground = "#F2EDD7",
                                    font=('Source Sans Pro',15,font.BOLD),
                                    activebackground="#3A6351",
                                    activeforeground="#F6D167",
                                    relief="groove",
                                    borderwidth=2
                                    )
        self.DESVfr1_optMn["menu"].config(background='#3A6351',
                                            selectcolor='red',
                                            activebackground='#5F939A',
                                            foreground="#F2EDD7",
                                            font=('Source Sans Pro', 13, font.BOLD))
        self.DESVfr1_optMn.grid(row=0, column=0, padx=5, pady=5, sticky='new', columnspan=2)
        # -----------------------------------------------------------------------------#
        ## --- widgets para buscar
        self.DESVfr1_entModulo = ttk.Entry(self.DESV_frame1, width=30)
        self.DESVfr1_entModulo.config(foreground="black",
                                    font=self.text_font,
                                    state='disabled')
        self.DESVfr1_entModulo.grid(row=1, column=0, pady=5, padx=5, ipady=5, sticky='nsew',columnspan=2)
        self.DESVfr1_btnBuscar = ttk.Button(self.DESV_frame1, 
                                                    image=self.BuscarModulo_icon,
                                                    state='disabled',
                                                    command=lambda: self.buscar_Modulos(self.DESVfr1_entModulo.get()),
                                                    style='DESV.TButton'
                                                    )
        self.DESVfr1_btnBuscar.grid(row=1, column=0, pady=5, padx=5, sticky='nse',columnspan=2)
        self.DESVfr1_btnLimpiar = ttk.Button(self.DESV_frame1, 
                                                    image=self.LimpiarModulo_icon,
                                                    command=self.limpiar_busqueda2,
                                                    style='DESV.TButton'
                                                    )
        #self.DESVfr1_btnLimpiar.grid(row=1, column=0, pady=5, padx=5, sticky='nse',columnspan=2)
        # -----------------------------------------------------------------------------#
        self.DESVlist_yScroll = tk.Scrollbar(self.DESV_frame1, orient=tk.VERTICAL)
        self.DESVlist_yScroll.grid(row=2, column=1, pady=5, sticky='nse')
        self.DESVlist_xScroll = tk.Scrollbar(self.DESV_frame1, orient=tk.HORIZONTAL)
        self.DESVlist_xScroll.grid(row=3, column=0, padx=5, sticky='ew', columnspan=2)
        self.DESVfr1_listbox = tk.Listbox(self.DESV_frame1,
                                            state='disabled',
                                            xscrollcommand=self.DESVlist_xScroll.set, 
                                            yscrollcommand=self.DESVlist_yScroll.set,
                                            font=self.text_font,
                                            foreground='blue',
                                            selectbackground='#297F87',
                                            selectforeground='#F6D167',
                                            disabledforeground='black',
                                            exportselection=False,
                                            highlightbackground='gray88',
                                            highlightthickness=2,
                                            highlightcolor='#297F87',
                                            )
        self.DESVfr1_listbox.grid(row=2, column=0, pady=5, padx=5, sticky='nsew')
        self.DESVlist_xScroll['command'] = self.DESVfr1_listbox.xview
        self.DESVlist_yScroll['command'] = self.DESVfr1_listbox.yview
        ## ======================== FRAME 2 ========================================= ##
        ## --- Modulo
        self.DESVfr2_lblModulo = ttk.Label(self.DESV_frame2,
                                            text='MODULO', 
                                            width=10)
        self.DESVfr2_lblModulo.grid(row=0, column=0, padx=5, pady=5, sticky='new', columnspan=3)
        ## --- Descripcion
        self.DESVfr2_lblDescripcion = ttk.Label(self.DESV_frame2,
                                                    text='',
                                                    font=('Source Sans Pro', 12),
                                                    width=10, 
                                                    background='#f1ecc3',
                                                    foreground='gray55') 
        self.DESVfr2_lblDescripcion.grid(row=1, column=0, padx=5, pady=5, sticky='new', columnspan=3)
        ## --- Comprobacion
        self.DESVfr2_lblComprobacion = ttk.Label(self.DESV_frame2, text='COMPROBACIÓN', width=15) 
        self.DESVfr2_lblComprobacion.grid(row=2, column=0, padx=5, pady=5, sticky='w' )
        self.DESV_btnDirectory = ttk.Button(self.DESV_frame2,
                                            text='Directory',
                                            compound='left',
                                            image=self.Expandir_icon,
                                            state='disabled',
                                            command=self.abrir_DIRECTORY,
                                            style='TOPS.TButton'
        )
        self.DESV_btnDirectory.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
        self.DESV_btn1Expandir = ttk.Button(self.DESV_frame2,
                                            image=self.Expandir_icon,
                                            state='disabled',
                                            command=self.expandir1,
                                            )
        self.DESV_btn1Expandir.grid(row=2, column=2, padx=5, pady=5, sticky='ne')
        self.DESVfr2_srcComprobacion = st.ScrolledText(self.DESV_frame2)
        self.DESVfr2_srcComprobacion.config(width=10,
                                            state='disabled',
                                            wrap='word',
                                            font=('Consolas', 13), 
                                            selectbackground='lightblue',
                                            insertbackground='#297F87',
                                            highlightbackground='gray88',
                                            highlightthickness=2,
                                            highlightcolor='#297F87',
                                            )
        self.DESVfr2_srcComprobacion.grid(row=3, column=0, padx=5, pady=5, sticky='new', columnspan=3)
        ## --- Backup
        self.DESVfr2_lblBackup = ttk.Label(self.DESV_frame2, text='BACKUP', width=10) 
        self.DESVfr2_lblBackup.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.DESV_btn2Expandir = ttk.Button(self.DESV_frame2,
                                            image=self.Expandir_icon,
                                            state='disabled',
                                            command=self.expandir2,
                                            )
        self.DESV_btn2Expandir.grid(row=4, column=1, padx=5, pady=5, sticky='nse', columnspan=2)
        self.DESVfr2_srcBackup = st.ScrolledText(self.DESV_frame2)
        self.DESVfr2_srcBackup.config(width=10,
                                            state='disabled',
                                            wrap='word',
                                            font=self.text_font, 
                                            selectbackground='lightblue',
                                            insertbackground='#297F87',
                                            highlightbackground='gray88',
                                            highlightthickness=2,
                                            highlightcolor='#297F87',)
        self.DESVfr2_srcBackup.grid(row=5, column=0, padx=5, pady=5, sticky='new', columnspan=3)
        ## ======================== FRAME 3 ========================================= ##
        ## --- Editar
        self.DESVfr3_lblEditar = ttk.Label(self.DESV_frame3, text='EDITAR ✍')
        self.DESVfr3_lblEditar.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.DESV_btn3Expandir = ttk.Button(self.DESV_frame3,
                                            image=self.Expandir_icon,
                                            state='disabled',
                                            command=self.expandir3,
                                            )
        self.DESV_btn3Expandir.grid(row=0, column=1, padx=5, pady=5, sticky='nse', columnspan=3)
        self.DESVfr3_srcEditar = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcEditar.config(width=10,
                                            state='disabled',
                                            wrap='word',
                                            font=self.text_font, 
                                            selectbackground='lightblue',
                                            insertbackground='#297F87',
                                            highlightbackground='gray88',
                                            highlightthickness=2,
                                            highlightcolor='#297F87',
                                            )
        self.DESVfr3_srcEditar.grid(row=1, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        ## --- Refrescar
        self.DESVfr3_lblRefrescar = ttk.Label(self.DESV_frame3, text='REFRESCAR')
        self.DESVfr3_lblRefrescar.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.DESV_btn4Expandir = ttk.Button(self.DESV_frame3,
                                            image=self.Expandir_icon,
                                            state='disabled',
                                            command=self.expandir4,
                                            )
        self.DESV_btn4Expandir.grid(row=2, column=1, padx=5, pady=5, sticky='nse', columnspan=3)
        self.DESVfr3_srcRefrescar = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcRefrescar.config(width=10,
                                            state='disabled',
                                            wrap='word',
                                            font=self.text_font, 
                                            selectbackground='lightblue',
                                            insertbackground='#297F87',
                                            highlightbackground='gray88',
                                            highlightthickness=2,
                                            highlightcolor='#297F87',)
        self.DESVfr3_srcRefrescar.grid(row=3, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        ## --- Evidencia
        self.DESVfr3_lblEvidencia = ttk.Label(self.DESV_frame3, text='EVIDENCIA')
        self.DESVfr3_lblEvidencia.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.DESV_btnCopyALL = ttk.Button(self.DESV_frame3,
                                            image=self.CopyALL_icon,
                                            state='disabled',
                                            command=self.copiarALL,
                                            )
        self.DESV_btnCopyALL.grid(row=4, column=1, padx=(20,5), pady=5, sticky='ne')
        self.DESV_btnScreamEvidencia = ttk.Button(self.DESV_frame3,
                                            image=self.Captura_icon,
                                            state='disabled',
                                            command=self.ScreamEvidencia,
                                            )
        self.DESV_btnScreamEvidencia.grid(row=4, column=2, padx=5, pady=5, sticky='ne')
        self.DESV_btn5Expandir = ttk.Button(self.DESV_frame3,
                                            image=self.Expandir_icon,
                                            state='disabled',
                                            command=self.expandir5,
                                            )
        self.DESV_btn5Expandir.grid(row=4, column=3, padx=5, pady=5, sticky='ne')
        self.DESVfr3_srcEvidencia = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcEvidencia.config(width=10,
                                            state='disabled',
                                            wrap='word',
                                            font=self.text_font, 
                                            selectbackground='lightblue',
                                            insertbackground='#297F87',
                                            highlightbackground='gray88',
                                            highlightthickness=2,
                                            highlightcolor='#297F87',)
        self.DESVfr3_srcEvidencia.grid(row=5, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        ## ------------------------------------------------------------------------------ ##
    ## --- FUNCIONES PARA ABRIR VENTANAS EMERGENTE --------------- ##
    def abrir_DIRECTORY(self):
        global asigne_Ciente
        global directory
        directory = Directory(self,asigne_Ciente)
    def abrir_COMMAND(self):
        pass
    def abrir_ACCOUNT(self):
        pass
    def abrir_SERVICE(self):
        pass
    ## ----------------------------------------------------------- ##
    def cambiar_NamePestaña(self, customer):
        app.cuaderno.tab(idOpenTab, option=None, text='DESVIACIONES : {}'.format(customer))
        app.cuaderno.notebookContent.tab(idOpenTab, option=None, text='DESVIACIONES : {}'.format(customer))
class Aplicacion():
    def __init__(self):
        self.root= Tk()
        self.root.title("CONTINOUS COMPLIANCE")
        self.root.geometry("1028x768")
        self.root.configure(background='black') 
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=path_icon+'compliance.png'))       
        self.iconos()
        self.cuaderno = ScrollableNotebook(self.root,wheelscroll=True,tabmenu=True)
        self.contenedor= ttk.Frame(self.cuaderno)
        self.contenedor.columnconfigure(1, weight=1)
        self.contenedor.rowconfigure(1, weight=1)
        self.cuaderno.add(self.contenedor,text='WorkSpace  ', underline=0, image=self.WorkSpace_icon, compound='left')
        self.cuaderno.pack(fill="both",expand=True)
        self.cuaderno.bind_all("<<NotebookTabChanged>>",lambda e:self.alCambiar_Pestaña(e))
        self.cuaderno.enable_traversal()
        self.root.bind("<Control-l>", lambda x : self.ocultar())
        self.estilos()
        self.menu_clickDerecho()
        self.widgets_APP()
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
        self.SelAllBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"selall.png").resize((30, 30)))
        self.BuscarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"buscar1.png").resize((30, 30)))
        self.CopiarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"copiarBarra.png").resize((30, 30)))
        self.PegarBar_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"pegarBarra.png").resize((30, 30)))
        self.Ayuda_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"ayuda.png").resize((30, 30)))
        self.AcercaDe_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"acercaDe.png").resize((30, 30)))
        self.WorkSpace_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"workspace.png").resize((20, 20)))
    def estilos(self):
        self.style = Style()
        self.style.configure('TCombobox',
                        fieldbackground= 'white',
                        background='#F4D19B',
                        selectbackground="#476072",
                        selectforeground="#CDFFEB"
        )
        self.style.map('TCombobox',
            background=[
                ("active","#D7E9F7")
            ]
        )
        self.style.configure('TFrame',
                            background='#f1ecc3',
        )
        self.style.configure('TLabelframe',
            background='#f1ecc3',
        )
        self.style.configure('TLabelframe.Label',
            background='#1A1C20',
            foreground='#F0A500',
            font=('Source Sans Pro',12, font.BOLD),
        )
        ## --- ESTILOS DE VENTANAS TOP
        self.style.configure(
            'TOP.TLabelframe',
            background='#F9F3DF',
        )
        self.style.configure(
            'TOP.TLabelframe.Label',
            background='#D7E9F7',
            foreground='black',
        )
        self.style.configure(
            'TOP.TButton',
            background = "#F4D19B",
            relief='sunke',
            borderwidth=1,
            padding=7,
        )
        self.style.map(
            'TOP.TButton',
            background = [("active","#D7E9F7")],
            padding=[("active",7),("pressed",10)],
            relief=[("active",'ridge'),("pressed",'groove')],
            borderwidth=[("active",1)],
        )
        self.style.configure('TOP1.TButton',
                            background = "#F4D19B",
                            relief='sunke',
                            borderwidth=1,
                            padding=10,
        )
        self.style.map('TOP1.TButton',
                            background = [("active","#D7E9F7")],
                            padding=[("active",7),("pressed",10)],
                            relief=[("active",'ridge'),("pressed",'groove')],
                            borderwidth=[("active",1)],
        )
        self.style.configure(
            'TOPS.TButton',
            background = "#96BB7C",
            foreground="white",
            relief='sunke',
            borderwidth=1,
            anchor="center",
            padding=7,
            font=('Source Sans Pro', 13, font.BOLD), 
        )
        self.style.map(
            'TOPS.TButton',
            background=[("active","#FAD586")],
            foreground=[("active","#C64756")],
            padding=[("active",7)],
            relief=[("active",'ridge'),("pressed",'groove')],
            borderwidth=[("active",1)],
        )
        self.style.configure(
            'TOP.TLabel',
            background = "#F9F3DF",
            foreground = "#A45D5D",
            font=('Source Sans Pro',12, font.BOLD)
        )
        ## ===============================================================================
        self.style.configure(
            'APP.TButton',
            background = "#297F87",
            foreground = "#FFF7AE",
            font=('Source Sans Pro',14,font.BOLD),
            padding=20,
            relief='sunke',
            borderwidth=5,
        )
        self.style.map(
            'APP.TButton',
            background = [("active","#F6D167")],
            foreground = [("active","#DF2E2E")],
            padding=[("active",20),("pressed",20)],
            relief=[("active",'ridge'),("pressed",'groove')],
            borderwidth=[("active",5)],
        )
        self.style.configure('TButton',
                            background = "#D4ECDD",
                            relief='sunke',
                            borderwidth=1,
                            padding=7,
                            )
        self.style.map('TButton',
                            background = [("active","#F6D167")],
                            padding=[("active",7),("pressed",5)],
                            relief=[("active",'ridge'),("pressed",'groove')],
                            borderwidth=[("active",1)],
                            )
        self.style.configure('DESV.TButton',
                            background = "#D4ECDD",
                            relief='sunke',
                            borderwidth=1,
                            padding=10,
                            )
        self.style.map('DESV.TButton',
                            background = [("active","#F6D167")],
                            padding=[("active",10),("pressed",10)],
                            relief=[("active",'ridge'),("pressed",'groove')],
                            borderwidth=[("active",1)],
                            )
        self.style.configure('APP.TLabel',
                            background = "#082032",
                            foreground = "#CDFFEB",
                            font=('Source Sans Pro',20,font.BOLD))
        self.style.configure('TLabel',
                            background = "#f1ecc3",
                            foreground = "gray17",
                            font=('Helvetica',12, font.BOLD))
    ## --- MENU CONTEXTUAL --- ##
    def menu_clickDerecho(self):
        self.text_font = tkFont.Font(family='Consolas', size=13)   
        self.menu_Contextual = Menu(self.root, tearoff=0)
        self.menu_Contextual.add_command(label="  Buscar", 
                                accelerator='Ctrl+F',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.buscar,
                                state='disabled',
                                )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(label="  Copiar", 
                                accelerator='Ctrl+C',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command= self.copiar_texto_seleccionado,
                                state='disabled',
                                )
        self.menu_Contextual.add_command(label="  Pegar", 
                                accelerator='Ctrl+V',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command= self.pegar_texto_seleccionado,
                                state='disabled',
                                )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(label="  Seleccionar todo", 
                                accelerator='Ctrl+A',
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=lambda : self.seleccionar_todo(event=None),
                                state='disabled',
                                )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(label="  Cerrar pestaña", 
                                #image=self.cerrar_icon,
                                compound=LEFT,
                                background='#ccffff', foreground='black',
                                activebackground='#004c99',activeforeground='white',
                                font=self.text_font,
                                command=self.cerrar_vtn_desviacion
                                )
    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
    def buscar(self, *args):
        desviacion.buscar(event=None)
    def pegar_texto_seleccionado(self):
        #desviacion.DESVfr1_entModulo.focus()
        global txtWidget
        txtWidget.event_generate("<<Paste>>")
        return 'break'
    def copiar_texto_seleccionado(self):
        global txtWidget_focus
        global txtWidget
        if txtWidget_focus:
            seleccion = txtWidget.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(txtWidget.get(*seleccion).strip())
                txtWidget.tag_remove("sel","1.0","end")
                return 'break'
    def seleccionar_todo(self, event):
        if txtWidget_focus:
            txtWidget.tag_add("sel","1.0","end")
            return 'break'
    def cerrar_vtn_desviacion(self):
        if idOpenTab == 0:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
        else:
            self.cuaderno.forget(idOpenTab)
            self.cuaderno.notebookContent.forget(idOpenTab)
    ## ----------------------- ##
    def alCambiar_Pestaña(self, event):
        global idOpenTab
        global top_active_LBK
        global asigne_Ciente
        #nn_top = 
        idOpenTab = event.widget.index('current')
        tab = event.widget.tab(idOpenTab)['text']
        if idOpenTab != 0:
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
        elif idOpenTab == 0:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
            self.cuaderno._release_callback(e=None)
        if idOpenTab == 1 or idOpenTab == 2 or idOpenTab == 3 or idOpenTab == 4:
            self.cuaderno.rightArrow.configure(foreground='#297F87')
            Thread(target=self.cuaderno._leftSlide, daemon=True).start()
            self.cuaderno._release_callback(e=None)
            self.cuaderno.rightArrow.configure(foreground='#297F87')

        ## -----------ASIGNAMOS A UNA VARIABLE CADA CLIENTE----------------------------
        if tab == 'WorkSpace  ':
            asigne_Ciente = ""
            self.fileMenu.entryconfig('  Clientes', state='disabled')
            self.menu_Contextual.entryconfig('  Buscar', state='disabled')
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
        elif tab == 'DESVIACIONES : AFB':
            asigne_Ciente = 'AFB'
        elif tab == 'DESVIACIONES : ASISA':
            asigne_Ciente = 'ASISA'
        elif tab == 'DESVIACIONES : CESCE':
            asigne_Ciente = 'CESCE'
        elif tab == 'DESVIACIONES : CTTI':
            asigne_Ciente = 'CTTI'
        elif tab == 'DESVIACIONES : ENEL':
            asigne_Ciente = 'ENEL'
        elif tab == 'DESVIACIONES : EUROFRED':
            asigne_Ciente = 'EUROFRED'
        elif tab == 'DESVIACIONES : FT':
            asigne_Ciente = 'FT'
        elif tab == 'DESVIACIONES : INFRA':
            asigne_Ciente = 'INFRA'
        elif tab == 'DESVIACIONES : IDISO':
            asigne_Ciente = 'IDISO'
        elif tab == 'DESVIACIONES : LBK':
            asigne_Ciente = 'LBK'
        elif tab == 'DESVIACIONES : PLANETA':
            asigne_Ciente = 'PLANETA'
        elif tab == 'DESVIACIONES : SERVIHABITAT':
            asigne_Ciente = 'SERVIHABITAT'
        else:
            self.fileMenu.entryconfig('  Clientes', state='normal')
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')
        if 'asigne_Ciente' in globals() and len(asigne_Ciente) != 0:
            with open(path_modulo.format(asigne_Ciente)) as g:
                global listClave
                global listModulo
                data = json.load(g)
                listModulo = []
                listClave = []
                for md in data:
                    listModulo.append(md['modulo'])
                    listClave.append(md['clave'])
    def abrir_issuesDesviacion(self):
        global desviacion
        global idOpenTab
        desviacion = Desviacion(self.cuaderno)
        self.cuaderno.add(desviacion, text='Issues DESVIACIONES')
        #self.cuaderno.select('.!scrollablenotebook.!notebook2.!frame2')
    def abrir_issuesExtracion(self):
        global extracion
        # extracion = Extracion(self.cuaderno)
        extracion = Extracione(self.cuaderno)
        self.cuaderno.add(extracion, text='Issues EXTRACIONES')
    def ocultar(self):
        extracion.hide()
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
                                                #command=self.cargame_elmodulo
                                                )

            self.IssuesVar = tk.IntVar()
            for i, m in enumerate(list_issues):
                self.issuesMenu.add_radiobutton(label=m,
                                                variable=self.IssuesVar,
                                                value=i,
                                                #command=self.abrir_issues
                                                )

            self.editMenu = Menu(self.menuBar, tearoff=0)
            self.editMenu.config(background='#003638',
                                foreground='#F3F2C9',
                                font=('Sans serif',12,font.BOLD),
                                activebackground='#003638',
                                activeforeground='#53B8BB',
                                )
            self.editMenu.add_command(label="  Buscar",
                                        accelerator='Ctrl+F',
                                        #command=self.buscar,
                                        image=self.BuscarBar_icon,
                                        compound=LEFT)
            self.fileMenu.add_separator()
            # self.editMenu.add_command(label="  Selecionar todo",
            #                             accelerator='Ctrl+A',
            #                             command=lambda : self.seleccionar_todo(event=None),                                
            #                             image=self.SelAllBar_icon,
            #                             compound=LEFT)
            # self.editMenu.add_command(label="  Copiar",
            #                             accelerator='Ctrl+C',
            #                             command= self.copiar_texto_seleccionado,
            #                             image=self.CopiarBar_icon,
            #                             compound=LEFT)
            # self.editMenu.add_command(label="  Pegar",
            #                             accelerator='Ctrl+V',
            #                             command= self.pegar_texto_seleccionado,
            #                             image=self.PegarBar_icon,
            #                             compound=LEFT)

            self.helpMenu = Menu(self.menuBar, tearoff=0)
            self.helpMenu.config(background='#003638',
                                foreground='#F3F2C9',
                                font=('Sans serif',12,font.BOLD),
                                activebackground='#003638',
                                activeforeground='#53B8BB',
                                )
            self.helpMenu.add_command(label="  Ayuda",
                                        image=self.Ayuda_icon,
                                        compound=LEFT,
                                        command=self.ocultar,
            )
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
                                        command=self.abrir_issuesDesviacion
                                        )
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
                                        command=self.abrir_issuesExtracion
                                        )
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