from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors
from funcionalidad import  web_controller, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
from datetime import datetime
import pandas as pd


class Inventario_postpago:

    def __init__(self,master, on_of):
        self.on_of = on_of
        self.titulo = label.Label().create_label(master, 'INVENTARIO POSTPAGO', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.link= 'https://190.144.217.66/Front_PortalComercial/controlseguridad/login-dos.asp'
        self.link2='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_factura.asp'
        self.link3='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_seriales_factura.asp'
        self.menu = sm.Sub_menu(master,2, boton1=['START', self.ejecuccionHilo], boton2=['Sucursales', self.abrir_excel2])
        self.compras = ''
        self.entry_user = tk.StringVar()
        self.entry_password = tk.StringVar()
        self.entry_first_date = tk.StringVar()
        self.entry_last_Date = tk.StringVar()
        self.title_user = label.Label().create_label(self.menu.submenu, 'Usuario: ', 0.0, 0.32, 0.3,0.2, letterSize= 14)
        self.title_password = label.Label().create_label(self.menu.submenu, 'Clave: ', 0.0, 0.45, 0.25,0.05, letterSize= 14)
        # self.title_first_date = label.Label().create_label(self.menu.submenu, 'Fecha inicial: ', 0.0, 0.39, 0.45,0.05, letterSize= 14)
        # self.title_last_date = label.Label().create_label(self.menu.submenu, 'Fecha final: ', 0.0, 0.46, 0.4,0.05, letterSize= 14)
        input_user= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_user)
        input_user.place(relx=0.4, rely=0.40, relheight=0.05, relwidth=0.6)
        input_password= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_password)
        input_password.place(relx=0.4, rely=0.46, relheight=0.05, relwidth=0.6)
        # input_first_date= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_first_date)
        # input_first_date.place(relx=0.4, rely=0.39, relheight=0.05, relwidth=0.6)
        # input_last_date= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_last_Date)
        # input_last_date.place(relx=0.4, rely=0.46, relheight=0.05, relwidth=0.6)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.excel = excel.Excel_controller()
    
    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()
    
    def abrir_excel(self):
        self.ventana_informacion.write('Abriendo resultado en Excel')
        p = Popen("src\inventario_postpago\openExcel.bat")
        stdout, stderr = p.communicate()
    
    def abrir_excel2(self):
        self.ventana_informacion.write('Abriendo codigos sucursales en Excel')
        p = Popen("src\inventario_postpago\openExcel2.bat")
        stdout, stderr = p.communicate()
        
    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        self.abrirPagina()
        try:
            self.getFacturasScraping()
            # self.getSerialesScraping()
        except Exception as e:
            self.ventana_informacion.write(f'error, se detiene el programa')
            raise Exception('error')
        # self.organizarData()
        # self.on_of(True)
    
    def abrirPagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.compras = Abrir_pagina1(0)
        self.compras.openEdge(headless=False)
        self.compras.selectPage(self.link)
        self.compras.click('details-button','id')
        self.compras.click('proceed-link','id')
        self.compras.insert('/html/body/section/form/input[1]', self.entry_user.get())
        self.compras.insert('password', self.entry_password.get(), 'id')
        # self.compras.insert('/html/body/section/form/input[1]', '39421730')
        # self.compras.insert('password', 'team10', 'id')
        self.compras.insert('SelServicio', 'Inventario Equipos', 'id')
        self.compras.click('/html/body/section/form/button')
        self.compras.click('Button2', 'id')
    
    def consultarFacturas(self):
        self.compras.selectPage(self.link2)
        self.compras.insert('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[1]/select', 'Factura')
        self.compras.insert('FecIni', self.entry_first_date.get(), 'id')
        self.compras.insert('FecFin', self.entry_last_Date.get(), 'id')
        self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td[1]/table/tbody/tr/td[4]/input')
        data=self.compras.wait('/html/body/form/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td/div/table/tbody/tr/td', 'Informe los campos del filtro para hacer la seleccion')

    def getFacturasScraping(self):
        self.excel.leer_excel('src\inventario_postpago\codigos_sucursales.xlsx','Codigo')
        sucursales = { self.excel.excel['Codigo'][i]: self.excel.excel['Sucursal'][i] for i in range(len(self.excel.excel))}
        

        self.ventana_informacion.write('Seleccionando')
        cantidadFacturas = self.compras.read('/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/table[1]/tbody/tr/td/table[2]/tbody/tr/td')
        self.cantidadFacturas = cantidadFacturas.replace('Total registros: ', '')
        html = self.compras.retornarHtml()
        soup = scraping.Scraping(html)
        data = soup.extrarDataTablas()
        for i in range(1, int(self.cantidadFacturas)+1):
            self.compras.click(f'/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/table[1]/tbody/tr/td/div/table/tbody/tr[{i}]/td[1]/input')
        self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/table[2]/tbody/tr/td/input')
        self.compras.browser.switch_to_alert().accept()
        self.diccionario_txt = []
        for i in range(1, int(self.cantidadFacturas)+1):
            self.compras.click_ctr(f'/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td/table[2]/tbody/tr/td/a[{i}]')
            self.compras.cambiar_pestaña()
            data_txt = self.compras.leer_txt()
            self.compras.cerrar_pestaña()
            self.compras.volver_pestaña()
            lineas = data_txt.split('\n')
            datos_txt = [linea.split(';') for linea in lineas]
            if i == 1:
                self.diccionario_txt.append(datos_txt[0])
                self.diccionario_txt[0].append('SUCURSAL')
            for j in range(1, len(datos_txt)):
                datos_txt[j][4] = datos_txt[j][4].lstrip('0')
                datos_txt[j][5] = datos_txt[j][5].lstrip('0')
                try:
                    datos_txt[j].append(sucursales[datos_txt[j][0]])
                except:
                    datos_txt[j].append('Codigo sin registrar')
                self.diccionario_txt.append(datos_txt[j])
        self.compras.cerrar()
        self.excel.export(self.diccionario_txt, 'src\inventario_postpago\\inventario_postpago.xlsx')
        self.abrir_excel()