import tkinter as tk
from tkinter import scrolledtext
from recursos import create_frame


class Ventana_informacion:

    def __init__(self, master) -> None:
        self.create_frame = create_frame.Frames().create_frame
        self.ventana = self.create_frame(master, height=0.7, width=0.7, x=0.05, y=0.15)
        # Crear el widget de texto
        self.text_widget = scrolledtext.ScrolledText(self.ventana, wrap=tk.WORD)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.config(state='disabled')


    def write(self,mensaje):
        self.text_widget.config(state='normal')
        self.text_widget.insert(tk.END, f"{mensaje}\n")
        self.text_widget.config(state='disabled')
        self.text_widget.see(tk.END)



