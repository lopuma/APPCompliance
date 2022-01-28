#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#import tkinter as tk
import json
import os
import subprocess
import time
from tkinter import *
from tkinter import ttk
from getpass import getuser
from tkinter import scrolledtext as st
from tkinter import messagebox as mb
from tkinter import font as font
from PIL import Image, ImageTk
from tkinter.ttk import Style
from threading import Thread
from ScrollableNotebook  import *
from Extraciones import Extracion
from Ventanas import *
#-----------------------------------------------------------#
user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
clt = ''
path_modulo = mypath+"Compliance/file/desviaciones_{}.json"
path_modulo_clave = mypath+"Compliance/file/{}.json"
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
top_active_LBK = False
sis_oper = ""
idpTab = 0
varNum = 0
text_aExpandir = ""
value = ""
valor_activo_list = ""
list_motion = ""
srcCom = ""
srcBac = ""
srcEdi = ""
srcRes = ""
srcEvi = ""
srcDes = ""
srcMod = ""
srcSO = ""
_tt_Desv = ""
listbox_list = []

class Expandir(ttk.Frame):
    
    def __init__(self, parent, text_EXP, widget_EXP, customer, titulo, so, st_btnDIR, st_btnAUTH, st_btnSER, st_btnACC, st_btnCMD, st_btnIDR, varNum, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.customer = customer
        self.titulo = titulo
        self.so = so
        # Recibe el text del SRC a expandir
        self.txt_Expan = text_EXP
        self.widget_EXP = widget_EXP
        ##-----------------------------------
        self.st_btnDIR = st_btnDIR
        self.st_btnAUTH = st_btnAUTH
        self.st_btnSER = st_btnSER
        self.st_btnACC = st_btnACC
        self.st_btnCMD = st_btnCMD
        self.st_btnIDR = st_btnIDR
        self.varNum = varNum
        self.vtn_expandir = tk.Toplevel(self)
        self.vtn_expandir.config(background='#F1ECC3')
        window_width=1010
        window_height=650
        screen_width = app.root.winfo_x()
        screen_height= app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_expandir.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_expandir.tk.call('wm', 'iconphoto', self.vtn_expandir._w, tk.PhotoImage(file=path_icon+r'expandir1.png'))       
        self.vtn_expandir.transient(self.parent)
        self.vtn_expandir.title("DESVIACIONES : {} - {}".format(self.customer,self.so))
        self.vtn_expandir.columnconfigure(0, weight=1)
        self.vtn_expandir.rowconfigure(1, weight=1)
        
        # FUENTE PARA MENU CLICK DERECHO DE EXPLANDIR
        self._font_MC_Expan = font.Font(family='Courier', size=14)
        # ----------------------------------------------------------------
        self.icono()
        self.menu_clickDerecho()
        self.widgets_EXPANDIR()
        self.Expan_color_lineas()
        self.EXP_srcExpandir.bind("<Button-3><ButtonRelease-3>", self.display_menu_clickDerecho)
        self.EXP_srcExpandir.bind("<Motion>", lambda e:desviacion.activar_Focus(e))
        self.EXP_srcExpandir.bind("<Key>", lambda e: desviacion.widgets_SoloLectura(e))
        self.EXP_srcExpandir.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
    ## --- MENU CONTEXTUAL --------------------------- ##
    def icono(self):
        self.previous_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"previous.png").resize((40, 40)))
        self.next_icon = ImageTk.PhotoImage(
            Image.open(path_icon+r"next.png").resize((40, 40)))    
    
    def cerrar_vtn_expandir(self):
        #if txtWidget_focus:
        self.vtn_expandir.destroy()
    
    def menu_clickDerecho(self):
        self.menu_Contextual = Menu(self.vtn_expandir, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Copiar", 
            compound=LEFT,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_Expan,
            command= desviacion.copiar_texto_seleccionado,
            state="disabled"
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Seleccionar todo", 
            compound=LEFT,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_Expan,
            command=lambda : desviacion.seleccionar_todo(event=None),
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña", 
            #image=self.cerrar_icon,
            compound=LEFT,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_Expan,
            command=self.cerrar_vtn_expandir
        )
    
    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
        self.srcEvent = event.widget
        self.srcEvent.focus()
        txt_select = event.widget.tag_ranges(tk.SEL)
        if txt_select:
            self.menu_Contextual.entryconfig("  Copiar", state="normal")
        else:
            self.menu_Contextual.entryconfig("  Copiar", state="disabled")
    ## ----------------------------------------------- ##
    def copiarALL(self, event):
        event.focus()
        if event:
            event.tag_add("sel","1.0","end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel","1.0","end")
    
    def _copiar_texto_seleccionado(self, event):
        scrText = event.widget
        seleccion = scrText.tag_ranges(tk.SEL)
        if seleccion:
            app.root.clipboard_clear()
            app.root.clipboard_append(scrText.get(*seleccion).strip())
            scrText.tag_remove("sel","1.0","end")
            return 'break'
        else:
            pass
        
    def _siguiente(self):
        global _tt_Desv
        self.EXP_btnScreamEvidencia.configure(state="disabled")
        self.EXP_btnCopyALL.configure(state="disabled")
        if self.varNum == 1:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['copia']
                        if self._txt_Desv is None:
                            _tt_Desv = "EDITAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['editar'])
                            self.varNum = 3
                            self.descativar_botones()
                        else:
                            _tt_Desv = "BACKUP"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.varNum = 2
                            self.descativar_botones()
        elif self.varNum == 2:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['editar']
                        if self._txt_Desv is None:
                            _tt_Desv = "REFRESCAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['refrescar'])
                            self.EXP_btnCopyALL.configure(state="normal")                        
                            self.varNum = 4
                            self.descativar_botones()
                        else:
                            _tt_Desv = "EDITAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.varNum = 3
                            self.descativar_botones()
        elif self.varNum == 3:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['refrescar']
                        if self._txt_Desv is None:
                            _tt_Desv = "EVIDENCIA"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['evidencia'])
                            self.EXP_btnScreamEvidencia.configure(state="normal")
                            self.EXP_btnCopyALL.configure(state="normal")
                            self.varNum = 5
                            self.descativar_botones()
                        else:
                            _tt_Desv = "REFRESCAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.EXP_btnCopyALL.configure(state="normal")                        
                            self.varNum = 4      
                            self.descativar_botones()
        elif self.varNum == 4:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['evidencia']
                        if self._txt_Desv is None:
                            _tt_Desv = "COMPROBACION"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['comprobacion'])
                            self.varNum = 1
                            self.activar_botones()
                        else:
                            _tt_Desv = "EVIDENCIA"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.EXP_btnScreamEvidencia.configure(state="normal")
                            self.EXP_btnCopyALL.configure(state="normal")
                            self.varNum = 5
                            self.descativar_botones()
        elif self.varNum == 5:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['comprobacion']
                        if self._txt_Desv is None:
                            _tt_Desv = "BACKUP"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['copia'])
                            self.varNum = 2
                            self.descativar_botones()
                        else:
                            _tt_Desv = "COMPROBACION"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.varNum = 1
                            self.activar_botones()
        self.Expan_color_lineas()

    def activar_botones(self):
        if self.st_btnDIR:
            self.EXP_btn_VentanasDIR.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnAUTH:
            self.EXP_btn_VentanasAUTH.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnSER:
            self.EXP_btn_VentanasSER.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnACC:
            self.EXP_btn_VentanasACC.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnCMD:
            self.EXP_btn_VentanasCMD.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnIDR:
            self.EXP_btn_VentanasIDR.grid(row=0, column=3, pady=5, sticky='ne')

    def _anterior(self):
        global _tt_Desv
        self.EXP_btnScreamEvidencia.configure(state="disabled")
        self.EXP_btnCopyALL.configure(state="disabled")
        if self.varNum == 1:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['evidencia']
                        if self._txt_Desv is None:
                            _tt_Desv = "REFRESCAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['refrescar'])
                            self.EXP_btnCopyALL.configure(state="normal")                        
                            self.varNum = 4
                            self.descativar_botones()
                        else:
                            _tt_Desv = "EVIDENCIA"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.EXP_btnScreamEvidencia.configure(state="normal")
                            self.EXP_btnCopyALL.configure(state="normal")
                            self.varNum = 5
                            self.descativar_botones()
        elif self.varNum == 2:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['comprobacion']
                        if self._txt_Desv is None:
                            _tt_Desv = "EVIDENCIA"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['evidencia'])
                            self.EXP_btnScreamEvidencia.configure(state="normal")
                            self.EXP_btnCopyALL.configure(state="normal")
                            self.varNum = 5
                            self.descativar_botones()
                        else:
                            _tt_Desv = "COMPROBACION"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.varNum = 1
                            self.activar_botones()
        elif self.varNum == 3:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['copia']
                        if self._txt_Desv is None:
                            _tt_Desv = "COMPROBACION"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['evidencia'])
                            self.varNum = 1
                            self.activar_botones()
                        else:
                            _tt_Desv = "BACKUP"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.varNum = 2
                            self.descativar_botones()
        elif self.varNum == 4:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['editar']
                        if self._txt_Desv is None:
                            _tt_Desv = "BACKUP"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['copia'])
                            self.varNum = 2
                            self.descativar_botones()
                        else:
                            _tt_Desv = "EDITAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.varNum = 3
                            self.descativar_botones()
        elif self.varNum == 5:
            with open(path_modulo.format(asigne_Ciente)) as g:
                data = json.load(g)
                for md in data:
                    if value in md['modulo']:
                        self._txt_Desv = md['refrescar']
                        if self._txt_Desv is None:
                            _tt_Desv = "EDITAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,md['editar'])
                            self.varNum = 2
                            self.descativar_botones()
                        else:
                            _tt_Desv = "REFRESCAR"
                            self.EXP_lblWidget['text'] =  _tt_Desv
                            self.EXP_srcExpandir.delete('1.0',END)
                            self.EXP_srcExpandir.insert(END,self._txt_Desv)
                            self.EXP_btnCopyALL.configure(state="normal")                        
                            self.varNum = 1
                            self.activar_botones()
        self.Expan_color_lineas()

    def widgets_EXPANDIR(self):
        self.EXP_lblWidget = ttk.Label(
            self.vtn_expandir, 
            text=self.titulo,
            foreground='blue',
            font=('Source Sans Pro', 16, font.BOLD),
        )
        self.EXP_lblWidget.grid(row=0, column=0, padx=5, pady=5,sticky='w')
        self.EXP_srcExpandir = st.ScrolledText(
            self.vtn_expandir,
        )
        self.EXP_srcExpandir.config(
            font=('IBM Plex Sans', 15), 
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=3,
            insertbackground='#297F87',
            selectbackground='lightblue',
        )
        ## Inserta el TEXT DEL SRC RECIBIO
        self.EXP_srcExpandir.insert('1.0',self.txt_Expan)
        ## -------------------------------
        self.EXP_btn_VentanasDIR = ttk.Button(
            self.vtn_expandir,
            text='Permissions',
            compound='left',
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_DIRECTORY,
            style='DESV.TButton',
            state="normal"
        )
        self.EXP_btn_VentanasAUTH = ttk.Button(
            self.vtn_expandir,
            text='Authorized',
            compound='left',
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_AUTHORIZED,
            style='DESV.TButton',
            state="normal"
        )
        self.EXP_btn_VentanasSER = ttk.Button(
            self.vtn_expandir,
            text='Service',
            compound='left',
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_SERVICE,
            style='DESV.TButton',
            state="normal"
        )
        self.EXP_btn_VentanasACC = ttk.Button(
            self.vtn_expandir,
            text='Account',
            compound='left',
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_ACCOUNT,
            style='DESV.TButton',
            state="normal"
        )
        self.EXP_btn_VentanasCMD = ttk.Button(
            self.vtn_expandir,
            text='Command',
            compound='left',
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_COMMAND,
            style='DESV.TButton',
            state="normal"
        )
        self.EXP_btn_VentanasIDR = ttk.Button(
            self.vtn_expandir,
            text='Id_Rsa',
            compound='left',
            image=desviacion.Expandir_icon1,            
            command=desviacion.abrir_IDRSA,
            style='DESV.TButton',
            state="normal"
        )
        self.EXP_btn_Siguiente = tk.Button(
            self.vtn_expandir,
            text='SIGUIENTE',
            image=self.next_icon,            
            command=self._siguiente,
            border=0,
            borderwidth=0,
            highlightthickness=0,
            background='#f1ecc3',
            relief="flat",
            highlightbackground='#f1ecc3',
            activebackground='#f1ecc3',
        )
        self.EXP_btn_Siguiente.grid(row=0, column=2, pady=5, padx=10, sticky='ns')
        
        self.EXP_btn_Anterior = tk.Button(
            self.vtn_expandir,
            text='ANTERIOR',
            image=self.previous_icon,            
            command=self._anterior,
            border=0,
            borderwidth=0,
            highlightthickness=0,
            background='#f1ecc3',
            relief="flat",
            highlightbackground='#f1ecc3', 
            activebackground='#f1ecc3',
        )
        self.EXP_btn_Anterior.grid(row=0, column=1, pady=5, sticky='ns')
        if self.st_btnDIR and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasDIR.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnAUTH and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasAUTH.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnSER and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasSER.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnACC and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasACC.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnCMD and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasCMD.grid(row=0, column=3, pady=5, sticky='ne')
        elif self.st_btnIDR and self.titulo == "COMPROBACION" and self.varNum == 1:
            self.EXP_btn_VentanasIDR.grid(row=0, column=3, pady=5, sticky='ne')
        else:
            self.descativar_botones()     
        
        self.EXP_btnCopyALL = ttk.Button(
            self.vtn_expandir,
            image=desviacion.CopyALL1_icon,
            command=lambda e=self.EXP_srcExpandir : self.copiarALL(e),
            style='DESV.TButton',
            state="disabled"
        )
        self.EXP_btnCopyALL.grid(row=0, column=4, padx=20, pady=5, sticky='ne')
        self.EXP_btnScreamEvidencia = ttk.Button(
            self.vtn_expandir,
            image=desviacion.Captura1_icon,
            command=desviacion.ScreamEvidencia,
            style='DESV.TButton',
            state="disabled",
        )
        self.EXP_btnScreamEvidencia.grid(row=0, column=5, pady=5, sticky='ne')
        self.EXP_btnReducir = ttk.Button(
            self.vtn_expandir,
            image=desviacion.Reducir_icon,
            command=self.cerrar_vtn_expandir,
            style='DESV.TButton',
        )
        self.EXP_btnReducir.grid(row=0, column=6, padx=20, pady=5, sticky='ne')
        self.EXP_srcExpandir.grid(row=1, column=0, padx=5, pady=5, sticky='nsew', columnspan=7)

    def descativar_botones(self):
        self.EXP_btn_VentanasDIR.grid_forget()     
        self.EXP_btn_VentanasAUTH.grid_forget()     
        self.EXP_btn_VentanasSER.grid_forget()     
        self.EXP_btn_VentanasACC.grid_forget()     
        self.EXP_btn_VentanasCMD.grid_forget()     
        self.EXP_btn_VentanasIDR.grid_forget()

    def Expan_color_lineas(self):
        indx = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx = self.EXP_srcExpandir.search(line1, indx, nocase=1, stopindex=tk.END)
                if not indx: 
                    break
                lastidx = '%s+%dc' % (indx, len(line1))
                self.EXP_srcExpandir.tag_add('found1', indx, lastidx)
                indx = lastidx
                self.EXP_srcExpandir.tag_config(
                'found1', 
                foreground='#396eb0',
                font=("Consolas", 14, font.BOLD)
                )

