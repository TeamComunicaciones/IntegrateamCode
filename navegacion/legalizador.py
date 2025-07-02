from navegacion import sub_menu as sm, ventana_informacion
from recursos import label, botones, colors
from funcionalidad import web_controller, poliedro, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
        except Exception as e:
            self.log_error("definirBrowser", e)
            return

        try:
            self.legalizador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
        except Exception as e:
            self.log_error("click en menú", e)
            return
        
        if not self.wait_for_loading(legalizador=False):
            raise Exception("Timeout esperando carga inicial en captura_datos")

        try:
            self.poliedro.seleccionAcceso('362')
        except Exception as e:
            self.log_error("seleccionAcceso", e)
            return

        try:
            self.position(self.legalizador.retornarHtml(), 'paso1', True)
        except Exception as e:
            self.log_error("position paso1", e)
            return

        try:
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

                            mensaje_valido = str(self.mensaje) not in ['nan', 'error']
                            min_invalido = str(self.excel.excel['Min'][self.contador]) in ['error', 'procesado']

                            if mensaje_valido or min_invalido:
                                self.ventana_informacion.write(f'Legalizacion {self.min} ya realizada o con error ya detectado')
                                self.contador += 1
                            else:
                                if self.contador >= 1:
                                    try:
                                        self.legalizador.click('toggleProductBTN', 'id')
                                    except Exception as e:
                                        self.log_error("click toggleProductBTN", e)
                                    self.legalizador.seleccionAcceso('Seleccione...', start=False)
                                    self.legalizador.seleccionAcceso('362', start=False)
                                    if not self.wait_for_loading():
                                        raise Exception("Timeout esperando carga inicial en captura_datos")

                                self.cookie_header['Cookie'] = self.legalizador.getCookies()
                                self.verificar_urls()
                                self.contador += 1
                        except Exception as e:
                            self.log_error("iteración de ciclo", e)
                            self.contador += 1
                self.ventana_informacion.write('Proceso terminado')
                self.ventana_informacion.write(f'Ciclo {i+1} finalizado')
            try:
                self.legalizador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
            except Exception as e:
                self.log_error("click en menú", e)
            self.on_of(True)
        except Exception as e:
            self.log_error("bloque principal", e)

    def log_error(self, contexto, e):
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{contexto}] Error: {str(e)}\n")
            f.write(traceback.format_exc())
        self.ventana_informacion.write(f"Error en {contexto}: {str(e)}") 
    
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
        # ELIMINAR DEPENDENCIAS DE API - Solo usar datos necesarios para pantalla
        self.imei = self.imei.replace(' ','')
    
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
    
    def captura_datos_optimized(self):
        """
        Versión optimizada de captura_datos usando wait_for_loading()
        """
        try:
            # USAR MÉTODO REUTILIZABLE PARA ESPERA INICIAL
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga inicial en captura_datos")
            
            self.position(self.legalizador.retornarHtml(), 'paso1', True)
            
            # Click en el campo select2 para abrirlo
            self.legalizador.click('select2-DetailProduct_DocumentTypeId-container', 'id')
            # Escribir en el input de búsqueda que aparece dinámicamente
            if self.documentType == 2:  # NIT
                self.legalizador.write('/html/body/span/span/span[1]/input', 'nit', 'xpath')
            else:  # CC
                self.legalizador.write('/html/body/span/span/span[1]/input', 'cedula', 'xpath')
            # Presionar Enter para seleccionar la opción encontrada
            self.legalizador.write('/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')
           
            # Llenar campos del formulario usando métodos existentes
            self.legalizador.write('DetailProduct_DocumentNumber', self.cedula, 'id')
            if self.documentType != 2:  # NIT
                self.legalizador.write('DetailProduct_LastName', self.apellido, 'id')
            self.legalizador.write('DetailProduct_Imei', self.imei, 'id')
            self.legalizador.write('DetailProduct_Iccid', self.iccid, 'id')
            self.legalizador.write('DetailProduct_SellerId', self.cedulaVendedor, 'id')
            self.legalizador.write('DetailProduct_Msisdn', self.min, 'id')
            
            # Hacer clic en siguiente
            self.legalizador.click('btnNext', 'id')
            
            # USAR MÉTODO REUTILIZABLE PARA ESPERA FINAL
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de hacer clic en Siguiente")
                    
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def captura_demografica_optimized(self):
        """
        Versión optimizada de captura_demografica usando wait_for_loading()
        """
        try:
            # USAR MÉTODO REUTILIZABLE PARA ESPERA INICIAL
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga inicial en captura_demografica")
                
            try:
                self.position(self.legalizador.retornarHtml(), 'demographic', True)
            except:
                self.position(self.legalizador.retornarHtml(), 'validate', True)
                self.legalizador.click('btnNext', 'id')
                self.position(self.legalizador.retornarHtml(), 'demographic', True)

            # USAR MÉTODO REUTILIZABLE PARA SEGUNDA ESPERA
            if not self.wait_for_loading(timeout=15, sleep_interval=0.3):
                raise Exception("Timeout esperando carga del formulario demográfico")
            
            errors = self.legalizador.read('viewErrors', 'id')
            if errors:
                self.excel.guardar(self.contador, 'Mensaje', errors)
                self.excel.guardar(self.contador, 'Min', 'error')
                self.ventana_informacion.write(f"{self.iccid} {errors}")
                raise('error controlado en formulario demografico')

            # Saludo - Dropdown select2
            self.legalizador.click('select2-PersonalInfo_GreetingId-container', 'id')
            self.legalizador.write('/html/body/span/span/span[1]/input', 'sr', 'xpath')
            self.legalizador.write('/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')
                
            self.legalizador.write('PersonalInfo_Name', self.nombre, 'id')

            if self.documentType != 2:
                self.legalizador.write('PersonalInfo_LastName', self.apellido, 'id')

            self.legalizador.write('PersonalInfo_Email', self.correo, 'id')
            
            # Tipo de teléfono - Dropdown select2
            self.legalizador.click('select2-PhoneClass-container', 'id')
            self.legalizador.write('/html/body/span/span/span[1]/input', 'fijo', 'xpath')
            self.legalizador.write('/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')

            # ESPERAR DINÁMICAMENTE CON MÉTODO REUTILIZABLE
            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar tipo de teléfono")
            
            self.legalizador.write('PersonalInfo.Phone.PhoneNumber', '0313123', 'name')
            
            # Tipo de dirección - Dropdown select2
            self.legalizador.click('select2-AddressClassId-container', 'id')
            self.legalizador.write('/html/body/span/span/span[1]/input', 'otras', 'xpath')
            self.legalizador.write('/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')

            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar tipo de dirección")
                
            self.legalizador.write('PersonalInfo.Address.Address', 'central', 'name')

            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de escribir dirección")
            
            # Departamento - Dropdown select2
            self.legalizador.click('select2-Department-container', 'id')
            self.legalizador.write('/html/body/span/span/span[1]/input', 'antio', 'xpath')
            self.legalizador.write('/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')
                
            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar departamento")
            
            # Ciudad - Dropdown select2
            self.legalizador.click('select2-City-container', 'id')
            self.legalizador.write('/html/body/span/span/span[1]/input', 'mede', 'xpath')
            self.legalizador.write('/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')

            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar ciudad")

            self.legalizador.write('PersonalInfo.Address.Town', 'central', 'name')

            # Prefijo teléfono - Dropdown select2
            self.legalizador.click('select2-Prefix-container', 'id')
            self.legalizador.write('/html/body/span/span/span[1]/input', '604', 'xpath')
            self.legalizador.write('/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')
            
            # Hacer clic en siguiente
            self.legalizador.click('btnNext', 'id')
            
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de hacer clic en Siguiente en demografica")
                    
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
            self.excel.guardar(self.contador, 'Min', 'Procesado')
            self.ventana_informacion.write(f"{self.iccid} {message_element}")
            self.legalizador.click('btnPrev', 'id')
            self.position_detect()
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def restart_new(self):
        raise('error')
        
    def verificar_urls(self):
        lista_ejecucion = {
            'paso1' : self.captura_datos_optimized,
            'validate' : self.validate_data,
            'demographic' : self.captura_demografica_optimized,
            'equipo plan' : self.datos_equipo_plan,
            'activacion' : self.activacion,
        }
        self.establecer_datos()
        mode = 'on'
        while True:
            track = self.position_detect()
            print(track, mode)
            if track in ['login']:
                raise Exception('session cerrada')
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
                        self.excel.guardar(self.contador, 'Min', 'Procesado')
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
        pass

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
        
        count = 0
        max_iterations = 50  # LÍMITE MÁXIMO DE ITERACIONES
        
        while count < max_iterations:
            self.scrap = scraping.Scraping(self.legalizador.retornarHtml())
            soup = self.scrap.soup
            pos = None
            
            for i, j in position.items():
                if self.validate_position(j, soup, 'class'):
                    pos = i
                    print(f"Posición detectada: {pos}")
                    return pos
            
            # SI NO ENCUENTRA NINGUNA POSICIÓN, ESPERAR Y REINTENTAR
            print(f"Posición no detectada. Intento {count + 1}/{max_iterations}")
            time.sleep(1)  # Esperar antes de reintentar
            count += 1
        
        # SI SE AGOTA EL LÍMITE, LANZAR EXCEPCIÓN ESPECÍFICA
        raise Exception(f'No se pudo detectar posición después de {max_iterations} intentos')


    
    def validate_position(self, elementos_requeridos, soup, type='id'):
        """
        Valida si los elementos están presentes Y visibles en la página
        """
        for tag, id_value in elementos_requeridos:
            if type == 'id':
                element = soup.find(tag, id=id_value)
            elif type == 'class':
                element = soup.find(tag, class_=id_value)
            else:
                return False
            
            if not element:
                return False
                
        return True

    def wait_for_loading(self, timeout=30, sleep_interval=1, legalizador=True):
        """
        Método reutilizable para esperar que termine la carga.
        
        Args:
            timeout (int): Tiempo máximo de espera en segundos
            sleep_interval (float): Intervalo entre verificaciones
            
        Returns:
            bool: True si terminó la carga, False si hubo timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                if legalizador:
                    loading_style = self.legalizador.style('loading', 'id')
                else:
                    loading_style = self.poliedro.style('loading', 'id')
                if "display: none" in loading_style:
                    return True
                elif "display: block" in loading_style:
                    print(f'Loading... ({time.time() - start_time:.1f}s)')
            except Exception:
                # Si no puede leer el estilo, asumir que terminó la carga
                return True
                
            time.sleep(sleep_interval)
        
        print(f"Timeout después de {timeout} segundos esperando que termine la carga")
        return False  # Timeout