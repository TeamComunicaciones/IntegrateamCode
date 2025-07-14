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
import numpy as np
import os


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
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.compras = Abrir_pagina1(0)
    
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
        time.sleep(4)
        self.consultarFacturas()
        try:
            self.getFacturasScraping()
            # self.getSerialesScraping()
        except Exception as e:
            self.ventana_informacion.write(f'error, se detiene el programa: {e}')
            raise Exception('error')
        # self.organizarData()
        self.on_of(True)

    def validate_position(self, elementos_requeridos, soup, type='id'):
        for tag, id_value in elementos_requeridos:
            if soup.find(tag, class_=id_value):
                return True
        return False

    
    def abrirPagina(self):
        if not self.compras.browser or not self.compras.isBrowserOpen():
            self.compras.openEdge(headless=False)
            self.ventana_informacion.write('Navegador abierto')
        while True:
            self.compras.selectPage(self.link)
            time.sleep(5)
            self.scrap = scraping.Scraping(self.compras.retornarHtml())
            soup = self.scrap.soup
            elementos_requeridos = [
                ("div", "new-icon"),
                ("input", "passwordLogin"),
            ]
            if self.validate_position(elementos_requeridos, soup):
                break
        try:
            self.ventana_informacion.write('Pagina iniciada')
            time.sleep(5)
            self.compras.click('details-button','id')
            time.sleep(2)
            self.compras.click('proceed-link','id')
            time.sleep(2)
        except:pass
        self.compras.insert('/html/body/section/form/input[1]', self.entry_user.get())
        time.sleep(2)
        self.compras.insert('password', self.entry_password.get(), 'id')
        time.sleep(2)
        self.compras.insert('SelServicio', 'Pedidos en Línea', 'id')
        time.sleep(2)
        self.compras.click('/html/body/section/form/button')
        time.sleep(2)
        self.compras.insert('sel_regionlogin', 'Occidente', 'id')
        time.sleep(2)
        self.compras.insert('SelOrgCanalSector', 'Kit Prepago', 'id')
        time.sleep(2)
        self.compras.click('Button1', 'id')
        time.sleep(2)
    
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
        while True:
            html = self.compras.retornarHtml()
            soup = scraping.Scraping(html)
            divs = soup.soup.find_all('div', class_='DivLista')
            tables = []
            for div in divs:
                tables.extend(div.find_all('table'))
            tables_detail = [{'detail':soup.extrarDataTablas(tabla=tables[(i*3)-2]), 'title':soup.extrarDataTablas(tabla=tables[(i*3)-3])} for i in range(1, int(len(tables)/3)+1)]
            if len(tables_detail) == int(self.cantidadFacturas):
                break
        
        procesadas = {}
        for table in tables_detail:
            for i in range(1, len(table['detail'])):
                factura = table['title'][1][0]
                ref = table['detail'][i][1]
                codigo = table['detail'][i][0].lstrip("0")
                titulo = table['detail'][i][7]
                value =  table['detail'][i][8].replace('.','').replace(',','.').replace('.00','')

                if factura not in procesadas.keys():
                    procesadas[factura] = {}
                if ref not in procesadas[factura].keys():
                    procesadas[factura][ref] = {}
                # if codigo not in procesadas[factura][ref].keys():
                #     procesadas[factura][ref][codigo] = {}
                procesadas[factura][ref]['CODIGO'] = table['detail'][i][0].lstrip("0")
                procesadas[factura][ref]['REFERENCIA'] = table['detail'][i][1]
                procesadas[factura][ref]['FECHA'] = table['title'][1][1]
                procesadas[factura][ref]['FACTURA'] = factura
                procesadas[factura][ref]['Vencimiento'] = datetime.strptime(table['title'][1][1], "%d/%m/%Y") - datetime.strptime(table['title'][1][5], "%d/%m/%Y")
                if titulo == 'Precio SIMCARD':
                    procesadas[factura][ref]['KIT/SIM'] = 'SIM'
                    procesadas[factura][ref]['Prec sin IVA sin SIM'] = 0
                elif titulo == 'Prec sin IVA sin SIM':
                    procesadas[factura][ref]['Precio SIMCARD'] = 0
                    procesadas[factura][ref]['KIT/SIM'] = 'EQUIPO'
                procesadas[factura][ref][titulo] = int(value) / int(table['detail'][i][2])


        self.compras.selectPage(self.link3)
        count = 0
        invoices = []
        seriales = []
        for index, factura_serial in enumerate(procesadas.keys()):
            self.ventana_informacion.write(f'integracion {index+1} de {len(procesadas.keys())}')
            self.compras.insert('text_Factura', factura_serial, 'id')
            self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            countWhile = 0
            while True:  
                try:

                    tables2_2 = []
                    html = ''
                    divs = []


                    html = self.compras.retornarHtml()
                    soup = scraping.Scraping(html)
                    divs = soup.soup.find_all('div', class_='DivLista3')
                    
                    tables2 = []
                    serials = {}
                    
                    for div in divs:
                        tables2.extend(div.find_all('table'))
                    if len(tables2) > 1:
                        pass
                    tables2_2 = soup.extrarDataTablas(tabla=tables2[0])
                    cantidadFacturas = self.compras.read('/html/body/form/table/tbody/tr/td/table/tbody/tr[4]/td/table/tbody/tr/td/table[2]/tbody/tr/td[1]')
                    cantidadFacturas = cantidadFacturas.replace('Total registros: ', '')
                    if int(cantidadFacturas) == len(tables2_2):
                        check3 = True
                        for row in tables2_2:
                            if row[2] != '':
                                ref = row[1]
                                if ref not in procesadas[factura_serial] or row[2] in seriales:
                                    check3 = False
                        if check3:
                            break
                        else:
                            countWhile +=1
                            print(countWhile)
                            if countWhile > 100000:
                                raise('error controlado')

                except:
                    countLast = 0
                    while True:
                        # try:
                        #     self.compras.cerrar()
                        # except:
                        #     pass
                        try:
                            self.abrirPagina()
                            self.compras.selectPage(self.link3)
                            self.compras.insert('text_Factura', factura_serial, 'id')
                            self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
                            countLast = 0
                            break
                        except:
                            countLast += 1
                            if countLast > 15:
                                break

            for row in tables2_2:
                if row[2] != '':
                    seriales.append(row[2])
                    ref = row[1]
                    if ref not in procesadas[factura_serial]:
                        pass
                    data_row = procesadas[factura_serial][ref]
                    d1 = data_row['IVA repercutido']
                    d2 = data_row['Dcto Comercial'] if 'Dcto Comercial' in data_row.keys() else 0
                    d3 = data_row['Precio SIMCARD']
                    d4 = data_row['Prec sin IVA sin SIM']
                    invoices.append({
                        'SERIAL': row[2].lstrip("0"),
                        'COSTO': d2 + d3 + d4,
                        'CODIGO': data_row['CODIGO'],
                        'REFERENCIA': data_row['REFERENCIA'],
                        'FECHA': data_row['FECHA'],
                        'FACTURA': data_row['FACTURA'],
                        'KIT/SIM': data_row['KIT/SIM'],
                        'Vencimiento': data_row['Vencimiento'],
                        'IVA': data_row['IVA repercutido'],
                        'TOTAL CON IVA': d1 + d2 + d3 + d4,
                    })

        self.facturas_df = pd.DataFrame(invoices)

        archivo_excel = 'src\compras\\archivo_excel.xlsx'
        if os.path.exists(archivo_excel):
            # Cargar el libro existente
            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                self.facturas_df.to_excel(writer, sheet_name='seriales', index=False)
        else:
            # Crear un nuevo archivo Excel con la hoja
            with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
                self.facturas_df.to_excel(writer, sheet_name='seriales', index=False)

        resumen = []
        for table in tables_detail:  
            resumen.append({table['title'][0][i]:table['title'][1][i] for i in range(len(table['title'][0]))})
        self.facturas_resumen = pd.DataFrame(resumen)
        self.facturas_resumen = self.facturas_resumen[['Numero', 'Fecha Factura', 'Fecha Venc.', 'Total' ]]
        factura_dates = pd.to_datetime(self.facturas_resumen['Fecha Factura'], format='%d/%m/%Y')
        venc_dates = pd.to_datetime(self.facturas_resumen['Fecha Venc.'], format='%d/%m/%Y')
        self.facturas_resumen['Fecha Venc.'] = (venc_dates - factura_dates).dt.days
        if os.path.exists(archivo_excel):
            # Cargar el libro existente
            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                self.facturas_resumen.to_excel(writer, sheet_name='resumen', index=False)
        else:
            # Crear un nuevo archivo Excel con la hoja
            with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
                self.facturas_resumen.to_excel(writer, sheet_name='resumen', index=False)
        
        detalles = []
        for table in tables_detail:
            for n in range(1, len(table['detail'])):
                detalles.append({table['detail'][0][i]:table['detail'][n][i] for i in range(len(table['detail'][0]))} | {'Factura': table['title'][1][0]})

        self.facturas_detalles = pd.DataFrame(detalles)

        if os.path.exists(archivo_excel):
            # Cargar el libro existente
            with pd.ExcelWriter(archivo_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                self.facturas_detalles.to_excel(writer, sheet_name='detalles', index=False)
        else:
            # Crear un nuevo archivo Excel con la hoja
            with pd.ExcelWriter(archivo_excel, engine='openpyxl') as writer:
                self.facturas_detalles.to_excel(writer, sheet_name='detalles', index=False)

        self.abrir_excel()

        # invoices = []
        # summary = []
        # count = 0
        # self.compras.selectPage(self.link3)
        # for table in tables_detail:
        #     while True:
        #         try:
        #             dict1 = {table['title'][0][x]:table['title'][1][x] for x in range(len(table['title'][0]))}
        #             summary.append(dict1)
        #             numeroFatura = table['title'][1][0]
        #             porcentaje = ((count+1)/ int(self.cantidadFacturas))*100
                    
        #             self.ventana_informacion.write(f'Obteniendo Seriales {round(porcentaje,2)}%')
        #             self.compras.insert('text_Factura', numeroFatura, 'id')
        #             self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
        #             while True:
        #                 html = self.compras.retornarHtml()
        #                 soup = scraping.Scraping(html)
        #                 divs = soup.soup.find_all('div', class_='DivLista3')
                        
        #                 tables2 = []
        #                 serials = {}
                        
        #                 for div in divs:
        #                     tables2.extend(div.find_all('table'))
        #                 if len(tables2) > 1:
        #                     pass
        #                 tables2_2 = soup.extrarDataTablas(tabla=tables2[0])
        #                 for table2 in tables2_2:
        #                     if table2[1] not in serials.keys():
        #                         serials[table2[1]] = {}
        #                     if table2[0] not in serials[table2[1]].keys():
        #                         serials[table2[1]][table2[0]] = []
        #                     if table2[2] != '':
        #                         serials[table2[1]][table2[0]].append(table2[2]) 
                                
        #                 check = True
        #                 for i in range(1, len(table['detail'])):
        #                     if table['detail'][i][1] not in serials.keys():
        #                         check = False
        #                         break
        #                 if check:
        #                     break
        #             count += 1
        #             break
        #         except:
        #             try:
        #                 self.compras.cerrar()
        #             except:
        #                 pass
        #             self.abrirPagina()
        #             self.compras.selectPage(self.link3)

        #     for i in range(1, len(table['detail'])):
        #         try:
        #             serial = {'serial':serials[table['detail'][i][1]]}
        #         except:
        #             serial = {'serial':''}
        #         dict2 = {table['detail'][0][x]:table['detail'][i][x] for x in range(len(table['detail'][0]))}
        #         invoices.append(dict1 | dict2 | serial)
        # total_invoices = []
        # acumulado = 0
        # acumulado2 = 0
        # contador = 0
        # test_fact = 'no'
        # for invoice in invoices:
        #     if invoice['Numero'] == test_fact:
        #         pass
        #     porcentaje = ((contador+1)/ len(invoices))*100     
        #     self.ventana_informacion.write(f'Asignando Seriales {round(porcentaje,2)}%')
        #     cantidad = int(invoice['Cantidad'])
        #     seriales_disponibles = len(invoice['serial'])
        #     factura = invoice['Numero']
        #     for i in range(seriales_disponibles):
        #         check2 = False
        #         if len(invoice['serial'][i]) == cantidad:
        #             seriales_para_uso = invoice['serial'][list(invoice['serial'].keys())[i]].copy()
        #             del invoice['serial'][list(invoice['serial'].keys())[i]]
        #             check2 = True
        #             break


        #     if cantidad > len(seriales_para_uso[acumulado:]):
        #         self.compras.insert('text_Factura', factura, 'id')
        #         self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
        #         while True:
        #             try:
        #                 html = self.compras.retornarHtml()
        #                 soup = scraping.Scraping(html)
        #                 divs = soup.soup.find_all('div', class_='DivLista3')
                        
        #                 tables2 = []
        #                 serials = {}
        #                 for div in divs:
        #                     tables2.extend(div.find_all('table'))
        #                 if len(tables2) > 1:
        #                     pass
        #                 tables2_2 = soup.extrarDataTablas(tabla=tables2[0])
        #                 for table2 in tables2_2:
        #                     if table2[1] not in serials.keys():
        #                         serials[table2[1]] = []
        #                     if table2[2] != '':
        #                         serials[table2[1]].append(table2[2])
        #                 if len(serials[invoice['Descripción']][acumulado:]) == cantidad:
        #                     seriales_disponibles = len(serials)
        #                     seriales_para_uso = serials[invoice['Descripción']]
        #                     acumulado = 0
        #                     break
        #             except:
        #                 try:
        #                     self.compras.cerrar()
        #                 except:
        #                     pass
        #                 self.abrirPagina()
        #                 self.compras.selectPage(self.link3)
        #                 self.compras.insert('text_Factura', factura, 'id')
        #                 self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
        #     elif cantidad < len(seriales_para_uso[acumulado:]):
        #         acumulado = acumulado + cantidad
        #     else:
        #         acumulado = 0

        #     tem_invoice = invoice.copy()
        #     del tem_invoice['serial']
        #     tem_invoice['Fecha Venc.'] = datetime.strptime(tem_invoice['Fecha Venc.'], "%d/%m/%Y") - datetime.strptime(tem_invoice['Fecha Factura'], "%d/%m/%Y")
        #     tem_invoice['Cod Material'] = tem_invoice['Cod Material'].lstrip("0")
        #     if tem_invoice['Desc. Condición'] == 'IVA repercutido':
        #         tem_invoice['Valor'] = int(tem_invoice['SubTotal'].replace('.','').replace(',','.').replace('.00','')) / cantidad
        #     for i in range(len(seriales_para_uso[acumulado2:])):
        #          total_invoices.append(tem_invoice | {'serial' : seriales_para_uso[acumulado2:][i].lstrip("0")} )
        #     acumulado2 = acumulado
        #     contador += 1
        # df = pd.DataFrame(total_invoices)
        # self.summary_df = pd.DataFrame(summary)
        # self.facturas_df = pd.concat([df.drop(columns=["Desc. Condición"]), 
        #               pd.get_dummies(df["Desc. Condición"])], axis=1)
        # columns_name = df["Desc. Condición"].unique()
        # for colum in columns_name:
        #     self.facturas_df[colum] = np.where(self.facturas_df[colum], self.facturas_df['SubTotal'], '0')
        #     self.facturas_df[colum] = self.facturas_df[colum].astype(str).str.replace(".", "")
        #     self.facturas_df[colum] = self.facturas_df[colum].astype(str).str.replace(",", ".")
        #     self.facturas_df[colum] = self.facturas_df[colum].astype(str).str.replace(".00", "")
        #     self.facturas_df[colum] = pd.to_numeric(self.facturas_df[colum], errors="coerce")
        # self.facturas_df['Factura'] = self.facturas_df['Numero']
        # self.facturas_df = self.facturas_df.groupby(["Factura", "Cod Material", "serial"]).agg({
        #     "IVA repercutido": "sum",
        #     "Dcto Comercial": "sum",
        #     "Precio SIMCARD": "sum",
        #     "Prec sin IVA sin SIM": "sum",
        #     **{col: "last" for col in self.facturas_df.columns if col not in ["Factura", "Cod Material", 
        #                                                         "IVA repercutido", "Dcto Comercial",
        #                                                         "Precio SIMCARD", "Prec sin IVA sin SIM"]}
        # }).reset_index()
        # self.facturas_df["Categoria"] = np.where(self.facturas_df["Precio SIMCARD"].notna() & (self.facturas_df["Precio SIMCARD"] != 0), "SIM", "EQUIPO")
        # self.facturas_df["Costo"] = self.facturas_df[["Precio SIMCARD", "Prec sin IVA sin SIM"]].max(axis=1)
        # self.facturas_df.drop(columns=["Precio SIMCARD", "Prec sin IVA sin SIM", "SubTotal"], inplace=True)
        # self.facturas_df["Suma"] = self.facturas_df[["IVA repercutido", "Dcto Comercial", "Costo"]].sum(axis=1)
        # self.facturas_df['Total_2'] = self.facturas_df.groupby('Factura')['Suma'].transform('sum')
        # self.facturas_df["Total"] = self.facturas_df["Total"].astype(str).str.replace(".", "")
        # self.facturas_df["Total"] = self.facturas_df["Total"].astype(str).str.replace(",", ".")
        # self.facturas_df["Total"] = self.facturas_df["Total"].astype(str).str.replace(".00", "")
        # self.facturas_df["Total"] = pd.to_numeric(self.facturas_df["Total"], errors="coerce")
        # self.facturas_df["Test"] = self.facturas_df["Total_2"] == self.facturas_df["Total"]
        # df_true = self.facturas_df[self.facturas_df["Test"] == True].copy()
        # df_false = self.facturas_df[self.facturas_df["Test"] == False].copy()
        # if len(df_false) > 0:
        #     raise('error no coinciden todos los campos')
        # else:
        #     self.facturas_df = df_true
        # self.excel.export(self.facturas_df, 'src\compras\\archivo_excel.xlsx', type=False)
        # self.excel.export(self.summary_df, 'src\compras\\resumido_excel.xlsx', type=False)
        # self.abrir_excel()

    def getSerialesScraping(self):
        self.compras.selectPage(self.link3)

        serials = []
        for i, x in self.summary_df.iterrows():
            numeroFatura = x['Numero']
            porcentaje = ((i+1)/ int(self.cantidadFacturas))*100
            self.ventana_informacion.write(f'Obteniendo Seriales {round(porcentaje,2)}%')
            self.compras.insert('text_Factura', numeroFatura, 'id')
            self.compras.click('/html/body/form/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input')
            html = self.compras.retornarHtml()
            soup = scraping.Scraping(html)
            divs = soup.soup.find_all('div', class_='DivLista3')
            tables = []
            for div in divs:
                tables.extend(div.find_all('table'))
            pass
            if len(tables) > 1:
                pass
            tables = soup.extrarDataTablas(tabla=tables[0])
            for table in tables:
                if table[2] != '':
                    serials.append({'Factura':numeroFatura, 'Descripción':table[1], 'Serial':table[2]})
        serials_df = pd.DataFrame(serials)
        df_merged = self.facturas_df.merge(serials_df[['Factura', 'Descripción', 'Serial']],
                      on=['Factura', 'Descripción'],
                      how='left')
        self.excel.export(df_merged, 'src\compras\\archivo_excel.xlsx', type=False)
        self.excel.export(self.facturas_df, 'src\compras\\resumido_excel.xlsx', type=False)
        self.abrir_excel()
    
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
        self.excel.export(self.summary_df, 'src\compras\\resumido_excel.xlsx')
        self.abrir_excel()