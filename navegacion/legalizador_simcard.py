'''
45972161
Asesor%%31

legalizacion de simcard
abre poliedro
actualizacion IVR
tecnologia IVR gsm
ingresamos min
Ingresamos 12 digitos ICCID
cedula vendedor
damos ingresar
si ya esta sale min ya el proceso sino sigue y rellena
cedula
nombre
apellidos
presiona reconocer si no tiene info toca llenarla

direccion otras
ciudad medellin
depar antioquia
saludo por lo general no necesita los otros datos 
nro centro
telefono se consulta excel
modelo equipo cualquiera
dijin 1234
presiona guardar
y queda en el mensaje que salia si ya esta legalizado para pasar con el siguiente
'''


'''
legalizacion de simcard  tropas y solo con min
abre poliedro
click parte azul nuevo
actualizacion IVR diferente
digite min nuevo diferente
damos ingresar diferente
revisar lo del telefono si es diferente
si ya esta sale min ya el proceso sino sigue y rellena
cedula
nombre
apellidos
presiona reconocer si no tiene info toca llenarla
direccion otras
ciudad medellin
depar antioquia
saludo por lo general no necesita los otros datos 
nro centro
telefono se consulta excel
modelo equipo cualquiera
dijin 1234
presiona guardar
y queda en el mensaje que salia si ya esta legalizado para pasar con el siguiente
'''


from navegacion import sub_menu as sm, ventana_informacion 
from funcionalidad import  web_controller, poliedro, excel, clickImage
from recursos import botones, label, checkbox, colors
import threading
from subprocess import Popen
import pyperclip
from datetime import datetime, timedelta
import time
import tkinter as tk
import customtkinter as ctk


class Legalizador_sims:

    def __init__(self, master, on_of):
        self.pagina = ''
        self.on_of = on_of
        self.errorCorreo=False
        self.master = master
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.label = label.Label().create_label(master, 'Legalizador Sims', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.submenu= sm.Sub_menu(master, 3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.time = tk.StringVar()
        self.time.set('0')
        boton = botones.Buttons()
        color = colors.Colors()
        self.checkbox = checkbox.Checkbox()
        self.checkbox2 = checkbox.Checkbox()
        self.checkbox_var = tk.BooleanVar()
        self.tropas = tk.BooleanVar()
        self.validacionImgs = tk.BooleanVar()  
        self.checkbox_tropas =  checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Tropas.', self.on_checkbox_change_tropas, self.tropas)
    
    def on_checkbox_change_tropas(self):
        if self.tropas.get():
            self.ventana_informacion.write('Cambiando modalidad a Tropas')
        else:
            self.ventana_informacion.write('Cambiando modalidad a Estandar')
        self.poliedro.manejoTropas(self.tropas.get())

    def abrir_pagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.legalizador = Abrir_pagina1(int(self.time.get()))
        self.legalizador.openEdge()
        self.legalizador.selectPage(self.link)
    
    def abrir_excel(self):
        self.ventana_informacion.write('excel legalizador sims abierto recuerde cerrar antes de iniciar')
        p = Popen("src\legalizador_sims\openExcel.bat")
        stdout, stderr = p.communicate()
    
    def ejecuccionHilo(self):
        hilo_equipos = threading.Thread(target=self.ejecuccion)
        hilo_equipos.start()
    
    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        self.poliedro.definirBrowser(self.legalizador)
        self.individual()
    
    def insert(self, xpath, value):
        self.legalizador.eraseLetter(xpath, 20)
        self.legalizador.insert(xpath, value)
    
    def individual(self):
        self.min = '3232907895'
        self.iccid = '602510129972'
        self.ccVendedor = '1128272343'
        self.ccCliente = '1036601050'
        self.nombre = 'ANA'
        self.apellido = 'ESCOBAR'
        # acceder
        self.legalizador.click('/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[23]')
        self.legalizador.click('/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[24]/div[1]/a')
        #consulta
        self.insert('/html/body/p/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[1]/div/table/tbody/tr/td/form/table/tbody/tr[1]/td[2]/input', self.min)
        self.insert('/html/body/p/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[1]/div/table/tbody/tr/td/form/table/tbody/tr[2]/td[2]/input', self.iccid)
        self.insert('/html/body/p/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[1]/div/table/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input', self.ccVendedor)
        self.legalizador.click('/html/body/p/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[2]/td[1]/div/table/tbody/tr/td/form/table/tbody/tr[4]/td/div/input')
        #validacion
        self.insert('/html/body/form/div/dd/table[3]/tbody/tr[1]/td[3]/input', self.ccCliente)
        self.insert('/html/body/form/div/dd/table[3]/tbody/tr[1]/td[5]/input', self.nombre)
        self.insert('/html/body/form/div/dd/table[3]/tbody/tr[1]/td[4]/input', self.apellido)
        self.legalizador.click('/html/body/form/div/dd/table[4]/tbody/tr/td[1]/input[13]')
        #saludo
        self.legalizador.click('/html/body/form/div/dd/table[3]/tbody/tr[1]/td[1]/select')
        self.legalizador.selectDown('/html/body/form/div/dd/table[3]/tbody/tr[1]/td[1]/select')
        #direccion
        self.legalizador.click('/html/body/form/div/dd/table[3]/tbody/tr[2]/td[1]/nobr/select')
        self.legalizador.insert('/html/body/form/div/dd/table[3]/tbody/tr[2]/td[1]/nobr/select', 'o', enter=True)
        self.legalizador.insert('/html/body/form/div/dd/table[3]/tbody/tr[2]/td[3]/input[2]', 'centro')
        self.legalizador.insert('/html/body/form/div/dd/table[3]/tbody/tr[2]/td[4]/input', '6046679')
        self.legalizador.insert('/html/body/form/div/dd/table[3]/tbody/tr[3]/td[1]/input', 'medellin')
        self.legalizador.insert('/html/body/form/div/dd/table[3]/tbody/tr[3]/td[2]/b/input', 'antioquia')
        #equipo
        self.legalizador.click('/html/body/form/div/dd/table[3]/tbody/tr[3]/td[3]/select')
        self.legalizador.selectDown('/html/body/form/div/dd/table[3]/tbody/tr[3]/td[3]/select')
        self.legalizador.insert('/html/body/form/div/dd/table[3]/tbody/tr[3]/td[4]/input', '1234')
        self.legalizador.click('/html/body/form/div/dd/table[4]/tbody/tr/td[1]/input[16]')

    
    
