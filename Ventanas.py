# -*- coding: utf-8 -*-
import json
import os
import tkinter as tk
from getpass import getuser
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext as st
from tkinter import messagebox as mb
from tkinter import font as font
from PIL import Image, ImageTk
user = getuser()
mypath = os.path.expanduser("~/")
path_icon = mypath+"Compliance/image/"
class Ventana(ttk.Frame):
    def __init__(self, parent, name_vtn, customer, app, desviacion, path, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.customer = customer
        self.app = app
        self.desviacion = desviacion
        self.path_ventanas = mypath+path
        self.tt_vtn = name_vtn
        print(self.path_ventanas)
        self.vtn_ventanas = tk.Toplevel(self)
        self.vtn_ventanas.config(background='#F9F3DF')
        window_width=1028
        window_height=650
        screen_width = self.app.root.winfo_x()
        screen_height= self.app.root.winfo_y()
        position_top = int(screen_height+70)
        position_right = int(screen_width+150)
        self.vtn_ventanas.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.vtn_ventanas.resizable(0,0)
        self.vtn_ventanas.title('{} for client {}'.format(self.tt_vtn, self.customer))
        #self.vtn_ventanas.transient(self)
        #self.vtn_ventanas.grab_set()
        self.vtn_ventanas.columnconfigure(0, weight=1)
        self.vtn_ventanas.rowconfigure(2, weight=5)
        self.text_font = font.Font(family='Consolas', size=13) 
        self.iconos()
        self.widgets_ventanas()
        self.menu_clickDerecho()
        self.menuList_clickDerecho()
        self.cargar_ventanas()
        self.tree.bind("<ButtonRelease-1>", self.selecionar_elemntFile)
        self.tree.bind("<Key>", lambda e: self.desviacion.widgets_SoloLectura(e))
        self.srcRisk.bind("<Key>", lambda e: self.desviacion.widgets_SoloLectura(e))
        self.srcImpact.bind("<Key>", lambda e: self.desviacion.widgets_SoloLectura(e))
        self.srcVariable.bind("<Key>", lambda e: self.desviacion.widgets_SoloLectura(e))
        self.cbxUser.bind("<Key>", lambda e: self.desviacion.widgets_SoloLectura(e))
        self.textBuscar.bind("<Return>", lambda event=None: self.buscar(self.textBuscar.get()))
        #self.vtn_ventanas.bind("<Motion>", lambda e:desviacion.activar_Focus(e))
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
        self.textBuscar.bind("<FocusIn>", lambda e: self.clear_bsq(e))
        self.textBuscar.bind("<FocusOut>", lambda e: self.clear_bsq(e))    
        self.textBuscar.bind("<KeyPress>", lambda e: self.clear_bsq_buttom(e))    
        self.textBuscar.bind("<Control-v>",lambda e:self.sel_text(e))
        ## --- Selecionar elemento hacia abajo
        self.tree.bind("<Down>", lambda e:self.TreeDown(e))
        self.tree.bind("<Up>", lambda e:self.TreeUp(e))
        self.textBuscar.bind("<Control-x>",self.limpiar_bsq2)
        self.srcRisk.bind("<Control-a>",lambda e:self._seleccionar_todo(e))
        self.srcImpact.bind("<Control-a>",lambda e:self._seleccionar_todo(e))
        self.srcVariable.bind("<Control-a>",lambda e:self._seleccionar_todo(e))
        self.listServer.bind("<Control-a>",lambda e:self._selALL_optionLis(e))
        self.srcRisk.bind("<Control-f>",self.act_buscar)
        self.srcImpact.bind("<Control-f>",self.act_buscar)
        self.srcVariable.bind("<Control-f>",self.act_buscar)
        self.listServer.bind("<Control-f>",self.act_buscar)
        self.tree.bind("<Control-f>",self.act_buscar)
    def iconos(self):
        self.buscar_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"buscar.png").resize((25, 25)))
        self.cerrar_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"reduce.png").resize((25, 25)))
        self.copiar_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"copiarALL_evd.png").resize((20, 20)))
        self.limpiar_icon = ImageTk.PhotoImage(
                    Image.open(path_icon+r"limpiar.png").resize((25, 25)))
    def cerrar_vtn(self):
        self.vtn_ventanas.destroy()
    ## BUSCAR ventanas / FILE
    def clear_bsq_buttom(self, event):
        text_widget = event.widget
        entry = self.var_ent_buscar.get()
        long_entry = len(entry)
        if long_entry <=1:
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=W)
            self.cargar_ventanas()
            self.limpiar_widgets()
    def clear_bsq(self, event):
        text_widget = event.widget
        entry = self.var_ent_buscar.get()
        if entry == "Buscar Directories / File ...":
            text_widget.config(foreground="black", font=("Consolas", 14))
            self.var_ent_buscar.set("")
            text_widget.icursor(0)
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=W)
        elif entry == "":
            text_widget.config(foreground="gray75", font=("Consolas", 12))
            self.var_ent_buscar.set("Buscar Directories / File ...")
            text_widget.icursor(0)
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=W)
    def limpiar_bsq(self):
        self.var_ent_buscar.set("Buscar Directories / File ...")
        #self.var_ent_buscar.set("")
        self.textBuscar.focus()
        self.textBuscar.icursor(0)
        self.btnLimpiar.grid_forget()
        self.btnBuscar.grid(row=0, column=1, sticky=W)
        self.menu_Contextual.entryconfig("  Limpiar", state="disabled")
        self.cargar_ventanas()
        self.limpiar_widgets()
    def limpiar_bsq2(self, event=None):
        self.var_ent_buscar.set("")
        self.textBuscar.focus()
        self.textBuscar.icursor(0)
        self.btnLimpiar.grid_forget()
        self.btnBuscar.grid(row=0, column=1, sticky=W)
        self.menu_Contextual.entryconfig("  Limpiar", state="disabled")
        self.cargar_ventanas()
        self.limpiar_widgets()
    def buscar(self, event=None):
        valor_aBuscar = event
        valor_Buscado = [n for n in self.ventanas if valor_aBuscar.strip() in n]
        if valor_aBuscar == "":
            mb.showerror(
            "ERROR", "Esta vacio o no existe el directorio/fichero.\nPrueba a buscar de nuevo...", parent=self.vtn_ventanas
            )            
            self.cargar_ventanas()
            self.limpiar_widgets()
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=W)
            self.textBuscar.focus()
        else:
            if len(valor_Buscado) == 0:
                mb.showerror(
                "ERROR", "Esta vacio o no existe el directorio/fichero.\nPrueba a buscar de nuevo...", parent=self.vtn_ventanas
                )                 
                self.cargar_ventanas()
                self.limpiar_widgets()
                self.btnLimpiar.grid_forget()
                self.btnBuscar.grid(row=0, column=1, sticky=W)
                self.textBuscar.focus()
            else:
                self.limpiar_tree()
                with open(self.path_ventanas) as g:
                    data = json.load(g)
                    count = 0
                    for md in data[self.customer]:
                        for vb in valor_Buscado:
                            if vb == md['object']:
                                if count % 2 == 0:
                                    self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('evenrow'))
                                else:
                                    self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('oddrow'))
                                count += 1
                        self.limpiar_widgets()
            self.btnBuscar.forget()
            self.btnLimpiar.grid(row=0, column=1, sticky=W)
            self.menu_Contextual.entryconfig("  Limpiar", state="normal")
    def cargar_ventanas(self):
        self.ventanas = []
        #limpiando el arbol de vistas
        self.limpiar_tree()
        with open(self.path_ventanas) as g:
                data = json.load(g)
                count = 0
                for md in data[self.customer]:
                    self.ventanas.append(md['object'])
                    if count % 2 == 0:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('evenrow'))
                    else:
                        self.tree.insert(parent='', index='end', iid=count, text='', value=(md['object'],md['owner'],md['tipo'],md['ownerGroup'],md['code']), tags=('oddrow'))
                    count += 1
    def limpiar_tree(self):
        records = self.tree.get_children()
        for elemnt in records:
            self.tree.delete(elemnt)
    def selecionar_elemntFile(self, event):
        tree_event = event.widget
        try:
            item_id = tree_event.selection()[0]
            #item_id = tree_event.focus()
            index = tree_event.index(item_id)
            if tree_event.exists(index):
                dir_selecionado = tree_event.item(index, 'values')
                dir = dir_selecionado[0]
                self.cargar_elemt_seleccionado(dir)
        except:
            pass
    def cargar_elemt_seleccionado(self, dir):
        with open(self.path_ventanas) as g:
                data = json.load(g)
                for md in data[self.customer]:
                    if dir == md['object']:
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
            #self.menu_Contextual.entryconfig("  Limpiar", state="normal")
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
    def act_buscar(self, event=None):
        self.textBuscar.focus()
    def seleccionar_todo(self):
        self.srcEvent.tag_add("sel","1.0","end")
        return 'break'
    def _seleccionar_todo(self, event):
        srcEvent = event.widget
        srcEvent.tag_add("sel","1.0","end")
        return 'break'
    def copiar(self):
        seleccion = self.srcEvent.tag_ranges(tk.SEL)
        if seleccion:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(self.srcEvent.get(*seleccion).strip())
            self.srcEvent.tag_remove("sel","1.0","end")
            return 'break'
    def sel_text(self, event):
        if event.widget.select_present():
            self.var_ent_buscar.set("")
    def pegar(self):
        if self.srcEvent.select_present():
            self.var_ent_buscar.set("")
            self.btnLimpiar.grid_forget()
            self.btnBuscar.grid(row=0, column=1, sticky=W)
        self.srcEvent.event_generate("<<Paste>>")
        return 'break'
    def menu_clickDerecho(self):
        self.text_font = font.Font(family='Consolas', size=13)   
        self.menu_Contextual = Menu(self, tearoff=0)
        self.menu_Contextual.add_command(
            label="  Buscar", 
            accelerator='Ctrl+F',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=self.act_buscar,
        )
        self.menu_Contextual.add_separator(background='#ccffff')
        self.menu_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=self.copiar,
            state='normal',
        )
        self.menu_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=self.pegar,
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
            command=self.limpiar_bsq2,
            state='disabled',
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
        if str(self.srcEvent) == str(self.textBuscar):
            pass
        else:
            txt_select = event.widget.tag_ranges(tk.SEL)
            if txt_select:
                self.menu_Contextual.entryconfig("  Copiar", state="normal")
            else:
                self.menu_Contextual.entryconfig("  Copiar", state="disabled")
    def copiar_optionLis(self, event):
        listbox = event
        index = listbox.curselection()
        listCopiada = []
        for i in index:
            print(i)
            value = listbox.get(i)
            listCopiada.append(value)
        if listCopiada:
            self.app.root.clipboard_clear()
            self.app.root.clipboard_append(listCopiada)
    def selALL_optionLis(self, event):
        listbox = event
        listbox.selection_set(0, tk.END)
    def _selALL_optionLis(self, event):
        listbox = event.widget
        listbox.selection_set(0, tk.END)
    def menuList_clickDerecho(self):
        self.text_font = font.Font(family='Consolas', size=13)   
        self.menuLis_Contextual = Menu(self, tearoff=0)
        ## buscar
        self.menuLis_Contextual.add_command(
            label="  Buscar",
            accelerator='Ctrl+F',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=self.act_buscar,
        )
        self.menuLis_Contextual.add_separator(background='#ccffff')
        ## Copiar
        self.menuLis_Contextual.add_command(
            label="  Copiar", 
            accelerator='Ctrl+C',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=lambda e=self.listServer:self.copiar_optionLis(e),
            state='disabled',
        )
        ## Pegar
        self.menuLis_Contextual.add_command(
            label="  Pegar", 
            accelerator='Ctrl+V',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            state='disabled',
        )
        self.menuLis_Contextual.add_separator(background='#ccffff')
        ## Selecionar todo
        self.menuLis_Contextual.add_command(
            label="  Seleccionar todo", 
            accelerator='Ctrl+A',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            command=lambda e=self.listServer:self.selALL_optionLis(e),
            state='normal',
        )
        ## Limpiar
        self.menuLis_Contextual.add_command(
            label="  Limpiar", 
            accelerator='Ctrl+X',
            background='#ccffff', foreground='black',
            activebackground='#004c99',activeforeground='white',
            font=self.text_font,
            state='disabled',
        )
        self.menuLis_Contextual.add_separator(background='#ccffff')
        ## Cerrar pestñaa
        self.menuLis_Contextual.add_command(
            label="  Cerrar pestaña", 
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
        index = self.srcEvent.curselection()
        try:
            self.srcEvent.selection_includes(index)
            self.menuLis_Contextual.entryconfig("  Copiar", state="normal")
        except:
            self.menuLis_Contextual.entryconfig("  Copiar", state="disabled")
    def TreeDown(self, event):
        tree_event = event.widget
        item_id = tree_event.selection()[0]
        #item_id = tree_event.focus()
        index = tree_event.index(item_id)+1
        if tree_event.exists(index):
            dir_selecionado = tree_event.item(index, 'values')
            dir = dir_selecionado[0]
            self.cargar_elemt_seleccionado(dir)
    def TreeUp(self, event):
        tree_event = event.widget
        item_id = tree_event.selection()[0]
        index = tree_event.index(item_id)-1
        if tree_event.exists(index):
            dir_selecionado = tree_event.item(index, 'values')
            dir = dir_selecionado[0]
            self.cargar_elemt_seleccionado(dir)
    ## =============================================
    def copiarALL(self, event):
        event.focus()
        if event:
            event.tag_add("sel","1.0","end")
            seleccion = event.tag_ranges(tk.SEL)
            if seleccion:
                self.app.root.clipboard_clear()
                self.app.root.clipboard_append(event.get(*seleccion).strip())
        else:
            event.tag_remove("sel","1.0","end")
    def widgets_ventanas(self):
        self.var_ent_buscar = tk.StringVar(self)
        self.textBuscar = tk.Entry(
            self.vtn_ventanas,
            textvariable=self.var_ent_buscar,
            justify='left',
            width=40,
            foreground="gray75",
            font=("Consolas", 12),
            border=0,
            borderwidth=0,
            highlightthickness=3,
            highlightcolor='#316B83',
            selectforeground='#CDFFEB', 
            selectbackground='#476072'
        )
        self.var_ent_buscar.set("Buscar Directories / File ...")
        self.textBuscar.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        self.btnBuscar = ttk.Button(
            self.vtn_ventanas,
            text='Buscar',
            style='TOP1.TButton',
            image=self.buscar_icon,
            command=lambda:self.buscar(self.textBuscar.get())
        )
        self.btnBuscar.grid(row=0, column=1, sticky=W)

        self.btnLimpiar = ttk.Button(
            self.vtn_ventanas,
            text='Limpiar',
            style='TOP1.TButton',
            image=self.limpiar_icon,
            command= self.limpiar_bsq,            
        )
        #self.btnLimpiar.grid(row=0, column=1, sticky=W)

        self.btnCerrar = ttk.Button(
            self.vtn_ventanas, 
            text='Cerrar',
            style='TOP1.TButton',
            image=self.cerrar_icon,
            command=self.cerrar_vtn
        )
        self.btnCerrar.grid(row=0, column=2, padx=10, pady=5, sticky=E)
        
        ## ====================================================================================
        ## --- CREAMOS EL PRIMER LABEL FRAME
        self.labelframe1=ttk.LabelFrame(
            self.vtn_ventanas, 
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
            self.vtn_ventanas, 
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
        
        self.listServer = tk.Listbox(
            self.labelframe2, 
            height=3
        )
        self.fr2_scroll1 = tk.Scrollbar(self.labelframe2, orient=tk.VERTICAL)
        self.listServer.config(
            selectmode=tk.EXTENDED,
            foreground='#334257',
            selectforeground='black', 
            selectbackground='lightblue', 
            font=self.text_font,
            highlightcolor='#297F87',
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
        
        self.srcRisk = st.ScrolledText(
            self.labelframe2,
        )
        self.srcRisk.config(
            font=self.text_font, 
            height=6,
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=3,
            insertbackground='#297F87',
            selectbackground='lightblue',
        )

        self.btnCpRisk = ttk.Button(
            self.labelframe2, 
            text='Copiar',
            style='TOP.TButton',
            image=self.copiar_icon,
            command=lambda e=self.srcRisk:self.copiarALL(e),
        )
        self.btnCpRisk.grid(row=0, column=3, padx=20, pady=5, sticky=E)
        
        self.srcRisk.grid(row=1, column=2, pady=5, padx=5, sticky='new', columnspan=2)
        
        ## --- IMPACT
        self.lbl3 = ttk.Label(
            self.labelframe2,
            text='IMPACT',
            style='TOP.TLabel',
        )
        self.lbl3.grid(row=0, column=4, pady=5, padx=5, sticky='W')
        
        self.srcImpact = st.ScrolledText(
            self.labelframe2,
        )
        self.srcImpact.config(
            font=self.text_font, 
            height=6,
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=3,
            insertbackground='#297F87',
            selectbackground='lightblue',
        )

        self.btnCpImp = ttk.Button(
            self.labelframe2,
            text='Copiar',
            style='TOP.TButton',                
            image=self.copiar_icon,
            command=lambda e=self.srcImpact:self.copiarALL(e),
        )
        self.btnCpImp.grid(row=0, column=5, padx=20, pady=5, sticky=E)   
        
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

        self.srcVariable = st.ScrolledText(
            self.labelframe2,
        )
        self.srcVariable.config(
            font=self.text_font, 
            height=4,
            wrap=tk.WORD,
            highlightcolor='#297F87',
            borderwidth=0, 
            highlightthickness=2,
            insertbackground='#297F87',
            selectbackground='lightblue',
        )

        self.btnCpVariable = ttk.Button(
            self.labelframe2, 
            text='Copiar',
            style='TOP.TButton',                
            image=self.copiar_icon,
            command=lambda e=self.srcVariable:self.copiarALL(e),
        )
        self.btnCpVariable.grid(row=2, column=5, padx=20, pady=5, sticky=E)

        self.srcVariable.grid(row=3, column=3, pady=5, padx=5, sticky='new', columnspan=3)
