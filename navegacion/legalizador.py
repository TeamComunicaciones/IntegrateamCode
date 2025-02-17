from navegacion import sub_menu as sm, ventana_informacion
from recursos import label, botones, colors
from funcionalidad import web_controller, poliedro, excel
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
import requests
from selenium.webdriver.common.by import By

class Legalizador:

    def __init__(self, master, on_of, alertas):
        self.alertas = alertas
        self.etapa = 0
        self.on_of = on_of
        self.poliedro = poliedro.Poliedro(legalizador=True)
        self.excel = excel.Excel_controller()
        self.link = 'https://poliedrodist.comcel.com.co/'
        self.link2 = 'https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.titulo = label.Label().create_label(master, 'LEGALIZADOR', 0.2, 0.0, 0.5, 0.2, letterSize=25)
        self.ventana_informacion = ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master, 3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.legalizador = ''
        self.time = tk.StringVar()
        self.time2 = 3
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.0, 0.65, 0.5, 0.2, letterSize=16)
        self.titulo = label.Label().create_label(self.menu.submenu, 'Ciclos', 0.0, 0.78, 0.5, 0.05, letterSize=16)
        self.titulo2 = label.Label().create_label(self.menu.submenu, 'Correo', 0.25, 0.83, 0.5, 0.05, letterSize=16)
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.5, rely=0.73, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.73, 0.15, 0.05, self.cambioIntervalo)
        self.okBotton.configure(fg_color=color.team, text_color='white')
        self.correo = 'acruz@teamcomunicaciones.com'
        self.correoEdit = tk.StringVar()
        self.correoEdit.set(self.correo)
        self.cookie_header = {}
        self.repeticiones = '1'
        self.repeticionesEdit = tk.StringVar()
        self.repeticionesEdit.set(self.repeticiones)
        input_widget2 = ctk.CTkEntry(self.menu.submenu, textvariable=self.correoEdit)
        input_widget2.place(relx=0.15, rely=0.89, relheight=0.05, relwidth=0.7)
        input_widget3 = ctk.CTkEntry(self.menu.submenu, textvariable=self.repeticionesEdit)
        input_widget3.place(relx=0.5, rely=0.79, relheight=0.05, relwidth=0.2)
        self.okBotton2 = boton.create_button(self.menu.submenu, 'confirmar', 0.3, 0.95, 0.40, 0.05, self.cambioCorreo)
        self.okBotton2.configure(fg_color=color.team, text_color='white')
        self.okBotton3 = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.79, 0.15, 0.05, self.cambioCiclos)
        self.okBotton3.configure(fg_color=color.team, text_color='white')
    
    def abrir_excel(self):
        self.ventana_informacion.write('excel legalizador abierto recuerde cerrar antes de iniciar')
        p = Popen("src\\legalizador\\openExcel.bat")
        stdout, stderr = p.communicate()
    
    def cambioCiclos(self):
        self.repeticiones = self.repeticionesEdit.get()
        self.ventana_informacion.write(f'Numero de repeticiones configurado en {self.repeticiones}')
    
    def cambioIntervalo(self):
        self.legalizador.actualizarIntervalo(self.time.get())
        self.ventana_informacion.write(f'intervalo {self.time.get()} segundos')

    def cambioCorreo(self):
        self.correo = self.correoEdit.get()
        self.ventana_informacion.write(f'Correo actualizado por {self.correo}')
    
    def abrir_pagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller): pass
        self.legalizador = Abrir_pagina1(int(self.time.get()))
        self.legalizador.openEdge()
        self.legalizador.selectPage(self.link)
    
    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()
    
    def ejecuccion(self):
        self.poliedro.definirBrowser(self.legalizador)
        self.poliedro.seleccionAcceso('362')
        for i in range(int(self.repeticiones)):
            self.ciclo = True
            self.contador = 0
            self.excel.leer_excel('src\\legalizador\\legalizador.xlsx', 'iccid')
            self.excel.quitarFormatoCientifico('iccid')
            self.excel.quitarFormatoCientifico('imei')
            self.ventana_informacion.write(f'Ciclo {i+1}')
            while self.ciclo:
                if self.contador == self.excel.cantidad:
                    self.ciclo = False
                else:
                    try:
                        self.min = str(self.excel.excel['min'][self.contador])
                        self.mensaje = str(self.excel.excel['Mensaje'][self.contador])
                        if str(self.mensaje) != 'nan' and str(self.mensaje) != 'error':
                            self.ventana_informacion.write(f'Legalizacion {self.min} ya realizada o con error ya detectado')
                            self.contador += 1
                        else:
                            self.cookie_header['Cookie'] = self.legalizador.getCookies()
                            self.verificar_urls()
                    except:
                        self.contador += 1

            self.ventana_informacion.write('Proceso terminado')
            self.ventana_informacion.write(f'Ciclo {i+1} finalizado')
        self.on_of(True)
    def verificar_urls(self):
        self.ventana_informacion.write(f'legalizando numero {self.contador+1} de {self.excel.cantidad}')
        iccid = str(self.excel.excel['iccid'][self.contador])[-12:] 
        cedulaVendedor = str(self.excel.excel['idvendedor'][self.contador]).replace('.0','')
        imei = str(self.excel.excel['imei'][self.contador])
        min = str(self.excel.excel['min'][self.contador])
        self.nombre = str(self.excel.excel['nombre'][self.contador])
        self.apellido = str(self.excel.excel['apellido'][self.contador])
        cedula = str(self.excel.excel['cedula'][self.contador]).replace('.0','')
        self.tipoDoc = str(self.excel.excel['tipodoc'][self.contador])
        
        headers = {
            'Cookie': self.cookie_header['Cookie']
        }
        
        # Validar la primera URL
        imei = imei.replace(' ','')
        cookies = self.legalizador.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        url1 = f"https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData/ValidatIccidErrors?imei={imei}&iccid={iccid}&_=1738762903926"
        response1 = session.get(url1, headers=headers)
        if response1.status_code == 200:
            json_response1 = response1.json()
            if json_response1.get("InfoShowEsim") == False and json_response1.get("EsimErrorMsj") is None:
                pass
            else:
                self.excel.guardar(self.contador, 'Mensaje', "Error en la validación de EsimErrors")
                raise Exception("Error en la validación de EsimErrors")
        else:
            self.excel.guardar(self.contador, 'Mensaje', f"Error en la URL: {url1}")
            raise Exception(f"Error en la URL: {url1}")

        # Validar la segunda URL
        url2 = f"https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData/GetValPin?phone={min}&docNumber={cedula}&product=362&_=1738762903927"
        response2 = session.get(url2)
        if response2.status_code == 200:
            json_response2 = response2.json()
            if json_response2.get("code") == 0 and json_response2.get("description") is None and json_response2.get("response") is None and json_response2.get("Attempts") is None and json_response2.get("url") is None:
                pass
            else:
                self.excel.guardar(self.contador, 'Mensaje', "Error en la validación de GetValPin")
                raise Exception("Error en la validación de GetValPin")
        else:
            self.excel.guardar(self.contador, 'Mensaje', f"Error en la URL: {url2}")
            raise Exception(f"Error en la URL: {url2}")

        # Si ambas validaciones son exitosas, hacer la petición POST
        post_url = "https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData/Index2"
        post_data = {
            "ProductShortcutName": "362 - (GLKC) - Legalizacion Kit Contado",
            "Pospago": False,
            "TechnologyId": 1,
            "ObligaFlagImei": "",
            "NumIOT": "910,919",
            "productShortcut": 362,
            "ActivationId": 202,
            "ModuleId": 6,
            "ProductTypeId": 1,
            "PaymentId": 1,
            "PlanId": 1,
            "ProductId": 362,
            "Pospago": False,
            "IsSpecialUser": False,
            "ActiveFieldsPortability": True,
            "DetailProduct.ApplyPreactivedMin": False,
            "DetailProduct.CausalGsmServiceChange": 0,
            "DetailProduct.DealerCps": False,
            "DetailProduct.CodTechImei": "",
            "DetailProduct.DocumentTypeId": 2,
            "DetailProduct.DocumentNumber": cedula,
            "DetailProduct.LastName": self.apellido,
            "DetailProduct.ExpeditionDate": "",
            "DetailProduct.Imei": imei,
            "DetailProduct.AuxiliaryImei": "",
            "DetailProduct.Iccid": iccid,
            "DetailProduct.AuxiliaryIccid": "",
            "DetailProduct.DocumentTypeIdRL": "",
            "DetailProduct.DocumentNumberRL": "",
            "DetailProduct.ExpeditionDateRL": "",
            "DetailProduct.SellerId": cedulaVendedor,
            "DetailProduct.Msisdn": min
        }
        post_response = session.post(post_url, headers=headers, data=post_data)
        if post_response.status_code == 200:
            self.ventana_informacion.write(f"{iccid} procesada correctamente")
     # Hacer la petición GET a la URL final
        final_url = "https://traffic-md-webapp-prd01.traffic.claro.com.co/Validation"
        final_response = session.get(final_url)
        if final_response.status_code == 200:
            content = final_response.text
            start_index = content.find("<!-- LeaP Alert A -->")
            end_index = content.find("<!-- LeaP Alert B -->", start_index)
            if start_index != -1 and end_index != -1:
                specific_content = content[start_index:end_index]
                # self.ventana_informacion.write(f"Contenido específico encontrado: {specific_content}")
            else:
                self.excel.guardar(self.contador, 'Mensaje', "Error: Contenido específico no encontrado")
                raise Exception("Error: Contenido específico no encontrado")
        else:
            self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de validación final")
            raise Exception("Error en la URL de validación final")
            
        if post_response.status_code == 200:
            # Si la petición POST es exitosa, hacer la petición POST adicional
            demographic_url = "https://traffic-md-webapp-prd01.traffic.claro.com.co/Demographic/Index1"
            demographic_data = {
                "PersonalInfo.GreetingId": "O",
                "PersonalInfo.Name": self.nombre,
                "PersonalInfo.LastName": self.apellido,
                "PersonalInfo.Email": "acruz@teamcomunicaciones.com",
                "PersonalInfo.Phone.PhoneId": "",
                "PersonalInfo.Phone.PhoneClass": "2",
                "PersonalInfo.Phone.Prefix": "604",
                "PersonalInfo.Phone.PhoneNumber": "0313123",
                "PersonalInfo.EmailInitial": "",
                "PersonalInfo.DocumentTypeId": "2",
                "PersonalInfo.Document": cedula,
                "PersonalInfo.Address.AddressId": "",
                "PersonalInfo.Address.AddressClassId": "Otras",
                "PersonalInfo.Address.Address": "central",
                "PersonalInfo.Address.Department": "ANTIOQUIA",
                "PersonalInfo.Address.City": "MEDELLIN",
                "PersonalInfo.Address.Town": "Central"
            }
            self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Validation')
            try:
                self.legalizador.click('btnNext', 'id')
            except:
                try:
                    message = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
                    if message == 'El Kit ya se encuentra registrado':
                        self.excel.guardar(self.contador, 'Mensaje', message)
                        self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/')
                        self.poliedro.seleccionAcceso('362', start=False)
                        self.ventana_informacion.write(f"{iccid} El Kit ya se encuentra registrado")
                except:
                    self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/')
                    self.poliedro.seleccionAcceso('362', start=False)
                    self.ventana_informacion.write(f"{iccid} error no identificado")
                raise('error controlado kit registrado')
                
            demographic_response = session.post(demographic_url, headers=headers, data=demographic_data)
            if demographic_response.status_code == 200:
                demographic_json = demographic_response.json()
                if demographic_json.get("rta") == True and not demographic_json.get("errores") and demographic_json.get("url") == "/ProductService":
                    
                    
                    self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService')
                    self.legalizador.click('btnNext', 'id')
                    self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Activation')
                    self.legalizador.click('btnNext', 'id')
                    
                    # Buscar el mensaje en la página y guardarlo en el Excel
                    message_element = self.legalizador.browser.find_element(By.CLASS_NAME, 'messageFormItem')
                    self.excel.guardar(self.contador, 'Mensaje', message_element.text)
                    self.ventana_informacion.write(f"{iccid} {message_element.text}")
                    self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/')
                    self.poliedro.seleccionAcceso('362', start=False)
                    
                else:
                    self.excel.guardar(self.contador, 'Mensaje', "Error en la validación de Demographic/Index1")
                    raise Exception("Error en la validación de Demographic/Index1")
            else:
                self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de Demographic/Index1")
                raise Exception("Error en la URL de Demographic/Index1")
        else:
            self.excel.guardar(self.contador, 'Mensaje', "Error en la URL para legalizar")
            raise Exception("Error en la URL de validación final")