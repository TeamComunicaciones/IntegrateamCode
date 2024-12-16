from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors, checkbox
from funcionalidad import  web_controller, poliedro, excel
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time

class Preactivador:

    def __init__(self,master, on_of, alertas):
        self.alertas = alertas
        self.min = ''
        self.etapa = 0
        self.mensaje = 's'
        self.on_of = on_of
        self.time2 = 3
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.titulo = label.Label().create_label(master, 'PREACTIVADOR DE SIM', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.preactivador = ''
        self.time = tk.StringVar()
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.0, 0.60, 0.5,0.2, letterSize= 16)
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.5, rely=0.68, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.68, 0.15, 0.05, self.cambioIntervalo)
        self.okBotton.configure(fg_color= color.team, text_color= 'white')
        # self.correo = 'correo'
        # self.correoEdit = tk.StringVar()
        # self.correoEdit.set(self.correo) 
        # input_widget2 = ctk.CTkEntry(self.menu.submenu, textvariable=self.correoEdit)
        # input_widget2.place(relx=0.15, rely=0.89, relheight=0.05, relwidth=0.7)
        # self.okBotton2 = boton.create_button(self.menu.submenu, 'confirmar', 0.3, 0.95, 0.40, 0.05, self.cambioCorreo)
        # self.okBotton2.configure(fg_color= color.team, text_color= 'white')

        self.cedula = 'cedula'
        # self.cedulaEdit = tk.StringVar()
        # self.cedulaEdit.set(self.cedula) 
        # input_widget3 = ctk.CTkEntry(self.menu.submenu, textvariable=self.cedulaEdit)
        # input_widget3.place(relx=0.1, rely=0.74, relheight=0.05, relwidth=0.5)
        # self.okBotton3 = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.74, 0.15, 0.05, self.cambioCedula)
        # self.okBotton3.configure(fg_color= color.team, text_color= 'white')

        self.correo = 'correo'
        self.correoEdit = tk.StringVar()
        self.correoEdit.set(self.correo) 
        input_widget2 = ctk.CTkEntry(self.menu.submenu, textvariable=self.correoEdit)
        input_widget2.place(relx=0.1, rely=0.80, relheight=0.05, relwidth=0.5)
        self.okBotton2 = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.80, 0.15, 0.05, self.cambioCorreo)
        self.okBotton2.configure(fg_color= color.team, text_color= 'white')

        # self.nit = 'nit o cc'
        # self.nitEdit = tk.StringVar()
        # self.nitEdit.set(self.nit) 
        # input_widget1 = ctk.CTkEntry(self.menu.submenu, textvariable=self.nitEdit)
        # input_widget1.place(relx=0.1, rely=0.86, relheight=0.05, relwidth=0.5)
        # self.okBotton1 = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.86, 0.15, 0.05, self.cambioNit)
        # self.okBotton1.configure(fg_color= color.team, text_color= 'white')
        
        self.tropas = tk.BooleanVar()
        self.checkbox_tropas =  checkbox.Checkbox().create_checkbox(self.menu.submenu, 'Tropas.', self.on_checkbox_change_tropas, self.tropas)
       
    def on_checkbox_change_tropas(self):
        if self.tropas.get():
            self.ventana_informacion.write('Cambiando modalidad a Tropas')
        else:
            self.ventana_informacion.write('Cambiando modalidad a Estandar')
        self.poliedro.manejoTropas(self.tropas.get())
        
    
    def abrir_excel(self):
        self.ventana_informacion.write('excel preactivador abierto recuerde cerrar antes de iniciar')
        p = Popen("src\preactivador\openExcel.bat")
        stdout, stderr = p.communicate()
    
    # def cambioCedula(self):
    #     self.cedula = self.cedulaEdit.get()
    #     self.ventana_informacion.write(f'Cedula actualizada por {self.cedulaEdit.get()}')
    
    def cambioNit(self):
        self.nit = self.nitEdit.get()
        self.ventana_informacion.write(f'Nit actualizada por {self.nitEdit.get()}')
    
    def cambioIntervalo(self):
        self.preactivador.actualizarIntervalo(self.time.get())
        self.ventana_informacion.write(f'intervalo {self.time.get()} segundos')

    def cambioCorreo(self):
        self.correo = self.correoEdit.get()
        self.ventana_informacion.write(f'Correo actualizado por {self.correo}')
    
    def abrir_pagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.preactivador = Abrir_pagina1(int(self.time.get()))
        self.preactivador.openEdge()
        self.preactivador.selectPage(self.link)
    
    def ejecuccionHilo(self):
        hilo_equipos = threading.Thread(target=self.ejecuccion)
        hilo_equipos.start()
        
    def ejecuccion(self):
        try:
            self.on_of(False)
            self.ventana_informacion.write('Empezando ejecuccion')
            self.poliedro.definirBrowser(self.preactivador)
            self.poliedro.seleccionAcceso('195')
            self.excel.leer_excel('src\preactivador\preactivador.xlsx','Iccid')
            self.excel.quitarFormatoCientifico('Iccid')
            self.ciclo = True
            self.contador = 0

            while self.ciclo:
                if self.contador == self.excel.cantidad:
                    self.ciclo = False
                else:
                    self.min= str(self.excel.excel['Min'][self.contador])
                    if str(self.min) != 'nan':
                            self.ventana_informacion.write(f'Preactivación ya realizada')
                            self.contador += 1
                    else:
                        self.mensaje = ''
                        self.min = ''
                        self.EquiposInd()
            self.ventana_informacion.write('Proceso terminado')
            self.on_of(True)
        except:
            self.alertas('se detiene el programa error')
    

    def EquiposInd(self):
        self.ventana_informacion.write(f'Activando Equipo {self.contador+1} de {self.excel.cantidad}')
        self.iccid = str(self.excel.excel['Iccid'][self.contador])[-12:] 
        self.nit = str(self.excel.excel['Nit'][self.contador])
        self.cedula_excel = str(self.excel.excel['Cedula'][self.contador])
        
        try:
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[1]/div/span/span[1]/span/span[1]')
            self.preactivador.click('/html/body/span/span/span[2]/ul/li[3]')
            self.preactivador.eraseLetter('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input',20, self.nit)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input', self.nit)
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[4]/div[1]/div/span/span[1]/span/span[1]')
            self.preactivador.click('/html/body/span/span/span[2]/ul/li[2]')
            self.preactivador.eraseLetter('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[4]/div[3]/div/input',20, self.iccid)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[4]/div[3]/div/input', self.iccid)
            self.preactivador.eraseLetter('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[2]/div/div[1]/div/input', 20, self.cedula_excel)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[2]/div/div[1]/div/input', self.cedula_excel)
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[5]/input[1]')
            self.etapa = 1
            self.poliedro.detectOption([['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[4]/ul/li']], [self.errorPrincipal], NoneFunc=self.siguiente)
            



        except:
            self.ventana_informacion.write(f'Activacion erronea de equipo {self.iccid}')
            self.poliedro.reinicio()
            self.contador += 1
    
    def siguiente(self):
        self.preactivador.waitExist2('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
        optionsList = [
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span'],
        ]
        funcionList = [
            self.terminarActivacion
        ]
        self.poliedro.detectOption(optionsList, funcionList, NoneFunc=self.errorValidacion)
    
    def errorPrincipal(self):
        self.ventana_informacion.write(f'Activacion erronea de equipo {self.iccid}')
        self.reinicio()
        self.contador += 1
        self.min = ''
        self.mensaje = self.preactivador.readNoValidate('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[4]/ul/li')
        self.guardarData()
        

    def errorValidacion(self):
        self.ventana_informacion.write(f'Activacion erronea de equipo {self.iccid}')
        self.reinicio()
        self.contador += 1
        # self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
        # self.preactivador.erase('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[3]/div[3]/div/input')
        # self.preactivador.erase('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input')
        self.min = ''
        self.mensaje = 'Error en activacion'
        self.guardarData()
    
    def terminarActivacion(self):
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[3]')
        self.etapa = 2
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[1]/div/span/span[1]/span/span[1]')
        self.preactivador.click('/html/body/span/span/span[2]/ul/li[2]')
        self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[4]/div/input', self.correo)
        time.sleep(2)
        #telefono
        try:
            self.preactivador.waitExist2('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/select')
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/select', 'fijo')
            time.sleep(2)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select', '604')
            time.sleep(2)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
            time.sleep(2)
        except: pass
        #direccion
        try:
            self.preactivador.waitExist2('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select')
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', 'Otras')
            time.sleep(2)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'CENTRO')
            time.sleep(2)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[3]/div/select','ANTIOQUIA')
            time.sleep(4)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[4]/div/select', 'MEDELLIN')
            time.sleep(2)
            self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'CENTRO')
            time.sleep(2)
        except: pass
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]')
        self.etapa = 3
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]')
        self.preactivador.click('/html/body/span/span/span[2]/ul/li[2]')
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
        self.preactivador.click('/html/body/span/span/span[2]/ul/li[2]')
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]')
        self.etapa = 4
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
        self.etapa = 5
        self.min = self.preactivador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p/strong[3]')
        self.min = self.min[-10:]
        self.mensaje = ''
        time.sleep(0.5)
        self.ventana_informacion.write(f'Activacion exitosa de equipo {self.iccid}')
        self.guardarData()
        self.reinicio()
        self.contador += 1
        # self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[1]')
        # self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[1]/div[1]/div[1]/div/div/ul/li[1]/span/input')
        # self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[2]/div/div[1]/div/input', '1010014821')


    def guardarData(self):
        self.excel.guardar(self.contador, 'Min', self.min, 'src\preactivador\preactivador.xlsx')
        self.excel.guardar(self.contador, 'Mensaje', self.mensaje, 'src\preactivador\preactivador.xlsx')

    def reinicio(self):
        if self.etapa == 0:
            pass
        if self.etapa == 5:
            time.sleep(self.time2)
            self.preactivador.click('btnPrev', 'id')
            self.poliedro.seleccionAcceso('195', start=False)
        else:
            for i in range(self.etapa):
                time.sleep(self.time2)
                self.preactivador.click('btnPrev', 'id')
        self.etapa == 0