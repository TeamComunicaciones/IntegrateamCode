from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors, checkbox, spinbox
from funcionalidad import  web_controller, poliedro, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
import requests
import datetime
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from funcionalidad import poliedro_login_service
import random

class Equipos:

    def __init__(self,master, on_of, alertas):
        self.alertas = alertas
        self.on_of = on_of
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.cookie_header = {}
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.link_google_messages = 'https://messages.google.com/web/conversations'
        self.link_mysms = 'https://app.mysms.com/#87472'

        self.titulo = label.Label().create_label(master, 'ACTIVADOR DE EQUIPO', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.equipos = ''
        self.time = tk.StringVar()
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.0, 0.62, 0.5,0.2, letterSize= 16)
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.45, rely=0.7, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.65, 0.7, 0.15, 0.05, self.cambioIntervalo)
        self.okBotton.configure(fg_color= color.team, text_color= 'white')
        self.repeticiones = '1'
        self.repeticionesEdit = tk.StringVar()
        self.repeticionesEdit.set(self.repeticiones) 
        self.titulo = label.Label().create_label(self.menu.submenu, 'Ciclos', 0.0, 0.76, 0.5,0.05, letterSize= 16)
        input_widget3 = ctk.CTkEntry(self.menu.submenu, textvariable=self.repeticionesEdit)
        input_widget3.place(relx=0.45, rely=0.76, relheight=0.05, relwidth=0.2)
        self.okBotton3 = boton.create_button(self.menu.submenu, 'OK', 0.65, 0.76, 0.15, 0.05, self.cambioCiclos)
        self.okBotton3.configure(fg_color= color.team, text_color= 'white')

        # Configuracion para tiempo de espera
        self.tiempo_espera_label = label.Label().create_label(self.menu.submenu, 'Tiempo de espera', 0.10, 0.36, 0.6, 0.04, letterSize=16)

        self.spinbox_tiempo_espera = spinbox.CTkSpinbox(self.menu.submenu, from_=5, to=60, default=5)
        self.spinbox_tiempo_espera.place(relx=0.10, rely=0.40, relheight=0.06, relwidth=0.55)

        # Si el usuario no presiona OK, toma el valor por defecto
        self.valor = self.spinbox_tiempo_espera.get_value()

        self.tiempo_espera_okbutton = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.40, 0.15, 0.05, self.guardar_tiempo_espera)
        self.tiempo_espera_okbutton.configure(fg_color=color.team, text_color='white')

        # Configuraciones para campo de usuario y contrasena poliedro
        # Etiquetas
        self.titulo3 = label.Label().create_label(self.menu.submenu, 'Poliedro User', 0.10, 0.49, 0.5, 0.04, letterSize=16)
        self.titulo4 = label.Label().create_label(self.menu.submenu, 'Poliedro Pass', 0.10, 0.59, 0.5, 0.04, letterSize=16)

        # Variables
        self.poliedro_user = ''
        self.poliedro_pass = ''
        self.poliedro_user_edit = tk.StringVar()
        self.poliedro_user_edit.set(self.poliedro_user)
        self.poliedro_pass_edit = tk.StringVar()
        self.poliedro_pass_edit.set(self.poliedro_pass)

        # Entradas (más angostas, alineadas a la izquierda)
        input_widget4 = ctk.CTkEntry(self.menu.submenu, textvariable=self.poliedro_user_edit)
        input_widget4.place(relx=0.10, rely=0.53, relheight=0.05, relwidth=0.55)

        input_widget5 = ctk.CTkEntry(self.menu.submenu, textvariable=self.poliedro_pass_edit)
        input_widget5.place(relx=0.10, rely=0.63, relheight=0.05, relwidth=0.55)

        # Botones OK a la derecha de cada entrada
        self.okBotton4 = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.53, 0.15, 0.05, self.cambioPoliedroUser)
        self.okBotton4.configure(fg_color=color.team, text_color='white')

        self.okBotton5 = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.63, 0.15, 0.05, self.cambioPoliedroPass)
        self.okBotton5.configure(fg_color=color.team, text_color='white')

        # Elegir si se usa MySMS o Google Messages para obtener el OTP
        self.checkbox_mysms = checkbox.Checkbox()
        self.mysms = tk.BooleanVar()
        self.checkbox_mysms = checkbox.Checkbox().create_checkbox(self.menu.submenu, 'MySMS', self.on_checkbox_change_mysms, self.mysms)

        self.checkbox_google_messages = checkbox.Checkbox()
        self.google_messages = tk.BooleanVar()
        self.checkbox_google_messages = checkbox.Checkbox().create_checkbox(self.menu.submenu, 'Google Messages', self.on_checkbox_change_google_messages, self.google_messages)

        self.checkbox_modo_captura_datos = checkbox.Checkbox()
        self.modo_captura_datos = tk.BooleanVar()
        self.checkbox_modo_captura_datos = checkbox.Checkbox().create_checkbox(self.menu.submenu, 'Envio de datos por API', self.on_checkbox_change_modo_captura, self.modo_captura_datos)
    
    def abrir_pagina(self):
        if not self.mysms.get() and not self.google_messages.get():
            self.ventana_informacion.write('Seleccione un método para recibir el OTP')
            return

        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.equipos = Abrir_pagina1(int(self.time.get()))
        self.equipos.openEdge()
        time.sleep(3)
        self.equipos.selectPage(self.link)

        time.sleep(2)
        if self.mysms.get():
            self.equipos.script(f"window.open('{self.link_mysms}', '_blank');")
        elif self.google_messages.get():
            self.equipos.script(f"window.open('{self.link_google_messages}', '_blank');")

    def guardar_tiempo_espera(self):
        self.valor = self.spinbox_tiempo_espera.get_value()
        self.ventana_informacion.write(f'Tiempo de espera configurado: {self.valor} segundos')  
    
    def on_checkbox_change_modo_captura(self):
        if self.modo_captura_datos.get():
            self.ventana_informacion.write('Envio de datos por API (No visible en navegador)')
        else:
            self.ventana_informacion.write('Envio de datos por Web (Visible en navegador)')
    
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

    def cambioPoliedroUser(self):
        self.poliedro_user = self.poliedro_user_edit.get()
        self.ventana_informacion.write(f'Usuario Poliedro actualizado por {self.poliedro_user}')

    def cambioPoliedroPass(self):
        self.poliedro_pass = self.poliedro_pass_edit.get()
        self.ventana_informacion.write(f'Contraseña Poliedro actualizada por {self.poliedro_pass}')

    def on_checkbox_change_mysms(self):
        if self.mysms.get():
            self.ventana_informacion.write('Cambiando modalidad a MySMS')
        else:
            self.ventana_informacion.write('Cambiando modalidad a Estandar')
    
    def on_checkbox_change_google_messages(self):
        if self.google_messages.get():
            self.ventana_informacion.write('Cambiando modalidad a Google Messages')
        else:
            self.ventana_informacion.write('Cambiando modalidad a Estandar')

    def ejecuccionHilo(self):
        hilo_equipos = threading.Thread(target=self.ejecuccion)
        hilo_equipos.start()
        
    def ejecuccion(self):
        try:
            self.on_of(False)
            self.ventana_informacion.write('Empezando ejecuccion')
            self.poliedro.definirBrowser(self.equipos)

            # Inicializar el servicio de login
            self.poliedro_login_service = None
            if not self.login():
                self.ventana_informacion.write('Error en login, verifique sus credenciales')
                self.on_of(True)
                self.alertas('se detiene el programa error en login')
                # Lanzar excepción para salir del bloque try y entrar al except final
                raise Exception("Error crítico: Fallo en login de Poliedro")
            time.sleep(2)

            try:
                self.equipos.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
            except Exception as e:
                self.ventana_informacion.write('Error en click de menú "Regresar a poliedro"')
                return

            # self.equipos.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
            time.sleep(3)
            self.poliedro.seleccionAcceso('194')
            if not self.wait_for_loading():
                raise Exception("Timeout esperando que cargue la página")
            
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
                            try:
                                min = str(self.excel.excel['Min'][self.contador])
                                if str(min) == 'nan' or str(min) == '':
                                    self.mensaje = ''
                                    self.EquiposInd()
                                else:
                                    self.ventana_informacion.write(f'ya procesada')
                                    self.contador += 1
                                    continue
                            except:
                                # self.ventana_informacion.write(f'Activacion erronea de equipo {self.imei}')
                                self.equipos.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                                try:
                                    self.poliedro.seleccionAcceso('194', start=False)
                                except: 
                                    # Reintentar login si falla
                                    self.poliedro_login_service = None
                                    if not self.login():
                                        self.ventana_informacion.write('❌ Error en login, verifique sus credenciales')
                                        self.on_of(True)
                                        raise Exception("Error crítico: Fallo en login de Poliedro")
                                    
                                    time.sleep(2)
                                    try:
                                        try:
                                            self.equipos.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
                                        except:
                                            pass
                                        time.sleep(1)
                                        self.equipos.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                                        time.sleep(2)
                                        self.poliedro.seleccionAcceso('194')
                                        time.sleep(1)
                                        if not self.wait_for_loading():
                                            raise Exception("Timeout esperando que cargue la página")
                                    except Exception as e:
                                        return
                                    
                                self.position(self.equipos.retornarHtml(), 'paso1', True)   
                                self.contador += 1
                        except Exception as e:
                            if "Error crítico: Fallo en login de Poliedro" in str(e):
                                raise Exception("Error crítico: Fallo en login de Poliedro")
                            self.ventana_informacion.write(f"Error en la iteración {self.contador}: {e}")
                            self.equipos.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                            """ self.equipos.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]/a/span/text()')
                            time.sleep(2)
                            self.equipos.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]/a/span')
                            self.ventana_informacion.write("Redirigido para reintentar.")
                            time.sleep(3) """
                        base = self.valor
                        variacion = random.randint(1,3)
                        tiempo_pausa = random.randint(base - variacion, base + variacion)
                        self.ventana_informacion.write(f"⏳ Pausa anti-bot: {tiempo_pausa}s entre transacciones...")
                        time.sleep(tiempo_pausa)
                    
                self.ventana_informacion.write(f'ciclo {i} terminado')
            self.ventana_informacion.write('Proceso terminado')
            self.on_of(True)
        except Exception as e:
            print(f"Error ocurrido: {e}")
            self.alertas('se detiene el programa error')
    

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

        if self.modo_captura_datos.get():
            self.captura_datos_api()
        else:
            self.captura_datos_web()

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

    def captura_datos_web(self):
        """Versión Web de la captura de datos (visible en UI)"""
        self.equipos.write("DetailProduct_Imei", self.imei.replace(' ', ''), 'id')
        self.equipos.write("DetailProduct_Iccid", self.iccid, 'id')
        self.equipos.write("DetailProduct_SellerId", self.cedulaVendedor, 'id')

        time.sleep(2)
        if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de validación")
        
        # click en siguiente
        self.equipos.click("btnNext", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente")
        
        # --- Captura de errores en Web ---
        errores = self.equipos.readMulty("errorFormItem", "class")
        if errores and errores != "none":  
            # guardar primer error (o concatenar todos si quieres)
            self.excel.guardar(self.contador, "Mensaje", errores[0], destino="src\equipos\equipos.xlsx")
            self.excel.guardar(self.contador, "Min", "error", destino="src\equipos\equipos.xlsx")
            self.ventana_informacion.write(f"Error detectado en web: {errores[0]}")
            raise Exception("Error validación WEB")
    
    def captura_datos_api(self):
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

        cookies = self.equipos.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        self.cookie_header['Cookie'] = self.equipos.getCookies()
        headers = {
            'Cookie': self.cookie_header['Cookie']
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
            raise('error validacion API')

    
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
    
    def login(self):
        """
        Método simplificado que usa el servicio de login
        """
        try:
            # Inicializar el servicio si no existe
            if not self.poliedro_login_service:
                self.inicializar_login_service()
            
            # Configurar credenciales actuales
            self.poliedro_login_service.configurar_credenciales(
                self.poliedro_user, 
                self.poliedro_pass
            )
            
            # Ejecutar login automático
            return self.poliedro_login_service.login_automatico()

        except Exception as e:
            self.log_error("login", e)
            return False
    
    def inicializar_login_service(self):
        """
        Inicializa el servicio de login cuando el navegador esté listo
        """
        if self.equipos and not self.poliedro_login_service:
            self.poliedro_login_service = poliedro_login_service.LoginService(
                self.equipos, 
                self.ventana_informacion
            )
            # CONFIGURAR REINTENTOS
            self.poliedro_login_service.configurar_reintentos(
                max_intentos=2, 
                intervalo_minutos=2
            )
            self.poliedro_login_service.configurar_credenciales(
                self.poliedro_user, 
                self.poliedro_pass
            )
            self.poliedro_login_service.configurar_portales_otp(
                mysms=self.mysms.get(),
                google_messages=self.google_messages.get(),
            )
    
    def wait_for_loading(self, timeout=120, sleep_interval=1, equipos=True):
        """
        Método reutilizable para esperar que termine la carga.
        
        Args:
            timeout (int): Tiempo máximo de espera en segundos
            sleep_interval (float): Intervalo entre verificaciones
            equipos (bool): True para usar self.equipos, False para self.poliedro

        Returns:
            bool: True si terminó la carga, False si hubo timeout
        """

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if equipos:
                    try:
                        loading_style = self.equipos.style('loading', 'id')
                    except Exception:
                        loading_style = self.poliedro.style('loading', 'id')
                else:
                    loading_style = self.poliedro.style('loading', 'id')
                if "display: none" in loading_style:
                    return True
                elif "display: block" in loading_style:
                    print(f'Loading... ({time.time() - start_time:.1f}s)')
                else:
                    print(f'Loading style no reconocido: {loading_style}')
                    return True # Asumir que terminó si no se puede leer el estilo
            except Exception:
                # Si no puede leer el estilo, asumir que terminó la carga
                return True
                
            time.sleep(sleep_interval)
        
        return False  # Timeout