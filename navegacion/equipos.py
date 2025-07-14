from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors
from funcionalidad import  web_controller, poliedro, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
import requests
import datetime
import re

class Equipos:

    def __init__(self,master, on_of, alertas):
        self.alertas = alertas
        self.on_of = on_of
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.cookie_header = {}
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.titulo = label.Label().create_label(master, 'ACTIVADOR DE EQUIPO', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.equipos = ''
        self.time = tk.StringVar()
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.0, 0.65, 0.5,0.2, letterSize= 16)
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.5, rely=0.73, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.73, 0.15, 0.05, self.cambioIntervalo)
        self.okBotton.configure(fg_color= color.team, text_color= 'white')
        self.repeticiones = '1'
        self.repeticionesEdit = tk.StringVar()
        self.repeticionesEdit.set(self.repeticiones) 
        self.titulo = label.Label().create_label(self.menu.submenu, 'Ciclos', 0.0, 0.78, 0.5,0.05, letterSize= 16)
        input_widget3 = ctk.CTkEntry(self.menu.submenu, textvariable=self.repeticionesEdit)
        input_widget3.place(relx=0.5, rely=0.79, relheight=0.05, relwidth=0.2)
        self.okBotton3 = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.79, 0.15, 0.05, self.cambioCiclos)
        self.okBotton3.configure(fg_color= color.team, text_color= 'white')
       
        
    
    def abrir_excel(self):
        self.ventana_informacion.write('excel equipos abierto recuerde cerrar antes de iniciar')
        p = Popen("src\equipos\openExcel.bat")
        stdout, stderr = p.communicate()
    
    def cambioIntervalo(self):
        self.equipos.actualizarIntervalo(self.time.get())
        self.ventana_informacion.write(f'intervalo {self.time.get()} segundos')

    def cambioCorreo(self):
        self.correo = self.correoEdit.get()
        self.ventana_informacion.write(f'Correo actualizado por {self.correo}')
    
    def cambioCiclos(self):
        self.repeticiones = self.repeticionesEdit.get()
        self.ventana_informacion.write(f'Numero de repeticiones configurado en {self.repeticiones}')
    
    def abrir_pagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.equipos = Abrir_pagina1(int(self.time.get()))
        self.equipos.openEdge()
        time.sleep(3)
        self.equipos.selectPage(self.link)
    
    def ejecuccionHilo(self):
        hilo_equipos = threading.Thread(target=self.ejecuccion)
        hilo_equipos.start()
        
    def ejecuccion(self):
        try:
            self.on_of(False)
            self.ventana_informacion.write('Empezando ejecuccion')
            self.poliedro.definirBrowser(self.equipos)
            self.poliedro.seleccionAcceso('194')
            for i in range(int(self.repeticiones)):
                self.contador = 0
                self.ciclo = True
                self.excel.leer_excel('src\equipos\equipos.xlsx','Iccid', dtype={'Iccid': str, 'Imei':str})
                self.excel.quitarFormatoCientifico('Iccid')
                self.excel.quitarFormatoCientifico('Imei')
                self.ventana_informacion.write(f'Inicio ciclo {i}')

                while self.ciclo:
                    if self.contador == self.excel.cantidad:
                        self.ciclo = False
                    else:
                        try:
                            min = str(self.excel.excel['Min'][self.contador])
                            if str(min) == 'nan' or str(min) == '':
                                self.mensaje = ''
                                self.EquiposInd()
                            else:
                                self.ventana_informacion.write(f'ya procesada')
                                self.contador += 1
                        except:
                            # self.ventana_informacion.write(f'Activacion erronea de equipo {self.imei}')
                            self.equipos.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                            try:
                                self.poliedro.seleccionAcceso('194', start=False)
                            except: pass
                            self.position(self.equipos.retornarHtml(), 'paso1', True)   
                            self.contador += 1
                self.ventana_informacion.write(f'ciclo {i} terminado')
            self.ventana_informacion.write('Proceso terminado')
            self.on_of(True)
        except:
            self.alertas('se detiene el programa error')
    

    def EquiposInd(self):
        self.ventana_informacion.write(f'Activando Equipo {self.contador+1} de {self.excel.cantidad}')
        self.iccid = str(self.excel.excel['Iccid'][self.contador])[-12:] 
        self.imei = str(self.excel.excel['Imei'][self.contador])
        self.cedulaVendedor = str(self.excel.excel['Cedula vendedor'][self.contador]).replace('.0','')
        self.codigo_distribuidor = self.equipos.read('userDataCodDistribuidor', 'id')
        self.vTecnologia = ""
        self.vKit = ""
        self.vLista = ""
        self.vEquipo = ""
        self.vRegion = ""

        self.position(self.equipos.retornarHtml(), 'paso1', True)
        cookies = self.equipos.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        self.cookie_header['Cookie'] = self.equipos.getCookies()
        headers = {
            'Cookie': self.cookie_header['Cookie']
        }

        #primera
        url = 'https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData/Index2'
        payload = {
            'ProductShortcutName': '194 - (GAKC) - Activación Kit Contado',
            'Pospago': False,
            'TechnologyId': 1,
            'ObligaFlagImei': '',
            'NumIOT': '910.919',
            'DealerCode': self.codigo_distribuidor,
            'productShortcut': 194,
            'ActivationId': 27,
            'ModuleId': 6,
            'ProductTypeId': 1,
            'PaymentId': 1,
            'PlanId': 13,
            'ProductId': 194,
            'Pospago': False,
            'IsSpecialUser': False,
            'ActiveFieldsPortability': True,
            'DetailProduct.ApplyPreactivedMin': False,
            'DetailProduct.CausalGsmServiceChange': 0,
            'DetailProduct.DealerCps': False,
            'DetailProduct.CodTechImei': '',
            'DetailProduct.DocumentTypeId': '',
            'DetailProduct.RutNumber': '',
            'DetailProduct.ExpeditionDate': '',
            'DetailProduct.Imei': self.imei.replace(' ',''),
            'DetailProduct.AuxiliaryIccid': '',
            'DetailProduct.Iccid': self.iccid,
            'DetailProduct.AuxiliaryIccid': '',
            'DetailProduct.DocumentTypeIdRL': '',
            'DetailProduct.DocumentNumberRL': '',
            'DetailProduct.ExpeditionDateRL': '',
            'DetailProduct.SellerId': self.cedulaVendedor,
            'DetailProduct.ContractNumber': '',
            'DetailProduct.PortabilityNumber': '',
            'DetailProduct.RutCheck': False,
            'DetailProduct.CheckEsim': False,
            'DetailProduct.ContractNumberCheck': False,
        }

        post_response = session.post(url, headers=headers, data=payload)
        if post_response.status_code == 200:
            if 'errores' in post_response.json():
                self.excel.guardar(self.contador, 'Mensaje', post_response.json()['errores'][0], destino='src\equipos\equipos.xlsx')
                self.excel.guardar(self.contador, 'Min', 'error', destino='src\equipos\equipos.xlsx')
                self.ventana_informacion.write(post_response.json()['errores'][0])
                raise('error validacion 1')
            else:
                self.equipos.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Validation')
        else:
            raise('error validacion 1')

        self.position(self.equipos.retornarHtml(), 'paso2', True)
        try:
            validate = self.equipos.readShort('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span')
            if validate != 'Validación Correcta':
                raise('error')
        except:
            scrap = scraping.Scraping(self.equipos.retornarHtml())
            soup = scrap.soup
            self.min = ""
            self.mensaje = ""
            self.iccid2 = self.get_value("ICC_ID - Identificación Tarjeta de Circuito Integrada.", soup)
            self.imei2 = self.get_value("IMEI - Identificación Internacional del Equipo Móvil.", soup)
            self.min = "Principal" if "Principal" in self.imei2 else self.min
            self.min = "En uso" if "En uso" in self.iccid2 else self.min
            self.vTecnologia = self.get_value("Validación Tecnología", soup)
            self.vKit = self.get_value("Validación Kit Prepago", soup)
            self.vLista = self.get_value("Validación en Listas de Imei Robados", soup)
            self.vEquipo = self.get_value("Validación Equipo Factura", soup)
            self.vRegion = self.get_value("Validación Region ICCID Distribuidor", soup)
            self.guardarData()
            raise('error')

        self.equipos.click('btnNext', 'id')

        self.position(self.equipos.retornarHtml(), 'paso3', True)
        self.equipos.click('btnNext', 'id')

        self.position(self.equipos.retornarHtml(), 'paso4', True)
        self.equipos.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
        self.equipos.click('/html/body/span/span/span[2]/ul/li[2]')

        self.equipos.click('btnNext', 'id')
        self.equipos.click('btnNext', 'id')

        message = self.equipos.read('messageFormItem', 'class')
        message = message.replace('* Su Solicitud fue enviada satisfactoriamente para el producto 194 y el MSISDN asignado es ', '')
        message = message[:10]
        self.excel.guardar(self.contador, 'Min', message, destino='src\equipos\equipos.xlsx')
        self.ventana_informacion.write(f'Preactivado con min {message}')
        raise('sin error')


        # optionsList = [
        #     ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span'],
        #     ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[4]/ul/li'],
        # ]
        # funcionList = [
        #     self.validado,
        #     self.error1
        # ]
        # self.poliedro.detectOption(optionsList, funcionList, NoneFunc=self.error2, short2=True)
        # self.guardarData()
        # # self.poliedro.reinicio()
        # self.contador += 1
    
    def validado(self):
        self.icc = ""
        self.imei = ""
        self.vTecnologia = ""
        self.vKit = ""
        self.vLista = ""
        self.vEquipo = ""
        self.vRegion = ""
        try:
            self.equipos.click('btnNext', 'id')
        except:
                try:
                    message = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
                    if message == 'Equipo procesado':
                        self.excel.guardar(self.contador, 'Mensaje', message)
                        self.equipos.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                        self.poliedro.seleccionAcceso('194', start=False)
                        self.ventana_informacion.write(f"{self.iccid} Equipo procesado'")
                except:
                    self.equipos.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                    self.poliedro.seleccionAcceso('194', start=False)
                    self.ventana_informacion.write(f"{self.iccid} error no identificado")
                raise('error controlado kit registrado')
        self.codigo_distribuidor = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div/div[2]/div')
        time.sleep(2)
        self.equipos.click('btnNext', 'id')#/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]
        try:
            self.equipos.click('btnNext', 'id')#/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]
        except:pass
        self.equipos.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
        self.equipos.click('/html/body/span/span/span[2]/ul/li[2]')
        self.equipos.click('btnNext', 'id')#/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]
        self.equipos.click('btnNext', 'id')
        self.min = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p/strong[2]')
        self.ventana_informacion.write(f'Activacion exitosa de equipo {self.imei} {self.min}')
        time.sleep(2)
        self.equipos.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[1]')
        
        self.poliedro.seleccionAcceso('194', start=False)
        
        
    def error1(self):
        self.icc = ""
        self.imei = ""
        self.vTecnologia = ""
        self.vKit = ""
        self.vLista = ""
        self.vEquipo = ""
        self.vRegion = ""
        self.min = ""
        self.codigo_distribuidor = ''
        self.mensaje = self.equipos.readNoValidate('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[4]/ul/li')
        self.ventana_informacion.write(f'{self.mensaje}')
        if '9918INV-021. El IMEI:' in self.mensaje:
            self.min = 'error 9918INV'
        else:
            self.equipos.click('btnPrev', 'id')

    def error2(self):
        self.mensaje = 'No deja preactivar por seriales en uso o principal'
        self.icc = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[1]/div/div/div')
        self.imei = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[2]/div/div/div')
        self.vTecnologia = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[3]/div/div/div')
        self.vKit = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[4]/div/div/div')
        self.vLista = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[5]/div/div/div')
        self.vEquipo = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[6]/div/div/div')
        self.vRegion = self.equipos.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[7]/div/div/div')
        self.min= ""
        self.codigo_distribuidor = ''
        self.ventana_informacion.write(f'{self.mensaje}')
        self.equipos.click('btnPrev', 'id')

    def guardarData(self):
        self.excel.guardar(self.contador, 'Min', self.min, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'Mensaje', self.mensaje, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'ICC_ID_Identificacion_Tarjeta_de_Circuito_Integrada', self.iccid2, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'IMEI_Identificacion_Internacional_del_Equipo_Movil', self.imei2, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'Validacion_Tecnologia', self.vTecnologia, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'Validacion_Kit_Prepago', self.vKit, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'Validacion_Region_ICCID_Distribuidor', self.vRegion, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'Validacion_Equipo', self.vEquipo, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'Validacion_Lista', self.vLista, 'src\equipos\equipos.xlsx')
        self.excel.guardar(self.contador, 'Codigo_distribuidor', self.codigo_distribuidor, 'src\equipos\equipos.xlsx')

    def position(self, html, paso=None, wait=False):
        self.scrap = scraping.Scraping(html)
        soup = self.scrap.soup
        count = 0
        top = 100

        while wait:
            if paso == 'paso1':
                elementos_requeridos = [
                    ("h3", "iconoTituloEquipo"),
                    ("h3", "iconoTituloInfoVenta"),
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.equipos.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        break

            elif paso == 'paso2':
                elementos_requeridos = [
                    ("h3", "iconoTituloValidacionesyRestricciones"),
                    ("h3", "iconoTituloOtrasValidaciones"),
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.equipos.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        break

            elif paso == 'paso3':
                elementos_requeridos = [
                    ("h3", "iconoTituloDatosDistribuidor")
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.equipos.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        break

            elif paso == 'paso4':
                elementos_requeridos = [
                    ("h3", "iconoTituloDatosEquipoyPlan")
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.equipos.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    try:
                        find = self.equipos.browser.find_element_by_id('btnNext')
                        find.click()
                    except:
                        pass
                    if count == top + 200:
                        break
        raise('error')

    
    def validate_position(self, elementos_requeridos, soup, type='id'):
        for tag, id_value in elementos_requeridos:
            if type == 'id':
                if not soup.find(tag, id=id_value):
                    return False
            elif type == 'class':
                if not soup.find(tag, class_=id_value):
                    return False
            else:
                return False
        return True
    
    def get_value(self, label_text, soup):
        label = soup.find("label", text=re.compile(label_text, re.IGNORECASE))
        if label:
            siguiente_div = label.find_next("div")
            if siguiente_div:
                return siguiente_div.text.strip()
        return "No encontrado"