import customtkinter as ctk
from recursos import colors

class Combobox:
        
    def __init__(self):
        self.colors = colors.Colors()
    
    def create_combobox(self,master, opciones ,letterSize = 16, x=None, y=None, widht=None, height=None, textvariable=None, command=None):
        self.color = getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}')
        if getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}') == self.colors.fondo_Dark: self.text_color = 'white'
        else: self.text_color = 'black'
        # command: callback opcional que recibe el valor elegido al cambiar la selección.
        self.combobox = ctk.CTkComboBox(master, values=opciones, font=('Bold',letterSize), text_color=self.text_color, command=command)
        self.combobox.place(relx=x, rely=y, relheight=height, relwidth=widht)


        return self.combobox