class Desviacion(ttk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        ttk.Frame.__init__(self, parent,*args)
        self.parent = parent
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)

        # FUENTE PARA DESVIACIONES
        # Fuente Menu click derecho 
        self._font_MC_DESV = font.Font(family='Courier', size=14)
        # ----------------------------------------------------------
        # Fuente para TXT de DESV
        self._font_TXT_DESV = font.Font(family='IBM Plex Sans', size=13)
        # -----------------------------------------------------------

        self.iconos()
        self.widgets_DESVIACION()
        self._menu_clickDerecho()
        ## --- SELECCIONAR ELEMENTO DEL LISTBOX. --- #
        self.DESVfr1_listbox.bind("<<ListboxSelect>>",lambda e :self.seleccionar_Modulo(e))
        ## --- ADJUTAR EL TEXT DE LOS LABEL --- #
        self.DESVfr2_lblModulo.bind("<Configure>", self.label_resize)
        self.DESVfr2_lblDescripcion.bind("<Configure>", self.label_resize)
        ## --- ACTIVAR WIDGET. --- #
        self.DESVfr2_lblModulo.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESV_frame2.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr2_lblDescripcion.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr2_srcComprobacion.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr2_srcBackup.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcEditar.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcRefrescar.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr3_srcEvidencia.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr1_entModulo.bind("<Motion>",lambda e:self._act_focus_ent(e))
        app.cuaderno.bind("<Motion>",lambda e:self.activar_Focus(e))
        self.DESVfr1_listbox.bind("<Motion>",lambda e:self._activar_Focus(e))
        ## --- MOSTRAR MENU DERECHO  --- ##
        #app.root.bind("<Button-3><ButtonRelease-3>", app.display_menu_clickDerecho)
        self.DESVfr2_srcComprobacion.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr2_srcBackup.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr3_srcEditar.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr3_srcRefrescar.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr3_srcEvidencia.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        self.DESVfr1_entModulo.bind("<Button-3><ButtonRelease-3>",self._display_menu_clickDerecho)
        ## --- ACTIVAR MODO SOLO LECTURA --- ##
        self.DESVfr2_srcComprobacion.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr2_srcBackup.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcEditar.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcRefrescar.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        self.DESVfr3_srcEvidencia.bind("<Key>", lambda e: self.widgets_SoloLectura(e))
        ## --- SELECCIONAR TOD --- ##
        self.DESVfr2_srcComprobacion.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr2_srcBackup.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr3_srcEditar.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr3_srcRefrescar.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        self.DESVfr3_srcEvidencia.bind('<Control-a>', lambda e: self._seleccionar_todo(e))
        ## --- BUSCAR --- ##
        #self.DESVfr1_entModulo.bind("<Any-KeyRelease>", lambda event=None: self.buscar_Modulos(self.DESVfr1_entModulo.get()))
        self.DESVfr1_entModulo.bind("<Return>", lambda event=None: self.buscar_Modulos(self.DESVfr1_entModulo.get()))
        self.DESVfr1_entModulo.bind("<FocusIn>", lambda e: self.clear_busqueda(e))
        self.DESVfr1_entModulo.bind("<FocusOut>", lambda e: self.clear_busqueda(e))
        self.DESVfr1_entModulo.bind("<KeyPress>", lambda e: self.clear_bsq_buttom(e))
        self.DESVfr2_srcComprobacion.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr2_srcBackup.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr3_srcEditar.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr3_srcRefrescar.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr3_srcEvidencia.bind('<Control-f>', lambda e : self.buscar(e))
        self.DESVfr1_listbox.bind('<Control-f>', lambda e : self.buscar(e))
        
        self.DESVfr2_srcComprobacion.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr2_srcBackup.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr3_srcEditar.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr3_srcRefrescar.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr3_srcEvidencia.bind('<Control-F>', lambda e : self.buscar(e))
        self.DESVfr1_listbox.bind('<Control-F>', lambda e : self.buscar(e))
        
        self.DESVfr1_entModulo.bind('<Control-F>', lambda e : self._buscar_focus(e))
        self.DESVfr1_entModulo.bind('<Button-1>', lambda e : self._buscar_focus(e))
        self.DESVfr1_entModulo.bind('<Control-f>', lambda e : self._buscar_focus(e))
        
        self.DESVfr1_listbox.bind("<Down>",lambda e : self.ListDown(e))
        self.DESVfr1_listbox.bind("<Up>",lambda e : self.ListUp(e))
        
        self.DESVfr1_entModulo.bind('<Control-v>', lambda e : self.sel_text(e))
        self.DESVfr1_entModulo.bind('<Control-V>', lambda e : self.sel_text(e))
        
        self.DESVfr2_srcComprobacion.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr2_srcBackup.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr3_srcEditar.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr3_srcRefrescar.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr3_srcEvidencia.bind('<Control-c>', lambda e : self._copiar_texto_seleccionado(e))
        self.DESVfr1_entModulo.bind('<Control-x>', lambda e : self._clear_busqueda(e))        
        ## --- --- ##
        self._btnDir = False
        self._btnAuth = False
        self._btnSer = False
        self._btnAcc = False
        self._btnCmd = False
        self._btnIdr = False
    
    def iconos(self): #TODO ICONOS DE VENTANA DESVIACION
        self.BuscarModulo_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"buscar.png").resize((25, 25)))
        self.LimpiarModulo_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"limpiar.png").resize((25, 25)))
        self.Expandir_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"expandir.png").resize((20, 20)))
        self.Expandir_icon1 = ImageTk.PhotoImage(
                    Image.open(path_icon+r"expandir.png").resize((30, 30)))
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
        if(20==event.state and event.keysym=='c' or event.keysym=='Down' or event.keysym=='Up' or 20==event.state and event.keysym=='f' or 20==event.state and event.keysym=='a'):
            return
        else:
            return "break"
    ## --- ACTIVAR WIDGET ---------------------------------------- ##
    def _act_focus_ent(self, event):
        self.txtWidget = event.widget
        self.txtWidget.select_range(0,tk.END)
        self.txtWidget.focus_set()
        return 'break'

    def activar_Focus(self, event):
        global txtWidget
        global srcDes
        global srcCom
        global srcBac
        global srcEdi
        global srcRes
        global srcEvi
        global srcMod
        global srcSO
        global txtWidget_focus
        txtWidget = event.widget
        if txtWidget == self.DESVfr1_entModulo:
            txtWidget.focus()
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr2_srcComprobacion:
            srcCom = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr2_srcBackup:
            srcBac = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
        elif txtWidget == self.DESVfr3_srcEditar:
            srcEdi = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEvidencia.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr3_srcRefrescar:
            srcRes = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
        elif txtWidget == self.DESVfr3_srcEvidencia:
            srcEvi = txtWidget
            txtWidget.focus()
            txtWidget_focus = True
            self.DESVfr2_srcComprobacion.tag_remove("sel","1.0","end")
            self.DESVfr2_srcBackup.tag_remove("sel","1.0","end")
            self.DESVfr3_srcEditar.tag_remove("sel","1.0","end")
            self.DESVfr3_srcRefrescar.tag_remove("sel","1.0","end")
        elif txtWidget == self.DESVfr2_lblDescripcion:
            srcDes = txtWidget
        elif txtWidget == self.DESVfr2_lblModulo:
            srcMod = txtWidget
        elif txtWidget == self.DESV_frame2:
            srcSO = txtWidget

    def _activar_Focus(self, event):
        global list_motion
        list_motion = event.widget
        list_motion.focus()
    
    def disabled_copy(self, txt_select):
        if txt_select:
            app.menu_Contextual.entryconfig('  Copiar', state='normal')
        else:
            app.menu_Contextual.entryconfig('  Copiar', state='disabled')
    ## ------ VENTANAS TOP EXPANDIR ------------------------------ ##
    def expandir(self, event, var): #TODO comprobando expandir
        global expandir
        global sis_oper
        global asigne_Ciente
        global varNum
        global text_aExpandir
        self.widget_Expan = event
        tittleExpand = var
        
        self.widget_Expan.focus()
        text_aExpandir = self.widget_Expan.get('1.0', tk.END)
        if tittleExpand == "COMPROBACION":
            varNum= 1
        elif tittleExpand == "BACKUP":
            varNum= 2
        elif tittleExpand == "EDITAR":
            varNum= 3            
        elif tittleExpand == "REFRESCAR":
            varNum= 4
        elif tittleExpand == "EVIDENCIA":        
            varNum= 5
        expandir = Expandir(self, text_aExpandir, self.widget_Expan, asigne_Ciente,tittleExpand, sis_oper, self._btnDir, self._btnAuth, self._btnSer, self._btnAcc, self._btnCmd, self._btnIdr, varNum)         
        if tittleExpand == "REFRESCAR":
            expandir.EXP_btnCopyALL.configure(state="normal")            
        elif tittleExpand == "EVIDENCIA":        
            varNum= 5
            expandir.EXP_btnScreamEvidencia.configure(state="normal")
            expandir.EXP_btnCopyALL.configure(state="normal")
    # ## --- MENU CONTEXTUAL --- ##    
    def _menu_clickDerecho(self):   
        self.menu_Contextual = Menu(self, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar", 
            accelerator='Ctrl+F',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_DESV,
            command=lambda e=self.DESVfr1_entModulo:self._buscar(e),
            state='disabled',
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_DESV,
            command=self.copiar_texto_seleccionado,
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_DESV,
            command=lambda e=self.DESVfr1_entModulo:self.pegar_texto_seleccionado(e),
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_DESV,
            command=lambda : self.seleccionar_todo(event=None),
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_DESV,
            command=lambda e=None:self._clear_busqueda(e),
            state='disabled',
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña", 
            compound=LEFT,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_DESV,
            command=app.cerrar_vtn_desviacion
        )
    
    def _display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
        self.scrEvent = event.widget
        self.scrEvent.focus()
        if str(self.scrEvent) == str(self.DESVfr1_entModulo):
            self.menu_Contextual.entryconfig('  Buscar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='normal')            
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
            if len(self.DESVfr1_entModulo.get()) > 0:
                self.menu_Contextual.entryconfig('  Limpiar', state='normal')
            else:
                self.menu_Contextual.entryconfig('  Limpiar', state='disabled')
        else:
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Buscar', state='normal')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='normal')
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')
            self.menu_Contextual.entryconfig('  Limpiar', state='disabled')       
            txt_select = event.widget.tag_ranges(tk.SEL)
            if txt_select:
                self.menu_Contextual.entryconfig("  Copiar", state="normal")
            else:
                self.menu_Contextual.entryconfig("  Copiar", state="disabled")
    ## --- FUNCIONES DEL MENU CONTEXTUAL --- ##
    def seleccionar_todo(self, event):
        if txtWidget_focus:
            txtWidget.tag_add("sel","1.0","end")
            return 'break'
    
    def _seleccionar_todo(self, event):
        scr_Event = event.widget
        scr_Event.tag_add("sel","1.0","end")
        return 'break'
    
    def sel_text(self, event):
        if event.widget.select_present():
            self.var_entry_bsc.set("")
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
    
    def pegar_texto_seleccionado(self, event):
        entModulo_event = event
        if entModulo_event.select_present():
            self.var_entry_bsc.set("")
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
        entModulo_event.event_generate("<<Paste>>")
    
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
    
    def _copiar_texto_seleccionado(self, event):
        scrText = event.widget
        seleccion = scrText.tag_ranges(tk.SEL)
        if seleccion:
            app.root.clipboard_clear()
            app.root.clipboard_append(scrText.get(*seleccion).strip())
            scrText.tag_remove("sel","1.0","end")
            return 'break'
        else:
            pass
    
    def buscar(self, event):
        self.DESVfr1_entModulo.focus()
        self._buscar_Ativate_focus()
    
    def _buscar_focus(self, event):
        entry_event = event.widget
        entry_event.select_range(0,tk.END)
        entry_event.focus_set()
        return 'break'

    def _buscar_Ativate_focus(self):
        self.DESVfr1_entModulo.select_range(0,tk.END)
        self.DESVfr1_entModulo.focus_set()
        return 'break'

    def _buscar(self, event):
        self._buscar_Ativate_focus()
    ## ------------------------------------- ##
    ## --- FUNCIONES AL SELECIONAR MODULO, O BUSCAR MODULO ------- ##
    def limpiar_Widgets(self):
        self.DESV_frame2['text'] = 'SISTEMA OPERATIVO'
        self.DESVfr2_lblModulo['text'] = 'MODULO'
        self.DESVfr2_lblDescripcion['text'] = ''
        self.DESVfr2_srcComprobacion.delete('1.0',END)
        self.DESVfr2_srcBackup.delete('1.0',END)
        self.DESVfr3_srcEditar.delete('1.0',END)
        self.DESVfr3_srcRefrescar.delete('1.0',END)
        self.DESVfr3_srcEvidencia.delete('1.0',END)
    
    def seleccionar_Modulo(self, event):
        global value
        list_event = event.widget
        index = list_event.curselection()
        value = list_event.get(index[0])
        self.cargar_elemt_selected(value)
    
    def cargar_elemt_selected(self, modulo_selecionado): #TODO CARGAR MODULO
        with open(path_modulo.format(asigne_Ciente)) as g:
            data = json.load(g)
            for md in data:
                if modulo_selecionado in md['modulo']:
                    ## --- LIMPIAR ------------------------------------- ##                      
                    self.limpiar_Widgets()
                    ## ------------------------------------------------- ##
                    self.asignarValor_aWidgets(md)
            self.mostrar_buttons_modulo(modulo_selecionado)
    
    def asignarValor_aWidgets(self, md):
        global sis_oper
        if md['SO'] is not None:
            sis_oper = md['SO']
            self.DESV_frame2['text'] = md['SO']
        if md['modulo'] is not None:
            self.DESVfr2_lblModulo['text'] = md['modulo']
        if md['descripcion'] is not None:
            self.DESVfr2_lblDescripcion['text'] = md['descripcion']

        if md['comprobacion'] is not None:
            self.DESVfr2_srcComprobacion.insert(END,md['comprobacion'])
            self.DESV_btn1Expandir.configure(state='normal')
        else:
            self.DESV_btn1Expandir.configure(state='disabled')

        if md['copia'] is not None:
            self.DESVfr2_srcBackup.insert(END,md['copia'])
            self.DESV_btn2Expandir.configure(state='normal')
        else:
            self.DESV_btn2Expandir.configure(state='disabled')

        if md['editar'] is not None:
            self.DESVfr3_srcEditar.insert(END,md['editar'])
            self.DESV_btn3Expandir.configure(state='normal')
        else:
            self.DESV_btn3Expandir.configure(state='disabled')

        if md['refrescar'] is not None:
            self.DESV_btn4Expandir.configure(state='normal')
            self.DESVfr3_srcRefrescar.insert(END,md['refrescar'])
        else:
            self.DESV_btn4Expandir.configure(state='disabled')

        if md['evidencia'] is not None:
            self.DESVfr3_srcEvidencia.insert(END,md['evidencia'])
            self.DESV_btn5Expandir.configure(state='normal')
        else:
            self.DESV_btn5Expandir.configure(state='disabled')
        
        self.colour_line_com()
        self.colour_line_bak()
        self.colour_line_edi()
        self.colour_line_ref()
        self.colour_line_evi()
    
    def mostrar_buttons_modulo(self, modulo_selecionado): #TODO añadir demas botones
        #DIRECTORY
        if str(modulo_selecionado) == "Protecting Resources-mixed/Ensure sticky bit is set on all world-writable directories" or str(modulo_selecionado) == "Protecting Resources-OSRs/CRON Command WW Permissions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /TMP Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /VAR Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /OPT Files Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /ETC Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/OSR /USR Restrictions" or str(modulo_selecionado) == "Protecting Resources-OSRs/CRON Command Group Permissions":
            self._btnDir = True
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnDirectory.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnIdrsa.grid_forget()
        #AUTHORIZED
        elif str(modulo_selecionado) == "Password Requirements/Private Key File Restriction" or str(modulo_selecionado) == "Identify and Authenticate Users/Public Key Authentication" or str(modulo_selecionado) == "AV.1.1.6 Password Requirements" or str(modulo_selecionado) == "Identify and Authenticate Users/Public Key Label" or str(modulo_selecionado) == "AV.1.1.7 Password Requirements":
            self._btnDir = False
            self._btnAuth = True
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnIdrsa.grid_forget()
            self.DESV_btnAuthorized.grid(row=2, column=1, padx=5, pady=5, sticky='ne')    
        #SERVICE
        elif str(modulo_selecionado) == "Network Settings/Ensure LDAP Server is not enabled" or str(modulo_selecionado) == "Network Settings/NFS root restrictions" or str(modulo_selecionado) == "E.1.5.22.3 Network Settings" or str(modulo_selecionado) == "Password Requirements/SSH PermitRootLogin Restriction" or str(modulo_selecionado) == "Network Settings/Prohibited Processes" or str(modulo_selecionado) == "Identify and Authenticate Users/PermitRootLogin Restriction" or str(modulo_selecionado) == "Network Settings/Disable NFS server":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = True
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnIdrsa.grid_forget()
            self.DESV_btnService.grid(row=2, column=1, padx=5, pady=5, sticky='ne')    
        #ACCOUNT
        elif str(modulo_selecionado) == "Password Requirements/Password MAX Age /etc/shadow" or str(modulo_selecionado) == "Password Requirements/Password MAX Age":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = True
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnIdrsa.grid_forget()
            self.DESV_btnAccount.grid(row=2, column=1, padx=5, pady=5, sticky='ne')  
        #COMMAND
        elif str(modulo_selecionado) == "protecting Resources-OSRs/SUDO Command WW Permissions":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = True
            self._btnIdr = False
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnIdrsa.grid_forget()
            self.DESV_btnCommand.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
        #ID RSA
        elif str(modulo_selecionado) == "Password Requirements/NULL Passphrase" or str(modulo_selecionado) == "Password Requirements/Private Key Passphrase":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = True
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnIdrsa.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
        else:
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnIdrsa.grid_forget() 
    
    def mostrar_buttons_clave(self, clave_Buscado):
        if clave_Buscado == "STICKY" or clave_Buscado =="OSRsCRON" or clave_Buscado == "OSRTMP" or clave_Buscado == "OSRCRON" or clave_Buscado == "OSRVAR" or clave_Buscado == "OSROPT" or clave_Buscado == "OSRETC" or clave_Buscado == "OSRUSR":
            self._btnDir = True
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnDirectory.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnCommand.grid_forget() 
            self.DESV_btnIdrsa.grid_forget()
        elif clave_Buscado == "COMMAND":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = True
            self._btnIdr = False
            self.DESV_btnCommand.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnIdrsa.grid_forget()
        elif clave_Buscado == "IDRSA" or clave_Buscado == "NOT PASSPHRASE":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = True
            self.DESV_btnIdrsa.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnDirectory.grid_forget()
        elif clave_Buscado == "PERMITROOTLOGIN" or clave_Buscado == "LDAP" or clave_Buscado == "PROCESSES" or clave_Buscado == "NFS":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = True
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnIdrsa.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid(row=2, column=1, padx=5, pady=5, sticky='ne')
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnDirectory.grid_forget()
        elif clave_Buscado == "AUTHORIZED_KEY" or clave_Buscado == "PUBLICKEY" or clave_Buscado == "LABEL":
            self._btnDir = False
            self._btnAuth = True
            self._btnSer = False
            self._btnAcc = False
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnAccount.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnIdrsa.grid_forget()
            self.DESV_btnAuthorized.grid(row=2, column=1, padx=5, pady=5, sticky='ne')    
        elif clave_Buscado == "MAXAGE":
            self._btnDir = False
            self._btnAuth = False
            self._btnSer = False
            self._btnAcc = True
            self._btnCmd = False
            self._btnIdr = False
            self.DESV_btnDirectory.grid_forget()
            self.DESV_btnAuthorized.grid_forget()
            self.DESV_btnService.grid_forget()
            self.DESV_btnCommand.grid_forget()
            self.DESV_btnIdrsa.grid_forget()
            self.DESV_btnAccount.grid(row=2, column=1, padx=5, pady=5, sticky='ne')  
        else:
            self._disabled_buttons()   
    
    def buscar_Modulos(self, event=None):
        global value
        try:
            valor_aBuscar = event
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
            # ## --------- OBTENER MODULO POR CLAVE O MODULO -------------- ## //TODO "definir si buscar por clave o modulo"
            if len(clave_Buscado) == 0 and len(modulo_Buscado) == 0:
                self.limpiar_Widgets()
                self.DESVfr1_listbox.select_clear(ANCHOR)
                mb.showerror("ERROR","Esta vacio o no existe el modulo.\nPrueba a buscar por CLAVE o el MODULO completo")
                self.DESVfr1_entModulo.focus()
                self._disabled_buttons()
            elif len(clave_Buscado) != 0:
                with open(path_modulo.format(asigne_Ciente)) as g:
                    data = []
                    data = json.load(g)
                    for md in data:
                        if clave_Buscado in md['clave']:
                            modulo_Encontrado = md['modulo']
                            value = modulo_Encontrado
                            ## --- LIMPIAR ------------------------------------- ##                      
                            self.limpiar_Widgets()
                            ## ------------------------------------------------- ##
                            self.asignarValor_aWidgets(md)
                    self.mostrar_buttons_clave(clave_Buscado)
                    self.DESVfr1_listbox.selection_clear(0, tk.END)        
                    modulo_ListBox = self.DESVfr1_listbox.get(0, tk.END)
                    indice = modulo_ListBox.index(modulo_Encontrado)
                    self.DESVfr1_listbox.selection_set(indice)
            else:
                data = []
                with open(path_modulo.format(asigne_Ciente)) as g:
                    data = json.load(g)
                    for md in data:
                        if modulo_Buscado in md['modulo']:
                            modulo_Encontrado = md['modulo']
                            value = modulo_Encontrado
                            ## --- LIMPIAR ------------------------------------- ##                      
                            self.limpiar_Widgets()
                            ## ------------------------------------------------- ##
                            self.asignarValor_aWidgets(md)
                    self.mostrar_buttons_modulo(modulo_Buscado)
                    self.DESVfr1_listbox.selection_clear(0, tk.END)
                    modulo_ListBox = self.DESVfr1_listbox.get(0, tk.END)
                    indice = modulo_ListBox.index(modulo_Encontrado)
                    self.DESVfr1_listbox.selection_set(indice)
            self.DESVfr1_btnBuscar.grid_forget()
            self.DESVfr1_btnLimpiar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')    
        except:
            self.DESVfr1_listbox.select_clear(ANCHOR)
            mb.showerror("ERROR","Esta vacio o no existe el modulo.\nPrueba a buscar por CLAVE o el MODULO completo")
            self.limpiar_Widgets()
            self.DESVfr1_entModulo.focus()
            self._disabled_buttons()
    
    def clear_busqueda(self, event):
        text_widget = event.widget
        entry = self.var_entry_bsc.get()
        if entry == "Buscar modulo...":
            text_widget.config(foreground="black", font=("IBM Plex Sans Arabic", 12))
            self.var_entry_bsc.set("")
            text_widget.icursor(0)
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
        elif entry == "":
            text_widget.config(foreground="gray75", font=("IBM Plex Sans Arabic", 12))
            self.var_entry_bsc.set("Buscar modulo...")
            text_widget.icursor(0)
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
        text_widget.select_clear()

    def _clear_busqueda(self, event):
        self.var_entry_bsc.set("")
        self.DESVfr1_btnLimpiar.grid_forget()
        self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
    
    def clear_bsq_buttom(self, event):
        entry = self.var_entry_bsc.get()
        long_entry = len(entry)
        if long_entry <=1:
            self.DESVfr1_btnLimpiar.grid_forget()
            self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
    
    def limpiar_busqueda(self):
        widget_event = self.DESVfr1_entModulo
        self.var_entry_bsc.set("Buscar modulo...")
        widget_event.focus()
        widget_event.icursor(0)
        self.DESVfr1_btnLimpiar.grid_forget()
        self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
    
    def ListDown(self, event):
        list_event = event.widget
        list_event.yview_scroll(1,"units")
        selecion = list_event.curselection()[0]+1
        modulo_selecionado = list_event.get(selecion)
        self.cargar_elemt_selected(modulo_selecionado)
    
    def ListUp(self, event):
        list_event = event.widget
        list_event.yview_scroll(-1,"units")
        selecion = list_event.curselection()[0]-1
        modulo_selecionado = list_event.get(selecion)
        self.cargar_elemt_selected(modulo_selecionado)
    
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
        self.DESV_btn1CopyALL.config(state='normal')
        self.DESV_btnDirectory.config(state='normal')
    
    def cargar_Modulos(self, clt_modulo=None, *args):
        self.enabled_Widgets()
        global asigne_Ciente
        global listModulo
        global listClave
        if clt_modulo is not None:
            customer = clt_modulo
            self.clientesVar.set(customer)
        else:
            customer = self.clientesVar.get()
        ## --- LIMPIAR -----------------------------
        self.DESVfr1_listbox.delete(0,END)
        self.limpiar_Widgets()
        self._disabled_buttons() 
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
        self.var_entry_bsc.set("Buscar modulo...")
        self.DESVfr1_listbox.insert(END,*listModulo)
        self.cambiar_NamePestaña(customer)

    def colour_line_com(self):
        indx = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx = self.DESVfr2_srcComprobacion.search(line1, indx, nocase=1, stopindex=tk.END)
                if not indx: #or not indx1 or not indx2 or not indx3 or not indx4: 
                    break
                lastidx = '%s+%dc' % (indx, len(line1))
                self.DESVfr2_srcComprobacion.tag_add('found1', indx, lastidx)
                indx = lastidx
                self.DESVfr2_srcComprobacion.tag_config(
                'found1', 
                foreground='#396eb0',
                font=("Consolas", 13)
                )
    
    def colour_line_bak(self):
        indx1 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx1 = self.DESVfr2_srcBackup.search(line1, indx1, nocase=1, stopindex=tk.END)
                if not indx1: #or not indx2 or not indx3 or not indx4: 
                    break
                lastidx1 = '%s+%dc' % (indx1, len(line1))
                self.DESVfr2_srcBackup.tag_add('found1', indx1, lastidx1)
                indx1 = lastidx1
                self.DESVfr2_srcBackup.tag_config(
                'found1', 
                foreground='#396eb0',
                font=("Consolas", 13)
                )
    
    def colour_line_ref(self):
        indx3 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx3 = self.DESVfr3_srcRefrescar.search(line1, indx3, nocase=1, stopindex=tk.END)
                if not indx3: #or not indx4: 
                    break
                lastidx3 = '%s+%dc' % (indx3, len(line1))
                self.DESVfr3_srcRefrescar.tag_add('found1', indx3, lastidx3)
                indx3 = lastidx3
                self.DESVfr3_srcRefrescar.tag_config(
                'found1', 
                foreground='#396eb0',
                font=("Consolas", 13)
                )

    def colour_line_edi(self):
        indx2 = '1.0'
        # indx4 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx2 = self.DESVfr3_srcEditar.search(line1, indx2, nocase=1, stopindex=tk.END)
                if not indx2: 
                    break
                lastidx2 = '%s+%dc' % (indx2, len(line1))
                self.DESVfr3_srcEditar.tag_add('found1', indx2, lastidx2)
                indx2 = lastidx2
                self.DESVfr3_srcEditar.tag_config(
                'found1', 
                foreground='#396eb0',
                font=("Consolas", 13)
                )

    def colour_line_evi(self):
        indx4 = '1.0'
        line1 = "+-------------------------------------------------------------------------------------+"
        if line1:
            while True:
                indx4 = self.DESVfr3_srcEvidencia.search(line1, indx4, nocase=1, stopindex=tk.END)
                if not indx4: 
                    break
                lastidx4 = '%s+%dc' % (indx4, len(line1))
                self.DESVfr3_srcEvidencia.tag_add('found1', indx4, lastidx4)
                indx4 = lastidx4
                self.DESVfr3_srcEvidencia.tag_config(
                'found1', 
                foreground='#396eb0',
                font=("Consolas", 13)
                )

    def _disabled_buttons(self):
        self._btnDir = False
        self._btnAuth = False
        self._btnSer = False
        self._btnAcc = False
        self._btnCmd = False
        self._btnIdr = False
        self.DESV_btnDirectory.grid_forget()
        self.DESV_btnAuthorized.grid_forget()
        self.DESV_btnService.grid_forget()
        self.DESV_btnAccount.grid_forget()
        self.DESV_btnCommand.grid_forget()
        self.DESV_btnIdrsa.grid_forget()
    
    def _cargar_Modulos(self):
        idx = app.ClientVar.get()
        itm = list_client[idx]
        self.cargar_Modulos(clt_modulo=itm)
    
    def ScreamEvidencia(self):
        global expandir
        app.root.withdraw()
        #expandir.transient(app)
        subprocess.call(["./scream.sh"])
        time.sleep(3)
        #mb.showinfo("INFO","Informacion")
        app.root.deiconify()
    
    def copiarALL(self, event):
        event.focus()
        if event:
            event.tag_add("sel","1.0","end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                app.root.clipboard_clear()
                app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel","1.0","end")
    
    def widgets_DESVIACION(self):
        # --- DEFINIMOS LOS LABEL FRAMEs, QUE CONTENDRAN LOS WIDGETS --------------------------#
        self.DESV_frame1=ttk.LabelFrame(
            self, 
            text="CLIENTE / MODULO", 
            border=1, 
            relief='sunken'
        )
        self.DESV_frame1.grid_propagate(False)
        self.DESV_frame1.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        self.DESV_frame2=ttk.LabelFrame(
            self, 
            text="SISTEMA OPERATIVO", 
            border=1, 
            relief='sunken'
        )
        self.DESV_frame2.grid_propagate(False)
        self.DESV_frame2.grid(column=1, row=0, padx=10, pady=10, sticky='nsew')
        self.DESV_frame3=ttk.LabelFrame(
            self, 
            text="EDITAR / EVIDENCIA", 
            border=1, 
            relief='sunken'
        )
        self.DESV_frame3.grid_propagate(False)
        self.DESV_frame3.grid(column=2, row=0, padx=10, pady=10, sticky='nsew')
        # -----------------------------------------------------------------------------#
        self.DESV_frame1.columnconfigure(0, weight=1)
        self.DESV_frame2.columnconfigure(0, weight=1)
        self.DESV_frame3.columnconfigure(0, weight=1)
        self.DESV_frame1.rowconfigure(2, weight=1)
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
        self.DESVfr1_optMn = tk.OptionMenu(
            self.DESV_frame1, 
            self.clientesVar, 
            *list_client, 
            command=self.cargar_Modulos,
        )
        self.DESVfr1_optMn.config(
            background = "#5F939A",
            foreground = "#F2EDD7",
            font=('Source Sans Pro',15,font.BOLD),
            activebackground="#3A6351",
            activeforeground="#F6D167",
            relief="groove",
            borderwidth=2,
            width=20
        )
        self.DESVfr1_optMn["menu"].config(
            background='#3A6351',
            selectcolor='red',
            activebackground='#5F939A',
            foreground="#F2EDD7",
            font=('Consolas', 13, font.BOLD),
        )
        self.DESVfr1_optMn.grid(row=0, column=0, padx=5, pady=5, sticky='new', columnspan=2)
        # -----------------------------------------------------------------------------#
        ## --- WIDGETS PARA BUSCAR
        self.var_entry_bsc = tk.StringVar(self)
        self.DESVfr1_entModulo = tk.Entry(
            self.DESV_frame1,
            textvariable=self.var_entry_bsc,
            #width=32
        )
        self.var_entry_bsc.set("Buscar modulo...")
        self.DESVfr1_entModulo.config(
            foreground="gray75",
            font=self._font_TXT_DESV,
            state='disabled',
            border=0,
            borderwidth=0,
            highlightthickness=2,
            highlightcolor='#316B83',
            selectforeground='#CDFFEB', 
            selectbackground='#476072'
        )
        self.DESVfr1_entModulo.grid(row=1, column=0, pady=5, padx=(5,0), sticky='nsew')
        self.DESVfr1_btnBuscar = ttk.Button(
            self.DESV_frame1, 
            image=self.BuscarModulo_icon,
            state='disabled',
            command=lambda: self.buscar_Modulos(self.DESVfr1_entModulo.get()),
            style='DESV.TButton'
        )
        self.DESVfr1_btnBuscar.grid(row=1, column=1, pady=5, padx=5, sticky='nsw')
        self.DESVfr1_btnLimpiar = ttk.Button(
            self.DESV_frame1, 
            image=self.LimpiarModulo_icon,
            command=self.limpiar_busqueda,
            style='DESV.TButton'
        )
        # -----------------------------------------------------------------------------#
        self.DESVlist_yScroll = tk.Scrollbar(self.DESV_frame1, orient=tk.VERTICAL)
        self.DESVlist_xScroll = tk.Scrollbar(self.DESV_frame1, orient=tk.HORIZONTAL)
        self.DESVfr1_listbox = tk.Listbox(
            self.DESV_frame1,
            state='disabled',
            xscrollcommand=self.DESVlist_xScroll.set, 
            yscrollcommand=self.DESVlist_yScroll.set,
            font=self._font_TXT_DESV,
            foreground='blue',
            selectbackground='#297F87',
            selectforeground='#F6D167',
            disabledforeground='black',
            exportselection=False,
            highlightbackground='gray88',
            highlightthickness=2,
            highlightcolor='#297F87',
        )
        self.DESVfr1_listbox.grid(row=2, column=0, pady=(5,15), padx=(5,15), sticky='nsew', columnspan=2)
        self.DESVlist_yScroll.grid(row=2, column=0, pady=(5,15), sticky='nse', columnspan=2)
        self.DESVlist_xScroll.grid(row=2, column=0, padx=5, sticky='sew', columnspan=2)
        self.DESVlist_xScroll['command'] = self.DESVfr1_listbox.xview
        self.DESVlist_yScroll['command'] = self.DESVfr1_listbox.yview
        ## ======================== FRAME 2 ========================================= ##
        ## --- MODULO
        self.DESVfr2_lblModulo = ttk.Label(
            self.DESV_frame2,
            text='MODULO', 
            #width=10,
        )
        self.DESVfr2_lblModulo.grid(row=0, column=0, padx=5, pady=5, sticky='new', columnspan=3)
        ## --- Descripcion
        self.DESVfr2_lblDescripcion = ttk.Label(
            self.DESV_frame2,
            text='',
            font=('Consolas', 12),
            width=10, 
            background='#f1ecc3',
            foreground='gray55'
        ) 
        self.DESVfr2_lblDescripcion.grid(row=1, column=0, padx=5, pady=5, sticky='new', columnspan=3)
        ## --- Comprobacion
        self.DESVfr2_lblComprobacion = ttk.Label(
            self.DESV_frame2, 
            text='COMPROBACIÓN'
        ) 
        self.DESVfr2_lblComprobacion.grid(row=2, column=0, padx=5, pady=5, sticky='w' )
        self.DESV_btnDirectory = ttk.Button(
            self.DESV_frame2,
            text='Permissions',
            compound='left',
            image=self.Expandir_icon,
            state='disabled',
            command=self.abrir_DIRECTORY,
            style='TOPS.TButton'
        )
        self.DESV_btnService = ttk.Button(
            self.DESV_frame2,
            text='Service',
            compound='left',
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_SERVICE,
            style='TOPS.TButton'
        )
        self.DESV_btnAuthorized = ttk.Button(
            self.DESV_frame2,
            text='Authorized',
            compound='left',
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_AUTHORIZED,
            style='TOPS.TButton'
        )
        self.DESV_btnAccount = ttk.Button(
            self.DESV_frame2,
            text='Account',
            compound='left',
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_ACCOUNT,
            style='TOPS.TButton'
        )
        self.DESV_btnCommand = ttk.Button(
            self.DESV_frame2,
            text='Command',
            compound='left',
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_COMMAND,
            style='TOPS.TButton'
        )
        self.DESV_btnIdrsa = ttk.Button(
            self.DESV_frame2,
            text='Id_Rsa',
            compound='left',
            image=self.Expandir_icon,
            state='enabled',
            command=self.abrir_IDRSA,
            style='TOPS.TButton'
        )
        self.DESVfr2_srcComprobacion = st.ScrolledText(self.DESV_frame2)
        self.DESVfr2_srcComprobacion.config(
            font=self._font_TXT_DESV,
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=2,
            insertbackground='#297F87',
            selectbackground='lightblue',
            state='disabled',
        )
        self.DESVfr2_srcComprobacion.grid(row=3, column=0, padx=5, pady=5, sticky='new', columnspan=3)
        self.varComprobacion = "COMPROBACION"
        self.DESV_btn1Expandir = ttk.Button(
            self.DESV_frame2,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr2_srcComprobacion:self.expandir(x, self.varComprobacion),
        )
        self.DESV_btn1Expandir.grid(row=2, column=2, padx=(5,20), pady=5, sticky='ne')
        ## --- BACKUP
        self.DESVfr2_lblBackup = ttk.Label(
            self.DESV_frame2, 
            text='BACKUP', 
            #width=10
        ) 
        self.DESVfr2_lblBackup.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        
        self.DESVfr2_srcBackup = st.ScrolledText(
            self.DESV_frame2,
        )
        self.DESVfr2_srcBackup.config(
            font=self._font_TXT_DESV,
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=2,
            insertbackground='#297F87',
            selectbackground='lightblue',
            state='disabled',
        )
        self.DESVfr2_srcBackup.grid(row=5, column=0, padx=5, pady=5, sticky='new', columnspan=3)
        
        self.varBackup = "BACKUP"
        self.DESV_btn2Expandir = ttk.Button(
            self.DESV_frame2,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr2_srcBackup:self.expandir(x, self.varBackup),
        )
        self.DESV_btn2Expandir.grid(row=4, column=1, padx=(5,20), pady=5, sticky='nse', columnspan=2)
        ## ======================== FRAME 3 ========================================= ##
        ## --- EDITAR
        self.DESVfr3_lblEditar = ttk.Label(
            self.DESV_frame3, 
            text='EDITAR ✍'
        )
        self.DESVfr3_lblEditar.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        
        self.DESVfr3_srcEditar = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcEditar.config(
            font=self._font_TXT_DESV,
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=2,
            insertbackground='#297F87',
            selectbackground='lightblue',
            state='disabled',
        )
        self.DESVfr3_srcEditar.grid(row=1, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        
        self.varEditar = "EDITAR"
        self.DESV_btn3Expandir = ttk.Button(
            self.DESV_frame3,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr3_srcEditar:self.expandir(x, self.varEditar),
        )
        self.DESV_btn3Expandir.grid(row=0, column=1, padx=(5,20), pady=5, sticky='nse', columnspan=3)
        ## --- REFEESCAR
        self.DESVfr3_lblRefrescar = ttk.Label(
            self.DESV_frame3, 
            text='REFRESCAR'
        )
        self.DESVfr3_lblRefrescar.grid(row=2, column=0, padx=5, pady=5, sticky='w', columnspan=2)
        self.DESVfr3_srcRefrescar = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcRefrescar.config(
            font=self._font_TXT_DESV,
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=2,
            insertbackground='#297F87',
            selectbackground='lightblue',
            state='disabled',
        )
        self.DESVfr3_srcRefrescar.grid(row=3, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        
        self.DESV_btn1CopyALL = ttk.Button(
            self.DESV_frame3,
            image=self.CopyALL_icon,
            state='disabled',
            command= lambda e=self.DESVfr3_srcRefrescar:self.copiarALL(e),
        )
        self.DESV_btn1CopyALL.grid(row=2, column=2, padx=5, pady=5, sticky='e')
        
        self.varRefrescar = "REFRESCAR"
        self.DESV_btn4Expandir = ttk.Button(
            self.DESV_frame3,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr3_srcRefrescar:self.expandir(x, self.varRefrescar),
        )
        self.DESV_btn4Expandir.grid(row=2, column=3, padx=(5,20), pady=5, sticky='e')
        
        ## --- EVIDENCIA
        self.DESVfr3_lblEvidencia = ttk.Label(
            self.DESV_frame3, 
            text='EVIDENCIA'
        )
        self.DESVfr3_lblEvidencia.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.DESVfr3_srcEvidencia = st.ScrolledText(self.DESV_frame3)
        self.DESVfr3_srcEvidencia.config(
            font=self._font_TXT_DESV,
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=2,
            insertbackground='#297F87',
            selectbackground='lightblue',
            state='disabled',
        )
        self.DESVfr3_srcEvidencia.grid(row=5, column=0, padx=5, pady=5, sticky='new', columnspan=4)
        self.DESV_btnCopyALL = ttk.Button(
            self.DESV_frame3,
            image=self.CopyALL_icon,
            state='disabled',
            command=lambda e=self.DESVfr3_srcEvidencia:self.copiarALL(e),
        )
        self.DESV_btnCopyALL.grid(row=4, column=1, padx=(20,5), pady=5, sticky='ne')
        self.DESV_btnScreamEvidencia = ttk.Button(
            self.DESV_frame3,
            image=self.Captura_icon,
            state='disabled',
            command=self.ScreamEvidencia,
        )
        self.DESV_btnScreamEvidencia.grid(row=4, column=2, padx=5, pady=5, sticky='ne')
        
        self.varEvidencia = "EVIDENCIA"
        self.DESV_btn5Expandir = ttk.Button(
            self.DESV_frame3,
            image=self.Expandir_icon,
            state='disabled',
            command=lambda x=self.DESVfr3_srcEvidencia:self.expandir(x, self.varEvidencia),
        )
        self.DESV_btn5Expandir.grid(row=4, column=3, padx=(5,20), pady=5, sticky='ne')
        ## ------------------------------------------------------------------------------ ##
    ## --- FUNCIONES PARA ABRIR VENTANAS EMERGENTE --------------- ##
    def _QuitarSeleccion(self):
        global list_motion
        global txtWidget
        srcCom.delete('1.0',END)
        srcBac.delete('1.0',END)
        srcEdi.delete('1.0',END)
        srcRes.delete('1.0',END)
        srcEvi.delete('1.0',END)
        srcDes['text'] = ''
        srcSO['text'] = 'SISTEMA OPERATIVO'
        srcMod['text'] = 'MODULO'
        if list_motion:
            list_motion.selection_clear(0,tk.END)
            self.limpiar_Widgets()

    def abrir_DIRECTORY(self):
        global asigne_Ciente
        global directory
        name_vtn = "PERMISSIONS"
        path = "Compliance/file/directory.json"
        directory = Ventana(self,name_vtn, asigne_Ciente, app,desviacion,path)
    
    def abrir_COMMAND(self):
        global asigne_Ciente
        global command
        name_vtn = "COMMAND"
        path = "Compliance/file/command.json"
        command = Ventana(self,name_vtn, asigne_Ciente, app,desviacion,path)
    
    def abrir_AUTHORIZED(self):
        global asigne_Ciente
        global authorized
        name_vtn = "AUTHORIZED"
        path = "Compliance/file/authorized_keys.json"
        authorized = Ventana(self,name_vtn, asigne_Ciente, app,desviacion,path)
    
    def abrir_ACCOUNT(self):
        global asigne_Ciente
        global account
        name_vtn = "ACCOUNT"
        path = "Compliance/file/account.json"
        account = Ventana(self,name_vtn, asigne_Ciente, app,desviacion,path)
    
    def abrir_SERVICE(self):
        global asigne_Ciente
        global service
        name_vtn = "SERVICE"
        path = "Compliance/file/service.json"
        service = Ventana(self,name_vtn, asigne_Ciente, app,desviacion,path)
    
    def abrir_IDRSA(self):
        global asigne_Ciente
        global idrsa
        name_vtn = "ID_RSA"
        path = "Compliance/file/idrsa.json"
        idrsa = Ventana(self,name_vtn, asigne_Ciente, app,desviacion,path)
    ## ----------------------------------------------------------- ##
    def cambiar_NamePestaña(self, customer):
        app.cuaderno.tab(idOpenTab, option=None, text='DESVIACIONES : {} '.format(customer))
        app.cuaderno.notebookContent.tab(idOpenTab, option=None, text='DESVIACIONES : {} '.format(customer))

class Aplicacion():
    
    def __init__(self):
        self.root= tk.Tk()
        self.root.title("CONTINUOUS COMPLIANCE")
        window_width,window_height=1028,768
        screen_width = self.root.winfo_screenwidth()
        screen_height= self.root.winfo_screenheight()
        position_top = int(screen_height/2 - window_height/2)
        position_right = int(screen_width/2 - window_width/2)
        self.root.geometry(f'{window_width}x{window_height}+{position_top}+{position_right}')
        self.root.configure(background='black') 
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file=path_icon+r'compliance.png'))       
        self.iconos()
        self.cuaderno = ScrollableNotebook(self.root,wheelscroll=False,tabmenu=True, application=self)
        self.contenedor= ttk.Frame(self.cuaderno)
        self.contenedor.columnconfigure(1, weight=1)
        self.contenedor.rowconfigure(1, weight=1)
        self.cuaderno.add(self.contenedor, text='WorkSpace  ', underline=0, image=self.WorkSpace_icon, compound='left')
        self.cuaderno.pack(fill="both",expand=True)
        self.cuaderno.bind_all("<<NotebookTabChanged>>",lambda e:self.alCambiar_Pestaña(e))
        self.cuaderno.enable_traversal()
        self.cuaderno.notebookTab.bind("<Button-3>", self.display_menu_clickDerecho)
        self.contenedor.bind("<Button-3>", self._display_menu_clickDerecho)
        self.root.bind_all("<Control-l>", lambda x : self.ocultar())

        # Fuente MENU CLICK DERECHO APP
        self._font_MC_APP = font.Font(family='Courier', size=14)
        # ----------------------------------------------------------

        # Fuente para la barra de MENU
        self._font_BARRA_APP = font.Font(family='Segoe Script', size=13, weight=font.BOLD)
        # ----------------------------------------------------------

        self.estilos()
        self.menu_clickDerecho()
        self._menu_clickDerecho()
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
        self.style.configure(
            'TCombobox',
            fieldbackground= 'white',
            background='#F4D19B',
            selectbackground="lightblue",
            selectforeground="black"
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
        self.style.configure(
            'DESV.TButton',
            background = "#D4ECDD",
            relief='sunke',
            borderwidth=1,
            padding=10,
            font=('Source Sans Pro', 13, font.BOLD), 
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
                            font=('Comfortaa',30,font.BOLD))
        self.style.configure('TLabel',
                            background = "#f1ecc3",
                            foreground = "gray17",
                            font=('Helvetica',12, font.BOLD))
        self.style.configure('TEntry',
                            background = "#f1ecc3",
                            foreground = "gray17",
                            font=('Helvetica',12, font.BOLD))
    ## --- MENU CONTEXTUAL --- ##
    def menu_clickDerecho(self):  
        self.menu_Contextual = Menu(self.root, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar", 
            accelerator='Ctrl+F',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self.menu_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Cerrar pestaña", 
            compound=LEFT,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            command=self.cerrar_vtn_desviacion
        )
    
    def display_menu_clickDerecho(self, event):
        self.menu_Contextual.tk_popup(event.x_root, event.y_root)
    
    def _menu_clickDerecho(self):
        self._menu_Contextual = Menu(self.root, tearoff=0)
        self._menu_Contextual.add_command(
            label="  Buscar", 
            accelerator='Ctrl+F',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background='#ccffff')
        self._menu_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self._menu_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background='#ccffff')
        self._menu_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self._menu_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled',
        )
        self._menu_Contextual.add_separator(background='#ccffff')
        self._menu_Contextual.add_command(
            label="  Cerrar pestaña", 
            compound=LEFT,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            state='disabled'
        )
        self._menu_Contextual.add_command(
            label="  Salir", 
            compound=LEFT,
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self._font_MC_APP,
            command=self.root.quit
        )
    
    def _display_menu_clickDerecho(self, event):
        self._menu_Contextual.tk_popup(event.x_root, event.y_root)
        #desviacion.DESVfr1_entModulo.select_range(0,tk.END)
        #desviacion.DESVfr1_entModulo.focus_set()

    def cerrar_vtn_desviacion(self):
        if idOpenTab == 0:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
        else:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')
            self.cuaderno.forget(idOpenTab)
            self.cuaderno.notebookContent.forget(idOpenTab)
    ## ----------------------- ##
    def alCambiar_Pestaña(self, event):
        global idOpenTab
        global top_active_LBK
        global asigne_Ciente
        idOpenTab = event.widget.index('current')
        tab = event.widget.tab(idOpenTab)['text']
        if idOpenTab != 0:
            self.menu_Contextual.entryconfig('  Copiar', state='disabled')
            self.menu_Contextual.entryconfig('  Pegar', state='disabled')
            self.menu_Contextual.entryconfig('  Seleccionar todo', state='disabled')
        elif idOpenTab == 0:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='disabled')
            self.cuaderno._release_callback(e=None)
        else:
            self.menu_Contextual.entryconfig('  Cerrar pestaña', state='normal')
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
        elif tab == 'DESVIACIONES : AFB ':
            asigne_Ciente = 'AFB'
        elif tab == 'DESVIACIONES : ASISA ':
            asigne_Ciente = 'ASISA'
        elif tab == 'DESVIACIONES : CESCE ':
            asigne_Ciente = 'CESCE'
        elif tab == 'DESVIACIONES : CTTI ':
            asigne_Ciente = 'CTTI'
        elif tab == 'DESVIACIONES : ENEL ':
            asigne_Ciente = 'ENEL'
        elif tab == 'DESVIACIONES : EUROFRED ':
            asigne_Ciente = 'EUROFRED'
        elif tab == 'DESVIACIONES : FT ':
            asigne_Ciente = 'FT'
        elif tab == 'DESVIACIONES : INFRA ':
            asigne_Ciente = 'INFRA'
        elif tab == 'DESVIACIONES : IDISO ':
            asigne_Ciente = 'IDISO'
        elif tab == 'DESVIACIONES : LBK ':
            asigne_Ciente = 'LBK'
        elif tab == 'DESVIACIONES : PLANETA ':
            asigne_Ciente = 'PLANETA'
        elif tab == 'DESVIACIONES : SERVIHABITAT ':
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
        if tab == 'Issues EXTRACIONES':
            self.fileMenu.entryconfig('  Clientes', state='disabled')
            self.editMenu.entryconfig('  Buscar', state='normal')
        else:
            self.editMenu.entryconfig('  Buscar', state='disabled')
        try:
            self.valor_activo_list = desviacion.DESVfr1_listbox.get(ANCHOR)
            self.extracion.on_closing_busca_top()
        except:
            pass
        try:
            expandir.cerrar_vtn_expandir()
            desviacion.limpiar_Widgets()
        except:
            pass

        self._QuitarSeleccion()

    def _QuitarSeleccion(self):
        try:
            desviacion._QuitarSeleccion()
            desviacion.limpiar_Widgets()
            desviacion._disabled_buttons()
        except:
            pass

    def abrir_issues(self):
        idx = self.IssuesVar.get()
        itm = list_issues[idx]
        if str(itm) == "DESVIACIONES":
            self.abrir_issuesDesviacion()
        else:
            self.abrir_issuesExtracion()

    def abrir_issuesDesviacion(self):
        global idOpenTab
        global desviacion
        desviacion = Desviacion(self.cuaderno)
        self.cuaderno.add(desviacion, text='Issues DESVIACIONES ')
    
    def abrir_issuesExtracion(self):
        global idpTab
        self.extracion = Extracion(self.cuaderno, app, application=self)
        self.cuaderno.add(self.extracion, text='Issues EXTRACIONES')
        idpTab = self.cuaderno.index('current')

    def ocultar(self):
        self.extracion.hide()

    def bsc(self):
        self.extracion.panel_buscar()
    
    def cargar_modulos(self):
        desviacion._cargar_Modulos()
    
    def label_resize(self, event):
        event.widget['wraplength'] = event.width 
    
    def cerrar_vtn(self):
        self.vtn_acerca_de.destroy()

    def _acerca_de(self):
        self.vtn_acerca_de = tk.Toplevel(self.root)
        self.vtn_acerca_de.config(background='#F1ECC3')
        window_width=780
        window_height=370
        screen_width = app.root.winfo_x()
        screen_height= app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_acerca_de.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_acerca_de.tk.call('wm', 'iconphoto', self.vtn_acerca_de._w, tk.PhotoImage(file=path_icon+r'acercaDe.png'))       
        #self.vtn_acerca_de.transient(self.root)
        self.vtn_acerca_de.resizable(False,False)
        self.vtn_acerca_de.title("Continuous Compliance")

        self.icono_Acerca_de = ImageTk.PhotoImage(
            Image.open(path_icon+r"img_acerca_de.png").resize((200, 200)))

        self.AcercaDe_ico_frame = tk.Frame(
                self.vtn_acerca_de,
                background='#F1ECC3',
                width=300,
            )
        self.AcercaDe_ico_frame.pack(fill='both', expand=1, side='left')
        self.AcercaDe_ico_frame.pack_propagate(False)

        self.ico_Acerca_de = tk.Label(
            self.AcercaDe_ico_frame, 
            text='imagen',
            image=self.icono_Acerca_de,
            background='#F1ECC3',
        )
        self.ico_Acerca_de.place(x=50, y=50)

        self.AcercaDe_txt_frame = tk.Frame(
                self.vtn_acerca_de, 
                background='#F1ECC3',
                #width=40,
                #height=50 
            )
        self.AcercaDe_txt_frame.pack(fill='both', expand=1, side='left')
        #self.AcercaDe_txt_frame.pack_propagate(False)

        self.lbl1 = tk.Label(
            self.AcercaDe_txt_frame, 
            text='CONTINUOUS COMPLIANCE',
            background="#F1ECC3",
            anchor='center',
            font=("Consolas", 16, "bold")
        )
        self.lbl1.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.lbl5 = tk.Label(
            self.AcercaDe_txt_frame,
            width=20,
            text='Herramienta para resolucion    de ISSUES Desviaciones / Extraciones',
            background="#F1ECC3",
            anchor='w',
            font=("Consolas", 13)
        )
        self.lbl5.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.lbl5.bind("<Configure>", self.label_resize)

        self.lbl2 = tk.Label(
            self.AcercaDe_txt_frame, 
            text='Versión:   1.6',
            background="#F1ECC3",
            anchor='w',
            #width=20,
            font=("Consolas", 13)
        )
        self.lbl2.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl2.bind("<Configure>", self.label_resize)

        self.lbl3 = tk.Label(
            self.AcercaDe_txt_frame, 
            text='Fecha:   miercoles diciciembre 22 CET 2021',
            background="#F1ECC3",
            anchor='w',
            #width=20,
            font=("Consolas", 11)
        )
        self.lbl3.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl3.bind("<Configure>", self.label_resize)

        self.lbl4 = tk.Label(
            self.AcercaDe_txt_frame, 
            #width=20,
            text='OS: x86_64 GNU/Linux',
            background="#F1ECC3",
            anchor='w',
            font=("Consolas", 11)
        )
        self.lbl4.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl4.bind("<Configure>", self.label_resize)

        

        self.lbl6 = tk.Label(
            self.AcercaDe_txt_frame, 
            #width=20,
            foreground='gray',
            text='Documentado por el equipo de PHC - UNIX',
            background="#F1ECC3",
            anchor='w',
            font=("Consolas", 11)
        )
        self.lbl6.grid(row=5, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl6.bind("<Configure>", self.label_resize)


        self.lbl7 = tk.Label(
            self.AcercaDe_txt_frame, 
            #width=20,
            foreground='gray',
            text='Creado por Jose Alvaro Cedeño Panchana',
            background="#F1ECC3",
            anchor='w',
            font=("Consolas", 11)
        )
        self.lbl7.grid(row=6, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl7.bind("<Configure>", self.label_resize)

        self.lbl8 = tk.Label(
            self.AcercaDe_txt_frame, 
            #width=20,
            foreground='gray',
            text='Copyright © 2021 - 2022 Jose Alvaro Cedeño Panchana',
            background="#F1ECC3",
            anchor='w',
            font=("Consolas", 11, 'bold')
        )
        self.lbl8.grid(row=7, column=0, padx=5, pady=5, sticky='nsew')
        #self.lbl8.bind("<Configure>", self.label_resize)

        self.boton = ttk.Button(
            self.AcercaDe_txt_frame,
            text='Close',
            command=self.cerrar_vtn
        )
        self.boton.grid(row=8, column=0, sticky='e', pady=20, padx=10)
    
    def _cargar_modulo_glosario(self, clt_modulo=None, *args):
        with open(path_modulo_clave.format('GLOSARIO')) as g:
            data = json.load(g)
            listModulo = []
            listClave = []
            for md in data:
                listModulo.append(md['modulo'])
                listClave.append(md['clave'])
        #listModulo.sort()
        self._list_modulo.insert(END,*listModulo)
        self._list_clave.insert(END,*listClave)

    def on_select(self, event):
        global listbox_list
    
        widget = event.widget
        items = widget.curselection()
        
        for listbox in listbox_list:
            if listbox != widget:
                listbox.selection_clear(0, tk.END)
                for index in items:
                    listbox.selection_set(int(index))

    def _glosario(self):
        self.vtn_glosario = tk.Toplevel(self.root)
        self.vtn_glosario.config(background='#F1ECC3')
        window_width=800
        window_height=400
        screen_width = app.root.winfo_x()
        screen_height= app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_glosario.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_glosario.tk.call('wm', 'iconphoto', self.vtn_glosario._w, tk.PhotoImage(file=path_icon+r'acercaDe.png'))       
        #self.vtn_acerca_de.transient(self.root)
        self.vtn_glosario.resizable(False,False)
        self.vtn_glosario.title("Continuous Compliance")
        
        self.frame1 = tk.Frame(
            self.vtn_glosario,
            background='#F1ECC3',
            height=40,
        )
        self.frame1.pack(fill='both', side='top', expand=0)

        self.titulo = tk.Label(
            self.frame1,
            text='PALABRAS CLAVES DESVIACIONES',
            font=('Consolas', 20, font.BOLD),
            background='#F1ECC3'
        )
        self.titulo.pack(expand=1)

        self.frame2 = tk.Frame(
            self.vtn_glosario,
            background='#F1ECC3',
        )
        self.frame2.pack(fill='both', side='left', expand=0, pady=10)
        
        #self.frame2.rowconfigure(0, weight=1)
        self.frame2.rowconfigure(1, weight=1)

        self.titulo_modulo = tk.Label(
            self.frame2,
            text='MODULO',
            font=('Consolas', 15, font.BOLD),
            background='#F1ECC3',
            anchor='center',
            width=50
        )
        self.titulo_modulo.grid(row=0, column=0, sticky='nsew', pady=5, padx=5)

        self.ListModulo_yScroll = tk.Scrollbar(self.frame2, orient=tk.VERTICAL)
        
        ## LISTBOX MODULO
        self._list_modulo = tk.Listbox(
            self.frame2,
            font=('Consolas', 12),
            foreground='blue',
            selectbackground='#297F87',
            selectforeground='#F6D167',
            disabledforeground='black',
            exportselection=False,
            highlightbackground='gray88',
            highlightthickness=1,
            highlightcolor='#297F87',
            yscrollcommand=self.ListModulo_yScroll.set,
        )
        self._list_modulo.grid(row=1, column=0, sticky='nsew', pady=10)
        listbox_list.append(self._list_modulo)
        
        
        self.frame3 = tk.Frame(
            self.vtn_glosario,
            background='#F1ECC3',
            width=40
        )
        self.frame3.pack(fill='both', side='right', expand=1, pady=10,padx=10)
        self.frame3.columnconfigure(0, weight=1)
        self.frame3.rowconfigure(1, weight=1)

        self.titulo_clave = tk.Label(
            self.frame3,
            text='CLAVE',
            font=('Consolas', 15, font.BOLD),
            background='#F1ECC3',
            anchor='center'
        )
        self.titulo_clave.grid(row=0, column=0, sticky='nsew', pady=5, padx=5, columnspan=2)

        self.ListClave_yScroll = tk.Scrollbar(self.frame3, orient=tk.VERTICAL)
        
        ## LISTBOX CLAVE
        self._list_clave = tk.Listbox(
            self.frame3,
            font=('Consolas', 12),
            foreground='blue',
            selectbackground='#297F87',
            selectforeground='#F6D167',
            disabledforeground='black',
            exportselection=False,
            highlightbackground='gray88',
            highlightthickness=1,
            highlightcolor='#297F87',
            yscrollcommand=self.ListClave_yScroll.set,
        )
        self._list_clave.grid(row=1, column=0, sticky='nsew', pady=10,)
        listbox_list.append(self._list_clave)

        self.ListClave_yScroll.grid(row=1, column=1, pady=10, sticky='nse')
        self.ListModulo_yScroll.grid(row=1, column=1, pady=10, sticky='nse')

        self._list_modulo.bind('<<ListboxSelect>>', self.on_select)
        self._list_clave.bind('<<ListboxSelect>>', self.on_select)

        self._cargar_modulo_glosario()

    def widgets_APP(self):
            self.menuBar = tk.Menu(self.root, relief=FLAT, border=0)
            self.root.config(menu=self.menuBar)
            self.menuBar.config(
                background='#1A1C20',
                foreground='#CF7500',
                font=self._font_BARRA_APP,
                activebackground='#003638',
                activeforeground='#53B8BB',
            )
            self.fileMenu = Menu(self.menuBar, tearoff=0)
            self.fileMenu.config(
                background='#003638',
                foreground='#F3F2C9',
                font=self._font_BARRA_APP,
                activebackground='#003638',
                activeforeground='#53B8BB',
            )
            # --- INICIAMOS SUB MENU -------------------------- #
            self.clientMenu = Menu(self.fileMenu, tearoff=0)
            self.issuesMenu = Menu(self.fileMenu, tearoff=0)
            # -------------------------------------------------- #

            self.issuesMenu.config(
                background='#003638',
                foreground='#F3F2C9',
                font=self._font_BARRA_APP,
                activebackground='#003638',
                activeforeground='#53B8BB',
                selectcolor='#CF7500'
            )
            self.clientMenu.config(
                background='#003638',
                foreground='#F3F2C9',
                font=self._font_BARRA_APP,
                activebackground='#003638',
                activeforeground='#53B8BB',
                selectcolor='#CF7500'
            )

            self.fileMenu.add_cascade(
                label="  Abrir",
                compound=LEFT,
                image=self.Abrir_icon,
                menu = self.issuesMenu
            )

            self.fileMenu.add_cascade(
                label="  Clientes",
                image=self.Client_icon,
                compound=LEFT,
                menu=self.clientMenu
            )

            self.fileMenu.add_separator()

            self.fileMenu.add_command(
                label="  Salir",
                image=self.Salir_icon,
                compound=LEFT,
                command=self.root.quit
            )

            self.ClientVar = tk.IntVar()
            for i, m in enumerate(list_client):
                self.clientMenu.add_radiobutton(
                    label=m,
                    variable=self.ClientVar,
                    value=i,
                    command=self.cargar_modulos,
                )

            self.IssuesVar = tk.IntVar()
            for i, m in enumerate(list_issues):
                self.issuesMenu.add_radiobutton(
                    label=m,
                    variable=self.IssuesVar,
                    value=i,
                    command=self.abrir_issues
                )

            self.editMenu = Menu(self.menuBar, tearoff=0)
            self.editMenu.config(
                background='#003638',
                foreground='#F3F2C9',
                font=self._font_BARRA_APP,
                activebackground='#003638',
                activeforeground='#53B8BB',
            )
            self.editMenu.add_command(
                label="  Buscar",
                accelerator='Ctrl+F',
                command=self.bsc,
                image=self.BuscarBar_icon,
                compound=LEFT,
                state="disabled"
            )
            self.fileMenu.add_separator()
            self.helpMenu = Menu(self.menuBar, tearoff=0)
            self.helpMenu.config(
                background='#003638',
                foreground='#F3F2C9',
                font=self._font_BARRA_APP,
                activebackground='#003638',
                activeforeground='#53B8BB',
            )
            self.helpMenu.add_command(
                label="  Ayuda",
                image=self.Ayuda_icon,
                compound=LEFT,
                command=self._glosario
            )
            self.helpMenu.add_separator()
            self.helpMenu.add_command(
                label="  Acerca de...",
                image=self.AcercaDe_icon,
                compound=LEFT,
                command=self._acerca_de
            )

            self.menuBar.add_cascade(label=" Archivo ", menu=self.fileMenu)
            self.menuBar.add_cascade(label=" Editar ", menu=self.editMenu)
            self.menuBar.add_cascade(label=" Ayuda ", menu=self.helpMenu)

            self.btn_AbrirDesv = ttk.Button(
                self.contenedor, text='DESVIACIONES',
                width=15,
                style='APP.TButton',
                image=self.Desviaciones_icon,
                compound='top',
                command=self.abrir_issuesDesviacion
            )
            self.btn_AbrirDesv.grid(
                padx=30, 
                pady=30, 
                row=0, 
                column=0, 
                ipady=20, 
                sticky='wn'
            )
            self.btn_AbrirExt = ttk.Button(
                self.contenedor, text='EXTRACIONES',
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
                sticky='wn'
            )
            self.lbl_Bienvenido = ttk.Label(
                self.contenedor,
                style='APP.TLabel',
                text='Bienvenido : '+user,
                anchor='center'
            )
            self.lbl_Bienvenido.grid(
                row=1, 
                column=0, 
                columnspan=3,
                sticky='sew'
            )
    
    def mainloop(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()