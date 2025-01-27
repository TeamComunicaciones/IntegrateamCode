from navegacion import sub_menu as sm, ventana_informacion
from recursos import label, botones, colors
from funcionalidad import web_controller, poliedro, excel
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
import pandas as pd
from selenium import webdriver

class Consulta_seriales:

    def __init__(self, master, on_of):
        self.min = ''
        self.mensaje = 's'
        self.on_of = on_of
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.link = 'https://poliedrodist.comcel.com.co/'
        self.link2 = 'https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.titulo = label.Label().create_label(master, 'CONSULTA DE SERIALES', 0.2, 0.0, 0.5, 0.2, letterSize=25)
        self.ventana_informacion = ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master, 3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.seriales = ''
        self.time = tk.StringVar()
        self.time.set('0')

    def abrir_pagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller): pass
        self.seriales = Abrir_pagina1(int(self.time.get()))
        self.seriales.openEdgeModeIE()

    def abrir_excel(self):
        self.df_imei = pd.read_excel('src/consulta_seriales/seriales.xlsx', sheet_name='IMEI')
        self.df_iccid = pd.read_excel('src/consulta_seriales/seriales.xlsx', sheet_name='ICCID')
        self.ventana_informacion.write('Excel consultado y cargado')

    def ejecuccionHilo(self):
        hilo_equipos = threading.Thread(target=self.ejecuccion)
        hilo_equipos.start()

    def ejecuccion(self):
        driver = webdriver.Edge()

        # Procesar lista IMEI
        for index, row in self.df_imei.iterrows():
            imei = row['IMEI']
            url_imei = f"https://poliedrodist.comcel.com.co/POL_REPCON/MSISDNYICCID/getConsultarIMEI?IMEI={imei}"
            driver.get(url_imei)
            response_message = driver.find_element_by_tag_name('body').text
            self.df_imei.at[index, 'Mensaje'] = response_message
            self.ventana_informacion.write(f'IMEI {imei}: {response_message}')

        # Procesar lista ICCID
        for index, row in self.df_iccid.iterrows():
            iccid = row['ICCID']
            code = self.CalculaDigitoChequeo(iccid)
            url_iccid = f"https://poliedrodist.comcel.com.co/POL_REPCON/MSISDNYICCID/getConsultarICCID?ICCID=8957101{iccid}{code}"
            driver.get(url_iccid)
            response_message = driver.find_element_by_tag_name('body').text
            self.df_iccid.at[index, 'Mensaje'] = response_message
            self.ventana_informacion.write(f'ICCID {iccid}: {response_message}')

        driver.quit()

        # Exportar resultados a Excel
        with pd.ExcelWriter('src/consulta_seriales/resultados.xlsx') as writer:
            self.df_imei.to_excel(writer, sheet_name='IMEI', index=False)
            self.df_iccid.to_excel(writer, sheet_name='ICCID', index=False)

        self.ventana_informacion.write('Resultados exportados a Excel')

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