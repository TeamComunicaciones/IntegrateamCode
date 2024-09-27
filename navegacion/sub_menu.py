import customtkinter as ctk
from tkinter import StringVar
from recursos import create_frame, colors, botones


class Sub_menu:

    def __init__(self,
                 master,
                 cantidad,
                 boton1=['BOTON1',None],
                 boton2=['BOTON2',None],
                 boton3=['BOTON3',None],
                 boton4=['BOTON4',None],
                 boton5=['BOTON5',None],
                 boton6=['BOTON6',None],
                 agrandar = False
                ):
        self.boton1 = boton1
        self.boton2 = boton2
        self.boton3 = boton3
        self.boton4 = boton4
        self.boton5 = boton5
        self.boton6 = boton6
        self.cantidad = cantidad
        self.master = master
        self.colors = colors.Colors()
        self.button = botones.Buttons()
        self.create_frame = create_frame.Frames()
        self.submenu = self.create_frame.create_frame(master, height=0.7, width=0.25, x=0.75, y=0.15)
        self.button_name = [
            [self.boton1[0]],
            [self.boton2[0]],
            [self.boton3[0]],
            [self.boton4[0]],
            [self.boton5[0]],
            [self.boton6[0]]
        ]
        self.button_func = [
            self.boton1[1],
            self.boton2[1],
            self.boton3[1],
            self.boton4[1],
            self.boton5[1],
            self.boton6[1]
        ]

        self.move = 0
        for i in range(self.cantidad):
            self.func = '' 
            self.boton = botones.Buttons()
            nombre_variable = f'boton {i}'
            funcion = lambda f =self.button_func[i]: f()
            valor = self.boton.create_button2(self.submenu, self.button_name[i][0], 0.15 , 0.05 + self.move, 0.7, 0.10, func= funcion, agrandar=agrandar)
            setattr(self,nombre_variable,valor)
            self.move += 0.15
        
    
    def indicator(self):
        for i in range(self.cantidad):
            self.create_frame.list_botones[self.button_name[i][0]].configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
            for frame in self.master.winfo_children():
                frame.destroy()
            self.__init__(self.master,
                          self.cantidad, 
                          boton1=self.boton1,
                          boton2=self.boton2,
                          boton3=self.boton3,
                          boton4=self.boton4,
                          boton5=self.boton5,
                          boton6=self.boton6,
                         )
            
    
    def submenu_boton(self,boton,func):
        self.indicator()
        self.create_frame.list_botones[boton].configure(fg_color= self.colors.team, text_color= 'white')
        self.conciliar_frame = self.create_frame.create_frame(self.create_frame.interfas_frame, 0.97, 0.97, 0.015, 0.015)
        if func != None:
            func(self.conciliar_frame)
    
    def ejecuteInit(self):
        self.__init__(self.master,
                          self.cantidad, 
                          boton1=self.boton1,
                          boton2=self.boton2,
                          boton3=self.boton3,
                          boton4=self.boton4,
                          boton5=self.boton5,
                          boton6=self.boton6,
                         )


        
       

    
        


