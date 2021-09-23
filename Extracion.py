import tkinter as tk
import glob
from tkinter import Button, ttk
from tkinter.constants import W
from PIL import Image, ImageTk
from tkinter import scrolledtext as st



class Extracione(tk.Frame):

	def __init__(self, parent, *args,**kwargs):
		tk.Frame.__init__(self, parent, *args)
		self = self
		self.configure(background="gold")
		self.navIcon = ImageTk.PhotoImage(Image.open("/home/esy9d7l1/compliance/image/menu.png").resize((25, 25)))
		self.closeIcon = ImageTk.PhotoImage(Image.open("/home/esy9d7l1/compliance/image/close.png").resize((25, 25)))
		self.menu()
		self.text()
		self.bind("<Control-l>", lambda x: self.hide())
		self.hidden = 0
		#self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=5)
		self.rowconfigure(0, weight=1)
	
	def menu(self):
		self.frame1 = tk.Frame(
			self,
			background="gold",
			width=300
		)

		#self.frame1.pack(side="left", fill=tk.BOTH, expand=1)
		self.frame1.grid_propagate(False)
		self.frame1.grid(row=0, column=0, sticky="nsew")
		self.frame1.columnconfigure(0, weight=1)
		self.frame1.rowconfigure(1, weight=1)
		#self.frame1.rowconfigure(0, weight=1)
		self.btn_nav = Button(self,
		background="gold",
		border=0,
		borderwidth=0,
		highlightthickness=0,
		relief='flat',
		image=self.navIcon,
		command=self.show_btn_nav,
		)

		#self.btn_nav.grid(row=0, column=0, sticky="nw")
		# self.frame1.columnconfigure(1, weight=1)
		self.btn_close = tk.Button(self.frame1,
		background="gold",
		border=0,
		borderwidth=0,
		highlightthickness=0,
		relief='flat',
		image=self.closeIcon,
		command=self.hide_btn_nav,
		)
		#self.btn.pack(side="top", fill=tk.X)
		self.btn_close.grid(row=0, column=0, sticky="e")
		#self.btn_nav.grid_forget()
		self.lb = tk.Listbox(self.frame1)
		self.lb['bg'] = "white"
		self.lb['fg'] = "blue"
		self.lb['font'] = "Consolas",13
		self.lb.grid(row=1, column=0, sticky="nsew")
		# self.lb.pack(side="left", fill=tk.BOTH, expand=1)
		for file in glob.glob("extracion/*"):
			self.lb.insert(tk.END, file)

	def text(self):
		self.frame2 = tk.Frame(self)
		#self.frame2.pack(side="left", fill=tk.BOTH, expand=1)
		self.frame2.grid(row=0, column=1, sticky="nsew")
		self.frame2.columnconfigure(0,weight=1)
		self.frame2.rowconfigure(0,weight=1)
		self.txt = st.ScrolledText(
			self.frame2, 
			font=("Consolas", 14),
		)
		#self.txt.config(state='disabled')
		self.txt['bg'] = 'white'
		#self.txt.pack(fill=tk.BOTH, expand=1)
		self.txt.grid(row=0, column=0, sticky="nsew")
	
	def hide(self):
		if self.hidden == 0:
			self.frame1.destroy()
			self.hidden = 1
			self.btn_nav.grid(row=0, column=0, sticky="nw")
			print("Hidden", self.hidden)
		else:
			#self.frame2.destroy()
			self.menu()
			#self.text()
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
			self.frame2.destroy()
			self.menu()
			self.text()
			self.hidden = 0
			self.btn_nav.grid_forget()
			print("Hidden", self.hidden)