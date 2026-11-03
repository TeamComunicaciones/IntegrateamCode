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
from funcionalidad import perfiles_credenciales as perfiles
from navegacion import modal_credenciales
from funcionalidad.mixin_validacion_codigos import ValidacionCodigosMixin
import random
import os
import re
import shutil
import unicodedata
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException


# Modo eSIM: el checkbox de CaptureData (en PRE-EQUIPOS se envía por API como
# 'DetailProduct.CheckEsim') y el plan que siempre se escoge en ProductService.
ID_CHECK_ESIM = 'DetailProduct_CheckEsim'
PLAN_ESIM = 'ESTRATEGICO Control'

# Dropdowns (select2) de ProductService
XPATH_DROPDOWN_EQUIPO = '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]'
XPATH_DROPDOWN_PLAN = '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]'
XPATH_PLAN_ESIM = '//*[@id="select2-EquipmentPlanDataViewModel_Plan-container"]'
XPATH_OPCIONES_PLAN = '//ul[@id="select2-EquipmentPlanDataViewModel_Plan-results"]/li'

# Columnas de la plantilla, en el orden en que quedan para todos los operarios
COLUMNAS_PLANTILLA = ['Iccid', 'Documento', 'TipoDoc', 'Cedula', 'Nombre', 'Apellido',
                      'Correo_cliente', 'Correo_QR', 'Telefono', 'Direccion',
                      'Min', 'Mensaje', 'Codigo_distribuidor']

# Banner de Activation que pregunta a qué correo enviar el QR de la eSIM
ID_CORREO_QR = 'textmailvalidate'
ID_ACEPTAR_QR = 'btnOkModal'
ID_ERROR_CORREO_QR = 'msjerrormail'


def _normalizar(texto):
    """Minúsculas y sin tildes, para comparar textos de la página."""
    texto = unicodedata.normalize('NFKD', str(texto or ''))
    return ''.join(c for c in texto if not unicodedata.combining(c)).strip().lower()


def _primero(*valores):
    """Devuelve el primer valor no vacío (orden de prioridad), o ''."""
    for valor in valores:
        if valor is not None and str(valor).strip() and str(valor).strip().lower() != 'nan':
            return str(valor).strip()
    return ''


class AvisoPoliedro(Exception):
    """Poliedro respondió con un aviso (alert o error en el banner) al activar."""
    def __init__(self, aviso):
        super().__init__(aviso)
        self.aviso = aviso


class SessionExpiredError(Exception):
    """Excepción para indicar que la sesión expiró y el bot fue redirigido al login."""
    pass

