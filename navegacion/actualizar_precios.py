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
import traceback

class Actualizar_precios:

    def __init__(self,master, on_of):
        self.on_of = on_of
        self.titulo = label.Label().create_label(master, 'ACTUALIZAR PRECIOS', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.link= 'https://ventas-dot-krediapp-colombia.uw.r.appspot.com/auth/login'
        self.link2='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_factura.asp'
        self.link3='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_seriales_factura.asp'
        self.menu = sm.Sub_menu(master, 2, boton1=['START', self.ejecuccionHilo], boton2=['EXCEL', self.abrir_excel])
        self.compras = ''
        self.entry_user = tk.StringVar()
        self.entry_password = tk.StringVar()
        self.entry_first_date = tk.StringVar()
        self.entry_last_Date = tk.StringVar()
        self.title_user = label.Label().create_label(self.menu.submenu, 'Usuario: ', 0.0, 0.50, 0.3,0.2, letterSize= 14)
        self.title_password = label.Label().create_label(self.menu.submenu, 'Clave: ', 0.0, 0.65, 0.25,0.05, letterSize= 14)
        input_user= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_user)
        input_user.place(relx=0.4, rely=0.58, relheight=0.05, relwidth=0.6)
        input_password= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_password)
        input_password.place(relx=0.4, rely=0.65, relheight=0.05, relwidth=0.6)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.excel = excel.Excel_controller()

    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()

    def abrir_excel(self):
        self.ventana_informacion.write('Abriendo resultado en Excel')
        p = Popen("src\\actualizar_precios\\openExcel.bat")
        stdout, stderr = p.communicate()

    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        try:
            self.abrirPagina()
        except Exception as e:
            error_completo = traceback.format_exc()
            self.ventana_informacion.write(f'ERROR CRÍTICO:\n{error_completo}')
        finally:
            self.on_of(True)
            self.ventana_informacion.write('Proceso finalizado.')

    def abrirPagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.compras = Abrir_pagina1(0)
        self.compras.openEdge()
        self.compras.selectPage(self.link)
        self.compras.insert('/html/body/app-root/app-tpl-login/div/div/div/div/app-login/form/div/div/div[2]/div/span[2]/input', self.entry_user.get())
        self.compras.insert('/html/body/app-root/app-tpl-login/div/div/div/div/app-login/form/div/div/div[3]/div/span[2]/input', self.entry_password.get())
        self.compras.click('/html/body/app-root/app-tpl-login/div/div/div/div/app-login/form/div/div/div[4]/div[1]/button/span')
        self.compras.click('/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-home/div/div/div[3]/div[2]/div/button')
        self.compras.click('/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-product-batch-edit/div/div[2]/div[2]/button')
        time.sleep(5)
        html = self.compras.retornarHtml()
        soup = scraping.Scraping(html)
        data = soup.extrarDataTablas()

        productos = {data[row][1]:{'id': row, 'nombre': data[row][2], 'minimo': data[row][3], 'maximo': data[row][-1] } for row in range(len(data)) if row !=0}

        self.excel.leer_excel('src\\actualizar_precios\\actualizar_precios.xlsx','codigo')
        lista_productos = [{'codigo':self.excel.excel['codigo'][i], 'precio':self.excel.excel['Precio'][i]} for i in range(len(self.excel.excel))]

        codigos_en_excel = {str(item['codigo']) for item in lista_productos}

        for row in range(len(lista_productos)):
            self.ventana_informacion.write(f'Procesando registro {row + 1} de {len(lista_productos)}')
            i = lista_productos[row]
            
            codigo = str(i['codigo'])
            precio = i['precio']

            nombre_col_resultado = 'Resultado Ejecucion'

            if codigo in productos.keys():
                linea = productos[codigo]['id']
                minimo = productos[codigo]['minimo'].replace('$\xa0','').replace(',00','').replace('.','')
                maximo = productos[codigo]['maximo'].replace('$\xa0','').replace(',00','').replace('.','')
                
                if precio >= int(minimo) and precio <= int(maximo):
                    xpath_checkbox = f'/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-product-batch-edit-by-product/div/div[3]/form/div/div[1]/p-table/div/div/table/tbody/tr[{linea}]/td[1]/p-checkbox/div/div[2]'
                    self.compras.js_click(xpath_checkbox)

                    self.compras.insert( f'/html/body/app-root/app-tpl-logged-in/div/div[2]/div/app-product-batch-edit-by-product/div/div[3]/form/div/div[1]/p-table/div/div/table/tbody/tr[{linea}]/td[5]/div/p-inputnumber/span/input', str(precio), enter=True)
                    self.excel.guardar(row, nombre_col_resultado, 'exitosa', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                else:
                    texto = f'{precio} no esta dentro del rango {minimo} a {maximo}'
                    self.excel.guardar(row, nombre_col_resultado, texto, destino='src\\actualizar_precios\\actualizar_precios.xlsx')
            else:
                self.excel.guardar(row, nombre_col_resultado, 'codigo no encontrado en la pagina', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
        
        self.ventana_informacion.write('Verificando productos de la pagina sin correspondencia en Excel...')
        cantidad = len(lista_productos)
        for codigo_pagina, datos_producto in productos.items():
            if codigo_pagina not in codigos_en_excel:
                nombre_producto = datos_producto['nombre']
                self.excel.guardar(cantidad, 'codigo', codigo_pagina, destino='src\\actualizar_precios\\actualizar_precios.xlsx', nuevo=True)
                self.excel.guardar(cantidad, 'Producto', nombre_producto, destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                self.excel.guardar(cantidad, nombre_col_resultado, 'producto en pagina pero no en excel', destino='src\\actualizar_precios\\actualizar_precios.xlsx')
                cantidad += 1

        self.abrir_excel()