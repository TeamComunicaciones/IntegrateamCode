from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors
from funcionalidad import  web_controller, poliedro, excel
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
import pandas as pd
import requests

class Consulta_seriales:

    def __init__(self,master, on_of):
        self.min = ''
        self.mensaje = 's'
        self.on_of = on_of
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.titulo = label.Label().create_label(master, 'CONSULTA DE SERIALES', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR LISTA', self.abrir_excel2], boton2=['START', self.ejecuccionHilo2], boton3=['GENERAR', self.ejecuccionHilo])
        # self.menu = sm.Sub_menu(master,1, boton1=['GENERAR', self.ejecuccionHilo])
        self.seriales = ''
        self.time = tk.StringVar()
        self.time.set('0')
        # self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.0, 0.65, 0.5,0.2, letterSize= 16)
        # input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        # input_widget.place(relx=0.5, rely=0.73, relheight=0.05, relwidth=0.2)
        # boton = botones.Buttons()
        # color = colors.Colors()
        # self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.73, 0.15, 0.05)
        # self.okBotton.configure(fg_color= color.team, text_color= 'white')
        self.serial1= tk.StringVar()
        self.serial2 = tk.StringVar()
        self.title_serial1 = label.Label().create_label(self.menu.submenu, 'Inicio: ', 0.0, 0.67, 0.25,0.05, letterSize= 14)
        self.title_serial2 = label.Label().create_label(self.menu.submenu, 'Final: ', 0.0, 0.74, 0.25,0.05, letterSize= 14)
        input_serial1= ctk.CTkEntry(self.menu.submenu, textvariable=self.serial1)
        input_serial1.place(relx=0.4, rely=0.67, relheight=0.05, relwidth=0.6)
        input_serial2= ctk.CTkEntry(self.menu.submenu, textvariable=self.serial2)
        input_serial2.place(relx=0.4, rely=0.74, relheight=0.05, relwidth=0.6)
    
    def abrir_pagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.seriales = Abrir_pagina1(int(self.time.get()))
        self.seriales.openEdge()
        self.seriales.selectPage(self.link)

    def abrir_excel(self):
        self.ventana_informacion.write('excel consultar seriales abierto recuerde cerrar antes de iniciar')
        p = Popen("src\consulta_seriales\openExcel.bat")
        stdout, stderr = p.communicate()

    def abrir_excel2(self):
        self.ventana_informacion.write('excel consultar seriales abierto recuerde cerrar antes de iniciar')
        p = Popen("src\consulta_seriales\openExcel2.bat")
        stdout, stderr = p.communicate()

    def ejecuccionHilo(self):
        hilo_equipos = threading.Thread(target=self.ejecuccion)
        hilo_equipos.start()

    def ejecuccionHilo2(self):
        hilo_equipos2 = threading.Thread(target=self.ejecuccion2)
        hilo_equipos2.start()

    def ejecuccion(self):  
        df = pd.DataFrame(columns=['seriales'])
        for i in range(int(self.serial1.get()), int(self.serial2.get())+1):
            df.loc[len(df)] = [f'{i}']
            self.ventana_informacion.write(f'Generando serial {i}')
            
        nombre_archivo = 'src\consulta_seriales\seriales.xlsx'
        df.to_excel(nombre_archivo, index=False)
        self.abrir_excel()
        
    
    def ejecuccion2(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        # self.poliedro.definirBrowser(self.seriales)
        # self.seriales.script("location.href='/activaciones/http/REINGENIERIA/DispatcherPoliedroRepcon/DispacherEntrada.ASP?Site=10';")
        column_types = {'Iccid': 'str', 'Imei': 'str'}
        self.excel.excel = pd.read_excel('src\consulta_seriales\seriales2.xlsx', dtype=column_types)
        self.excel.cantidad = len(self.excel.excel['Iccid'])
        self.excel.quitarFormatoCientifico('Iccid')
        self.excel.quitarFormatoCientifico('Imei')
        self.individual()
    
    def crearVariablesExcel(self,i):
        self.iccid = str(self.excel.excel['Iccid'][i])[-12:]
        self.imei = str(self.excel.excel['Imei'][i])

    def CalculaDigitoChequeo(self, textIccId):
        icc = "8957101"
        iccval = icc + textIccId
        suma = 0

        for i in range(len(iccval)):
            digito = int(iccval[-(i+1)])
            if i % 2 == 0:
                dnum = digito * 2
                if dnum >= 10:
                    suma += dnum - 9
                else:
                    suma += dnum
            else:
                suma += digito

        return (10 - (suma % 10)) % 10
        
    def individual(self):
        self.contador = 0
        self.ciclo = True
        while self.ciclo:
            if self.contador == self.excel.cantidad:
                self.ciclo = False
            else:
                try:
                    self.ventana_informacion.write(f'Consultando numero {self.contador+1} de {self.excel.cantidad}')
                    self.crearVariablesExcel(self.contador)
                    if str(self.iccid).strip() != 'nan':
                        if len(str(self.iccid)) ==12:
                            iccid = self.iccid
                            code = self.CalculaDigitoChequeo(iccid)
                            url_iccid = f"https://poliedrodist.comcel.com.co/POL_REPCON/MSISDNYICCID/getConsultarICCID?ICCID=8957101{iccid}{code}"
                            response_iccid = requests.get(url_iccid)
                            self.mensaje = response_iccid.text.replace('"','')
                            self.ventana_informacion.write(f'ICCID {iccid}: {self.mensaje}')
                        else:
                            self.mensaje = 'el iccid debe tener 12 digitos'
                    elif str(self.imei) != 'nan':
                        imei = self.imei
                        url_imei = f"https://poliedrodist.comcel.com.co/POL_REPCON/MSISDNYICCID/getConsultarIMEI?IMEI={imei.replace(' ','')}"
                        response_iccid = requests.get(url_imei)
                        self.mensaje = response_iccid.text.replace('"','')
                        self.ventana_informacion.write(f'IMEI {imei}: {self.mensaje}')
                    else:
                        self.mensaje = 'no detecta ni iccid ni imei'
                    self.excel.guardar(self.contador, 'Mensaje', self.mensaje, 'src\consulta_seriales\seriales2.xlsx')
                    self.contador += 1
                except:
                    self.ventana_informacion.write(f'Siguiente por error en portabilidad de {self.min}')
                    self.excel.guardar(self.contador, 'Mensaje', 'error', destino='src\consulta_seriales\seriales2.xlsx')
                    self.contador += 1
        self.abrir_excel2()


    # def individual(self):
    #     self.contador = 0
    #     self.ciclo = True
    #     while self.ciclo:
    #         if self.contador == self.excel.cantidad:
    #             self.ciclo = False
    #         else:
    #             try:
    #                 self.ventana_informacion.write(f'Consultando numero {self.contador+1} de {self.excel.cantidad}')
    #                 self.crearVariablesExcel(self.contador)
    #                 if str(self.iccid).strip() != 'nan':
    #                     if len(str(self.iccid)) ==12:
    #                         self.seriales.eraseLetter('IccDig', 20, 'id')
    #                         self.seriales.insert('IccDig', self.iccid, 'id')
    #                         self.seriales.script('validIcc()')
    #                         time.sleep(0.1)
    #                         self.mensaje = self.seriales.read('/html/body/div/div[2]/section/div/div[2]/div/div[3]/main/div[2]/div/div[1]/p')
    #                         self.seriales.click('btnCerrar', 'id')
    #                     else:
    #                         self.mensaje = 'el iccid debe tener 12 digitos'
    #                 elif str(self.imei) != 'nan':
    #                     self.seriales.eraseLetter('imeiEstado', 20, 'id')
    #                     self.seriales.insert('imeiEstado', self.imei, 'id')
    #                     self.seriales.script('validImei();')
    #                     time.sleep(0.3)
    #                     self.mensaje = self.seriales.read('/html/body/div/div[2]/section/div/div[2]/div/div[3]/main/div[2]/div/div[1]/p[2]')
    #                     self.seriales.click('btnCerrar', 'id')
    #                 else:
    #                     self.mensaje = 'no detecta ni iccid ni imei'
    #                 self.ventana_informacion.write(self.mensaje)
    #                 self.excel.guardar(self.contador, 'Mensaje', self.mensaje, 'src\consulta_seriales\seriales2.xlsx')
    #                 self.contador += 1
    #             except:
    #                 self.ventana_informacion.write(f'Siguiente por error en portabilidad de {self.min}')
    #                 self.excel.guardar(self.contador, 'Mensaje', 'error', destino='src\consulta_seriales\seriales2.xlsx')
    #                 self.contador += 1
    #     self.abrir_excel2()
