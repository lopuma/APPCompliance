import tkinter as tk
import glob
from tkinter import ttk

class Extracione(ttk.Frame):
 
	def __init__(self, parent, *args,**kwargs):
		ttk.Frame.__init__(self, parent, *args)
		#self = self
		self.menu()
		self.text()
		self.bind("<Control-l>", lambda x: self.hide())
		self.hidden = 0
 
	def menu(self):
		self.frame1 = tk.Frame(self)
		self.frame1.pack(side="left", fill=tk.BOTH, expand=1)
		self.lb = tk.Listbox(self.frame1)
		self.lb['bg'] = "black"
		self.lb['fg'] = "lime"
		self.lb.pack(side="left", fill=tk.BOTH, expand=1)
		for file in glob.glob("extracion/*"):
			self.lb.insert(tk.END, file)
 
	def text(self):
		self.frame2 = tk.Frame(self)
		self.frame2.pack(side="left", fill=tk.BOTH, expand=1)
		self.txt = tk.Text(self.frame2)
		self.txt['bg'] = 'gold'
		self.txt.pack(fill=tk.BOTH, expand=1)
 
	def hide(self):
		if self.hidden == 0:
			self.frame1.destroy()
			self.hidden = 1
			print("Hidden", self.hidden)
		else:
			self.frame2.destroy()
			self.menu()
			self.text()
			self.hidden = 0
			print("Hidden", self.hidden)
 
 
 
# parent = tk.Tk()
# app = App(parent)
# parent.mainloop()