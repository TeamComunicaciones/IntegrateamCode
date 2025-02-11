from navegacion import sub_menu as sm, ventana_informacion
from recursos import label, botones, colors
from funcionalidad import web_controller, poliedro, excel
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
import requests

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
        # response1 = requests.get(url1, headers=headers)
        if response1.status_code == 200:
            json_response1 = response1.json()
            if json_response1.get("InfoShowEsim") == False and json_response1.get("EsimErrorMsj") is None:
                self.ventana_informacion.write("Validación de EsimErrors exitosa")
            else:
                self.excel.guardar(self.contador, 'Mensaje', "Error en la validación de EsimErrors")
                raise Exception("Error en la validación de EsimErrors")
        else:
            self.excel.guardar(self.contador, 'Mensaje', f"Error en la URL: {url1}")
            raise Exception(f"Error en la URL: {url1}")

        # Validar la segunda URL
        url2 = f"https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData/GetValPin?phone={min}&docNumber={cedula}&product=362&_=1738762903927"
        response2 = session.get(url2)
        # response2 = requests.get(url2, headers=headers)
        if response2.status_code == 200:
            json_response2 = response2.json()
            if json_response2.get("code") == 0 and json_response2.get("description") is None and json_response2.get("response") is None and json_response2.get("Attempts") is None and json_response2.get("url") is None:
                self.ventana_informacion.write("Validación de GetValPin exitosa")
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
            "DetailProduct.LastName": "",
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
        # final_response = requests.get(final_url, headers=headers)
        if final_response.status_code == 200:
            # Buscar el contenido específico en la respuesta
            content = final_response.text
            start_index = content.find("<!-- LeaP Alert A -->")
            end_index = content.find("<!-- LeaP Alert B -->", start_index)
            if start_index != -1 and end_index != -1:
                specific_content = content[start_index:end_index]
                self.ventana_informacion.write(f"Contenido específico encontrado: {specific_content}")
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
                "PersonalInfo.Name": "HNOS GOMEZ INVERSIONES S.A.S.",
                "PersonalInfo.LastName": "",
                "PersonalInfo.Email": "manuel.arango@teamcomunicaciones.com",
                "PersonalInfo.Phone.PhoneId": "",
                "PersonalInfo.Phone.PhoneClass": "2",
                "PersonalInfo.Phone.Prefix": "604",
                "PersonalInfo.Phone.PhoneNumber": "3131234",
                "PersonalInfo.EmailInitial": "",
                "PersonalInfo.DocumentTypeId": "2",
                "PersonalInfo.Document": "900721484",
                "PersonalInfo.Address.AddressId": "",
                "PersonalInfo.Address.AddressClassId": "Otras",
                "PersonalInfo.Address.Address": "central",
                "PersonalInfo.Address.Department": "ANTIOQUIA",
                "PersonalInfo.Address.City": "MEDELLIN",
                "PersonalInfo.Address.Town": "Central"
            }
            self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Validation')
            self.legalizador.click('btnNext', 'id')
            demographic_response = session.post(demographic_url, headers=headers, data=demographic_data)
            if demographic_response.status_code == 200:
                demographic_json = demographic_response.json()
                if demographic_json.get("rta") == True and not demographic_json.get("errores") and demographic_json.get("url") == "/ProductService":
                    self.ventana_informacion.write("Petición POST a Demographic/Index1 exitosa")
                    
                    # Si la petición POST a Demographic/Index1 es exitosa, hacer la petición POST a ProductService/Index1
                    # product_service_url = "https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService/Index1"
                    # product_service_data = {
                    #     "EquipmentPlanDataViewModel.SaleDate": "11/02/2025",
                    #     "EquipmentPlanDataViewModel.IMEI": "353167580614683",
                    #     "EquipmentPlanDataViewModel.ICCID": "89571017023099423516",
                    #     "EquipmentPlanDataViewModel.MobileEquipment": "TCL 4041 T311A GRIS",
                    #     "EquipmentPlanDataViewModel.Plan": "Plan Kit Prepago GSM",
                    #     "EquipmentPlanDataViewModel.InternalCode": "",
                    #     "ValorBussinesPlan2": "0",
                    #     "EquipmentPlanDataViewModel.ContractType": "2",
                    #     "EquipmentPlanDataViewModel_CfmToFirstInvoice": "false",
                    #     "IsCesionDifPostPost": "false",
                    #     "EquipmentPlanDataViewModel.InvoiceCustomer": ""
                    # }
                    self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService')
                    self.legalizador.click('btnNext', 'id')
                    # product_service_response = session.post(product_service_url, headers=headers, data=product_service_data)
                    self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Activation')
                    self.legalizador.click('btnNext', 'id')
                    self.legalizador.click('btnPrev', 'id')
                    # if product_service_response.status_code == 200:
                    #     product_service_json = product_service_response.json()
                    #     if product_service_json.get("rta") == True and not product_service_json.get("errores") and product_service_json.get("url") == "/ProductService":
                    #         self.ventana_informacion.write("Petición POST a ProductService/Index1 exitosa")
                    #     else:
                    #         self.excel.guardar(self.contador, 'Mensaje', "Error en la validación de ProductService/Index1")
                    #         raise Exception("Error en la validación de ProductService/Index1")
                    # else:
                    #     self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de ProductService/Index1")
                    #     raise Exception("Error en la URL de ProductService/Index1")
                else:
                    self.excel.guardar(self.contador, 'Mensaje', "Error en la validación de Demographic/Index1")
                    raise Exception("Error en la validación de Demographic/Index1")
            else:
                self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de Demographic/Index1")
                raise Exception("Error en la URL de Demographic/Index1")
        else:
            self.excel.guardar(self.contador, 'Mensaje', "Error en la URL para legalizar")
            raise Exception("Error en la URL de validación final")


        
    # def ejecuccion_old(self):
    #     try:
    #         self.on_of(False)
    #         self.ventana_informacion.write('Empezando ejecuccion')
    #         self.poliedro.definirBrowser(self.legalizador)
    #         self.poliedro.seleccionAcceso('362')
    #         for i in range(int(self.repeticiones)):
    #             self.ciclo = True
    #             self.contador = 0
    #             self.excel.leer_excel('src\legalizador\legalizador.xlsx','iccid')
    #             self.excel.quitarFormatoCientifico('iccid')
    #             self.ventana_informacion.write(f'Ciclo {i+1}')
    #             while self.ciclo:
    #                 if self.contador == self.excel.cantidad:
    #                     self.ciclo = False
    #                 else:
    #                     try:
    #                         self.min = str(self.excel.excel['min'][self.contador])
    #                         self.mensaje= str(self.excel.excel['Mensaje'][self.contador])
    #                         if str(self.mensaje) != 'nan' and str(self.mensaje) != 'error':
    #                             self.ventana_informacion.write(f'Legalizacion {self.min} ya realizada o con error ya detectado')
    #                             self.contador += 1
    #                         else:
    #                             self.mensaje = ''
    #                             self.min = ''
    #                             self.legalizadorInd()
    #                     except:
    #                         self.ventana_informacion.write(f'Siguiente por error en legalizacion de {self.min}')
    #                         if f'{len(self.cedula)}' == '9' and self.tipoDoc != 'nit':
    #                             self.excel.guardar(self.contador, 'Mensaje', 'error por cedula de 9 digitos')
    #                         else:
    #                             self.excel.guardar(self.contador, 'Mensaje', 'error')
    #                         self.contador += 1
    #                         try:
    #                             self.reinicio()
    #                         except:
    #                             try:
    #                                 self.poliedro.reinicio(start=False)
    #                             except:
    #                                 self.poliedro.reinicio()
    #             self.ventana_informacion.write('Proceso terminado')
    #             self.ventana_informacion.write(f'Ciclo {i+1} finalizado')
    #         self.on_of(True)
    #     except:
    #         self.alertas('se detiene el programa error')
    

    # def legalizadorInd(self):
    #     self.ventana_informacion.write(f'legalizando numero {self.contador+1} de {self.excel.cantidad}')
    #     self.iccid = str(self.excel.excel['iccid'][self.contador])[-12:] 
    #     self.cedulaVendedor = str(self.excel.excel['idvendedor'][self.contador]).replace('.0','')
    #     self.imei = str(self.excel.excel['imei'][self.contador])
    #     self.min = str(self.excel.excel['min'][self.contador])
    #     self.nombre = str(self.excel.excel['nombre'][self.contador])
    #     self.apellido = str(self.excel.excel['apellido'][self.contador])
    #     self.cedula = str(self.excel.excel['cedula'][self.contador]).replace('.0','')
    #     self.tipoDoc = str(self.excel.excel['tipodoc'][self.contador])
            

    #     primerFormulario = [
    #         ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[2]/div/div[1]/div/input', self.cedulaVendedor],
    #         ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[2]/div/div[2]/div/input', self.min],
    #         ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[3]/div[1]/div/input', self.imei],
    #         ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[3]/div[2]/div/input', self.iccid],
    #     ]

    #     if self.excel.excel['tipodoc'][self.contador].lower().replace(" ","") == 'nit':
    #         self.poliedro.seleccionNit()
    #         primerFormulario.append(['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[2]/div/input', self.cedula[:9]])
    #         self.poliedro.rellenoFormulario(5, primerFormulario)
    #     else:
    #         primerFormulario.append(['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[2]/div/input', self.cedula])
    #         primerFormulario.append(['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[3]/div/input', self.apellido])
    #         self.poliedro.rellenoFormulario(6, primerFormulario)
    #     time.sleep(self.time2)
    #     self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[5]/input[1]')
    #     self.etapa = 1
    #     options = [
    #         ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span'],
    #         ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div'],
    #     ]
    #     functionList = [
    #         self.validado,
    #         self.errorKitRegistrado,
    #     ]
    #     self.poliedro.detectOption(options, functionList, NoneFunc=self.errorGeneral)


    # def validado(self):
    #     validado = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span')
    #     if 'Validación Correcta' in validado: pass
    #     else: raise('invalido')
    #     time.sleep(0.5)
    #     time.sleep(self.time2)
    #     self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[3]')
    #     self.etapa = 2
    #     options = [
    #         ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/ul/li']
    #     ]
    #     self.poliedro.detectOption(options,[self.errorConsultaDemografica], NoneFunc=self.terminarValidado)

    # def terminarValidado(self):
    #     self.poliedro.saludo()
    #     if self.excel.excel['tipodoc'][self.contador].lower().replace(" ","") == 'nit':
    #         self.poliedro.tipoDoc('nit')
    #     else:
    #         self.poliedro.tipoDoc('cedula')
    #         self.poliedro.rellenoApellido(self.apellido)
    #     self.poliedro.rellenoNombre(self.nombre)
    #     self.poliedro.rellenoCedula(self.cedula)
    #     self.poliedro.correo(self.correo)
    #     self.poliedro.rellenoNumero()
    #     self.poliedro.rellenoDireccion(legalizador=True)
    #     time.sleep(self.time2)
    #     self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/input[2]')
    #     self.etapa = 3
    #     time.sleep(self.time2)
    #     self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[2]')
    #     self.etapa = 4
    #     time.sleep(self.time2)
    #     self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
    #     self.etapa = 5
    #     activado = True
    #     while activado:
    #         try:
    #             mensaje = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p')
    #             if 'Solicitud fue enviada satisfactoriamente' in mensaje:
    #                 activado = False
    #         except:
    #             time.sleep(1)
    #     #/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p
    #     # Su Solicitud fue enviada satisfactoriamente.
    #     self.ventana_informacion.write(f'Legalizacion exitosa de {self.min}')
    #     self.excel.guardar(self.contador, 'Mensaje', 'legalizada')
    #     self.reinicio()
    #     self.contador += 1
    
    # def errorConsultaDemografica(self):
    #     validado = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/ul/li')
    #     self.ventana_informacion.write(f'{self.min} {validado}')
    #     self.excel.guardar(self.contador, 'Mensaje', validado)
    #     self.reinicio()
    #     self.contador += 1
    
    # def errorKitRegistrado(self):
    #     validado = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
    #     self.ventana_informacion.write(f'{self.min} {validado}')
    #     self.excel.guardar(self.contador, 'Mensaje', validado)
    #     # self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
    #     self.reinicio()
    #     self.contador += 1

    # def errorGeneral(self):
    #     raise('error general')
    
    # def reinicio(self):
    #     if self.etapa == 0:
    #         pass
    #     if self.etapa == 5:
    #         time.sleep(self.time2)
    #         self.legalizador.click('btnPrev', 'id')
    #         self.poliedro.seleccionAcceso('362', start=False)
    #     else:
    #         for i in range(self.etapa):
    #             time.sleep(self.time2)
    #             self.legalizador.click('btnPrev', 'id')
    #     self.etapa == 0

        

    