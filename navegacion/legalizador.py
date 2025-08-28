from navegacion import sub_menu as sm, ventana_informacion
from recursos import label, botones, colors, checkbox
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
import re
from funcionalidad import poliedro_login_service
import random


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
        self.link_google_messages = 'https://messages.google.com/web/conversations'
        self.link_mysms = 'https://app.mysms.com/#87472'
        
        # ESTADO CRÍTICO PARA MANEJO CONSISTENTE DE SESIÓN
        self.error_critico_sesion = False
        self.ultimo_error_sesion = None
        self.intentos_recuperacion = 0
        self.max_intentos_recuperacion = 3

        # ✅ NUEVAS MÉTRICAS PARA MONITOREO
        self.inicio_proceso = None
        self.transacciones_exitosas = 0
        self.transacciones_fallidas = 0
        self.recent_timeouts = 0
        self.ultimo_reporte_metricas = 0
        self.titulo = label.Label().create_label(master, 'LEGALIZADOR', 0.2, 0.0, 0.5, 0.2, letterSize=25)
        self.ventana_informacion = ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master, 3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.legalizador = ''
        self.time = tk.StringVar()
        self.time2 = 3
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.0, 0.60, 0.5, 0.2, letterSize=16)
        self.titulo = label.Label().create_label(self.menu.submenu, 'Ciclos', 0.0, 0.73, 0.5, 0.05, letterSize=16)
        self.titulo2 = label.Label().create_label(self.menu.submenu, 'Correo', 0.25, 0.77, 0.5, 0.05, letterSize=16)
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.5, rely=0.67, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.67, 0.15, 0.05, self.cambioIntervalo)
        self.okBotton.configure(fg_color=color.team, text_color='white')
        self.correo = 'acruz@teamcomunicaciones.com'
        self.correoEdit = tk.StringVar()
        self.correoEdit.set(self.correo)
        self.cookie_header = {}
        self.repeticiones = '1'
        self.repeticionesEdit = tk.StringVar()
        self.repeticionesEdit.set(self.repeticiones)
        input_widget2 = ctk.CTkEntry(self.menu.submenu, textvariable=self.correoEdit)
        input_widget2.place(relx=0.15, rely=0.82, relheight=0.05, relwidth=0.7)
        input_widget3 = ctk.CTkEntry(self.menu.submenu, textvariable=self.repeticionesEdit)
        input_widget3.place(relx=0.5, rely=0.73, relheight=0.05, relwidth=0.2)
        self.okBotton2 = boton.create_button(self.menu.submenu, 'confirmar', 0.3, 0.87, 0.40, 0.04, self.cambioCorreo)
        self.okBotton2.configure(fg_color=color.team, text_color='white')
        self.okBotton3 = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.73, 0.15, 0.05, self.cambioCiclos)
        self.okBotton3.configure(fg_color=color.team, text_color='white')

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

        self.okBotton5 = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.59, 0.15, 0.05, self.cambioPoliedroPass)
        self.okBotton5.configure(fg_color=color.team, text_color='white')

        # Elegir si se usa MySMS o Google Messages para obtener el OTP
        self.checkbox_mysms = checkbox.Checkbox()
        self.mysms = tk.BooleanVar()
        self.checkbox_mysms = checkbox.Checkbox().create_checkbox(self.menu.submenu, 'MySMS', self.on_checkbox_change_mysms, self.mysms)

        self.checkbox_google_messages = checkbox.Checkbox()
        self.google_messages = tk.BooleanVar()
        self.checkbox_google_messages = checkbox.Checkbox().create_checkbox(self.menu.submenu, 'Google Messages', self.on_checkbox_change_google_messages, self.google_messages)
       

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

    def cambioPoliedroUser(self):
        self.poliedro_user = self.poliedro_user_edit.get()
        self.ventana_informacion.write(f'Poliedro User actualizado por {self.poliedro_user}')

    def cambioPoliedroPass(self):
        self.poliedro_pass = self.poliedro_pass_edit.get()
        self.ventana_informacion.write(f'Poliedro Pass actualizado por {self.poliedro_pass}')

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
    
    def abrir_pagina(self):
        if not self.mysms.get() and not self.google_messages.get():
            self.ventana_informacion.write('Seleccione un método para recibir el OTP')
            return

        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller): pass
        self.legalizador = Abrir_pagina1(int(self.time.get()))
        self.legalizador.openEdge()
        time.sleep(3)
        self.legalizador.selectPage(self.link)

        time.sleep(2)
        if self.mysms.get():
            self.legalizador.script(f"window.open('{self.link_mysms}', '_blank');")
        elif self.google_messages.get():
            self.legalizador.script(f"window.open('{self.link_google_messages}', '_blank');")
    
    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()
    
    def ejecuccion(self):
        try:
            self.poliedro.definirBrowser(self.legalizador)
        except Exception as e:
            self.log_error("definirBrowser", e)
            return
        
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
            self.legalizador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
        except Exception as e:
            self.log_error("click en menú", e)
            return
        
        time.sleep(3)
        self.poliedro.seleccionAcceso('362', start=True)
        if not self.wait_for_loading(legalizador=False):
            raise Exception("Timeout esperando carga")

        try:
            self.position(self.legalizador.retornarHtml(), 'paso1', True)
        except Exception as e:
            self.log_error("position paso1", e)
            return

        try:
            for i in range(int(self.repeticiones)):
                self.ciclo = True
                self.contador = 0
                self.inicio_proceso = time.time()  # INICIALIZAR MÉTRICAS
                self.transacciones_exitosas = 0
                self.transacciones_fallidas = 0
                
                # CONFIGURAR MODO PRODUCCIÓN PARA ALTO VOLUMEN
                self.configurar_modo_produccion()
                
                self.excel.leer_excel('src\\legalizador\\legalizador.xlsx', 'iccid')
                self.excel.quitarFormatoCientifico('iccid')
                self.excel.quitarFormatoCientifico('imei')
                self.ventana_informacion.write(f'🚀 Iniciando Ciclo {i+1} con {self.excel.cantidad} transacciones')
                
                # PROCESAMIENTO POR LOTES PARA MEJOR GESTIÓN DE MEMORIA
                self.procesar_por_lotes()
                
                # REPORTE FINAL DEL CICLO
                #self.reporte_final_ciclo(i+1)
                self.ventana_informacion.write('✅ Proceso terminado exitosamente')
                self.ventana_informacion.write(f'🏁 Ciclo {i+1} finalizado')
            try:
                self.legalizador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
            except Exception as e:
                self.log_error("click en menú", e)
            self.on_of(True)
        except Exception as e:
            self.log_error("bloque principal", e)
            self.alertas('se detiene el programa error')
    
    def inicializar_login_service(self):
        """
        Inicializa el servicio de login cuando el navegador esté listo
        """
        if self.legalizador and not self.poliedro_login_service:
            self.poliedro_login_service = poliedro_login_service.LoginService(
                self.legalizador, 
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
    
    def establecer_datos(self):
        self.ventana_informacion.write(f'📝 Procesando registro {self.contador+1}/{self.excel.cantidad} - MIN: {self.min}')
        
        # Obtener datos del Excel
        self.iccid = str(self.excel.excel['iccid'][self.contador])[-12:] 
        self.cedulaVendedor = str(self.excel.excel['idvendedor'][self.contador]).replace('.0','')
        self.imei = str(self.excel.excel['imei'][self.contador])
        self.min = str(self.excel.excel['min'][self.contador])
        self.nombre = str(self.excel.excel['nombre'][self.contador])
        self.apellido = str(self.excel.excel['apellido'][self.contador])
        self.cedula = str(self.excel.excel['cedula'][self.contador]).replace('.0','')
        self.tipoDoc = str(self.excel.excel['tipodoc'][self.contador])
        self.documentType = 2 if self.tipoDoc.lower() == 'nit' else 1
        self.imei = self.imei.replace(' ','')

        if self.documentType == 2:  # Si es NIT
            cedula_limpia = self.cedula.replace(' ', '').replace('.', '').replace('-', '')
            
            if len(cedula_limpia) > 9:
                cedula_original = cedula_limpia
                self.cedula = cedula_limpia[:9]  # Tomar solo los primeros 9 dígitos
                self.ventana_informacion.write(f"⚠️ NIT truncado de {len(cedula_original)} a 9 dígitos: {cedula_original} → {self.cedula}")
            else:
                self.cedula = cedula_limpia
                self.ventana_informacion.write(f"✅ NIT válido ({len(cedula_limpia)} dígitos): {self.cedula}")
        
        # Validar datos críticos antes de procesar
        if not self.validar_datos_transaccion():
            raise Exception("Datos inválidos - transacción saltada")
    
    def validar_datos_transaccion(self):
        """
        Valida datos críticos antes de procesar la transacción
        
        Returns:
            bool: True si los datos son válidos, False en caso contrario
        """
        errores = []
        
        # Validar ICCID (debe tener al menos 10 dígitos)
        if len(self.iccid.replace(' ', '')) < 10 or self.iccid in ['nan', 'None', '']:
            errores.append(f"ICCID inválido: {self.iccid}")
        
        # Validar cédula (debe ser numérica y tener al least 6 dígitos)
        cedula_limpia = self.cedula.replace(' ', '').replace('.', '')
        if not cedula_limpia.isdigit() or len(cedula_limpia) < 6 or len(cedula_limpia) == 9 or cedula_limpia in ['nan', 'None', '']:
            errores.append(f"Cédula inválida: {self.cedula}")
        
        # Validar IMEI (debe tener 15 dígitos)
        imei_limpio = self.imei.replace(' ', '').replace('.', '')
        if not imei_limpio.isdigit() or len(imei_limpio) != 15 or imei_limpio in ['nan', 'None', '']:
            errores.append(f"IMEI inválido: {self.imei}")
        
        # Validar MIN (número de teléfono)
        min_limpio = self.min.replace(' ', '').replace('.', '')
        if not min_limpio.isdigit() or len(min_limpio) < 7 or min_limpio in ['nan', 'None', '']:
            errores.append(f"MIN inválido: {self.min}")
        
        # Validar nombre (no puede estar vacío)
        if not self.nombre or self.nombre.strip() in ['nan', 'None', '']:
            errores.append(f"Nombre inválido: {self.nombre}")
        
        # Validar apellido para personas naturales
        if self.documentType != 2 and (not self.apellido or self.apellido.strip() in ['nan', 'None', '']):
            errores.append(f"Apellido inválido para CC: {self.apellido}")
        
        # Si hay errores, guardarlos y retornar False
        if errores:
            mensaje_error = '; '.join(errores)
            self.excel.guardar(self.contador, 'Mensaje', f"Validación: {mensaje_error}")
            self.excel.guardar(self.contador, 'Min', 'error')
            self.ventana_informacion.write(f"❌ Datos inválidos en fila {self.contador+1}: {mensaje_error}")
            return False
        
        # Datos válidos
        self.ventana_informacion.write(f"✅ Datos válidos para {self.min} - {self.nombre}")
        return True
    
    def validate_data(self):
        try:
            self.position(self.legalizador.retornarHtml(), 'validate', True)
            try:
                validate = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span')
            except:
                message = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
                if message and message.strip():
                    self.excel.guardar(self.contador, 'Mensaje', f'Error validación: {message}')
                    self.excel.guardar(self.contador, 'Min', 'error')
                    self.ventana_informacion.write(f"{self.iccid} Error validación: {message}")
                    raise Exception(f'Error validación: {message}')
                else:
                    self.excel.guardar(self.contador, 'Mensaje', 'Error validación desconocido')
                    self.excel.guardar(self.contador, 'Min', 'error')
                    self.ventana_informacion.write(f"{self.iccid} Error validación desconocido")
                    raise Exception('Error validación: mensaje no detectado')

            if validate == 'Validación Correcta':
                time.sleep(2)
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")
                self.legalizador.click('btnNext', 'id')
                # USAR MÉTODO MEJORADO CON TIMEOUT ADAPTATIVO
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")
                try:
                    self.position(self.legalizador.retornarHtml(), 'demographic', True)
                except:
                    time.sleep(2)
                    if not self.wait_for_loading():
                        raise Exception("Timeout esperando carga después de validación")
                    self.legalizador.click('btnNext', 'id')
            else:
                mensaje_error = f'Validación incorrecta: {validate}' if validate else 'Validación incorrecta: mensaje no detectado'
                self.excel.guardar(self.contador, 'Mensaje', mensaje_error)
                self.excel.guardar(self.contador, 'Min', 'error')
                self.ventana_informacion.write(f"{self.iccid} {mensaje_error}")
                raise Exception(mensaje_error)
        except Exception as e:
            # SI NO SE GUARDÓ UN MENSAJE ESPECÍFICO, USAR EL ERROR CAPTURADO
            try:
                mensaje_actual = str(self.excel.excel['Mensaje'][self.contador])
                if not mensaje_actual or mensaje_actual in ['nan', 'None', '']:
                    self.excel.guardar(self.contador, 'Mensaje', f'Error en validate_data: {str(e)}')
                    self.excel.guardar(self.contador, 'Min', 'error')
            except:
                pass
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def captura_datos_optimized(self):
        """
        Versión optimizada de captura_datos usando wait_for_loading()
        """
        try:
            # USAR MÉTODO REUTILIZABLE PARA ESPERA INICIAL
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga")
            
            self.position(self.legalizador.retornarHtml(), 'paso1', True)

            time.sleep(2)

            intentos = 0
            while intentos < 5:
                try:
                    self.legalizador.click('DetailProduct_Imei', 'id')
                    cedula_pantalla = self.legalizador.value('DetailProduct_DocumentNumber', 'id')

                    if cedula_pantalla and cedula_pantalla.strip():
                        raise Exception(f'Error al escribir cédula/nit: {cedula_pantalla}')
                    break
                except Exception as e:
                    intentos += 1
                    try:
                        self.legalizador.click('toggleProductBTN', 'id')
                        if not self.wait_for_loading():
                            raise Exception("Timeout esperando carga")
                    except Exception as e:
                        pass
                    self.poliedro.seleccionAcceso('Seleccione...', start=False)
                    if not self.wait_for_loading():
                        raise Exception("Timeout esperando carga")
                    time.sleep(1)
                    self.poliedro.seleccionAcceso('362', start=False)
            
            if intentos == 4:
                self.excel.guardar(self.contador, 'Mensaje', 'No se pudo acceder al formulario 362')
                self.excel.guardar(self.contador, 'Min', 'error')
                self.ventana_informacion.write(f"{self.iccid} No se pudo acceder al formulario 362")
                raise('error controlado en formulario demografico')

            # USAR MÉTODO REUTILIZABLE PARA ESPERA INICIAL
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga")
            
            time.sleep(1)
            # Click en el campo select2 para abrirlo
            self.legalizador.click('select2-DetailProduct_DocumentTypeId-container', 'id')
            time.sleep(1)
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
            
            time.sleep(2)
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de validación")
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
                time.sleep(2)
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")
                self.legalizador.click('btnNext', 'id')
                self.position(self.legalizador.retornarHtml(), 'demographic', True)

            # USAR MÉTODO REUTILIZABLE PARA SEGUNDA ESPERA
            if not self.wait_for_loading(timeout=15, sleep_interval=0.3):
                raise Exception("Timeout esperando carga del formulario demográfico")
            
            time.sleep(2)
            errors = self.legalizador.read('viewErrors', 'id')
            if errors:
                self.excel.guardar(self.contador, 'Mensaje', errors)
                self.excel.guardar(self.contador, 'Min', 'error')
                self.ventana_informacion.write(f"{self.iccid} {errors}")
                raise('error controlado en formulario demografico')
            
            contador = 0
            while contador < 5:
                try:
                    # Tipo de teléfono - Dropdown select2
                    self.selectDropDown('PhoneClass', 'fijo')
                    break
                except Exception as e:
                    contador += 1
                    try:
                        self.legalizador.click('btnPrev', 'id')
                    except Exception as btn_e:
                        self.log_error("btnPrev click en captura_demografica", btn_e)
                    time.sleep(2)
                    if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                        raise Exception("Timeout esperando carga después de ingresar correo")
                    time.sleep(2)
                    self.legalizador.click('btnNext', 'id')
                    if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                        raise Exception("Timeout esperando carga después de ingresar correo")
                    
            if contador == 4:
                self.excel.guardar(self.contador, 'Mensaje', 'No se pudo llenar los datos demograficos ya que el formulario no cargó correctamente')
                self.excel.guardar(self.contador, 'Min', 'error')
                self.ventana_informacion.write(f"{self.iccid} {errors}")
                raise('error controlado en formulario demografico')

            # Saludo - Dropdown select2
            self.selectDropDown('PersonalInfo_GreetingId', 'sr')

            self.legalizador.write('PersonalInfo_Name', self.nombre, 'id')

            if self.documentType != 2:
                self.legalizador.write('PersonalInfo_LastName', self.apellido, 'id')

            self.legalizador.write('PersonalInfo_Email', self.correo, 'id')

            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de ingresar correo")

            # ESPERAR DINÁMICAMENTE CON MÉTODO REUTILIZABLE
            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar tipo de teléfono")
            
            self.legalizador.write('PersonalInfo.Phone.PhoneNumber', '0313123', 'name')
            
            # Tipo de dirección - Dropdown select2
            self.selectDropDown('AddressClassId', 'otras')

            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar tipo de dirección")
                
            self.legalizador.write('PersonalInfo.Address.Address', 'central', 'name')

            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de escribir dirección")
            
            # Departamento - Dropdown select2
            self.selectDropDown('Department', 'antio')

            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar departamento")
            
            # Ciudad - Dropdown select2
            self.selectDropDown('City', 'mede')

            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar ciudad")

            self.legalizador.write('PersonalInfo.Address.Town', 'central', 'name')

            # Prefijo teléfono - Dropdown select2
            self.selectDropDown('Prefix', '604')

            time.sleep(2)
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de validación")
            # Hacer clic en siguiente
            self.legalizador.click('btnNext', 'id')
            
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de hacer clic en Siguiente en demografica")
                    
            self.position(self.legalizador.retornarHtml(), 'equipo plan', True)
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def selectDropDown(self, id, value):
        """
        Selecciona un valor de un dropdown usando el ID del elemento y el valor a seleccionar.
        """
        self.legalizador.click(f'select2-{id}-container', 'id')
        self.legalizador.write(f'/html/body/span/span/span[1]/input', value, 'xpath')
        self.legalizador.write(f'/html/body/span/span/span[1]/input', Keys.ENTER, 'xpath')

    
    def datos_equipo_plan(self):
        try:
            self.position(self.legalizador.retornarHtml(), 'equipo plan', True)
            # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService')
            time.sleep(2)
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de validación")
            self.legalizador.click('btnNext', 'id')
            self.position(self.legalizador.retornarHtml(), 'activacion', True)
        except Exception as e:
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()

    def activacion(self):
        try:
            self.position(self.legalizador.retornarHtml(), 'activacion', True)
            # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Activation')
            time.sleep(2)
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de validación")
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
            try:
                self.legalizador.click('btnPrev', 'id')
            except Exception as e:
                self.log_error("btnPrev click en captar_activacion", e)
            self.position_detect()
        except Exception as e:
            if "Error crítico: Fallo en login de Poliedro" in str(e):
                raise Exception("Error crítico: Fallo en login de Poliedro")
            self.logs.append([e,traceback.format_exc()])
            self.restart_new()
    
    def restart_new(self):
        """
        Marca la transacción actual como error y permite continuar con la siguiente
        en lugar de terminar todo el proceso
        """
        try:
            mensaje_actual = None
            try:
                mensaje_actual = str(self.excel.excel['Mensaje'][self.contador])
            except:
                pass
            
            # SOLO SOBRESCRIBIR SI NO HAY MENSAJE ESPECÍFICO O ES GENÉRICO
            if not mensaje_actual or mensaje_actual in ['nan', 'None', '', 'Error en procesamiento - transacción saltada']:
                #self.excel.guardar(self.contador, 'Mensaje', 'Error en procesamiento - transacción saltada')
                #self.ventana_informacion.write(f"Error genérico en transacción {self.contador+1}/{self.excel.cantidad}, continuando...")
                print(f"Error genérico en transacción {self.contador+1}/{self.excel.cantidad}, continuando...")
            else:
                # Preservar el mensaje específico que ya se guardó
                self.ventana_informacion.write(f"Error específico en transacción {self.contador+1}/{self.excel.cantidad}: {mensaje_actual[:100]}")
            
            # Siempre marcar el Min como error
            self.excel.guardar(self.contador, 'Min', 'error')
            
            # Intentar resetear el estado del navegador para la siguiente transacción
            try:
                # Volver al estado inicial si es posible
                try:
                    self.legalizador.click('btnPrev', 'id')
                except Exception as e:
                    self.log_error("btnPrev click en restart_new", e)
                time.sleep(2)
            except:
                pass
                
        except Exception as e:
            self.log_error("restart_new", e)
        # Solo levantar excepción si es un error crítico irrecuperable
        raise Exception('Error en transacción - continuando con siguiente')
        
    def verificar_urls(self):
        lista_ejecucion = {
            'paso1' : self.captura_datos_optimized,
            'validate' : self.validate_data,
            'demographic' : self.captura_demografica_optimized,
            'equipo plan' : self.datos_equipo_plan,
            'activacion' : self.activacion,
        }

        mode = 'on'
        intentos = 0
        max_intentos = 10
        procesado = False
        while intentos < max_intentos:
            intentos += 1
            if not self.wait_for_loading(timeout=35, sleep_interval=0.3):
                raise Exception("Timeout esperando carga después de seleccionar ciudad")
            track = self.position_detect()
            print(track, mode)
            if track in ['login']:
                raise Exception('session cerrada')
            elif track == 'restart':
                try:
                    if not self.wait_for_loading():
                        raise Exception("Timeout esperando carga inicial")
                    self.poliedro.seleccionAcceso('362', start=False)
                    if not self.wait_for_loading():
                        raise Exception("Timeout esperando carga inicial")
                except Exception as e:
                    self.log_error("Error en restart", e)
            elif track == 'paso1' and mode == 'off':
                procesado = True
                break
            elif mode == 'off':
                try:                        
                    self.legalizador.click('btnPrev', 'id')
                except Exception as e:
                    print("btnPrev click en modo off", e)
            elif track == 'activacion':
                try:
                    if self.legalizador.elementExists('btnPrev', 'id'):
                        nombre_boton = self.legalizador.value('btnPrev', 'id')
                    else:
                        nombre_boton = None
                except Exception as e:
                    print("btnPrev value read en activacion", e)
                    nombre_boton = None  # Valor por defecto si no se puede leer
                    
                if nombre_boton == 'Iniciar Nueva Activacion':
                    try:
                        message_element = self.legalizador.readShort2('messageFormItem', 'class')
                        print(f'legalizada {self.contador} {message_element}')
                        self.excel.guardar(self.contador, 'Mensaje', message_element)
                        self.excel.guardar(self.contador, 'Min', 'Procesado')
                        self.ventana_informacion.write(f"{self.iccid} {message_element}")
                        time.sleep(1)
                        if not self.wait_for_loading():
                            raise Exception("Timeout esperando carga después de validación")
                        try: 
                            self.legalizador.click('btnPrev', 'id')
                        except Exception as e: 
                            print("btnPrev click después de transacción exitosa", e)
                            # Intentar métodos alternativos de navegación si btnPrev falla
                            try:
                                self.position_detect()  # Detectar posición actual y navegar apropiadamente
                            except:
                                pass
                        # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                        procesado = True
                        break
                    except Exception as e:
                        try:
                            print(f'legalizada con error {self.contador}')
                            try:
                                self.legalizador.click('btnPrev', 'id')
                            except Exception as e:
                                print("btnPrev click después de error", e)
                            # self.legalizador.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/CaptureData')
                            procesado = True
                            break
                        except Exception as e:
                            self.log_error("verificar_urls - manejo de error", e)
                  
                else:
                    try:
                        time.sleep(2)
                        if not self.wait_for_loading():
                            raise Exception("Timeout esperando carga después de validación")
                        # Verificar si el botón existe antes de hacer clic
                        if self.legalizador.elementExists('btnNext', 'id'):
                            self.legalizador.click('btnNext', 'id')
                        else:
                            # El botón no existe, pero no es un error crítico
                            print("btnNext no disponible - continuando proceso")
                    except Exception as e:
                        # Solo loggear si no es el error de btnNext
                        if "btnNext" not in str(e):
                            self.log_error("btnNext click en legalizador", e)
            else:
                ejec = lista_ejecucion[track]
                try:
                    print(f'ejecutando {ejec.__name__}')
                    ejec()
                except Exception as e:
                    self.log_error("Error en ejecución de función", e)
                    mode = 'off'
        if not procesado:
            # Reintentar login y acceso desde cero
            self.poliedro_login_service = None
            if not self.login():
                self.ventana_informacion.write('❌ Error en login, verifique sus credenciales')
                self.on_of(True)
                # Lanzar excepción para salir del bloque try y entrar al except final
                raise Exception("Error crítico: Fallo en login de Poliedro")
            time.sleep(2)
            try:
                self.legalizador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
            except Exception as e:
                self.log_error("click en menú", e)
                return
            time.sleep(2)
            self.poliedro.seleccionAcceso('362', start=True)
            if not self.wait_for_loading(legalizador=False):
                raise Exception("Timeout esperando carga")
            raise Exception(f'No fue posible ejecutar el proceso de verificación de URLs, intentos agotados: {max_intentos}')

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
        max_iterations = 20  # LÍMITE MÁXIMO DE ITERACIONES
        
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
        
        # Acá se realiza el reintento login
        self.poliedro_login_service = None
        if not self.login():
            self.ventana_informacion.write('❌ Error en login, verifique sus credenciales')
            self.on_of(True)
            # Lanzar excepción para salir del bloque try y entrar al except final
            raise Exception("Error crítico: Fallo en login de Poliedro")
        time.sleep(2)
        try:
            self.legalizador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
        except Exception as e:
            self.log_error("click en menú", e)
            return
        time.sleep(2)
        self.poliedro.seleccionAcceso('362', start=True)
        if not self.wait_for_loading(legalizador=False):
            raise Exception("Timeout esperando carga")
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

    def wait_for_loading(self, timeout=120, sleep_interval=1, legalizador=True):
        """
        Método reutilizable para esperar que termine la carga con timeout adaptativo.
        
        Args:
            timeout (int): Tiempo máximo de espera en segundos
            sleep_interval (float): Intervalo entre verificaciones
            legalizador (bool): True para usar self.legalizador, False para self.poliedro
            
        Returns:
            bool: True si terminó la carga, False si hubo timeout
        """
        # ✅ APLICAR TIMEOUT ADAPTATIVO
        adaptive_timeout = self.get_adaptive_timeout(timeout)
        start_time = time.time()
        
        while time.time() - start_time < adaptive_timeout:
            try:
                if legalizador:
                    try:
                        loading_style = self.legalizador.style('loading', 'id')
                    except Exception:
                        loading_style = self.poliedro.style('loading', 'id')
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
        
        # ✅ REGISTRAR TIMEOUT PARA MÉTRICAS ADAPTATIVAS
        self.recent_timeouts += 1
        print(f"Timeout después de {adaptive_timeout} segundos esperando que termine la carga")
        self.ventana_informacion.write(f"⚠️ Timeout detectado ({adaptive_timeout}s) - Total recientes: {self.recent_timeouts}")
        return False  # Timeout
    
    def actualizar_metricas(self):
        """
        Actualiza y muestra métricas de rendimiento en tiempo real
        """
        if not self.inicio_proceso:
            return
            
        tiempo_transcurrido = time.time() - self.inicio_proceso
        total_procesadas = self.transacciones_exitosas + self.transacciones_fallidas
        
        if tiempo_transcurrido > 0:
            velocidad = total_procesadas / (tiempo_transcurrido / 60)  # transacciones por minuto
            tasa_exito = (self.transacciones_exitosas / total_procesadas * 100) if total_procesadas > 0 else 0
            
            transacciones_restantes = self.excel.cantidad - self.contador
            eta_minutos = (transacciones_restantes / velocidad) if velocidad > 0 else 0
            
            mensaje = f"📊 MÉTRICAS: {self.contador}/{self.excel.cantidad} | "
            mensaje += f"✅ {self.transacciones_exitosas} | ❌ {self.transacciones_fallidas} | "
            mensaje += f"🎯 {tasa_exito:.1f}% éxito"
            
            self.ventana_informacion.write(mensaje)
    
    def reporte_final_ciclo(self, numero_ciclo):
        """
        Genera reporte final de métricas del ciclo
        """
        if not self.inicio_proceso:
            return
            
        tiempo_total = time.time() - self.inicio_proceso
        total_procesadas = self.transacciones_exitosas + self.transacciones_fallidas
        tasa_exito = (self.transacciones_exitosas / total_procesadas * 100) if total_procesadas > 0 else 0
        
        reporte = f"🏁 CICLO {numero_ciclo} COMPLETADO:"
        reporte += f" | ✅ {self.transacciones_exitosas} exitosas"
        reporte += f" | ❌ {self.transacciones_fallidas} fallidas"
        reporte += f" | 🎯 {tasa_exito:.1f}% éxito"
        reporte += f" | ⏱️ {tiempo_total/60:.1f} minutos"
        
        self.ventana_informacion.write(reporte)
        
        # Guardar métricas en log
        with open("metricas_legalizador.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {reporte}")
    
    def get_adaptive_timeout(self, base_timeout=35):
        """
        Calcula timeout adaptativo basado en condiciones actuales
        
        Args:
            base_timeout (int): Timeout base en segundos
            
        Returns:
            int: Timeout ajustado
        """
        # Si han habido muchos timeouts recientes, incrementar timeout
        if self.recent_timeouts > 3:
            adjusted_timeout = int(base_timeout * 1.5)
            return adjusted_timeout
        
        # Si hay muchas transacciones fallidas, ser más conservador
        total_procesadas = self.transacciones_exitosas + self.transacciones_fallidas
        if total_procesadas > 10:
            tasa_fallo = (self.transacciones_fallidas / total_procesadas) * 100
            if tasa_fallo > 20:  # Si más del 20% fallan
                adjusted_timeout = int(base_timeout * 1.3)
                return adjusted_timeout
        
        return base_timeout

    def procesar_por_lotes(self, tamano_lote=None):
        """
        Procesa las transacciones en lotes para mejorar estabilidad y manejo de memoria.
        
        Args:
            tamano_lote (int, optional): Número de transacciones por lote. Si None, se calcula automáticamente.
        """
        total_transacciones = self.excel.cantidad
        
        # VALIDACIÓN PARA ARCHIVOS PEQUEÑOS
        if total_transacciones == 0:
            self.ventana_informacion.write("No hay transacciones para procesar en el archivo Excel")
            return
        elif total_transacciones <= 5:
            self.ventana_informacion.write(f"Archivo pequeño detectado ({total_transacciones} transacciones) - Procesamiento directo sin lotes")
            # Para archivos muy pequeños, procesar todo en un solo lote
            tamano_lote = total_transacciones
        else:
            # CALCULAR TAMAÑO DE LOTE ÓPTIMO SI NO SE ESPECIFICA
            if tamano_lote is None:
                tamano_lote = self.calcular_tamano_lote_optimo(total_transacciones)
        
        lotes = list(range(0, total_transacciones, tamano_lote))
        
        # MENSAJE INFORMATIVO SEGÚN TIPO DE PROCESAMIENTO
        if total_transacciones <= 5:
            self.ventana_informacion.write(f"Procesando {total_transacciones} transacciones en modo directo (sin lotes)")
        else:
            self.ventana_informacion.write(f"Procesando {total_transacciones} transacciones en {len(lotes)} lotes de max {tamano_lote}")
        
        # Inicializar setup una sola vez
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente en demografica")
        try:
            self.legalizador.click('toggleProductBTN', 'id')
        except:
            pass
        
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga inicial en procesar_por_lotes")
        
        self.cookie_header['Cookie'] = self.legalizador.getCookies()
        
        for i, inicio_lote in enumerate(lotes):
            if not self.ciclo:  # Si el usuario detuvo el proceso
                self.ventana_informacion.write('Proceso interrumpido por el usuario')
                break
            
            # VERIFICAR SESIÓN AL INICIO DE CADA LOTE
            if not self.verificar_sesion_activa():
                self.ventana_informacion.write(f"❌ Error crítico: No se pudo restaurar la sesión para el lote {i+1}")
                self.on_of(True)  # Detener el proceso
                raise Exception("Error crítico: Fallo en login de Poliedro")
                
            fin_lote = min(inicio_lote + tamano_lote, total_transacciones)
            
            self.ventana_informacion.write(f"LOTE {i+1}/{len(lotes)}: Procesando transacciones {inicio_lote+1} a {fin_lote}")
            
            # Procesar transacciones en este lote
            errores_consecutivos = 0
            max_errores_consecutivos = 5
            
            for j in range(inicio_lote, fin_lote):
                if not self.ciclo:  # Si el usuario detuvo el proceso
                    break
                    
                self.contador = j
                
                try:
                    self.min = str(self.excel.excel['min'][self.contador])
                    self.mensaje = str(self.excel.excel['Mensaje'][self.contador])

                    mensaje_valido = str(self.mensaje) not in ['nan', 'error']
                    min_invalido = str(self.excel.excel['Min'][self.contador]) in ['error', 'procesado']

                    if mensaje_valido or min_invalido:
                        self.ventana_informacion.write(f'✓ Legalizacion {self.min} ya realizada o con error ya detectado')
                        continue
                    
                    # VALIDAR DATOS ANTES DE PROCESAR
                    self.establecer_datos()  # Primero establecer los datos

                    self.cookie_header['Cookie'] = self.legalizador.getCookies()
                    
                    # PROCESAR TRANSACCIÓN CON MÉTRICAS
                    try:
                        self.verificar_urls()
                        self.transacciones_exitosas += 1
                        errores_consecutivos = 0  # Reset contador de errores
                        self.ventana_informacion.write(f'✅ Transacción {j+1} completada exitosamente')
                    except Exception as e:
                        if "Error crítico: Fallo en login de Poliedro" in str(e):
                            raise Exception("Error crítico: Fallo en login de Poliedro")
                        self.transacciones_fallidas += 1
                        errores_consecutivos += 1
                        self.log_error(f"verificar_urls transacción {j+1}", e)
                        self.ventana_informacion.write(f'❌ Error en transacción {j+1}: {str(e)[:100]}')
                        
                        # Si hay muchos errores consecutivos, hacer pausa extra
                        if errores_consecutivos >= max_errores_consecutivos:
                            self.ventana_informacion.write(f'⚠️ {errores_consecutivos} errores consecutivos, pausando 10s...')
                            time.sleep(10)
                            errores_consecutivos = 0
                    
                    # PAUSA ALEATORIA ENTRE TRANSACCIONES PARA EVITAR DETECCIÓN DE BOT
                    if j < fin_lote - 1:  # No pausar después de la última transacción del lote
                        tiempo_pausa = random.randint(15, 28)
                        self.ventana_informacion.write(f"Pausa anti-bot: {tiempo_pausa}s entre transacciones...")
                        time.sleep(tiempo_pausa)

                    # ACTUALIZAR MÉTRICAS CADA 5 TRANSACCIONES (más frecuente en lotes)
                    if (j + 1) % 5 == 0:
                        self.actualizar_metricas()
                        
                except Exception as e:
                    if "Error crítico: Fallo en login de Poliedro" in str(e):
                        raise Exception("Error crítico: Fallo en login de Poliedro")
                    self.log_error(f"iteración de lote {j+1}", e)
                    self.transacciones_fallidas += 1
                    errores_consecutivos += 1
                    self.ventana_informacion.write(f'Error crítico en transacción {j+1}: {str(e)[:100]}')
            
            # Guardar progreso después de cada lote
            try:
                #self.excel.guardar_archivo()  # Asegurar que se guarden los cambios
                self.ventana_informacion.write(f"Lote {i+1} completado y guardado - Éxitos: {self.transacciones_exitosas}, Fallos: {self.transacciones_fallidas}")
            except Exception as e:
                self.log_error("guardar_lote", e)
            
            # GENERAR REPORTE PERIÓDICO DETALLADO
            tiempo_actual = time.time()
            if tiempo_actual - self.ultimo_reporte >= self.intervalo_reporte:
                """ reporte = self.generar_reporte_estado()
                self.ventana_informacion.write(f"REPORTE PERIÓDICO:")
                self.ventana_informacion.write(f"   • Tiempo: {reporte['tiempo_transcurrido_min']} min")
                self.ventana_informacion.write(f"   • Procesadas: {reporte['total_procesadas']}/{reporte['total_transacciones']}")
                self.ventana_informacion.write(f"   • Tasa éxito: {reporte['tasa_exito']}%")
                self.ventana_informacion.write(f"   • Velocidad: {reporte['velocidad_por_min']} trans/min")
                self.ventana_informacion.write(f"   • ETA: {reporte['eta_minutos']} min") """
                self.ultimo_reporte = tiempo_actual
            
            # Pausa entre lotes para estabilidad (excepto el último)
            if i < len(lotes) - 1 and self.ciclo:
                tiempo_pausa = 3
                self.ventana_informacion.write(f"Pausa de {tiempo_pausa}s entre lotes para estabilidad...")
                time.sleep(tiempo_pausa)
                
                # Reset de métricas de timeouts para el nuevo lote
                self.recent_timeouts = max(0, self.recent_timeouts - 1)
        
        self.ventana_informacion.write(f"Procesamiento por lotes completado - Total éxitos: {self.transacciones_exitosas}, Total fallos: {self.transacciones_fallidas}")
    
    def calcular_tamano_lote_optimo(self, total_transacciones):
        """
        Calcula el tamaño de lote óptimo basado en el total de transacciones y condiciones del sistema.
        
        Args:
            total_transacciones (int): Total de transacciones a procesar
            
        Returns:
            int: Tamaño de lote recomendado
        """
        # MANEJO ESPECIAL PARA ARCHIVOS MUY PEQUEÑOS
        if total_transacciones <= 5:
            self.ventana_informacion.write(f"Archivo pequeño ({total_transacciones} transacciones) - Un solo lote")
            return total_transacciones
        elif total_transacciones <= 10:
            tamano_base = 5  # Lotes de 5 para 6-10 registros (más consistente)
            self.ventana_informacion.write(f"Archivo chico ({total_transacciones} transacciones) - Lotes de {tamano_base}")
        elif total_transacciones <= 15:
            tamano_base = 5  # Lotes de 5 para 11-15 registros
            self.ventana_informacion.write(f"Archivo chico ({total_transacciones} transacciones) - Lotes de {tamano_base}")
        elif total_transacciones <= 50:
            tamano_base = 10
        elif total_transacciones <= 200:
            tamano_base = 25
        elif total_transacciones <= 500:
            tamano_base = 30
        else:
            tamano_base = 40
        
        # Ajustar según tasa de fallos histórica si tenemos datos
        total_procesadas = self.transacciones_exitosas + self.transacciones_fallidas
        if total_procesadas > 20:
            tasa_fallo = (self.transacciones_fallidas / total_procesadas) * 100
            if tasa_fallo > 15:  # Si más del 15% fallan
                tamano_base = max(5, int(tamano_base * 0.7))  # Reducir tamaño del lote (mínimo 5)
            elif tasa_fallo < 5:  # Si menos del 5% fallan
                tamano_base = min(50, int(tamano_base * 1.2))  # Aumentar tamaño del lote (máximo 50)
        
        return tamano_base

    def configurar_modo_produccion(self):
        """
        Configura parámetros optimizados para modo producción de alto volumen.
        """
        # Configuración para operaciones de alto volumen
        self.recent_timeouts = 0
        self.ultimo_reporte = time.time()
        self.intervalo_reporte = 300  # Reportar cada 5 minutos
        
        # Timeouts más conservadores para producción
        self.timeout_base = 45  # Aumentar timeout base
        self.max_reintentos = 3
        
        # Configuración de logs más detallada
        self.log_detallado = True
    
    def verificar_sesion_activa(self):
        """
        Verifica si la sesión está activa y la renueva si es necesario
        
        Returns:
            bool: True si la sesión está activa o se renovó exitosamente, False en caso contrario
        """
        try:
            # Si ya estamos en estado crítico, no intentar más
            if self.error_critico_sesion:
                self.ventana_informacion.write("Se presenta un error crítico para iniciar sesión en Poliedro")
                return False
                
            # Inicializar el servicio si no existe
            if not self.poliedro_login_service:
                self.inicializar_login_service()
                
            # Verificar si la sesión está activa
            if not self.poliedro_login_service.validar_sesion_activa():
                self.ventana_informacion.write("Sesión expirada, reintentando login...")
                self.intentos_recuperacion += 1
                
                if not self.login():
                    self.ventana_informacion.write('❌ Error en login, verifique sus credenciales')
                    self.on_of(True)
                    # Lanzar excepción para salir del bloque try y entrar al except final
                    raise Exception("Error crítico: Fallo en login de Poliedro")
                else:
                    # Sesión recuperada exitosamente
                    self.intentos_recuperacion = 0  # Reset contador
                    self.ventana_informacion.write("Sesión renovada exitosamente")
                    
                    # Navegar al formulario principal después de renovar sesión
                    try:
                        self.legalizador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
                        time.sleep(3)
                        self.poliedro.seleccionAcceso('362', start=True)
                        if not self.wait_for_loading(legalizador=False):
                            return False
                    except Exception as e:
                        self.log_error("restaurar_navegacion", e)
                        self.intentos_recuperacion += 1
                        return False
            return True
        except Exception as e:
            if "Error crítico: Fallo en login de Poliedro" in str(e):
                raise Exception("Error crítico: Fallo en login de Poliedro")
            self.log_error("verificar_sesion_activa", e)
            self.intentos_recuperacion += 1
            
            # Si alcanzamos el máximo de intentos con excepciones, marcar error crítico
            if self.intentos_recuperacion >= self.max_intentos_recuperacion:
                self.error_critico_sesion = True
                self.ventana_informacion.write("ERROR CRÍTICO: Múltiples fallos al verificar sesión")
                
            return False