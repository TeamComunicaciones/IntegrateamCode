from navegacion import sub_menu as sm, ventana_informacion 
from funcionalidad import  web_controller, poliedro, excel, clickImage, scraping
from recursos import botones, label, checkbox, colors, spinbox
import threading
from subprocess import Popen
import pyperclip
from datetime import datetime, timedelta
import time
import tkinter as tk
import customtkinter as ctk
import traceback
from funcionalidad import poliedro_login_service
from selenium.webdriver.common.keys import Keys
import random
from selenium.webdriver.support.ui import Select

class Legalizador_sims:

    def __init__(self, master, on_of):
        self.on_of = on_of
        self.master = master
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()

        #Enlaces: poliedro, mysms y google messages
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link_google_messages = 'https://messages.google.com/web/conversations'
        self.link_mysms = 'https://app.mysms.com/#87472'

        #Diseño en UI
        self.label = label.Label().create_label(master, 'LEGALIZADOR SIMCARD', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion = ventana_informacion.Ventana_informacion(master)
        self.menu= sm.Sub_menu(master, 3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.legalizador_sims = ''
        self.time = tk.StringVar()
        self.time.set('0')
        boton = botones.Buttons()
        color = colors.Colors()

        #Ciclos
        self.repeticiones = '1'
        self.repeticionesEdit = tk.StringVar()
        self.repeticionesEdit.set(self.repeticiones) 
        self.titulo = label.Label().create_label(self.menu.submenu, 'Ciclos',  0.0, 0.62, 0.5,0.2, letterSize= 16)
        input_widget3 = ctk.CTkEntry(self.menu.submenu, textvariable=self.repeticionesEdit)
        input_widget3.place(relx=0.45, rely=0.7, relheight=0.05, relwidth=0.2)
        self.okBotton3 = boton.create_button(self.menu.submenu, 'OK', 0.65, 0.7, 0.15, 0.05, self.cambioCiclos)
        self.okBotton3.configure(fg_color= color.team, text_color= 'white')

        # Configuracion para tiempo de espera
        self.tiempo_espera_label = label.Label().create_label(self.menu.submenu, 'Tiempo de espera', 0.10, 0.36, 0.6, 0.04, letterSize=16)

        self.spinbox_tiempo_espera = spinbox.CTkSpinbox(self.menu.submenu, from_=5, to=60, default=5)
        self.spinbox_tiempo_espera.place(relx=0.10, rely=0.40, relheight=0.06, relwidth=0.55)

        # Si el usuario no presiona OK, toma el valor por defecto
        self.valor = self.spinbox_tiempo_espera.get_value()

        self.tiempo_espera_okbutton = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.40, 0.15, 0.05, self.guardar_tiempo_espera)
        self.tiempo_espera_okbutton.configure(fg_color=color.team, text_color='white')

        # Etiquetas
        self.titulo3 = label.Label().create_label(self.menu.submenu, 'Poliedro User', 0.10, 0.49, 0.5, 0.04, letterSize=16)
        self.titulo4 = label.Label().create_label(self.menu.submenu, 'Poliedro Pass', 0.10, 0.59, 0.5, 0.04, letterSize=16)

        # Poliedro user y pass
        self.poliedro_user = ''
        self.poliedro_pass = ''
        self.poliedro_user_edit = tk.StringVar()
        self.poliedro_user_edit.set(self.poliedro_user)
        self.poliedro_pass_edit = tk.StringVar()
        self.poliedro_pass_edit.set(self.poliedro_pass)

        
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

    def abrir_pagina(self):
        if not self.mysms.get() and not self.google_messages.get():
            self.ventana_informacion.write('Seleccione un método para recibir el OTP')
            return
        
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.legalizador_sims = Abrir_pagina1(int(self.time.get()))
        self.legalizador_sims.openEdge()
        self.legalizador_sims.selectPage(self.link)

        time.sleep(2)
        if self.mysms.get():
            self.legalizador_sims.script(f"window.open('{self.link_mysms}', '_blank');")
        elif self.google_messages.get():
            self.legalizador_sims.script(f"window.open('{self.link_google_messages}', '_blank');")

    def guardar_tiempo_espera(self):
        self.valor = self.spinbox_tiempo_espera.get_value()
        self.ventana_informacion.write(f'Tiempo de espera configurado: {self.valor} segundos')

    def cambioCiclos(self):
        self.repeticiones = self.repeticionesEdit.get()
        self.ventana_informacion.write(f'Numero de repeticiones configurado en {self.repeticiones}')

    def cambioPoliedroUser(self):
        self.poliedro_user = self.poliedro_user_edit.get()
        self.ventana_informacion.write(f'Poliedro User actualizado por {self.poliedro_user}')

    def cambioPoliedroPass(self):
        self.poliedro_pass = self.poliedro_pass_edit.get()
        self.ventana_informacion.write(f'Poliedro Pass actualizado por {self.poliedro_pass}')
    
    def on_checkbox_change_tropas(self):
        if self.tropas.get():
            self.ventana_informacion.write('Cambiando modalidad a Tropas')
        else:
            self.ventana_informacion.write('Cambiando modalidad a Estandar')
        self.poliedro.manejoTropas(self.tropas.get())
    
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
    
    def abrir_excel(self):
        self.ventana_informacion.write('Abriendo Excel legalizador_sims, recuerde cerrar antes de iniciar')
        p = Popen("src\legalizador_sims\openExcel.bat")
        stdout, stderr = p.communicate()
    
    def ejecuccionHilo(self):
        hilo_legalizador_sims = threading.Thread(target=self.ejecuccion)
        hilo_legalizador_sims.start()
    
    def ejecuccion(self):
        # --- Validar que el navegador esté abierto ---
        if not self.legalizador_sims:
            self.ventana_informacion.write("❌ Debe abrir la página antes de iniciar")
            return
        
        try:
            self.poliedro.definirBrowser(self.legalizador_sims)
        except Exception as e:
            self.log_error("definirBrowser", e)
            return

         # Inicializar el servicio de login
        self.poliedro_login_service = None
        if not self.login():
            self.ventana_informacion.write('Error en login, verifique sus credenciales')
            self.on_of(True)
            self.ventana_informacion.write("Se detiene el programa por error")
            # Lanzar excepción para salir del bloque try y entrar al except final
            raise Exception("Error crítico: Fallo en login de Poliedro")
        time.sleep(2)

        try:
            self.legalizador_sims.click('//*[@id="containerNavBar"]/ul/li[12]/a') #Cambiar por xpath dinamico //*[@id="containerNavBar"]/ul/li[12]/a
        except Exception as e:
            self.log_error("click en menú", e)
            return
        
        time.sleep(3)
        self.poliedro.seleccionAcceso('376', start=True)
        if not self.wait_for_loading(legalizador_sims=False):
            raise Exception("Timeout esperando carga")
        
        # try:
        #     self.position(self.legalizador_sims.retornarHtml(),'CaptureData', True)
        # except Exception as e:
        #     self.log_error("CaptureData", e)
        #     return
        
        try:
            for i in range(int(self.repeticiones)):
                self.contador = 0
                self.excel.leer_excel('src\\legalizador_sims\\legalizador_sims.xlsx', 'Iccid')
                self.excel.quitarFormatoCientifico('Iccid')
                
                for self.contador in range(self.excel.cantidad):
                    try:
                        self.establecer_datos()
                        if not self.ejecutar_etapa("Capture Data", self.capture_data): continue
                        if not self.ejecutar_etapa("Validation", self.validation): continue
                        if not self.ejecutar_etapa("Demographic", self.demographic): continue
                        if not self.ejecutar_etapa("Product/Service", self.product_service): continue
                        if not self.ejecutar_etapa("Activation", self.activation): continue

                        self.ventana_informacion.write(f"✅ Fila {self.contador+1} completada")

                        base = self.valor
                        variacion = random.randint(1,3)
                        tiempo_pausa = random.randint(base - variacion, base + variacion)
                        self.ventana_informacion.write(f"⏳ Pausa anti-bot: {tiempo_pausa}s entre transacciones...")
                        time.sleep(tiempo_pausa)

                    except Exception as e:
                        self.excel.guardar(self.contador, 'Min', 'error', destino="src\\legalizador_sims\\legalizador_sims.xlsx")
                        self.excel.guardar(self.contador, 'Mensaje', str(e), destino="src\\legalizador_sims\\legalizador_sims.xlsx") # Corregir
                        self.ventana_informacion.write(f"❌ Error en fila {self.contador+1}")
                        self.log_error(f"fila {self.contador+1}", e)
                        continue

                # REPORTE FINAL DEL CICLO
                self.ventana_informacion.write('✅ Proceso terminado exitosamente')
                self.ventana_informacion.write(f'🏁 Ciclo {i+1} finalizado con {self.excel.cantidad} registros procesados')
           
            self.on_of(True)
        except Exception as e:
            self.log_error("bloque principal", e)
            self.ventana_informacion.write("Se detiene el programa por error")
    
    def ejecutar_etapa(self, nombre, funcion):
        try:
            self.ventana_informacion.write(f"➡️ {nombre}...")
            funcion()
            self.ventana_informacion.write(f"✅ {nombre} completada")
            return True
        except Exception as e:
            self.log_error(nombre, e)
            self.ventana_informacion.write(f"❌ Error en {nombre}")

            # Reiniciar proceso
            self.legalizador_sims.click('//*[@id="containerNavBar"]/ul/li[12]/a')
            time.sleep(1)
            self.legalizador_sims.click('//*[@id="containerNavBar"]/ul/li[12]/a')
            self.poliedro.seleccionAcceso('376', start=True)
            if not self.wait_for_loading(legalizador_sims=False):
                raise Exception("Timeout esperando carga")
            
            return False

    def establecer_datos(self):
        # Obtener datos del Excel
        self.min = str(self.excel.excel['min'][self.contador])
        self.iccid = str(self.excel.excel['Iccid'][self.contador])[-12:] 
        self.id_vendedor = str(self.excel.excel['CcVendedor'][self.contador]).replace('.0','')
        self.nombre = str(self.excel.excel['nombre'][self.contador])
        self.apellido = str(self.excel.excel['apellido'][self.contador])
        self.tipo_documento = str(self.excel.excel['tipoDoc'][self.contador])
        if self.tipo_documento.lower() == 'cc':
            self.tipo_documento = 'Cedula'
        self.id_cliente = str(self.excel.excel['CcCliente'][self.contador]).replace('.0','')

        self.ventana_informacion.write(f'📝 Procesando registro {self.contador+1}/{self.excel.cantidad} - MIN: {self.min}')

    def capture_data(self):
        #Info Cliente
        self.selectDropDown("DetailProduct_DocumentTypeId", self.tipo_documento)
        self.legalizador_sims.write("DetailProduct_DocumentNumber",self.id_cliente,"id")

        if self.tipo_documento.lower() in {"cedula", "cédula", "cc"}:
            self.legalizador_sims.write("DetailProduct_LastName",self.apellido,"id")

        #Info Equipo
        self.legalizador_sims.write("DetailProduct_Iccid",self.iccid,"id")
        
        #Info venta
        self.legalizador_sims.write("DetailProduct_SellerId",self.id_vendedor,"id")
        self.legalizador_sims.write("DetailProduct_Msisdn",self.min,"id")

        time.sleep(2)
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de validación")
        
        self.legalizador_sims.click('btnNext', 'id')

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente en Capture Data")
        
    def validation(self):
        # try:
        #     self.position(self.legalizador_sims.retornarHtml(),'Validation', True)
        # except Exception as e:
        #     self.log_error("Validation", e)
        #     return

        try:
            # Intentar leer el mensaje principal
            validate = self.legalizador_sims.read(
                '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span'
            )
        except Exception:
            # Si no puede leer el mensaje, forzar a que sea None
            validate = None
        
        # --- Caso exitoso ---
        if validate == "Validación Correcta":
            self.ventana_informacion.write("✅ Validación correcta")
        else:
            # --- Captura de errores en Web ---
            errores = []
            try:
                errores = self.legalizador_sims.readMulty("errorFormItem", "class")
            except Exception as e:
                self.log_error("readMulty Validation", e)

            if errores and errores != "none":
                mensaje_error = "; ".join(errores)
                self.excel.guardar(
                    self.contador, "Mensaje", mensaje_error,
                    destino="src\\legalizador_sims\\legalizador_sims.xlsx"
                )
                self.excel.guardar(
                    self.contador, "Min", "error",
                    destino="src\\legalizador_sims\\legalizador_sims.xlsx"
                )
                raise Exception(f"Error en validación web: {mensaje_error}")
            else:
                raise Exception("No se detectó mensaje de validación ni error visible")
        
        # --- Si todo está bien, continuar ---
        self.legalizador_sims.click("btnNext", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente en Validación")
        
    def demographic(self):
        time.sleep(2)
        # --- Saludo ---
        self.selectDropDown("PersonalInfo_GreetingId", "Sr")

        # --- Nombre ---
        nombre_actual = self.legalizador_sims.value("PersonalInfo_Name", "id")
        if not nombre_actual.strip():
            self.legalizador_sims.write("PersonalInfo_Name", self.nombre, "id")

        # --- Apellido ---
        if self.tipo_documento.lower() in {"cedula", "cédula", "cc"}:
            apellido_actual = self.legalizador_sims.value("PersonalInfo_LastName", "id")
            if not apellido_actual.strip():
                self.legalizador_sims.write("PersonalInfo_LastName", self.apellido, "id")

        # --- Correo ---
        correo_actual = self.legalizador_sims.value("PersonalInfo_Email", "id")
        if not correo_actual or not correo_actual.strip():
            self.legalizador_sims.write("PersonalInfo_Email", 'master.33@gmail.com', "id")

        # --- Teléfono ---
        telefono_actual = self.legalizador_sims.value("PhoneId", "id")
        if not telefono_actual or not telefono_actual.strip():
            # Tipo de teléfono
            self.selectDropDownNormal("PhoneClass", "fijo")

            time.sleep(2)
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de seleccionar tipo de teléfono")

            # Indicativo
            self.selectDropDownNormal("Prefix", "7")

            # Número
            self.legalizador_sims.write("PhoneNumber", "8883136", "id")

        # --- Tipo de documento ---
        self.poliedro.tipoDoc(self.tipo_documento, '//*[@id="select2-PersonalInfo_DocumentTypeId-container"]')

        # --- Documento ---
        id_actual = self.legalizador_sims.value("PersonalInfo_Document", "id")
        if not id_actual.strip() or id_actual.strip() == "0":
            campo = self.legalizador_sims.browser.find_element_by_id("PersonalInfo_Document")
            campo.clear()
            self.legalizador_sims.write("PersonalInfo_Document", self.id_cliente, "id")

        # --- Dirección ---
        direccion_actual = self.legalizador_sims.value("AddressId", "id")
        if not direccion_actual or not direccion_actual.strip():
            self.selectDropDownNormal("AddressClassId", "Otras")

            time.sleep(2)
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de seleccionar tipo de dirección")

            self.legalizador_sims.write("Address", "central", "id")
            self.selectDropDownNormal("Department", "ANTIOQUIA")
            time.sleep(2)
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de seleccionar tipo de dirección")
            self.selectDropDownNormal("City", "MEDELLIN")
            self.legalizador_sims.write("Town", "Central", "id")
        
        time.sleep(2)
        # --- Continuar a la siguiente etapa ---
        self.legalizador_sims.click("btnNext", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente en Demographic")
        
    def product_service(self):
        time.sleep(2)
        self.selectDropDown("ProductInfo_ProductModelId", "Al")

        time.sleep(2)
        self.legalizador_sims.click("btnNext", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente en ProductService")
        
    def activation(self):
        time.sleep(2)
        self.legalizador_sims.click("btnNext", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente en ProductService")
        
        message_element = self.legalizador_sims.readShort2('messageFormItem', 'class')
        self.excel.guardar(self.contador, 'Mensaje', message_element, destino="src\\legalizador_sims\\legalizador_sims.xlsx")
        self.excel.guardar(self.contador, 'Min', 'Procesado', destino="src\\legalizador_sims\\legalizador_sims.xlsx")
        self.ventana_informacion.write(f"{self.iccid} {message_element}")
        
        time.sleep(2)
        if not self.wait_for_loading():    
            raise Exception("Timeout esperando carga después de validación")
        
        self.legalizador_sims.click("btnPrev", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en 'Iniciar nueva activación'")
        
        self.selectDropDown("productShortcut", "270")

    def selectDropDown(self, id, value):
        """
        Selecciona un valor de un dropdown usando el ID del elemento y el valor a seleccionar.
        """
        self.legalizador_sims.click(f'select2-{id}-container', 'id')
        self.legalizador_sims.write(f'/html/body/span/span/span[1]/input', value, 'xpath')
        self.legalizador_sims.write(f'/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')

    def selectDropDownNormal(self, id, value):
        """
        Selecciona un valor de un <select> HTML clásico usando el ID del elemento y el texto visible.
        Coincidencia exacta, insensible a mayúsculas/minúsculas y tildes.
        """
        try:
            select_element = self.legalizador_sims.browser.find_element_by_id(id)
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

    def position(self, html, paso=None, wait=False):
        self.scrap = scraping.Scraping(html)
        soup = self.scrap.soup
        count = 0
        top = 100 if paso != 'Validation' else 500

        while wait:
            if paso == 'CaptureData':
                elementos_requeridos = [
                    ("h3", "iconoTituloCliente"),
                    ("h3", "iconoTituloInfoVenta"),
                    ("h3", "iconoTituloEquipo"),
                ]
                if self.validate_position(elementos_requeridos, soup):
                    return 1
                else:
                    self.scrap = scraping.Scraping(self.legalizador_sims.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'Validation':
                elementos_requeridos = [
                    ("h3", "iconoTituloDatosDistribuidor"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador_sims.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'Demographic':
                elementos_requeridos = [
                    ("h3", "iconoTituloInfoPersonal"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador_sims.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'ProductService':
                elementos_requeridos = [
                    ("h3", "iconoTituloDatosEquipoyPlan"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador_sims.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
            elif paso == 'Activation':
                elementos_requeridos = [
                    ("h3", "iconoTituloActivacionesCliente"),
                    ("h3", "iconoTituloActivacionesServicios"),
                    ("h3", "iconoTituloActivacionesProducto"),
                ]
                if self.validate_position(elementos_requeridos, soup, 'class'):
                    return 9
                else:
                    self.scrap = scraping.Scraping(self.legalizador_sims.retornarHtml())
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
                    self.scrap = scraping.Scraping(self.legalizador_sims.retornarHtml())
                    soup = self.scrap.soup
                    count += 1
                    time.sleep(0.1)
                    if count == top:
                        raise('restar controlado')
                    
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

    def inicializar_login_service(self):
        """
        Inicializa el servicio de login cuando el navegador esté listo
        """
        if self.legalizador_sims and not self.poliedro_login_service:
            self.poliedro_login_service = poliedro_login_service.LoginService(
                self.legalizador_sims, 
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

    def log_error(self, contexto, e):
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{contexto}] Error: {str(e)}\n")
            f.write(traceback.format_exc())
        self.ventana_informacion.write(f"Error en {contexto}: {str(e)}")

    def wait_for_loading(self, timeout=120, sleep_interval=1, legalizador_sims=True):
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
                if legalizador_sims:
                    try:
                        loading_style = self.legalizador_sims.style('loading', 'id')
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