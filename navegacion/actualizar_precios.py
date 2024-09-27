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


class Actualizar_precios:

    def __init__(self,master, on_of):
        self.on_of = on_of
        self.titulo = label.Label().create_label(master, 'ACTUALIZAR PRECIOS', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.link= 'https://ventas-dot-krediapp-colombia.uw.r.appspot.com/auth/login'
        self.link2='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_factura.asp'
        self.link3='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_seriales_factura.asp'
        self.menu = sm.Sub_menu(master,3, boton1=['START', self.ejecuccionHilo], boton2=['EXCEL', self.abrir_excel], boton3=['TRADUCCION', self.abrir_excel2])
        self.compras = ''
        self.entry_user = tk.StringVar()
        self.entry_password = tk.StringVar()
        self.entry_first_date = tk.StringVar()
        self.entry_last_Date = tk.StringVar()
        self.title_user = label.Label().create_label(self.menu.submenu, 'Usuario: ', 0.0, 0.50, 0.3,0.2, letterSize= 14)
        self.title_password = label.Label().create_label(self.menu.submenu, 'Clave: ', 0.0, 0.65, 0.25,0.05, letterSize= 14)
        # self.title_first_date = label.Label().create_label(self.menu.submenu, 'Fecha inicial: ', 0.0, 0.39, 0.45,0.05, letterSize= 14)
        # self.title_last_date = label.Label().create_label(self.menu.submenu, 'Fecha final: ', 0.0, 0.46, 0.4,0.05, letterSize= 14)
        input_user= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_user)
        input_user.place(relx=0.4, rely=0.58, relheight=0.05, relwidth=0.6)
        input_password= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_password)
        input_password.place(relx=0.4, rely=0.65, relheight=0.05, relwidth=0.6)
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
        self.ventana_informacion.write('Abriendo resultado en Excels')
        p = Popen("src\\actualizar_precios\\openExcel.bat")
        stdout, stderr = p.communicate()

    def abrir_excel2(self):
        self.ventana_informacion.write('Abriendo resultado en Excels')
        p = Popen("src\\actualizar_precios\\openExcel2.bat")
        stdout, stderr = p.communicate()
        
    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        try:
            self.abrirPagina()
        except Exception as e:
            self.ventana_informacion.write(f'error: {e}')
    
    def abrirPagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.compras = Abrir_pagina1(0)
        self.compras.openEdge()
        self.compras.selectPage(self.link)
        # self.entry_user.set('controlinterno2@teamcomunicaciones.com')
        # self.entry_password.set('douh5')
        self.compras.insert('/html/body/app-root/app-tpl-login/div/div/div/div/app-login/form/div/div/div[2]/div/span[2]/input', self.entry_user.get())
        self.compras.insert('/html/body/app-root/app-tpl-login/div/div/div/div/app-login/form/div/div/div[3]/div/span[2]/input', self.entry_password.get())
        self.compras.click('/html/body/app-root/app-tpl-login/div/div/div/div/app-login/form/div/div/div[4]/div[1]/button/span')
        self.compras.click('/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-home/div/div/div[3]/div[2]/div/button')
        self.compras.click('/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-product-batch-edit/div/div[2]/div[2]/button')
        time.sleep(5)
        html = self.compras.retornarHtml()
        soup = scraping.Scraping(html)
        data = soup.extrarDataTablas()
        productos = {data[row][2]:{'id': row, 'minimo': data[row][3], 'maximo': data[row][-1] } for row in range(len(data)) if row !=0}

        self.excel.leer_excel('src\\actualizar_precios\\actualizar_precios.xlsx','Producto')
        lista_productos = [{'producto':self.excel.excel['Producto'][i], 'precio':self.excel.excel['Precio'][i]} for i in range(len(self.excel.excel))]
        self.excel.leer_excel('src\\actualizar_precios\\traduccion.xlsx','Pagina')
        traducciones = { self.excel.excel['Stock'][i]: self.excel.excel['Pagina'][i] for i in range(len(self.excel.excel))}
        for row in range(len(lista_productos)):
            self.ventana_informacion.write(f'procesando registro {row} de {len(lista_productos)}')
            i = lista_productos[row]
            producto = traducciones[i['producto']]
            precio = i['precio']
            linea = productos[producto]['id']
            minimo = productos[producto]['minimo'].replace('$\xa0','').replace(',00','').replace('.','')
            maximo = productos[producto]['maximo'].replace('$\xa0','').replace(',00','').replace('.','')
            self.excel.leer_excel('src\\actualizar_precios\\actualizar_precios.xlsx','Producto')
            if producto in productos.keys():
                if precio >= int(minimo) and precio <= int(maximo):
                    self.compras.click(f'/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-product-batch-edit-by-product/div/div[3]/form/div/div[1]/p-table/div/div/table/tbody/tr[{linea}]/td[1]/p-checkbox/div/div[2]')
                    # self.compras.eraseLetter(f'/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-product-batch-edit-by-product/div/div[3]/form/div/div[1]/p-table/div/div/table/tbody/tr[{linea}]/td[5]/div/p-inputnumber/span/input', 25)
                    self.compras.insert( f'/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-product-batch-edit-by-product/div/div[3]/form/div/div[1]/p-table/div/div/table/tbody/tr[{linea}]/td[5]/div/p-inputnumber/span/input', str(precio), enter=True)
                    self.excel.guardar(row, 'Resultado', 'exitosa', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                else:
                    texto = f'{precio} no esta dentro del rango {minimo} a {maximo}'
                    self.excel.guardar(row, 'Resultado', texto, destino='src\\actualizar_precios\\actualizar_precios.xlsx')
            else:
                self.excel.guardar(row, 'Producto', producto, destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                self.excel.guardar(row, 'Resultado', 'producto no en la lista de la pagina', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
        cantidad = self.excel.cantidad
        for i in productos.keys():
            if i not in traducciones.values():
                self.excel.guardar(cantidad, 'Producto', i, destino='src\\actualizar_precios\\actualizar_precios.xlsx', nuevo=True)
                self.excel.guardar(cantidad, 'Resultado', 'producto sin traduccion', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                cantidad += 1
        self.abrir_excel()