class Preactivador(ValidacionCodigosMixin):

    def __init__(self,master, on_of, alertas):
        self.traffic_base = "https://prod-md.azpol.claro.com.co"
        self.alertas = alertas
        self.min = ''
        self.etapa = 0
        self.mensaje = 's'
        self.on_of = on_of
        self.time2 = 3
        self.cookie_header = {}
        self.poliedro_login_service = None  # servicio de login (OTP incluido)
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        _carpeta = os.path.join(os.path.expanduser("~"), "Documents", "TeamComunicaciones", "preactivador")
        os.makedirs(_carpeta, exist_ok=True)
        self.excel_path = os.path.join(_carpeta, "preactivador.xlsx")
        if not os.path.exists(self.excel_path):
            shutil.copy2(r'src\preactivador\preactivador.xlsx', self.excel_path)
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.link_google_messages = 'https://messages.google.com/web/conversations'
        self.link_mysms = 'https://app.mysms.com/#87472'

        self.titulo = label.Label().create_label(master, 'PREACTIVADOR DE SIM', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master, 4, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['CREDENCIALES', lambda: modal_credenciales.abrir_modal(master.winfo_toplevel())], boton4=['START', self.ejecuccionHilo])
        self.preactivador = ''
        self.time = tk.StringVar()
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.10, 0.59, 0.33, 0.05, letterSize=16)
        self.titulo.configure(anchor='w')
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.45, rely=0.59, relheight=0.05, relwidth=0.20)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.59, 0.15, 0.05, self.cambioIntervalo)
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

        # Correo de respaldo: se usa si Poliedro y la plantilla no traen correo
        # (y para el QR de la eSIM si la fila no trae Correo_QR).
        self.correo = 'acruz@teamcomunicaciones.com'
        self.correoEdit = tk.StringVar()
        self.correoEdit.set(self.correo) 
        input_widget2 = ctk.CTkEntry(self.menu.submenu, textvariable=self.correoEdit)
        input_widget2.place(relx=0.10, rely=0.66, relheight=0.05, relwidth=0.55)
        self.okBotton2 = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.66, 0.15, 0.05, self.cambioCorreo)
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

        # Modo eSIM: se toma al pulsar START (self.es_esim)
        self.esim = tk.BooleanVar()
        self.es_esim = False
        self.checkbox_esim = checkbox.Checkbox().create_checkbox(self.menu.submenu, 'eSIM', self.on_checkbox_change_esim, self.esim)

        # Configuracion para tiempo de espera
        self.tiempo_espera_label = label.Label().create_label(self.menu.submenu, 'Tiempo de espera', 0.10, 0.46, 0.6, 0.04, letterSize=16)
        self.tiempo_espera_label.configure(anchor='w')

        self.spinbox_tiempo_espera = spinbox.CTkSpinbox(self.menu.submenu, from_=5, to=60, default=5)
        self.spinbox_tiempo_espera.place(relx=0.10, rely=0.50, relheight=0.06, relwidth=0.55)

        # Si el usuario no presiona OK, toma el valor por defecto
        self.valor = self.spinbox_tiempo_espera.get_value()

        self.tiempo_espera_okbutton = boton.create_button(self.menu.submenu, 'OK', 0.66, 0.50, 0.15, 0.05, self.guardar_tiempo_espera)
        self.tiempo_espera_okbutton.configure(fg_color=color.team, text_color='white')

        # Las credenciales se editan con el botón CREDENCIALES del submenú
        # (ventana compartida por los módulos de Poliedro: navegacion/modal_credenciales.py).
        self.perfil = None  # copia del perfil activo, tomada al pulsar START

        self.checkbox_modo_captura_datos = checkbox.Checkbox()
        self.modo_captura_datos = tk.BooleanVar()
        self.checkbox_modo_captura_datos = checkbox.Checkbox().create_checkbox(self.menu.submenu, 'Envio de datos por API', self.on_checkbox_change_modo_captura, self.modo_captura_datos)

        # Validación de códigos de distribuidor (siempre activa; lista independiente para PRE-SIM)
        self._init_validacion_codigos('pre-sim')

        self._actualizar_columnas_plantilla()

    def _actualizar_columnas_plantilla(self):
        """Agrega al Excel del operario las columnas que le falten y las deja en el orden de COLUMNAS_PLANTILLA.

        Las filas no se tocan; las columnas propias del operario pasan al final.
        """
        if self._excel_abierto():
            self.ventana_informacion.write('⚠️ Cierre el Excel de PRE-SIM para actualizar sus columnas.')
            return
        try:
            self.excel.leer_excel(self.excel_path, dtype=str)
            datos = self.excel.excel
            orden = COLUMNAS_PLANTILLA + [c for c in datos.columns if c not in COLUMNAS_PLANTILLA]
            if list(datos.columns) == orden:
                return
            faltantes = [c for c in COLUMNAS_PLANTILLA if c not in datos.columns]
            datos.reindex(columns=orden).to_excel(self.excel_path, index=False)
            if faltantes:
                self.ventana_informacion.write(f'Plantilla actualizada, columnas nuevas: {", ".join(faltantes)}')
        except Exception as e:
            self.ventana_informacion.write(f'⚠️ No se pudieron actualizar las columnas del Excel: {e}')

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

    def on_checkbox_change_esim(self):
        if self.esim.get():
            self.ventana_informacion.write('Modo eSIM: Sin IMEI + eSIM, plan ESTRATEGICO Control (solo envío por Web)')
        else:
            self.ventana_informacion.write('Modo SIM física')

    
    def abrir_excel(self):
        self._actualizar_columnas_plantilla()
        self.ventana_informacion.write('excel preactivador abierto recuerde cerrar antes de iniciar')
        os.startfile(self.excel_path)
    
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
        perfil = modal_credenciales.credenciales_listas(self.menu.submenu, self.ventana_informacion)
        if perfil is None:
            return

        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.preactivador = Abrir_pagina1(int(self.time.get()))
        self.preactivador.openEdge()
        time.sleep(3)
        self.preactivador.selectPage(self.link)

        time.sleep(2)
        if perfil['metodo_otp'] == perfiles.METODO_MYSMS:
            self.preactivador.script(f"window.open('{self.link_mysms}', '_blank');")
        elif perfil['metodo_otp'] == perfiles.METODO_GOOGLE:
            self.preactivador.script(f"window.open('{self.link_google_messages}', '_blank');")

    def ejecuccionHilo(self):
        perfil = modal_credenciales.credenciales_listas(self.menu.submenu, self.ventana_informacion)
        if perfil is None:
            return
        if self._excel_abierto():
            self.ventana_informacion.write('❌ El Excel está abierto. Ciérrelo y pulse START de nuevo.')
            return
        self.perfil = perfil
        self.es_esim = self.esim.get()
        if self.es_esim and self.modo_captura_datos.get():
            self.ventana_informacion.write('Modo eSIM: se ignora "Envio de datos por API", se usa la Web')
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

            # Validación de códigos de distribuidor: se hace apenas termina el login
            # (el código de distribuidor está en el header, presente tras login) para
            # abortar antes de navegar al módulo si el código está bloqueado.
            if self.es_esim:
                self.ventana_informacion.write('Modo eSIM: no se validan códigos de distribuidor bloqueados')
            elif not self._codigo_distribuidor_permitido(self.preactivador):
                self.on_of(True)
                return

            try:
                self.preactivador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
            except:
                pass

            # self.preactivador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
            self.poliedro.seleccionAcceso('195')
            self.sync_traffic_base_from_browser()
            if not self.safe_wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")

            self.excel.leer_excel(self.excel_path,'Documento', dtype={'Iccid': str, 'Documento': str, 'Cedula': str, 'Telefono': str})
            if not self.es_esim:
                # En eSIM el Iccid lo genera Poliedro y viene vacío en la plantilla
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
                            self._run_with_relogin(self.EquiposInd)
                    except Exception as e:
                        if isinstance(e, PermissionError):
                            # Excel abierto: seguir solo quemaría ICCIDs sin poder guardarlos
                            self.ventana_informacion.write('❌ No se pudo guardar en el Excel porque está abierto. Ciérrelo y pulse START de nuevo.')
                            self.on_of(True)
                            return
                        # Los raise('...') de EquiposInd (TypeError) ya escribieron su mensaje
                        if not isinstance(e, TypeError):
                            self.ventana_informacion.write(f'⚠️ Registro {self.contador+1}: {e}')
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
        tipo = 'eSIM' if self.es_esim else 'Equipo'
        self.ventana_informacion.write(f'Activando {tipo} {self.contador+1} de {self.excel.cantidad}')
        # En eSIM el Iccid lo genera Poliedro en CaptureData
        self.iccid = '' if self.es_esim else excel.limpiar_decimal(self.excel.excel['Iccid'][self.contador])[-12:]
        self.documento = excel.limpiar_decimal(self.excel.excel['Documento'][self.contador])
        self.cedula_excel = excel.limpiar_decimal(self.excel.excel['Cedula'][self.contador])
        self.codigo_distribuidor = self.preactivador.read('userDataCodDistribuidor', 'id')
        # Datos del cliente: se usan solo si Poliedro no los trae en Demographic
        self.nombre = self._celda('Nombre')
        self.apellido = self._celda('Apellido') or ' '
        self.correo_cliente = self._celda('Correo_cliente')
        self.correo_qr = self._celda('Correo_QR')
        self.telefono = self._celda('Telefono')
        self.direccion = self._celda('Direccion')
        self.tipoDoc = str(self.excel.excel['TipoDoc'][self.contador])
        self.documentType = 2 if self.tipoDoc.lower() == 'nit' else 1
        self.tipoDoc_aux = "Cedula" if self.documentType == 1 else "NIT"

        self.position(self.preactivador.retornarHtml(), 'paso1', True)

        if self._usar_api():
            self.captura_datos_api()
        else:
            self.captura_datos_web()
        
        self.position(self.preactivador.retornarHtml(), 'paso2', True)
        
        try:
            errors = self.preactivador.readMulty('errorFormItem', 'class')
        except Exception:
            errors = ''

        # 2) Catálogo de errores a detecta  r (en el orden que quieres priorizar)
        ERROR_MAP = [
            (
                "ICC_ID - Identificación Tarjeta de Circuito Integrada. = v",
                "ICC_ID - Identificación Tarjeta de Circuito Integrada.",
            ),
            (
                "Validacion Causal Desactivacion IccId = Falso",
                "Validacion Causal Desactivacion IccId = Falso",
            ),
            (
                "Documentos invalidos = Falso",
                "Documentos invalidos",
            ),
        ]

        for needle, msg in ERROR_MAP:
            if needle in errors:
                self.excel.guardar(self.contador, 'Mensaje', msg, destino=self.excel_path)
                self.excel.guardar(self.contador, 'Min', 'error', destino=self.excel_path)
                self.ventana_informacion.write(msg)
                raise('error validacion 2')

        validate = self.preactivador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span')
        if validate != 'Validación Correcta':
            raise('error')
        self.preactivador.click('btnNext', 'id')
        self.position(self.preactivador.retornarHtml(), 'paso3', True)

        if self._usar_api():
            self.datos_demograficos_api()
        else:
            self.datos_demograficos_web()

        self.position(self.preactivador.retornarHtml(), 'paso4', True)

        # Equipo: primera opción de la lista
        self.preactivador.click(XPATH_DROPDOWN_EQUIPO)
        self.preactivador.click('/html/body/span/span/span[2]/ul/li[2]')
        if self.es_esim:
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de escoger equipo")
            self.seleccionar_plan_esim()
        else:
            # Plan: primera opción de la lista
            self.preactivador.click(XPATH_DROPDOWN_PLAN)
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
        if self.es_esim:
            # Activar + banner con el correo al que llega el QR de la eSIM
            texto = self.activar_con_qr()
        else:
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
            texto = self.preactivador.read('messageFormItem', 'class')
        encontrado = re.search(r'MSISDN asignado es\s*(\d{10})', texto)
        if encontrado:
            message = encontrado.group(1)
        else:
            message = texto.replace('* Su Solicitud fue enviada satisfactoriamente para el producto 195 y el MSISDN asignado es ', '')
            message = message[:10]
        self.excel.guardar(self.contador, 'Min', message, destino=self.excel_path)
        self.excel.guardar(self.contador, 'Codigo_distribuidor', self.codigo_distribuidor, destino=self.excel_path)
        if self.es_esim:
            self.ventana_informacion.write(f'Preactivada eSIM con min {message} (ICCID {self.iccid})')
        else:
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

        if self.es_esim:
            #Opción serial + eSIM (el Iccid lo genera Poliedro)
            self.poliedro.tipoDoc('Sin IMEI','//*[@id="select2-DetailProduct_OptionImei-container"]')
            self.activar_esim()
        else:
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

    # ---------------------------------------------------------------------
    # Modo eSIM
    # ---------------------------------------------------------------------

    def activar_esim(self, timeout=30):
        """Marca el checkbox eSIM, espera el Iccid que genera Poliedro y lo guarda en la plantilla."""
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de escoger Sin IMEI")
        check = self.preactivador.browser.find_element_by_id(ID_CHECK_ESIM)
        if not check.is_selected():
            try:
                check.click()
            except Exception:
                # Checkbox oculto por estilos: click por JS
                self.preactivador.browser.execute_script("arguments[0].click();", check)
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de marcar eSIM")

        fin = time.time() + timeout
        while time.time() < fin:
            self.iccid = self._valor_pagina('DetailProduct_Iccid')
            if self.iccid:
                self.excel.guardar(self.contador, 'Iccid', self.iccid, destino=self.excel_path)
                self.ventana_informacion.write(f'ICCID eSIM generado: {self.iccid}')
                return
            time.sleep(1)
        # Sin Min='error': la fila se reintenta en la siguiente corrida
        mensaje = 'Poliedro no generó el ICCID de la eSIM'
        self.excel.guardar(self.contador, 'Mensaje', mensaje, destino=self.excel_path)
        self.ventana_informacion.write(mensaje)
        raise Exception(mensaje)

    def seleccionar_plan_esim(self):
        """Escoge el plan ESTRATEGICO Control en ProductService y verifica que quedó seleccionado."""
        self.preactivador.click(XPATH_PLAN_ESIM)
        buscado = _normalizar(PLAN_ESIM)
        opciones = self.preactivador.browser.find_elements_by_xpath(XPATH_OPCIONES_PLAN)
        for opcion in opciones:
            if _normalizar(opcion.text) == buscado:
                opcion.click()
                break
        else:
            self.preactivador.write('/html/body/span/span/span[1]/input', Keys.ESCAPE)

        if buscado not in _normalizar(self.preactivador.read(XPATH_PLAN_ESIM)):
            mensaje = f'Plan {PLAN_ESIM} no disponible'
            self.excel.guardar(self.contador, 'Mensaje', mensaje, destino=self.excel_path)
            self.excel.guardar(self.contador, 'Min', 'error', destino=self.excel_path)
            self.ventana_informacion.write(mensaje)
            raise Exception(mensaje)

    def activar_con_qr(self):
        """Pulsa Activar, confirma el correo del QR y devuelve el texto con el MSISDN.

        Si Poliedro responde "Buzón no válido" se reintenta: primero con el mismo
        correo (el rechazo a veces es pasajero) y luego con los siguientes en
        prioridad: Correo_QR, el de la pantalla, Correo_cliente.
        """
        correos = []
        for correo in (self.correo_qr, self.correo, self.correo_cliente):
            correo = _primero(correo)
            if correo and _normalizar(correo) not in [_normalizar(c) for c in correos]:
                correos.append(correo)
        if not correos:
            raise Exception('No hay correo para enviar el QR')

        rechazados = []
        for correo in [correos[0]] + correos:
            if not self._banner_qr_visible():
                self.preactivador.click('btnNext', 'id')
            try:
                self.confirmar_correo_qr(correo)
                texto = self.esperar_resultado_activacion()
            except AvisoPoliedro as e:
                if 'buzon' not in _normalizar(e.aviso):
                    mensaje = f'Aviso de Poliedro al activar: {e.aviso}'
                    self.excel.guardar(self.contador, 'Mensaje', mensaje, destino=self.excel_path)
                    self.ventana_informacion.write(mensaje)
                    raise
                rechazados.append(correo)
                self.ventana_informacion.write(f'⚠️ Poliedro respondió "{e.aviso}" para {correo}. Reintentando...')
                time.sleep(2)
                continue
            if rechazados:
                mensaje = f'QR enviado a {correo} (Poliedro rechazó antes: {", ".join(dict.fromkeys(rechazados))})'
                self.excel.guardar(self.contador, 'Mensaje', mensaje, destino=self.excel_path)
                self.ventana_informacion.write(mensaje)
            return texto

        # Sin Min='error': el rechazo puede ser pasajero y la fila se reintenta en otra corrida
        mensaje = f'Poliedro rechazó el buzón de todos los correos del QR: {", ".join(correos)}'
        self.excel.guardar(self.contador, 'Mensaje', mensaje, destino=self.excel_path)
        self.ventana_informacion.write(mensaje)
        raise Exception(mensaje)

    def _banner_qr_visible(self):
        try:
            return self.preactivador.browser.find_element_by_id(ID_CORREO_QR).is_displayed()
        except Exception:
            return False

    def confirmar_correo_qr(self, destino, timeout=30):
        """En el banner del QR deja `destino` como correo y pulsa Aceptar."""
        fin = time.time() + timeout
        while time.time() < fin and not self._banner_qr_visible():
            aviso = self._leer_alerta()
            if aviso:
                raise AvisoPoliedro(aviso)
            time.sleep(1)
        if not self._banner_qr_visible():
            self._guardar_html('banner_qr')
            raise Exception('No apareció el banner del correo del QR')

        campo = self.preactivador.browser.find_element_by_id(ID_CORREO_QR)
        if _normalizar(campo.get_attribute('value')) != _normalizar(destino):
            campo.clear()
            campo.send_keys(destino)
        # Salir del campo y dar tiempo a que Poliedro tome el correo completo antes de Aceptar
        campo.send_keys(Keys.TAB)
        time.sleep(1.5)
        aviso = self._leer_alerta()
        if aviso:
            raise AvisoPoliedro(aviso)

        self.ventana_informacion.write(f'QR de la eSIM se envía a {destino}')
        self.preactivador.browser.find_element_by_id(ID_ACEPTAR_QR).click()
        time.sleep(1)

        # Poliedro también puede mostrar el error dentro del mismo banner
        aviso = self._leer_alerta()
        if aviso:
            raise AvisoPoliedro(aviso)
        try:
            error = self.preactivador.browser.find_element_by_id(ID_ERROR_CORREO_QR)
            texto_error = error.text.strip() if error.is_displayed() else ''
        except Exception:
            texto_error = ''
        if texto_error:
            raise AvisoPoliedro(texto_error)

    def _leer_alerta(self):
        """Texto del alert del navegador (y lo cierra), o None si no hay."""
        try:
            alerta = self.preactivador.browser.switch_to.alert
            texto = alerta.text
            alerta.accept()
            return (texto or '').strip() or 'Aviso sin texto'
        except NoAlertPresentException:
            return None
        except UnexpectedAlertPresentException as e:
            return (getattr(e, 'alert_text', None) or str(e)).strip()
        except Exception:
            return None

    def esperar_resultado_activacion(self, timeout=180):
        """Espera el mensaje con el MSISDN sin salir de la página (salir a mitad de la activación la interrumpe).

        Si Poliedro muestra un aviso (alert) lanza AvisoPoliedro con su texto.
        """
        browser = self.preactivador.browser
        fin = time.time() + timeout
        while time.time() < fin:
            aviso = self._leer_alerta()
            if aviso:
                raise AvisoPoliedro(aviso)
            try:
                for elemento in browser.find_elements_by_class_name('messageFormItem'):
                    if 'MSISDN' in (elemento.text or ''):
                        return elemento.text
            except UnexpectedAlertPresentException:
                continue
            except Exception:
                pass
            time.sleep(2)

        self._guardar_html('activacion_sin_min')
        mensaje = f'No salió el MIN después de {timeout} s'
        self.excel.guardar(self.contador, 'Mensaje', mensaje, destino=self.excel_path)
        self.ventana_informacion.write(f'⚠️ {mensaje}')
        raise Exception(mensaje)

    def _guardar_html(self, nombre):
        """Guarda el HTML actual junto a la plantilla, para ajustar selectores si algo falla."""
        try:
            ruta = os.path.join(os.path.dirname(self.excel_path),
                                f'html_{nombre}_{datetime.datetime.now():%Y%m%d_%H%M%S}.html')
            with open(ruta, 'w', encoding='utf-8') as archivo:
                archivo.write(self.preactivador.retornarHtml() or '')
            self.ventana_informacion.write(f'HTML guardado en {ruta}')
        except Exception:
            pass

    # ---------------------------------------------------------------------
    # Datos de la plantilla
    # ---------------------------------------------------------------------

    def _celda(self, columna):
        """Valor de la fila actual, o '' si la columna no existe (plantilla vieja) o está vacía."""
        if columna not in self.excel.excel.columns:
            return ''
        return _primero(excel.limpiar_decimal(self.excel.excel[columna][self.contador]))

    def _excel_abierto(self):
        """True si Excel tiene el archivo abierto (Windows lo bloquea para escritura)."""
        try:
            with open(self.excel_path, 'r+b'):
                return False
        except PermissionError:
            return True
        except Exception:
            return False

    def _usar_api(self):
        # eSIM solo funciona por Web: el Iccid se genera en la página
        return self.modo_captura_datos.get() and not self.es_esim

    def _valor_pagina(self, id):
        """Valor de un input por id, sin los reintentos de .value() ('' si no existe)."""
        try:
            return (self.preactivador.browser.find_element_by_id(id).get_attribute('value') or '').strip()
        except Exception:
            return ''

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

        #Correo: el de Poliedro, si no el de la plantilla, si no el de la pantalla
        correo_actual = self.preactivador.value("PersonalInfo_Email","id")
        if not correo_actual or not correo_actual.strip():
            self.preactivador.write("PersonalInfo_Email", _primero(self.correo_cliente, self.correo), 'id')

        #Telefono
        telefono_actual = self.preactivador.value("PhoneId","id")
        if not telefono_actual or not telefono_actual.strip():

            #Tipo: celular de la plantilla, si no el fijo de siempre
            celular = bool(self.telefono) and self._seleccionar_opcion("PhoneClass", ("celular", "movil"))
            if not celular:
                self.selectDropDownNormal("PhoneClass","fijo")

            time.sleep(2)
            if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")

            if celular:
                self.preactivador.write("PhoneNumber", self.telefono, "id")
            else:
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
            
            self.preactivador.write("Address", _primero(self.direccion, "central"), "id")
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
        # Misma prioridad que en Web: lo que trae Poliedro, luego la plantilla
        demographic_data = {
            "PersonalInfo.GreetingId": "O",
            "PersonalInfo.Name": _primero(self._valor_pagina("PersonalInfo_Name"), self.nombre),
            "PersonalInfo.LastName": _primero(self._valor_pagina("PersonalInfo_LastName"), self.apellido) or ' ',
            "PersonalInfo.Email": _primero(self._valor_pagina("PersonalInfo_Email"), self.correo_cliente, self.correo),
            "PersonalInfo.Phone.PhoneId": "",
            "PersonalInfo.Phone.PhoneClass": "2",
            "PersonalInfo.Phone.Prefix": "604",
            "PersonalInfo.Phone.PhoneNumber": "0313123",
            "PersonalInfo.EmailInitial": "",
            "PersonalInfo.DocumentTypeId": self.documentType,
            "PersonalInfo.Document": self.documento,
            "PersonalInfo.Address.AddressId": "",
            "PersonalInfo.Address.AddressClassId": "Otras",
            "PersonalInfo.Address.Address": _primero(self.direccion, "central"),
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
                    self.excel.guardar(self.contador, 'Mensaje', message, destino=self.excel_path)
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
            if not self.safe_wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
            self.pagina = 4
            self.poliedro.tipoDoc('al', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]')
            self.poliedro.tipoDoc('w', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]')
            self.preactivador.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
            self.pagina = 5
            self.preactivador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
            if not self.safe_wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
            optionsFinal = [
                ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p/text()[2]'],
                ['/html/body/div/strong/strong/div[3]/div[1]/div/button[2]'],
            ]
            self.poliedro.detectOption(optionsFinal, NoneFunc=self.errorGeneral)
        else:
            self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de Demographic/Index1", destino=self.excel_path)
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

    def _seleccionar_opcion(self, id, textos):
        """En un <select> clásico escoge la primera opción que contenga alguno de los textos. True si la encontró."""
        try:
            select = Select(self.preactivador.browser.find_element_by_id(id))
            for option in select.options:
                if any(t in _normalizar(option.text) for t in textos):
                    option.click()
                    return True
        except Exception as e:
            print(f"❌ Error en _seleccionar_opcion({id}): {e}")
        return False

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
                    self.excel.guardar(self.contador, 'Mensaje', message, destino=self.excel_path)
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
        self.excel.guardar(self.contador, 'Min', self.min, self.excel_path)
        self.excel.guardar(self.contador, 'Mensaje', self.mensaje, self.excel_path)

    def reinicio(self):
        if self.etapa == 0:
            pass
        if self.etapa == 5:
            time.sleep(self.time2)
            self.preactivador.click('btnPrev', 'id')
            if not self.safe_wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
            self.poliedro.seleccionAcceso('195', start=False)
            if not self.safe_wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
        else:
            for i in range(self.etapa):
                time.sleep(self.time2)
                self.preactivador.click('btnPrev', 'id')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando que la página cargue")
        self.etapa == 0
    
    def position(self, html, paso=None, wait=False):
        """Detecta en qué paso está la UI. Si cae al login, lanza SessionExpiredError.

        Nota: este método se usa para esperar la aparición de elementos.
        """
        if not self.safe_wait_for_loading():
            raise Exception('Timeout esperando que la página cargue')

        intentos = 0
        max_intentos = 30

        while wait and intentos < max_intentos:
            # Si caímos al login, cortar YA para que el caller haga relogin
            try:
                if self._looks_like_login_page(self.preactivador.retornarHtml() if self.preactivador else ''):
                    raise SessionExpiredError('Sesión expirada: detectado login durante position()')
            except SessionExpiredError:
                raise
            except Exception:
                pass

            self.scrap = scraping.Scraping(html)
            soup = self.scrap.soup

            if paso == 'paso1':
                elementos_requeridos = [
                    ('h3', 'iconoTituloCliente'),
                    ('h3', 'iconoTituloInfoVenta'),
                    ('h3', 'iconoTituloEquipo'),
                ]
            elif paso == 'paso2':
                elementos_requeridos = [
                    ('h3', 'iconoTituloValidacionesyRestricciones'),
                    ('h3', 'iconoTituloOtrasValidaciones'),
                ]
            elif paso == 'paso3':
                elementos_requeridos = [('h3', 'iconoTituloInfoPersonal')]
            elif paso == 'paso4':
                elementos_requeridos = [('h3', 'iconoTituloDatosEquipoyPlan')]
            else:
                elementos_requeridos = []

            if elementos_requeridos and self.validate_position(elementos_requeridos, soup):
                return 1

            # Reintentar con HTML fresco
            time.sleep(0.5)
            try:
                html = self.preactivador.retornarHtml()
            except Exception:
                pass
            intentos += 1

        raise Exception('Timeout esperando la posición de los elementos requeridos')



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
    # ---------------------------------------------------------------------
    # Manejo robusto de sesión (auto re-login)
    # ---------------------------------------------------------------------

    def _looks_like_login_page(self, html: str | None = None) -> bool:
        try:
            if self.poliedro_login_service:
                return self.poliedro_login_service._looks_like_login_page(html)
        except Exception:
            pass
        return False

    def verificar_sesion_activa(self) -> bool:
        """Verifica sesión y, si expiró, re-loguea y vuelve al acceso 195."""
        # 1) Si el login service existe y la sesión sigue viva, ok
        try:
            if self.poliedro_login_service and self.poliedro_login_service.validar_sesion_activa():
                return True
        except Exception:
            pass

        # 2) Recuperación: login normal (incluye OTP según tu configuración)
        self.poliedro_login_service = None
        if not self.login():
            return False

        time.sleep(2)
        # Intento de volver al menú y seleccionar el acceso de PREACTIVADOR (195)
        try:
            self.preactivador.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
        except Exception:
            pass

        time.sleep(2)
        try:
            self.poliedro.seleccionAcceso('195', start=True)
        except Exception:
            try:
                self.poliedro.seleccionAcceso('195', start=False)
            except Exception:
                pass

        # Mantener base URL sincronizada para los endpoints Traffic
        try:
            self.sync_traffic_base_from_browser()
        except Exception:
            pass

        try:
            return bool(self.wait_for_loading())
        except SessionExpiredError:
            return False
        except Exception:
            return True

    def safe_wait_for_loading(self, timeout=120, sleep_interval=1, preactivador=True, max_retries=2):
        """wait_for_loading que se recupera automáticamente si detecta sesión expirada."""
        attempts = 0
        while True:
            try:
                return self.wait_for_loading(timeout=timeout, sleep_interval=sleep_interval, preactivador=preactivador)
            except SessionExpiredError as e:
                attempts += 1
                self.ventana_informacion.write(f'🔐 {e}. Reintentando login...')
                if attempts > max_retries:
                    raise
                if not self.verificar_sesion_activa():
                    raise Exception('Error crítico: Fallo en login de Poliedro')
                # refrescar cookies si la sesión se renovó
                try:
                    self.cookie_header['Cookie'] = self.preactivador.getCookies()
                except Exception:
                    pass

    def _run_with_relogin(self, fn, *args, max_retries=2, **kwargs):
        """Ejecuta una acción y si la sesión expiró, re-loguea y reintenta."""
        tries = 0
        while True:
            try:
                return fn(*args, **kwargs)
            except SessionExpiredError as e:
                tries += 1
                self.ventana_informacion.write(f'🔐 {e}. Reintentando login...')
                if tries > max_retries:
                    raise
                if not self.verificar_sesion_activa():
                    raise Exception('Error crítico: Fallo en login de Poliedro')
                try:
                    self.cookie_header['Cookie'] = self.preactivador.getCookies()
                except Exception:
                    pass

    def log_error(self, context: str, error: Exception) -> None:
        """Loggea el error de forma segura sin tumbar el proceso."""
        try:
            self.ventana_informacion.write(f"⚠️ {context}: {str(error)}")
        except Exception:
            try:
                print(f"{context}: {error}")
            except Exception:
                pass

    def login(self):
        """Inicia sesión en Poliedro con el perfil tomado al pulsar START (ver modal_credenciales)."""
        self.poliedro_login_service, ok = poliedro_login_service.iniciar_sesion(
            getattr(self, 'poliedro_login_service', None), self.preactivador, self.ventana_informacion,
            self.perfil, 'PRE-SIM')
        return ok
    
    def inicializar_login_service(self):
        """Crea el servicio de login si no existe (lo usan las verificaciones de sesión)."""
        if not getattr(self, 'poliedro_login_service', None):
            self.poliedro_login_service = poliedro_login_service.preparar_login(
                None, self.preactivador, self.ventana_informacion, self.perfil, 'PRE-SIM')
            
    def wait_for_loading(self, timeout=120, sleep_interval=1, preactivador=True):
        """Espera a que termine el loading.

        Si detecta sesión expirada real, lanza SessionExpiredError.
        Usa una sola fuente de verdad para la sesión:
        - LoginService.validar_sesion_activa() si existe
        - _looks_like_login_page() solo como fallback
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            # 1) Verificar sesión UNA sola vez por iteración
            try:
                service = getattr(self, 'poliedro_login_service', None)
                if service and not service.validar_sesion_activa():
                    raise SessionExpiredError('Sesión expirada')
            except SessionExpiredError:
                raise
            except Exception:
                # Si falla la validación, no forces relogin todavía
                pass

            # 2) Revisar loading
            try:
                if preactivador and self.preactivador:
                    try:
                        loading_style = self.preactivador.style('loading', 'id')
                    except Exception:
                        loading_style = self.poliedro.style('loading', 'id')
                else:
                    loading_style = self.poliedro.style('loading', 'id')

                loading_style = str(loading_style)

                if 'display: none' in loading_style:
                    return True

                if 'display: block' in loading_style:
                    time.sleep(sleep_interval)
                    continue

                # Si el estado no es reconocible, no bloqueamos
                return True

            except SessionExpiredError:
                raise
            except Exception:
                return True

        return False # Timeout
