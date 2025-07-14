from navegacion import sub_menu as sm, ventana_informacion
from recursos import label, botones, colors
from funcionalidad import web_controller, poliedro, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
import requests
from selenium.webdriver.common.by import By
import json
import traceback

class Legalizador:

    def __init__(self, master, on_of, alertas):
        self.alertas = alertas
        self.etapa = 0
        self.on_of = on_of
        self.logs = []
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
        time.sleep(3)
        self.legalizador.selectPage(self.link)
    
    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()
    
    def ejecuccion(self):
        try:
            self.poliedro.definirBrowser(self.legalizador)
            self.poliedro.seleccionAcceso('362')
            self.position(self.legalizador.retornarHtml(), 'paso1', True)
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
                        # try:
                            self.min = str(self.excel.excel['min'][self.contador])
                            self.mensaje = str(self.excel.excel['Mensaje'][self.contador])
                            if str(self.mensaje) != 'nan' and str(self.mensaje) != 'error':
                                self.ventana_informacion.write(f'Legalizacion {self.min} ya realizada o con error ya detectado')
                                self.contador += 1
                            else:
                                self.cookie_header['Cookie'] = self.legalizador.getCookies()
                                self.verificar_urls()
                                self.contador += 1
                                # self.poliedro.seleccionAcceso('362', start=False)
                        # except:
                        #     self.position_detect()
                            # while True:
                            #     try:
                            #         self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                            #         self.position(self.legalizador.retornarHtml(), 'restart', True)
                            #         break
                            #     except: pass
                            # self.poliedro.seleccionAcceso('362', start=False)
                            # self.position(self.legalizador.retornarHtml(), 'paso1', True)
                            # self.contador += 1

                self.ventana_informacion.write('Proceso terminado')
                self.ventana_informacion.write(f'Ciclo {i+1} finalizado')
            self.on_of(True)
        except:
            self.alertas('se detiene el programa error')
    
    def establecer_datos(self):
        self.ventana_informacion.write(f'legalizando numero {self.contador+1} de {self.excel.cantidad}')
        self.iccid = str(self.excel.excel['iccid'][self.contador])[-12:] 
        self.cedulaVendedor = str(self.excel.excel['idvendedor'][self.contador]).replace('.0','')
        self.imei = str(self.excel.excel['imei'][self.contador])
        self.min = str(self.excel.excel['min'][self.contador])
        self.nombre = str(self.excel.excel['nombre'][self.contador])
        self.apellido = str(self.excel.excel['apellido'][self.contador])
        self.cedula = str(self.excel.excel['cedula'][self.contador]).replace('.0','')
        self.tipoDoc = str(self.excel.excel['tipodoc'][self.contador])
        self.documentType = 2 if self.tipoDoc.lower() == 'nit' else 1
        self.url_base = 'https://traffic-md-webapp-prd01.traffic.claro.com.co'
        self.headers = {
            'Cookie': self.cookie_header['Cookie']
        }
        self.imei = self.imei.replace(' ','')
        self.cookies = self.legalizador.browser.get_cookies()
        self.session = requests.Session()
        for cookie in self.cookies:
            self.session.cookies.set(cookie['name'], cookie['value'])
    
    def captura_datos(self):
        try:
            self.position(self.legalizador.retornarHtml(), 'paso1', True)
            post_url = f"{self.url_base}/CaptureData/Index2"
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
                "DetailProduct.DocumentTypeId": self.documentType,
                "DetailProduct.DocumentNumber": self.cedula,
                "DetailProduct.LastName": self.apellido,
                "DetailProduct.ExpeditionDate": "",
                "DetailProduct.Imei": self.imei,
                "DetailProduct.AuxiliaryImei": "",
                "DetailProduct.Iccid": self.iccid,
                "DetailProduct.AuxiliaryIccid": "",
                "DetailProduct.DocumentTypeIdRL": "",
                "DetailProduct.DocumentNumberRL": "",
                "DetailProduct.ExpeditionDateRL": "",
                "DetailProduct.SellerId": self.cedulaVendedor,
                "DetailProduct.Msisdn": self.min
            }
            post_response = self.session.post(post_url, headers=self.headers, data=post_data)
            if post_response.status_code == 200:
                ruta = json.loads(post_response.text)
                if ruta['url'] == '/Validation':
                    self.legalizador.selectPage(f'{self.url_base}{ruta["url"]}')
                else:
                    raise('error controlado ruta validation no disponible')
            else:
                raise('error controlado respuesta api captura datos')
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def validate_data(self):
        try:
            self.position(self.legalizador.retornarHtml(), 'validate', True)
            try:
                validate = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span')
            except:
                message = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
                if message == 'El Kit ya se encuentra registrado':
                    self.excel.guardar(self.contador, 'Mensaje', message)
                    self.ventana_informacion.write(f"{self.iccid} El Kit ya se encuentra registrado")
                elif message == 'Plan invalido':
                    self.excel.guardar(self.contador, 'Mensaje', message)
                    self.ventana_informacion.write(f"{self.iccid} {message}")
            if validate == 'Validación Correcta':
                self.legalizador.click('btnNext', 'id')
                while True:
                    time.sleep(1)
                    loading =self.legalizador.style('loading', 'id')
                    if "display: none" in loading:
                        break
                    elif "display: block" in loading:
                        print('loading')
                try:
                    self.position(self.legalizador.retornarHtml(), 'demographic', True)
                except:
                    self.legalizador.click('btnNext', 'id')
            else:
                raise('error controlado validacion no es correcta')
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def captura_demografica(self):
        try:
            try:
                self.position(self.legalizador.retornarHtml(), 'demographic', True)
            except:
                self.position(self.legalizador.retornarHtml(), 'validate', True)
                self.legalizador.click('btnNext', 'id')
                self.position(self.legalizador.retornarHtml(), 'demographic', True)

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
                "PersonalInfo.Document": self.cedula,
                "PersonalInfo.Address.AddressId": "",
                "PersonalInfo.Address.AddressClassId": "Otras",
                "PersonalInfo.Address.Address": "central",
                "PersonalInfo.Address.Department": "ANTIOQUIA",
                "PersonalInfo.Address.City": "MEDELLIN",
                "PersonalInfo.Address.Town": "Central"
            }
            demographic_response = self.session.post(demographic_url, headers=self.headers, data=demographic_data)
            if demographic_response.status_code == 200:
                ruta = json.loads(demographic_response.text)
                if ruta['url'] == '/ProductService':
                    self.legalizador.selectPage(f'{self.url_base}{ruta["url"]}')
                else:
                    raise('error controlado ruta ProductService no disponible')
            else:
                raise('error controlado respuesta api demografic')
            self.position(self.legalizador.retornarHtml(), 'equipo plan', True)
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def datos_equipo_plan(self):
        try:
            self.position(self.legalizador.retornarHtml(), 'equipo plan', True)
            # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService')
            self.legalizador.click('btnNext', 'id')
            self.position(self.legalizador.retornarHtml(), 'activacion', True)
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()

    def activacion(self):
        try:
            self.position(self.legalizador.retornarHtml(), 'activacion', True)
            # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Activation')
            self.legalizador.click('btnNext', 'id')
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def captar_activacion(self):
        try:
            self.position(self.legalizador.retornarHtml(), 'pasoFinal', True)
            time.sleep(2)
            message_element = self.legalizador.readShort2('messageFormItem', 'class')
            # message_element = self.legalizador.browser.find_element(By.CLASS_NAME, 'messageFormItem')
            self.excel.guardar(self.contador, 'Mensaje', message_element)
            self.ventana_informacion.write(f"{self.iccid} {message_element}")
            self.legalizador.click('btnPrev', 'id')
            self.position_detect()
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def restart_new(self):
        # self.position_detect()
        raise('error')
        
        
        
        
        
        
        
        
        


    def verificar_urls(self):
        lista_ejecucion = {
            'paso1' : self.captura_datos,
            'validate' : self.validate_data,
            'demographic' : self.captura_demografica,
            'equipo plan' : self.datos_equipo_plan,
            'activacion' : self.activacion,
        }
        self.establecer_datos()
        mode = 'on'
        while True:
            track = self.position_detect()
            print(track, mode)
            if track in ['login']:
                raise('session cerrada')
            elif track == 'restart':
                try:
                    self.poliedro.seleccionAcceso('362', start=False)
                except:
                    pass
            elif track == 'paso1' and mode == 'off':
                break
            elif mode == 'off':
                try:                        
                    self.legalizador.click('btnPrev', 'id')
                except:
                    pass
            elif track == 'activacion':
                nombre_boton = self.legalizador.value('btnPrev', 'id')
                if nombre_boton == 'Iniciar Nueva Activacion':
                    try:
                        message_element = self.legalizador.readShort2('messageFormItem', 'class')
                        print(f'legalizada {self.contador} {message_element}')
                        self.excel.guardar(self.contador, 'Mensaje', message_element)
                        self.ventana_informacion.write(f"{self.iccid} {message_element}")
                        self.legalizador.click('btnPrev', 'id')
                        # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                        break
                    except:
                        try:
                            error = self.legalizador.readShort2('alertFormItem', 'class')
                            print(f'legalizada con error {self.contador}')
                            self.legalizador.click('btnPrev', 'id')
                            # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                            break
                        except:
                            pass
                  
                else:
                    try:
                        self.legalizador.click('btnNext', 'id')
                    except:
                        pass
            else:
                ejec = lista_ejecucion[track]
                try:
                    print(f'ejecutando {ejec.__name__}')
                    ejec()
                except:
                    mode = 'off'
        # self.captura_datos()
        # self.validate_data()
        # self.captura_demografica()
        # self.datos_equipo_plan()
        # self.activacion()
        # self.captar_activacion()
        pass
    
        
        
        
    #     self.legalizador.click('btnNext', 'id')
      

        
    #     try:
    #         while True:
    #             try:
    #                 self.legalizador.readShort2('/html/body/div/div[2]/section/div/div[2]/div[1]/div[1]/hgroup/h4')
    #                 break
    #             except:
    #                 print('aun en while')
    #         # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Validation')
    #         time.sleep(2)
    #         try:
    #             message = self.legalizador.read('errorFormItem', 'class')
    #         except:
    #             try:
    #                 message = self.legalizador.read('messageFormItem', 'class')
    #             except:
    #                 message = ''
    #         if message == 'La consulta demograficos no arrojo informacion para este cliente':
    #             self.excel.guardar(self.contador, 'Mensaje', message)
    #             self.ventana_informacion.write(f"{iccid} {message}")
    #             raise(message)
    #         if message == 'Señor consultor, se presentó un inconveniente al intentar procesar su solicitud, por favor intente nuevamente':
    #             self.ventana_informacion.write(f"{iccid} {message}")
    #             raise(message)
    #         # self.legalizador.click('btnNext', 'id')
    #         # time.sleep(3)
    #     except:
    #         try:
    #             message = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
    #             if message == 'El Kit ya se encuentra registrado':
    #                 self.excel.guardar(self.contador, 'Mensaje', message)
    #                 self.ventana_informacion.write(f"{iccid} El Kit ya se encuentra registrado")
    #         except:
    #             pass
    #         raise('error')
            
    #     demographic_response = session.post(demographic_url, headers=headers, data=demographic_data)
    #     if demographic_response.status_code == 200:
    #         demographic_json = demographic_response.json()
    #         if demographic_json.get("rta") == True and not demographic_json.get("errores") and demographic_json.get("url") == "/ProductService":
                
                
    #             self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService')
    #             self.legalizador.click('btnNext', 'id')
    #             self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Activation')
    #             self.legalizador.click('btnNext', 'id')
                
    #             # Buscar el mensaje en la página y guardarlo en el Excel
    #             try:
    #                 self.position(self.legalizador.retornarHtml(), 'pasoFinal', True)
    #                 time.sleep(2)
    #                 message_element = self.legalizador.readShort2('messageFormItem', 'class')
    #                 # message_element = self.legalizador.browser.find_element(By.CLASS_NAME, 'messageFormItem')
    #                 self.excel.guardar(self.contador, 'Mensaje', message_element)
    #                 self.ventana_informacion.write(f"{iccid} {message_element}")
    #             except:pass
    #             self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
    #             self.poliedro.seleccionAcceso('362', start=False)
    #             self.position(self.legalizador.retornarHtml(), 'paso1', True)
                
    #         else:
    #             self.excel.guardar(self.contador, 'Mensaje', "Error en la validación de Demographic/Index1")
    #             raise Exception("Error en la validación de Demographic/Index1")
    #     else:
    #         self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de Demographic/Index1")
    #         raise Exception("Error en la URL de Demographic/Index1")
    # # else:
    # #     self.excel.guardar(self.contador, 'Mensaje', "Error en la URL para legalizar")
    # #     raise Exception("Error en la URL de validación final")

    def position(self, html, paso=None, wait=False, fast= False):
        self.scrap = scraping.Scraping(html)
        soup = self.scrap.soup
        count = 0
        top = 100 if paso != 'validate' else 500

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
                    self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'validate':
                elementos_requeridos = [
                    ("h3", "iconoTituloDatosDistribuidor"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'demographic':
                elementos_requeridos = [
                    ("h3", "iconoTituloInfoPersonal"),
                    # ("h3", "iconoTituloDatosUbicacion"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'equipo plan':
                elementos_requeridos = [
                    ("h3", "iconoTituloDatosEquipoyPlan"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'activacion':
                elementos_requeridos = [
                    ("h3", "iconoTituloActivacionesCliente"),
                    ("h3", "iconoTituloActivacionesServicios"),
                    ("h3", "iconoTituloActivacionesProducto"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'pasoFinal':
                elementos_requeridos = [
                    ("h3", "iconoTituloActivacionesCliente"),
                    ("h3", "iconoTituloActivacionesServicios"),
                    ("h3", "iconoTituloActivacionesProducto"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'restart':
                elementos_requeridos = [
                    ("h3", "iconoTituloProducto"),
                    ("span", "select2-selection__rendered"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 0
                else:
                    self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
                        
    def position_detect(self):
        position = {
            'paso1' : [("h3", "iconoTituloCliente"),("h3", "iconoTituloInfoVenta"),("h3", "iconoTituloEquipo")],
            'validate' : [ ("h3", "iconoTituloDatosDistribuidor")],
            'demographic' : [ ("h3", "iconoTituloInfoPersonal")],
            'equipo plan' : [ ("h3", "iconoTituloDatosEquipoyPlan")],
            'activacion' : [ ("h3", "iconoTituloActivacionesCliente"),("h3", "iconoTituloActivacionesServicios"),("h3", "iconoTituloActivacionesProducto")],
            'restart': [("h3", "iconoTituloProducto"), ("span", "select2-selection__rendered")],
            'login': [("input", "botonLoginhomePoliedro")]
        }
        while True:
            count = 0
            self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
            soup = self.scrap.soup
            pos = None
            for i, j in position.items():
                if self.validate_position(j, soup, 'class'):
                    pos = i
                    return pos
            print(pos)
            if pos == 'restart':
                self.poliedro.seleccionAcceso('362', start=False)
                break
            elif pos == 'paso1':
                break
            elif pos == 'login':
                raise('error login')
            count += 1
            if count == 100:
                raise('restar controlado')


    
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