from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors, checkbox
from funcionalidad import  web_controller, poliedro, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
import requests
import datetime


class Preactivador:

    def __init__(self,master, on_of, alertas):
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
        self.titulo = label.Label().create_label(master, 'PREACTIVADOR DE SIM', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.preactivador = ''
        self.time = tk.StringVar()
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.0, 0.60, 0.5,0.2, letterSize= 16)
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.5, rely=0.68, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.68, 0.15, 0.05, self.cambioIntervalo)
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
        input_widget2.place(relx=0.1, rely=0.80, relheight=0.05, relwidth=0.5)
        self.okBotton2 = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.80, 0.15, 0.05, self.cambioCorreo)
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
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.preactivador = Abrir_pagina1(int(self.time.get()))
        self.preactivador.openEdge()
        time.sleep(3)
        self.preactivador.selectPage(self.link)
    
    def ejecuccionHilo(self):
        hilo_equipos = threading.Thread(target=self.ejecuccion)
        hilo_equipos.start()
        
    def ejecuccion(self):
        try:
            self.on_of(False)
            self.ventana_informacion.write('Empezando ejecuccion')
            self.poliedro.definirBrowser(self.preactivador)
            self.poliedro.seleccionAcceso('195')
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
                        else:
                            self.mensaje = ''
                            self.min = ''
                            self.EquiposInd()
                    except:
                        self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                        self.poliedro.seleccionAcceso('195', start=False)
                        self.position(self.preactivador.retornarHtml(), 'paso1', True)
                        self.contador += 1
            self.ventana_informacion.write('Proceso terminado')
            self.on_of(True)
        except:
            self.alertas('se detiene el programa error')
    

    def EquiposInd(self):
        self.ventana_informacion.write(f'Activando Equipo {self.contador+1} de {self.excel.cantidad}')
        self.iccid = str(self.excel.excel['Iccid'][self.contador])[-12:] 
        self.nit = str(self.excel.excel['Nit'][self.contador])
        self.cedula_excel = str(self.excel.excel['Cedula'][self.contador])
        self.codigo_distribuidor = self.preactivador.read('userDataCodDistribuidor', 'id')
        self.nombre = ''
        self.apellido = ''

        self.position(self.preactivador.retornarHtml(), 'paso1', True)
        cookies = self.preactivador.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        self.cookie_header['Cookie'] = self.preactivador.getCookies()
        headers = {
            'Cookie': self.cookie_header['Cookie']
        }

        #primera
        url = 'https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData/Index2'
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
            'DetailProduct.DocumentTypeId': 2,
            'DetailProduct.DocumentNumber': self.nit,
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

        post_response = session.post(url, headers=headers, data=payload)
        if post_response.status_code == 200:
            self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Validation')
        else:
            raise('error validacion 1')
        
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
        demographic_url = 'https://traffic-md-webapp-prd01.traffic.claro.com.co/Demographic/Index1'
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
            "PersonalInfo.DocumentTypeId": "2",
            "PersonalInfo.Document": self.nit,
            "PersonalInfo.Address.AddressId": "",
            "PersonalInfo.Address.AddressClassId": "Otras",
            "PersonalInfo.Address.Address": "central",
            "PersonalInfo.Address.Department": "ANTIOQUIA",
            "PersonalInfo.Address.City": "MEDELLIN",
            "PersonalInfo.Address.Town": "Central"
        }

        demographic_response = session.post(demographic_url, headers=headers, data=demographic_data)
        if demographic_response.status_code == 200:
            self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService')
        else:
            raise('error demografic')

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
        self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Activation')
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
            
    def validado(self):
        self.cookie_header['Cookie'] = self.preactivador.getCookies()
        
        headers = {
            'Cookie': self.cookie_header['Cookie']
        }
        cookies = self.preactivador.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
            
        demographic_url = "https://traffic-md-webapp-prd01.traffic.claro.com.co/Demographic/Index1"
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
        
        self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Validation')
        try:
            self.preactivador.click('btnNext', 'id')
        except:
            try:
                message = self.preactivador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
                if message == 'Porta ya registrada':
                    self.excel.guardar(self.contador, 'Mensaje', message)
                    self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                    self.poliedro.seleccionAcceso('195', start=False)
                    self.ventana_informacion.write(f"{self.cedula} Porta ya registrada'")
            except:
                self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                self.poliedro.seleccionAcceso('195', start=False)
                self.ventana_informacion.write(f"{self.cedula} error no identificado")
            raise('error controlado kit registrado')
        
        demographic_response = session.post(demographic_url, demographic_data, headers = headers)
        if demographic_response.status_code == 200:
            self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService')
            self.pagina = 4
            self.poliedro.tipoDoc('al', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]')
            self.poliedro.tipoDoc('w', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]')
            self.preactivador.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
            self.pagina = 5
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
            optionsFinal = [
                ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p/text()[2]'],
                ['/html/body/div/strong/strong/div[3]/div[1]/div/button[2]'],
            ]
            self.poliedro.detectOption(optionsFinal, NoneFunc=self.errorGeneral)
        else:
            self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de Demographic/Index1")
            raise Exception("Error en la URL de Demographic/Index1")
    
    
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
                    self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/')
                    self.poliedro.seleccionAcceso('195', start=False)
                    self.ventana_informacion.write(f"{self.iccid} Sim ya registrada'")
            except:
                self.preactivador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/')
                self.poliedro.seleccionAcceso('195', start=False)
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
            self.poliedro.seleccionAcceso('195', start=False)
        else:
            for i in range(self.etapa):
                time.sleep(self.time2)
                self.preactivador.click('btnPrev', 'id')
        self.etapa == 0
    
    def position(self, html, paso=None, wait=False):
        self.scrap = scraping.Scraping(html)
        soup = self.scrap.soup

        while wait:
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
            elif paso == 'paso3':
                elementos_requeridos = [
                    ("h3", "iconoTituloInfoPersonal")
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.preactivador.retornarHtml())
                    soup = self.scrap.soup
            elif paso == 'paso4':
                elementos_requeridos = [
                    ("h3", "iconoTituloDatosEquipoyPlan")
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.preactivador.retornarHtml())
                    soup = self.scrap.soup

    
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