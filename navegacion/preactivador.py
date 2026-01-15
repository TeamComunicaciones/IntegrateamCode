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
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from funcionalidad import poliedro_login_service
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class Preactivador:

    def __init__(self,master, on_of, alertas):
        self.traffic_base = "https://prod-md.azpol.claro.com.co"
        self.alertas = alertas
        self.min = ''
        self.etapa = 0
        self.mensaje = 's'
        self.on_of = on_of
        self.time2 = 3
        self.cookie_header = {}
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.link_google_messages = 'https://messages.google.com/web/conversations'
        self.link_mysms = 'https://app.mysms.com/#87472'

        self.titulo = label.Label().create_label(master, 'PREACTIVADOR DE SIM', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.preactivador = ''
        self.time = tk.StringVar()
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.04, 0.61, 0.5, 0.2, letterSize=16)
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.45, rely=0.68, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.65, 0.68, 0.15, 0.05, self.cambioIntervalo)
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
        input_widget2.place(relx=0.1, rely=0.75, relheight=0.05, relwidth=0.5)
        self.okBotton2 = boton.create_button(self.menu.submenu, 'OK', 0.65, 0.75, 0.15, 0.05, self.cambioCorreo)
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
        self.titulo3 = label.Label().create_label(self.menu.submenu, 'Poliedro User', 0.10, 0.47, 0.5, 0.04, letterSize=16)
        self.titulo4 = label.Label().create_label(self.menu.submenu, 'Poliedro Pass', 0.10, 0.57, 0.5, 0.04, letterSize=16)

        # Variables
        self.poliedro_user = ''
        self.poliedro_pass = ''
        self.poliedro_user_edit = tk.StringVar()
        self.poliedro_user_edit.set(self.poliedro_user)
        self.poliedro_pass_edit = tk.StringVar()
        self.poliedro_pass_edit.set(self.poliedro_pass)

        # Entradas (más angostas, alineadas a la izquierda)
        input_widget4 = ctk.CTkEntry(self.menu.submenu, textvariable=self.poliedro_user_edit)
        input_widget4.place(relx=0.10, rely=0.51, relheight=0.05, relwidth=0.55)

        input_widget5 = ctk.CTkEntry(self.menu.submenu, textvariable=self.poliedro_pass_edit)
        input_widget5.place(relx=0.10, rely=0.61, relheight=0.05, relwidth=0.55)

        # Botones OK a la derecha de cada entrada
        self.okBotton4 = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.51, 0.15, 0.05, self.cambioPoliedroUser)
        self.okBotton4.configure(fg_color=color.team, text_color='white')

        self.okBotton5 = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.61, 0.15, 0.05, self.cambioPoliedroPass)
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
       
    def traffic_url(self, path: str) -> str:
        return self.traffic_base.rstrip("/") + "/" + path.lstrip("/")
    
    def sync_traffic_base_from_browser(self):
        from urllib.parse import urlparse
        u = self.preactivador.browser.current_url
        p = urlparse(u)
        if p.scheme and p.netloc:
            self.traffic_base = f"{p.scheme}://{p.netloc}"
            self.ventana_informacion.write(f"✅ Traffic base detectada: {self.traffic_base}")
    
    def guardar_tiempo_espera(self):
        self.valor = self.spinbox_tiempo_espera.get_value()
        self.ventana_informacion.write(f'Tiempo de espera configurado: {self.valor} segundos')
    
    def on_checkbox_change_modo_captura(self):
        if self.modo_captura_datos.get():
            self.ventana_informacion.write('Envio de datos por API (No visible en navegador)')
        else:
            self.ventana_informacion.write('Envio de datos por Web (Visible en navegador)')

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
        if not self.mysms.get() and not self.google_messages.get():
            self.ventana_informacion.write('Seleccione un método para recibir el OTP')
            return

        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.preactivador = Abrir_pagina1(int(self.time.get()))
        self.preactivador.openEdge()
        time.sleep(3)
        self.preactivador.selectPage(self.link)

        time.sleep(2)
        if self.mysms.get():
            self.preactivador.script(f"window.open('{self.link_mysms}', '_blank');")
        elif self.google_messages.get():
            self.preactivador.script(f"window.open('{self.link_google_messages}', '_blank');")

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
            self.poliedro.definirBrowser(self.preactivador)
            # Primer clic

            # Inicializar el servicio de login
            self.poliedro_login_service = None
            if not self.login():
                self.ventana_informacion.write('❌ Error en login, verifique sus credenciales')
                self.on_of(True)
            time.sleep(2)

            try:
                self.preactivador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
            except:
                pass

            # self.preactivador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
            self.poliedro.seleccionAcceso('195')
            self.sync_traffic_base_from_browser()
            if not self.wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
            self.excel.leer_excel('src\preactivador\preactivador.xlsx','Iccid')
            self.excel.quitarFormatoCientifico('Iccid')
            self.ciclo = True
            self.contador = 0

            while self.ciclo:
                if self.contador == self.excel.cantidad:
                    self.ciclo = False
                else:
                    try:
                        self.min= str(self.excel.excel['Min'][self.contador])
                        if str(self.min) != 'nan':
                                self.ventana_informacion.write(f'Preactivación ya realizada o con error')
                                self.contador += 1
                                continue
                        else:
                            self.mensaje = ''
                            self.min = ''
                            self.EquiposInd()
                    except:
                        try:
                            self.preactivador.selectPage(self.traffic_url("/CaptureData"))
                            if not self.wait_for_loading():
                                raise Exception("Timeout esperando que la página cargue")
                            self.poliedro.seleccionAcceso('195', start=False)
                            if not self.wait_for_loading():
                                raise Exception("Timeout esperando que la página cargue")
                            self.position(self.preactivador.retornarHtml(), 'paso1', True)
                            self.contador += 1
                        except:
                            self.poliedro_login_service = None
                            if not self.login():
                                self.ventana_informacion.write('❌ Error en login, verifique sus credenciales')
                                self.on_of(True)
                                raise Exception("Error crítico: Fallo en login de Poliedro")
                            
                            time.sleep(2)
                            try:
                                self.preactivador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
                            except Exception as e:
                                pass
                            time.sleep(2)
                            self.poliedro.seleccionAcceso('195', start=True)
                            if not self.wait_for_loading():
                                raise Exception("Timeout esperando que la página cargue")
                    
                    # PAUSA ALEATORIA ENTRE TRANSACCIONES PARA EVITAR DETECCIÓN DE BOT
                    base = self.valor
                    variacion = random.randint(1,3)
                    tiempo_pausa = random.randint(base - variacion, base + variacion)
                    self.ventana_informacion.write(f"⏳ Pausa anti-bot: {tiempo_pausa}s entre transacciones...")
                    time.sleep(tiempo_pausa)
            self.ventana_informacion.write('Proceso terminado')
            self.on_of(True)
        except:
            self.alertas('se detiene el programa error')
    

    def EquiposInd(self):
        self.ventana_informacion.write(f'Activando Equipo {self.contador+1} de {self.excel.cantidad}')
        self.iccid = str(self.excel.excel['Iccid'][self.contador])[-12:] 
        self.documento = str(self.excel.excel['Documento'][self.contador])
        self.cedula_excel = str(self.excel.excel['Cedula'][self.contador])
        self.codigo_distribuidor = self.preactivador.read('userDataCodDistribuidor', 'id')
        self.nombre = ''
        self.apellido = ' '
        self.tipoDoc = str(self.excel.excel['TipoDoc'][self.contador])
        self.documentType = 2 if self.tipoDoc.lower() == 'nit' else 1
        self.tipoDoc_aux = "Cedula" if self.documentType == 1 else "NIT"

        self.position(self.preactivador.retornarHtml(), 'paso1', True)
        
        if self.modo_captura_datos.get():
            self.captura_datos_api()
        else:
            self.captura_datos_web()
        
        self.position(self.preactivador.retornarHtml(), 'paso2', True)
        
        try:
            errors = self.preactivador.readMulty('errorFormItem', 'class')
        except:
            pass
        if 'ICC_ID - Identificación Tarjeta de Circuito Integrada. = v' in errors:
            self.excel.guardar(self.contador, 'Mensaje', 'ICC_ID - Identificación Tarjeta de Circuito Integrada.', destino='src\preactivador\preactivador.xlsx')
            self.excel.guardar(self.contador, 'Min', 'error', destino='src\preactivador\preactivador.xlsx')
            self.ventana_informacion.write('ICC_ID - Identificación Tarjeta de Circuito Integrada.')
            raise('error validacion 2')
        
        if 'Validacion Causal Desactivacion IccId = Falso' in errors:
            self.excel.guardar(self.contador, 'Mensaje', 'Validacion Causal Desactivacion IccId = Falso', destino='src\preactivador\preactivador.xlsx')
            self.excel.guardar(self.contador, 'Min', 'error', destino='src\preactivador\preactivador.xlsx')
            self.ventana_informacion.write('Validacion Causal Desactivacion IccId = Falso')
            raise('error validacion 2')

        validate = self.preactivador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span')
        if validate != 'Validación Correcta':
            raise('error')
        self.preactivador.click('btnNext', 'id')
        self.position(self.preactivador.retornarHtml(), 'paso3', True)
        self.nombre = self.preactivador.value('PersonalInfo_Name', 'id')

        if self.modo_captura_datos.get():
            self.datos_demograficos_api()
        else:
            self.datos_demograficos_web()
        
        self.position(self.preactivador.retornarHtml(), 'paso4', True)

        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]')
        self.preactivador.click('/html/body/span/span/span[2]/ul/li[2]')
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
        self.preactivador.click('/html/body/span/span/span[2]/ul/li[2]')
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]')

        # url_product_service = 'https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService/Index1'
        # payload_product_service = {
        #     'EquipmentPlanDataViewModel.SaleDate': datetime.datetime.now().strftime("%d/%m/%Y"),
        #     'EquipmentPlanDataViewModel.MobileEquipment': 'Alcaltel OT-918A',
        #     'EquipmentPlanDataViewModel.Plan': '19598,0',
        #     'ValorBussinesPlan2': 0,
        #     'EquipmentPlanDataViewModel_CfmToFirstInvoice': False,
        #     'IsCesionDifPostPost': False,
        #     'EquipmentPlanDataViewModel.InvoiceCustomer': ''
        # }
        # request_product_service = session.post(url_product_service, headers=headers, data=payload_product_service)
        # if request_product_service.status_code == 200:
        self.preactivador.selectPage(self.traffic_url("/Activation"))
        self.preactivador.click('btnNext', 'id')
        try:
            find = self.preactivador.browser.find_element_by_id('btnNext')
            find.click()
        except:
            try:
                find = self.preactivador.browser.find_element_by_id('btnNext')
                find.click()
            except: 
                pass
        time.sleep(2)
        message = self.preactivador.read('messageFormItem', 'class')
        message = message.replace('* Su Solicitud fue enviada satisfactoriamente para el producto 195 y el MSISDN asignado es ', '')
        message = message[:10]
        self.excel.guardar(self.contador, 'Min', message, destino='src\preactivador\preactivador.xlsx')
        self.ventana_informacion.write(f'Preactivado con min {message}')
        raise('sin error')

        # try:
        #     self.validado()
        # except:
        #     self.ventana_informacion.write(f'Activacion erronea de equipo {self.iccid}')
        #     self.poliedro.reinicio()
        #     self.contador += 1
    
    def captura_datos_web(self):
        #Tipo documento
        self.poliedro.tipoDoc(self.tipoDoc_aux,'//*[@id="select2-DetailProduct_DocumentTypeId-container"]')
        time.sleep(2)

        #Documento
        self.preactivador.write("DetailProduct_DocumentNumber",self.documento,"id")

        #Apellido
        if self.documentType == 1:  # Solo si es cédula
            self.preactivador.write("DetailProduct_LastName",self.apellido,"id")

        #Opción serial
        self.poliedro.tipoDoc('sin','//*[@id="select2-DetailProduct_OptionImei-container"]')

        #Serial
        self.preactivador.write("DetailProduct_Iccid",self.iccid,"id")

        #Documento vendedor
        self.preactivador.write("DetailProduct_SellerId",self.cedula_excel,"id")

        time.sleep(2)
        if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de validación")
        
        # click en siguiente
        self.preactivador.click("btnNext", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente")


    def captura_datos_api(self):
        url = self.traffic_url("/CaptureData/Index2")
        payload = {
            'ProductShortcutName': '195 - (GAWBE) - WelcomeBack',
            'Pospago': False,
            'TechnologyId': 1,
            'ObligaFlagImei': '',
            'NumIOT': '910.919',
            'DealerCode': self.codigo_distribuidor,
            'productShortcut': 195,
            'ActivationId': 28,
            'ModuleId': 7,
            'ProductTypeId': 1,
            'PaymentId': 1,
            'PlanId': 13,
            'ProductId': 195,
            'Pospago': False,
            'IsSpecialUser': False,
            'ActiveFieldsPortability': True,
            'DetailProduct.ApplyPreactivedMin': False,
            'DetailProduct.CausalGsmServiceChange': 0,
            'DetailProduct.DealerCps': False,
            'DetailProduct.CodTechImei': '',
            'DetailProduct.TypeActivationWB': 1,
            'DetailProduct.DocumentTypeId': self.documentType,
            'DetailProduct.DocumentNumber': self.documento,
            'DetailProduct.LastName': '',
            'DetailProduct.RutNumber': '',
            'DetailProduct.ExpeditionDate': datetime.datetime.now().strftime("%d/%m/%Y"),
            'DetailProduct.OptionImei': 2,
            'DetailProduct.Imei': '',
            'DetailProduct.AuxiliaryImei': '',
            'DetailProduct.Iccid': self.iccid,
            'DetailProduct.AuxiliaryIccid': '',
            'DetailProduct.IsPreviousIMEI': True,
            'DetailProduct.DocumentTypeIdRL': '',
            'DetailProduct.DocumentNumberRL': '',
            'DetailProduct.ExpeditionDateRL': '',
            'DetailProduct.SellerId': self.cedula_excel,
            'DetailProduct.ContractNumber': '',
            'DetailProduct.PortabilityNumber': '',
            'DetailProduct.RutCheck': False,
            'DetailProduct.IsPreviousIMEI': True,
            'DetailProduct.IsPreviousICCID': False,
            'DetailProduct.ContractNumberCheck': False
        }

        cookies = self.preactivador.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        self.cookie_header['Cookie'] = self.preactivador.getCookies()
        headers = {'Cookie': self.cookie_header['Cookie']}

        post_response = session.post(url, headers=headers, data=payload)
        if post_response.status_code != 200:
            raise('Error en la respuesta de CaptureData')
        self.preactivador.selectPage(self.traffic_url("/Validation"))


    def datos_demograficos_web(self):
        time.sleep(2)
        #Saludo
        self.poliedro.tipoDoc('Sr', '//*[@id="select2-PersonalInfo_GreetingId-container"]')

        #Nombres
        nombre_actual = self.preactivador.value("PersonalInfo_Name",'id')
        if not nombre_actual.strip():    
            self.preactivador.write("PersonalInfo_Name", self.nombre, 'id')

        #Apellidos
        if self.documentType == 1:  # Solo si es cédula
            apellido_actual = self.preactivador.value("PersonalInfo_LastName",'id')
            if not apellido_actual.strip():
                self.preactivador.write("PersonalInfo_LastName", self.apellido, 'id')

        #Correo
        correo_actual = self.preactivador.value("PersonalInfo_Email","id")
        if not correo_actual or not correo_actual.strip():
            self.preactivador.write("PersonalInfo_Email", self.correo, 'id')

        #Telefono
        telefono_actual = self.preactivador.value("PhoneId","id")
        if not telefono_actual or not telefono_actual.strip():
            
            #Tipo
            self.selectDropDownNormal("PhoneClass","fijo")

            time.sleep(2)
            if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")

            #Indicativo
            self.selectDropDownNormal("Prefix","604")

            #Numero
            self.preactivador.write("PhoneNumber","0313123","id")

        #Tipo documento
        self.poliedro.tipoDoc(self.tipoDoc_aux,'//*[@id="select2-PersonalInfo_DocumentTypeId-container"]')

        #Cedula
        id_actual = self.preactivador.value("PersonalInfo_Document",'id')
        if not id_actual.strip() or id_actual.strip() == "0":
            campo = self.preactivador.browser.find_element_by_id("PersonalInfo_Document")
            campo.clear()
            self.preactivador.write("PersonalInfo_Document", self.documento, 'id')

        #Dirección
        direccion_actual = self.preactivador.value("AddressId","id")
        if not direccion_actual or not direccion_actual.strip():
            self.selectDropDownNormal("AddressClassId","Otras")
            time.sleep(2)
            if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")
            
            self.preactivador.write("Address", "central", "id")
            self.selectDropDownNormal("Department","ANTIOQUIA")
            time.sleep(2)
            if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")
            self.selectDropDownNormal("City","MEDELLIN")
            self.preactivador.write("Town", "Central", "id")

        time.sleep(2)
        if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de validación")
        
        # click en siguiente
        self.preactivador.click("btnNext", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente")

    
    def datos_demograficos_api(self):
        demographic_url = self.traffic_url("/Demographic/Index1")
        demographic_data = {
            "PersonalInfo.GreetingId": "O",
            "PersonalInfo.Name": self.nombre,
            "PersonalInfo.LastName": self.apellido,
            "PersonalInfo.Email": self.correo,
            "PersonalInfo.Phone.PhoneId": "",
            "PersonalInfo.Phone.PhoneClass": "2",
            "PersonalInfo.Phone.Prefix": "604",
            "PersonalInfo.Phone.PhoneNumber": "0313123",
            "PersonalInfo.EmailInitial": "",
            "PersonalInfo.DocumentTypeId": self.documentType,
            "PersonalInfo.Document": self.documento,
            "PersonalInfo.Address.AddressId": "",
            "PersonalInfo.Address.AddressClassId": "Otras",
            "PersonalInfo.Address.Address": "central",
            "PersonalInfo.Address.Department": "ANTIOQUIA",
            "PersonalInfo.Address.City": "MEDELLIN",
            "PersonalInfo.Address.Town": "Central"
        }

        cookies = self.preactivador.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        self.cookie_header['Cookie'] = self.preactivador.getCookies()
        headers = {'Cookie': self.cookie_header['Cookie']}

        demographic_response = session.post(demographic_url, headers=headers, data=demographic_data)
        if demographic_response.status_code != 200:
            raise('error demografic')
        self.preactivador.selectPage(self.traffic_url("/ProductService"))
            
    def validado(self):
        self.cookie_header['Cookie'] = self.preactivador.getCookies()
        
        headers = {
            'Cookie': self.cookie_header['Cookie']
        }
        cookies = self.preactivador.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
            
        demographic_url = self.traffic_url("/Demographic/Index1")
        demographic_data = {               
            "PersonalInfo.GreetingId": "M",
            "PersonalInfo.Name": "",
            "PersonalInfo.LastName": "",
            "PersonalInfo.Email": "acruz@teamcomunicaciones.com",
            "PersonalInfo.Phone.PhoneId": "526553",
            "PersonalInfo.Phone.PhoneClass": "",
            "PersonalInfo.Phone.Prefix": "7",
            "PersonalInfo.Phone.PhoneNumber": "8883136",
            "PersonalInfo.EmailInitial": "acruz@teamcomunicaciones.com",
            "PersonalInfo.DocumentTypeId": "1",
            "PersonalInfo.Document": self.cedula,
            "PersonalInfo.Address.AddressId": "",
            "PersonalInfo.Address.AddressClassId": "Otras",
            "PersonalInfo.Address.Address": "central",
            "PersonalInfo.Address.Department": "ANTIOQUIA",
            "PersonalInfo.Address.City": "MEDELLIN",
            "PersonalInfo.Address.Town": "Central",
            "PersonalInfo.ProductDonorOperator": "2"
        }
        
        self.preactivador.selectPage(self.traffic_url("/Validation"))
        if not self.wait_for_loading(preactivador=False):
            raise Exception("Timeout esperando que la página cargue")
        try:
            self.preactivador.click('btnNext', 'id')
        except:
            try:
                message = self.preactivador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
                if message == 'Porta ya registrada':
                    self.excel.guardar(self.contador, 'Mensaje', message)
                    self.preactivador.selectPage(self.traffic_url("/CaptureData"))
                    self.poliedro.seleccionAcceso('195', start=False)
                    if not self.wait_for_loading():
                        raise Exception("Timeout esperando que la página cargue")
                    self.ventana_informacion.write(f"{self.cedula} Porta ya registrada'")
            except:
                self.preactivador.selectPage(self.traffic_url("/CaptureData"))
                self.poliedro.seleccionAcceso('195', start=False)
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando que la página cargue")
                self.ventana_informacion.write(f"{self.cedula} error no identificado")
            raise('error controlado kit registrado')
        
        demographic_response = session.post(demographic_url, demographic_data, headers = headers)
        if demographic_response.status_code == 200:
            self.preactivador.selectPage(self.traffic_url("/ProductService"))
            if not self.wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
            self.pagina = 4
            self.poliedro.tipoDoc('al', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]')
            self.poliedro.tipoDoc('w', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]')
            self.preactivador.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
            self.pagina = 5
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
            if not self.wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
            optionsFinal = [
                ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p/text()[2]'],
                ['/html/body/div/strong/strong/div[3]/div[1]/div/button[2]'],
            ]
            self.poliedro.detectOption(optionsFinal, NoneFunc=self.errorGeneral)
        else:
            self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de Demographic/Index1")
            raise Exception("Error en la URL de Demographic/Index1")
        
    def selectDropDown(self, id, value):
        """
        Selecciona un valor de un dropdown usando el ID del elemento y el valor a seleccionar.
        """
        self.preactivador.click(f'select2-{id}-container', 'id')
        self.preactivador.write(f'/html/body/span/span/span[1]/input', value, 'xpath')
        self.preactivador.write(f'/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')

    def selectDropDownNormal(self, id, value):
        """
        Selecciona un valor de un <select> HTML clásico usando el ID del elemento y el texto visible.
        Coincidencia exacta, insensible a mayúsculas/minúsculas y tildes.
        """
        try:
            select_element = self.preactivador.browser.find_element_by_id(id)
            select = Select(select_element)

            value_normalized = str(value).strip().lower()
            matched = False

            # Buscar coincidencia exacta por texto visible (sin mayúsculas)
            for option in select.options:
                if option.text.strip().lower() == value_normalized:
                    option.click()
                    matched = True
                    break

            # Si no hay coincidencia por texto, intentar por value
            if not matched:
                select.select_by_value(value)

        except Exception as e:
            print(f"❌ Error en selectDropDownNormal({id}): {e}")
    
    # def selectDropDown(self, id, value):
    #     """
    #     Selecciona un valor de un dropdown. Funciona tanto para Select2 como para <select> normales.
    #     """
    #     try:
    #         el = self.preactivador.browser.find_element_by_id(id)
    #         classes = el.get_attribute("class") or ""

    #         # 🟢 Caso 1: Select2
    #         if "select2-hidden-accessible" in classes:
    #             self.preactivador.click(f"select2-{id}-container", "id")
    #             self.preactivador.write("/html/body/span/span/span[1]/input", value, "xpath")
    #             self.preactivador.write("/html/body/span/span/span[1]/input", Keys.ENTER, "xpath")

    #         # 🟢 Caso 2: <select> HTML normal
    #         else:
    #             select = Select(el)
    #             # intenta primero por texto visible (insensible a mayúsculas)
    #             matched = False
    #             for option in select.options:
    #                 if option.text.strip().lower() == value.strip().lower():
    #                     option.click()
    #                     matched = True
    #                     break
    #             if not matched:
    #                 select.select_by_value(value)
    #     except Exception as e:
    #         print(f"Error en selectDropDown({id}): {e}")
    
    def captarError(self, path, mensaje=None):
        if mensaje == None:
            validado = self.preactivador.read(path)
        else:
            validado = mensaje
        self.ventana_informacion.write(f'{self.min} {validado}')
        self.excel.guardar(self.contador, 'MENSAJE', validado, destino='src\portas\portabilidad.xlsx')
        self.excel.guardar(self.contador,'MSISDN','error', destino='src\portas\portabilidad.xlsx')
        self.reinicio()
        self.contador += 1
    
    def errorGeneral(self):
        raise('error general')
    
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
        self.min = ''
        self.mensaje = self.preactivador.readNoValidate('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[4]/ul/li')
        self.guardarData()
        self.contador += 1
        

    def errorValidacion(self):
        self.ventana_informacion.write(f'Activacion erronea de equipo {self.iccid}')
        self.reinicio()
        # self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
        # self.preactivador.erase('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[3]/div[3]/div/input')
        # self.preactivador.erase('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input')
        self.min = ''
        self.mensaje = 'Error en activacion'
        self.guardarData()
        self.contador += 1
    
    def terminarActivacion(self):
        try:
            self.preactivador.click('btnNext', 'id')
        except:
            try:
                message = self.preactivador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
                if message == 'Porta ya registrada':
                    self.excel.guardar(self.contador, 'Mensaje', message)
                    self.preactivador.selectPage(self.traffic_url("/"))
                    self.poliedro.seleccionAcceso('195', start=False)
                    if not self.wait_for_loading():
                        raise Exception("Timeout esperando que la página cargue")
                    self.ventana_informacion.write(f"{self.iccid} Sim ya registrada'")
            except:
                self.preactivador.selectPage(self.traffic_url("/"))
                self.poliedro.seleccionAcceso('195', start=False)
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando que la página cargue")
                self.ventana_informacion.write(f"{self.iccid} error no identificado")
            raise('error controlado preactivador')
        self.etapa = 2
        self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[1]/div/span/span[1]/span/span[1]')
        self.preactivador.click('/html/body/span/span/span[2]/ul/li[2]')
        self.preactivador.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[4]/div/input', 'acruz@teamcomunicaciones.com')
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
            if not self.wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
            self.poliedro.seleccionAcceso('195', start=False)
            if not self.wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
        else:
            for i in range(self.etapa):
                time.sleep(self.time2)
                self.preactivador.click('btnPrev', 'id')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando que la página cargue")
        self.etapa == 0
    
    def position(self, html, paso=None, wait=False):
        self.scrap = scraping.Scraping(html)
        soup = self.scrap.soup

        if not self.wait_for_loading():
            raise Exception("Timeout esperando que la página cargue")
        
        intentos = 0
        max_intentos = 30
        while wait and intentos < max_intentos:
            if paso == 'paso1':
                elementos_requeridos = [
                    ("h3", "iconoTituloCliente"),
                    ("h3", "iconoTituloInfoVenta"),
                    ("h3", "iconoTituloEquipo"),
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.preactivador.retornarHtml())
                    soup = self.scrap.soup
                    intentos += 1

            elif paso == 'paso2':
                elementos_requeridos = [
                    ("h3", "iconoTituloValidacionesyRestricciones"),
                    ("h3", "iconoTituloOtrasValidaciones"),
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.preactivador.retornarHtml())
                    soup = self.scrap.soup
                    intentos += 1

            elif paso == 'paso3':
                elementos_requeridos = [
                    ("h3", "iconoTituloInfoPersonal")
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.preactivador.retornarHtml())
                    soup = self.scrap.soup
                    intentos += 1

            elif paso == 'paso4':
                elementos_requeridos = [
                    ("h3", "iconoTituloDatosEquipoyPlan")
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.preactivador.retornarHtml())
                    soup = self.scrap.soup
                    intentos += 1
        
        if intentos >= max_intentos:
            raise Exception("Timeout esperando la posición de los elementos requeridos")

    
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
        if self.preactivador and not self.poliedro_login_service:
            self.poliedro_login_service = poliedro_login_service.LoginService(
                self.preactivador, 
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
    
    def wait_for_loading(self, timeout=120, sleep_interval=1, preactivador=True):
        """
        Método reutilizable para esperar que termine la carga.
        
        Args:
            timeout (int): Tiempo máximo de espera en segundos
            sleep_interval (float): Intervalo entre verificaciones
            preactivador (bool): True para usar self.preactivador, False para self.poliedro

        Returns:
            bool: True si terminó la carga, False si hubo timeout
        """

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if preactivador:
                    try:
                        loading_style = self.preactivador.style('loading', 'id')
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