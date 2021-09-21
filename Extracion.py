import tkinter as tk
import glob
from tkinter import Button, ttk
from tkinter.constants import W
from PIL import Image, ImageTk

#navIcon = ImageTk.PhotoImage(Image.open("/home/esy9d7l1/compliance/image/menu.png").resize((25, 25)))
#closeIcon = ImageTk.PhotoImage(Image.open("/home/esy9d7l1/compliance/image/close.png").resize((25, 25)))

class Extracione(ttk.Frame):

	def __init__(self, parent, *args,**kwargs):
		ttk.Frame.__init__(self, parent, *args)
		#self = self
		
		self.menu()
		self.text()
		self.bind("<Control-l>", lambda x: self.hide())
		self.hidden = 0
		#self.columnconfigure(0, weight=2)
		self.columnconfigure(1, weight=5)
		self.rowconfigure(0, weight=1)
	def menu(self):
		self.frame1 = tk.Frame(self)
		#self.frame1.pack(side="left", fill=tk.BOTH, expand=1)
		self.frame1.grid(row=0, column=0, sticky="nsew")
		#self.frame1.rowconfigure(0, weight=1)
		self.btb = Button(self, command=self.show_btb)
		#self.btb.grid(row=0, column=0, sticky="nw")
		self.frame1.columnconfigure(0, weight=1)
		self.frame1.rowconfigure(1, weight=1)
		self.frame1.columnconfigure(1, weight=1)
		self.btn = tk.Button(self.frame1, command=self.hide_btb)
		self.btn.config(background='red')
		#self.btn.pack(side="top", fill=tk.X)
		self.btn.grid(row=0, column=0, sticky="w")
		#self.btb.grid_forget()
		self.lb = tk.Listbox(self.frame1, width=40)
		self.lb['bg'] = "black"
		self.lb['fg'] = "lime"
		self.lb.grid(row=1, column=0, sticky="nsew", columnspan=2)
		# self.lb.pack(side="left", fill=tk.BOTH, expand=1)
		for file in glob.glob("extracion/*"):
			self.lb.insert(tk.END, file)

	def text(self):
		self.frame2 = tk.Frame(self, background="red")
		#self.frame2.pack(side="left", fill=tk.BOTH, expand=1)
		self.frame2.grid(row=0, column=1, sticky="nsew")
		self.frame2.rowconfigure(0,weight=1)
		self.frame2.columnconfigure(0,weight=1)
		self.txt = tk.Text(self.frame2)
		self.txt['bg'] = 'gold'
		#self.txt.pack(fill=tk.BOTH, expand=1)
		self.txt.grid(row=0, column=0, sticky="nsew")
	def hide(self):
		if self.hidden == 0:
			self.frame1.destroy()
			self.hidden = 1
			self.btb.grid(row=0, column=0, sticky="nw")
			print("Hidden", self.hidden)
		else:
			self.frame2.destroy()
			self.menu()
			self.text()
			self.hidden = 0
			self.btb.grid_forget()
			print("Hidden", self.hidden)
	def hide_btb(self):
		if self.hidden == 0:
			self.frame1.destroy()
			self.hidden = 1
			self.btb.grid(row=0, column=0, sticky="nw")
			print("Hidden", self.hidden)
	
	def show_btb(self):
		if self.hidden == 1:
			self.frame2.destroy()
			self.menu()
			self.text()
			self.hidden = 0
			self.btb.grid_forget()
			print("Hidden", self.hidden)