from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors
from funcionalidad import  web_controller, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
from datetime import datetime


class Compras:

    def __init__(self,master, on_of):
        self.on_of = on_of
        self.titulo = label.Label().create_label(master, 'COMPRAS CONTROL INTERNO', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.link= 'https://190.144.217.66/Front_PortalComercial/controlseguridad/login-dos.asp'
        self.link2='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_factura.asp'
        self.link3='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_seriales_factura.asp'
        self.menu = sm.Sub_menu(master,1, boton1=['START', self.ejecuccionHilo])
        self.compras = ''
        self.entry_user = tk.StringVar()
        self.entry_password = tk.StringVar()
        self.entry_first_date = tk.StringVar()
        self.entry_last_Date = tk.StringVar()
        self.title_user = label.Label().create_label(self.menu.submenu, 'Usuario: ', 0.0, 0.18, 0.3,0.2, letterSize= 14)
        self.title_password = label.Label().create_label(self.menu.submenu, 'Clave: ', 0.0, 0.32, 0.25,0.05, letterSize= 14)
        self.title_first_date = label.Label().create_label(self.menu.submenu, 'Fecha inicial: ', 0.0, 0.39, 0.45,0.05, letterSize= 14)
        self.title_last_date = label.Label().create_label(self.menu.submenu, 'Fecha final: ', 0.0, 0.46, 0.4,0.05, letterSize= 14)
        input_user= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_user)
        input_user.place(relx=0.4, rely=0.25, relheight=0.05, relwidth=0.6)
        input_password= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_password)
        input_password.place(relx=0.4, rely=0.32, relheight=0.05, relwidth=0.6)
        input_first_date= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_first_date)
        input_first_date.place(relx=0.4, rely=0.39, relheight=0.05, relwidth=0.6)
        input_last_date= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_last_Date)
        input_last_date.place(relx=0.4, rely=0.46, relheight=0.05, relwidth=0.6)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.excel = excel.Excel_controller()
    
    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()
    
    def abrir_excel(self):
        self.ventana_informacion.write('Abriendo resultado en Excels')
        p = Popen("src\compras\openExcel.bat")
        stdout, stderr = p.communicate()
        
    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        self.abrirPagina()
        self.consultarFacturas()
        try:
            self.getFacturasScraping()
            self.getSerialesScraping()
        except Exception as e:
            self.ventana_informacion.write(f'error, se detiene el programa: {e}')
            raise Exception('error')
        self.organizarData()
        self.on_of(True)
    
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
        self.compras.insert('SelServicio', 'Pedidos en Línea', 'id')
        self.compras.click('/html/body/section/form/button')
        self.compras.insert('sel_regionlogin', 'Occidente', 'id')
        self.compras.insert('SelOrgCanalSector', 'Kit Prepago', 'id')
        self.compras.click('Button1', 'id')
    
    def consultarFacturas(self):
        self.compras.selectPage(self.link2)
        self.compras.insert('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[1]/select', 'Factura')
        self.compras.insert('FecIni', self.entry_first_date.get(), 'id')
        self.compras.insert('FecFin', self.entry_last_Date.get(), 'id')
        self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[3]/td[1]/table/tbody/tr/td[4]/input')
        data=self.compras.wait('/html/body/form/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td/div/table/tbody/tr/td', 'Informe los campos del filtro para hacer la seleccion')

    def getFacturasScraping(self):
        self.ventana_informacion.write('Obteniendo Facturas')
        cantidadFacturas = self.compras.read('/html/body/form/table/tbody/tr/td/table/tbody/tr[7]/td/table/tbody/tr/td/table[2]/tbody/tr/td[1]')
        self.cantidadFacturas = cantidadFacturas.replace('Total registros: ', '')
        html = self.compras.retornarHtml()
        soup = scraping.Scraping(html)
        data = soup.extrarDataTablas()
        empezar = False
        nuevoDato = False
        contador = 0
        newData=[]
        lineas = []
        contador2 = 1
        self.ventana_informacion.write('procesando facturas')
        for dato in data:
            porcentaje = (contador2/ int(self.cantidadFacturas))*100
            contador2 +=1
            if 'Cod Material' in dato[0]:
                continue
            if 'Consulta de Facturas en SAP' in dato[0] and len(dato)==1:
                empezar = True
                continue
            if empezar:
                if 'Numero' in dato[0]:
                    nuevoDato =True
                    continue
                if contador == 0 and nuevoDato == True:
                    titulo = dato
                    contador +=1
                elif contador > 0 and nuevoDato == True:
                    if str(dato[0]) == '\xa0\xa0':
                        nuevoDato = False
                        contador = 0
                        titulo.append(lineas)
                        newData.append(titulo)
                        lineas=[]
                        continue
                    contador +=1
                    lineas.append(dato)
        self.facturas = newData

    def getSerialesScraping(self):
        self.compras.selectPage(self.link3)
        newData = [None for i in range(int(self.cantidadFacturas))]
        contador2 = 0
        extraerSeriales = True
        while extraerSeriales:
            if f'{contador2}' == self.cantidadFacturas:
                extraerSeriales = False
            else:
                factura = self.facturas[contador2]
                try:
                    porcentaje = ((contador2+1)/ int(self.cantidadFacturas))*100
                    self.ventana_informacion.write(f'Obteniendo Seriales {round(porcentaje,2)}%')
                    numeroFatura = factura[0]
                    self.compras.insert('text_Factura', numeroFatura, 'id')
                    self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
                    html = self.compras.retornarHtml()
                    soup = scraping.Scraping(html)
                    data = soup.extrarDataTablas()
                    cantidadRegistros = self.compras.read('/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr/td[1]')
                    cantidadRegistros = cantidadRegistros.replace('Total registros: ', '')
                    empezar = False
                    detalles = []
                    for dato in data:
                        if '# Posición.' in dato[0] and len(dato)==3:
                            empezar = True
                            continue
                        if 'Total registros:' in dato[0]:
                            empezar=False
                            continue
                        if empezar:
                            if 'FACTURA OK' in dato[1]:
                                continue
                            detalles.append(dato)
                except:
                    try:self.compras.browser.close()
                    except:pass
                    self.abrirPagina()
                    self.compras.selectPage(self.link3)
                    try:
                        porcentaje = ((contador2+1)/ int(self.cantidadFacturas))*100
                        self.ventana_informacion.write(f'Obteniendo Seriales {round(porcentaje,2)}%')
                        numeroFatura = factura[0]
                        self.compras.insert('text_Factura', numeroFatura, 'id')
                        self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
                        html = self.compras.retornarHtml()
                        soup = scraping.Scraping(html)
                        data = soup.extrarDataTablas()
                        empezar = False
                        detalles = []
                        for dato in data:
                            if '# Posición.' in dato[0] and len(dato)==3:
                                empezar = True
                                continue
                            if 'Total registros:' in dato[0]:
                                empezar=False
                                continue
                            if empezar:
                                if 'FACTURA OK' in dato[1]:
                                    continue
                                detalles.append(dato)
                    except:
                        try:self.compras.browser.close()
                        except:pass
                        self.abrirPagina()
                        self.compras.selectPage(self.link3)
                        porcentaje = ((contador2+1)/ int(self.cantidadFacturas))*100
                        self.ventana_informacion.write(f'Obteniendo Seriales {round(porcentaje,2)}%')
                        numeroFatura = factura[0]
                        self.compras.insert('text_Factura', numeroFatura, 'id')
                        self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
                        html = self.compras.retornarHtml()
                        soup = scraping.Scraping(html)
                        data = soup.extrarDataTablas()
                        empezar = False
                        detalles = []
                        for dato in data:
                            if '# Posición.' in dato[0] and len(dato)==3:
                                empezar = True
                                continue
                            if 'Total registros:' in dato[0]:
                                empezar=False
                                continue
                            if empezar:
                                if 'FACTURA OK' in dato[1]:
                                    continue
                                detalles.append(dato)
                if len(detalles) != int(cantidadRegistros) -1:
                    continue

                factura.append(detalles)
                newData[contador2] = factura
                contador2 +=1
        self.FacturasConSerial = newData
    
    def organizarData(self):
        self.facturaExcel=[["factura", "fecha", "vencimiento", "total"]]
        self.result = [['serial','costoSinIva','codigo','producto','fecha','factura','tipo','vencimiento','iva','totalConIva']]
        contador2 = 1
        for dato in self.FacturasConSerial:
            porcentaje = (contador2/ int(self.cantidadFacturas))*100
            self.ventana_informacion.write(f'Organizando informacion {round(porcentaje,2)}%')
            contador2 +=1
            factura = dato[0]
            fecha = dato[1]
            vencimiento = datetime.strptime(dato[5], '%d/%m/%Y').date() - datetime.strptime(fecha, '%d/%m/%Y').date()
            vencimiento = vencimiento.days
            totalFactura = dato[6]
            item2 = [factura, fecha, vencimiento, totalFactura]
            self.facturaExcel.append(item2)

            for fila in dato[10]:
                serial = str(fila[2]).lstrip('0')
                productoFila = fila[1]
                ivaTaza = 0
                descuento = 0
                costo = 0
                tipo = ''

                for descripcion in dato[9]:
                    valor = descripcion[4].replace(".","").replace(",",".")
                    cantidad = descripcion[2]
                    productoDes = descripcion[1]

                    if productoFila == productoDes:
                        codigo = str(descripcion[0]).lstrip('0')

                        if descripcion[7] == 'IVA repercutido':
                            if valor == "0.00":
                                ivaTaza = 0
                            elif valor == "19000.00":
                                ivaTaza= 0.19
                            else: print(f'error con iva de {valor}')
                        elif descripcion[7] == 'Dcto Comercial':
                                descuento = int(valor.replace(".00",""))
                        elif descripcion[7] == 'Precio SIMCARD':
                            costo = int(valor.replace(".00",""))
                            tipo= 'SIM'
                        elif descripcion[7] == 'Prec sin IVA sin SIM':
                            costo = int(valor.replace(".00","")) 
                            tipo= 'KIT'
                        else:
                            print(f'error  {descripcion[7]} {valor}')

                costoSinIva = costo + descuento
                iva= costoSinIva * ivaTaza
                totalConIva= costoSinIva + iva
                renglon = [serial,costoSinIva,codigo,productoFila,fecha,factura,tipo,vencimiento,iva,totalConIva]
                self.result.append(renglon)
        self.ventana_informacion.write(f'Generando Excels')
        self.excel.export(self.result, 'src\compras\\archivo_excel.xlsx')
        self.excel.export(self.facturaExcel, 'src\compras\\resumido_excel.xlsx')
        self.abrir_excel()