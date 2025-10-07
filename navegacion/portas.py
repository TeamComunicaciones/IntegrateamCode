from navegacion import sub_menu as sm, ventana_informacion 
from funcionalidad import  web_controller, poliedro, excel, clickImage
from recursos import botones, label, checkbox, colors, spinbox
import threading
from subprocess import Popen
import pyperclip
from datetime import datetime, timedelta
import time
import tkinter as tk
import customtkinter as ctk
import requests
from funcionalidad import poliedro_login_service
import random
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class Portas:
 
    def __init__(self, master, on_of, alertas):
        self.pagina = ''
        self.alertas = alertas
        self.on_of = on_of
        self.errorCorreo=False
        self.master = master
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.link_google_messages = 'https://messages.google.com/web/conversations'
        self.link_mysms = 'https://app.mysms.com/#87472'

        self.label = label.Label().create_label(master, 'PORTABILIDADES', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.submenu= sm.Sub_menu(master, 3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.time = tk.StringVar()
        self.time.set('1.5')
        self.master = master
        boton = botones.Buttons()
        self.cookie_header = {}
        color = colors.Colors()
        self.checkbox = checkbox.Checkbox()
        self.checkbox2 = checkbox.Checkbox()
        self.checkbox_var = tk.BooleanVar()
        self.tropas = tk.BooleanVar()
        self.validacionImgs = tk.BooleanVar()
        # self.checkbox_validacionImgs =  checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Configurar Imagenes.', self.on_checkbox_change_configuracion, self.validacionImgs)
        self.checkbox_festivo = checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Lunes Festivo.', self.on_checkbox_change, self.checkbox_var)
        self.checkbox_tropas =  checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Tropas.', self.on_checkbox_change_tropas, self.tropas)
        self.repeticiones = '1'
        self.repeticionesEdit = tk.StringVar()
        self.repeticionesEdit.set(self.repeticiones)
        self.titulo = label.Label().create_label(self.submenu.submenu, 'Ciclos', 0.0, 0.70, 0.5,0.05, letterSize= 16)
        input_widget3 = ctk.CTkEntry(self.submenu.submenu, textvariable=self.repeticionesEdit)
        input_widget3.place(relx=0.45, rely=0.70, relheight=0.05, relwidth=0.2)
        self.okBotton3 = boton.create_button(self.submenu.submenu, 'OK', 0.65, 0.70, 0.15, 0.05, self.cambioCiclos)
        self.okBotton3.configure(fg_color= color.team, text_color= 'white')

        # Configuracion para tiempo de espera
        self.tiempo_espera_label = label.Label().create_label(self.submenu.submenu, 'Tiempo de espera', 0.10, 0.36, 0.6, 0.04, letterSize=16)

        self.spinbox_tiempo_espera = spinbox.CTkSpinbox(self.submenu.submenu, from_=5, to=60, default=5)
        self.spinbox_tiempo_espera.place(relx=0.10, rely=0.40, relheight=0.06, relwidth=0.55)

        # Si el usuario no presiona OK, toma el valor por defecto
        self.valor = self.spinbox_tiempo_espera.get_value()

        self.tiempo_espera_okbutton = boton.create_button(self.submenu.submenu, 'OK', 0.66, 0.40, 0.15, 0.05, self.guardar_tiempo_espera)
        self.tiempo_espera_okbutton.configure(fg_color=color.team, text_color='white')

        # Configuraciones para campo de usuario y contrasena poliedro
        # Etiquetas
        self.titulo3 = label.Label().create_label(self.submenu.submenu, 'Poliedro User', 0.10, 0.49, 0.5, 0.04, letterSize=16)
        self.titulo4 = label.Label().create_label(self.submenu.submenu, 'Poliedro Pass', 0.10, 0.59, 0.5, 0.04, letterSize=16)

        # Variables
        self.poliedro_user = ''
        self.poliedro_pass = ''
        self.poliedro_user_edit = tk.StringVar()
        self.poliedro_user_edit.set(self.poliedro_user)
        self.poliedro_pass_edit = tk.StringVar()
        self.poliedro_pass_edit.set(self.poliedro_pass)

        # Entradas (más angostas, alineadas a la izquierda)
        input_widget4 = ctk.CTkEntry(self.submenu.submenu, textvariable=self.poliedro_user_edit)
        input_widget4.place(relx=0.10, rely=0.53, relheight=0.05, relwidth=0.55)

        input_widget5 = ctk.CTkEntry(self.submenu.submenu, textvariable=self.poliedro_pass_edit)
        input_widget5.place(relx=0.10, rely=0.63, relheight=0.05, relwidth=0.55)

        # Botones OK a la derecha de cada entrada
        self.okBotton4 = boton.create_button(self.submenu.submenu, 'OK', 0.66, 0.53, 0.15, 0.05, self.cambioPoliedroUser)
        self.okBotton4.configure(fg_color=color.team, text_color='white')

        self.okBotton5 = boton.create_button(self.submenu.submenu, 'OK', 0.66, 0.63, 0.15, 0.05, self.cambioPoliedroPass)
        self.okBotton5.configure(fg_color=color.team, text_color='white')

        # Elegir si se usa MySMS o Google Messages para obtener el OTP
        self.checkbox_mysms = checkbox.Checkbox()
        self.mysms = tk.BooleanVar()
        self.checkbox_mysms = checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'MySMS', self.on_checkbox_change_mysms, self.mysms)

        self.checkbox_google_messages = checkbox.Checkbox()
        self.google_messages = tk.BooleanVar()
        self.checkbox_google_messages = checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Google Messages', self.on_checkbox_change_google_messages, self.google_messages)

        self.checkbox_modo_captura_datos = checkbox.Checkbox()
        self.modo_captura_datos = tk.BooleanVar()
        self.checkbox_modo_captura_datos = checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Envio de datos por API', self.on_checkbox_change_modo_captura, self.modo_captura_datos)

    def guardar_tiempo_espera(self):
        self.valor = self.spinbox_tiempo_espera.get_value()
        self.ventana_informacion.write(f'Tiempo de espera configurado: {self.valor} segundos')

    def on_checkbox_change_modo_captura(self):
        if self.modo_captura_datos.get():
            self.ventana_informacion.write('Envio de datos por API (No visible en navegador)')
        else:
            self.ventana_informacion.write('Envio de datos por Web (Visible en navegador)') 
        
    def on_checkbox_change(self):
        if self.checkbox_var.get():
            self.ventana_informacion.write('Lunes Festivo activado, se reagendara a martes de ser necesario')
        else:
            self.ventana_informacion.write('Lunes Festivo desactivado')

    def on_checkbox_change_tropas(self):
        if self.tropas.get():
            self.ventana_informacion.write('Cambiando modalidad a Tropas')
        else:
            self.ventana_informacion.write('Cambiando modalidad a Estandar')
        self.poliedro.manejoTropas(self.tropas.get())
    
    def cambioCiclos(self):
        self.repeticiones = self.repeticionesEdit.get()
        self.ventana_informacion.write(f'Numero de repeticiones configurado en {self.repeticiones}')

    
    def abrir_excel(self):
        self.ventana_informacion.write('excel portabilidad abierto recuerde cerrar antes de iniciar')
        p = Popen("src\portas\openExcel.bat")
        stdout, stderr = p.communicate()

    def cambioIntervalo(self):
        min = 1.5
        if float(self.time.get()) < min:
            self.time.set(str(min))
            self.ventana_informacion.write(f'intervalo no puede ser menor a {min} segundos')
        self.portas.actualizarIntervalo(self.time.get())
        self.ventana_informacion.write(f'intervalo {self.time.get()} segundos')
    
    def abrir_pagina(self):
        if not self.mysms.get() and not self.google_messages.get():
            self.ventana_informacion.write('Seleccione un método para recibir el OTP')
            return

        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.portas = Abrir_pagina1(float(self.time.get()))
        self.portas.openEdge()
        self.portas.selectPage(self.link)
        self.titulo = label.Label().create_label(self.submenu.submenu, 'Intervalos', 0.0, 0.69, 0.5,0.05, letterSize= 16)
        input_widget = ctk.CTkEntry(self.submenu.submenu, textvariable=self.time)
        input_widget.place(relx=0.5, rely=0.69, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.submenu.submenu, 'OK', 0.7, 0.69, 0.15, 0.05, self.cambioIntervalo)
        self.okBotton.configure(fg_color= color.team, text_color= 'white')

        time.sleep(2)
        if self.mysms.get():
            self.portas.script(f"window.open('{self.link_mysms}', '_blank');")
        elif self.google_messages.get():
            self.portas.script(f"window.open('{self.link_google_messages}', '_blank');")

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
        hilo_portas = threading.Thread(target=self.ejecuccion)
        hilo_portas.start()
    
    def ejecuccion(self):
        try:
            self.on_of(False)
            self.ventana_informacion.write('Empezando ejecuccion')

            self.poliedro.definirBrowser(self.portas)
            
            # Inicializar el servicio de login
            self.poliedro_login_service = None
            if not self.login():
                self.ventana_informacion.write('❌ Error en login, verifique sus credenciales')
                self.on_of(True)
            time.sleep(2)

            if not self.tropas.get():
                try:
                    self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
                except:
                    pass

            # self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
            self.poliedro.seleccionAcceso('290')
            if not self.wait_for_loading():
                raise Exception("Timeout esperando que la página cargue")
            self.excel.leer_excel('src\\portas\\portabilidad.xlsx', 'CC CLIENTE')
            self.excel.quitarFormatoCientifico('SERIAL')

            for i in range(int(self.repeticiones)):
                self.ciclo = True
                self.contador = 0
                self.iteraciones()

            self.ventana_informacion.write('Proceso terminado')
            self.on_of(True)
            
        except Exception as e:
            if "Error crítico: Fallo en login de Poliedro" in str(e):
                self.ventana_informacion.write(f'se detiene el programa error en login: {e}')
                self.alertas('se detiene el programa error en login')
            else: 
                self.ventana_informacion.write(f'se detiene el programa error: {e}')
                self.alertas('se detiene el programa error')
            
            raise Exception('se detiene el programa')

    def iteraciones(self):

        while self.ciclo:
            if self.contador == self.excel.cantidad:
                self.ciclo = False
            else:
                try:
                    self.ventana_informacion.write(f'Portando numero {self.contador+1} de {self.excel.cantidad}')
                    self.crearVariablesExcel(self.contador)
                    if str(self.msisdn) != 'nan':
                        self.ventana_informacion.write(f'Portabilidad ya realizada o con error ya detectado')
                        self.contador += 1
                        continue
                    else:
                        self.start_time = time.time()
                        self.rellenoPrimerFormulario()
                    # self.copiarMin(i)
                    # elapsed_time = time.time() - start_time
                    # self.excel.guardar(i,'MENSAJE',str(round(elapsed_time,2)), destino='src\portas\portabilidad.xlsx')
                    # self.reinicio()
                except:
                    self.ventana_informacion.write(f'Siguiente por error en portabilidad de {self.min}')
                    self.excel.guardar(self.contador, 'MENSAJE', 'error', destino='src\portas\portabilidad.xlsx')
                    self.reinicio()
                    self.contador += 1
                
                # PAUSA ALEATORIA ENTRE TRANSACCIONES PARA EVITAR DETECCIÓN DE BOT
                base = self.valor
                variacion = random.randint(1,3)
                tiempo_pausa = random.randint(base - variacion, base + variacion)
                self.ventana_informacion.write(f"⏳ Pausa anti-bot: {tiempo_pausa}s entre transacciones...")
                time.sleep(tiempo_pausa)

    def crearVariablesExcel(self,i):
        self.idCliente = str(self.excel.excel['CC CLIENTE'][i])
        self.fechaExpedicion = str(self.excel.excel['FECHA EXPEDICION'][i])
        self.apellido = str(self.excel.excel['APELLIDO CLIENTE'][i])
        self.nombre = str(self.excel.excel['NOMBRE CLIENTE'][i])
        self.idVendedor = str(self.excel.excel['CEDULA VENDEDOR'][i])
        self.min = str(self.excel.excel['NUMERO MOVIL'][i])
        self.iccid = str(self.excel.excel['SERIAL'][i])[-12:]
        self.iccid2 = str(self.excel.excel['SERIAL2'][i])[-12:]
        self.nip = str(self.excel.excel['NIP'][i])
        tamañoNip = len(self.nip)
        while (tamañoNip<5):
            self.nip = '0' + str(self.nip)
            tamañoNip += 1
        self.nombre = str(self.excel.excel['NOMBRE CLIENTE'][i])
        self.correo = str(self.excel.excel['CORREO'][i])
        self.tipoLinea = str(self.excel.excel['TIPO DE LINEA'][i])
        self.tipo = 'cedula'
        self.msisdn = str(self.excel.excel['MSISDN'][i])

    def rellenoPrimerFormulario(self):
        self.pagina = 1
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga inicial en captura_datos")
        if len(self.idCliente) == 9:
            self.captarError('','No se admite cedula de 9 digitos')
        else:
            self.portas.eraseLetter('//*[@id="DetailProduct_Iccid"]', 20)
            self.portas.insert('//*[@id="DetailProduct_Iccid"]', self.iccid, enter=True)
            if str(self.iccid2) != 'nan':
                try:
                    self.portas.insert('//*[@id="DetailProduct_MinBroughtPortability"]', self.iccid2)
                    minpre = False
                except: minpre = False
            else:
                try:
                    self.portas.waitExist('//*[@id="DetailProduct_MinBroughtPortability"]', write=True)
                    minpre = True
                except: minpre = False
            if minpre: 
                self.captarError('','Se necesita Min preactivado')
                # raise('Se necesita Min preactivado')
            else:
                self.poliedro.tipoDoc(self.tipo, '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[1]/div/span/span[1]/span/span[1]')
                primerFormulario = [
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[2]/div/input', self.idCliente],
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[2]/div[3]/div/input', self.apellido],
                    ['//*[@id="DetailProduct_SellerId"]', self.idVendedor],
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[3]/div/div[1]/div[2]/input', self.min],
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[3]/div/div[1]/div[3]/div/input', self.nip],
                ]
                print('listos formularios')
                self.poliedro.rellenoFormulario(5, primerFormulario)
                fecha = self.portas.value('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[3]/div/div[1]/div[4]/div/input')
                fecha = datetime.strptime(fecha, '%d/%m/%Y')
                if 5 <= fecha.weekday() <= 7:
                    print("La fecha cae entre sabado y domingo.")
                    if self.checkbox_var.get():
                        festivo = 1
                    else:
                        festivo = 0
                    dias_hasta_lunes = (0 + festivo - fecha.weekday()) % 7
                    proximo_lunes = fecha + timedelta(days=dias_hasta_lunes)
                    newfecha = proximo_lunes.strftime('%d/%m/%Y')
                    print(newfecha)
                    self.portas.eraseLetter('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[3]/div/div[1]/div[4]/div/input', 10)
                    self.portas.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[3]/div/div[1]/div[4]/div/input', newfecha)
                if self.checkbox_var.get() and fecha.weekday() ==0:
                    print("La fecha cae lunes festivo")
                    if self.checkbox_var.get():
                        festivo = 1
                    else:
                        festivo = 0
                    dias_hasta_lunes = (0 + festivo - fecha.weekday()) % 7
                    proximo_lunes = fecha + timedelta(days=dias_hasta_lunes)
                    newfecha = proximo_lunes.strftime('%d/%m/%Y')
                    print(newfecha)
                    self.portas.eraseLetter('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[3]/div/div[1]/div[4]/div/input', 10)
                    self.portas.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[3]/div/div[1]/div[4]/div/input', newfecha)

                else:
                    print("La fecha no cae entre sabado y domingo.")
                if str(self.fechaExpedicion) != 'nan':
                    try:
                        self.portas.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[3]/div[1]/div/input', self.fechaExpedicion)
                    except:
                        pass
                # Check de tratamiento de datos
                #self.portas.click('DetailProduct_PortaTrataDatosCheck', 'id')
                time.sleep(0.5)
                # Check de número de portabilidad
                self.portas.click('//*[@id="div_PortabilityNumber"]/div[1]/input', 'xpath')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[5]/input[1]')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
                try: self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[5]/input[1]')
                except: pass
                self.pagina = 2
                options = [
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span'],
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[4]/ul/li'],
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div'],
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[1]/div/div[2]/div[2]/div'],
                ]
                functionList = [
                    self.validado,
                    self.errorDuplaIccid,
                    self.errorKitRegistrado,
                    self.lecturaIccidResponse,
                ]
                self.poliedro.detectOption(options, functionList, NoneFunc=self.errorGeneral)
    
    def lecturaIccidResponse(self):
        self.captarError('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[1]/div/div[2]/div[2]/div')
    
    def errorDuplaIccid(self):
        self.captarError('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[4]/ul/li')
    
    def errorKitRegistrado(self):
        mensaje = self.portas.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[2]/div/div/div')
        if 'linea no se' in mensaje:
            self.captarError('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
        elif mensaje == '':
            self.captarError('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/div[2]/div[5]/div/div[2]/div[1]/div')
        else:
            self.captarError('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[2]/div/div/div')
    
    def validado(self):
            
            self.portas.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/Validation')
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga inicial en captura_datos")
            try:
                self.portas.click('btnNext', 'id')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
            except:
                try:
                    message = self.portas.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
                    if message == 'Porta ya registrada':
                        self.excel.guardar(self.contador, 'Mensaje', message)
                        self.portas.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/')
                        if not self.wait_for_loading():
                            raise Exception("Timeout esperando carga inicial en captura_datos")
                        self.poliedro.seleccionAcceso('290', start=False)
                        if not self.wait_for_loading():
                            raise Exception("Timeout esperando carga inicial en captura_datos")
                        self.ventana_informacion.write(f"{self.idCliente} Porta ya registrada'")
                except:
                    self.portas.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/')
                    if not self.wait_for_loading():
                        raise Exception("Timeout esperando carga inicial en captura_datos")
                    self.poliedro.seleccionAcceso('290', start=False)
                    if not self.wait_for_loading():
                        raise Exception("Timeout esperando carga inicial en captura_datos")
                    self.ventana_informacion.write(f"{self.idCliente} error no identificado")
                raise('error controlado kit registrado')

            if self.modo_captura_datos.get():
                self.validado_api()
            else:
                self.validado_web()
                
            self.pagina = 4
            self.poliedro.tipoDoc('al', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]')
            self.poliedro.tipoDoc('w', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
            self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]')
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga inicial en captura_datos")
            self.portas.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
            self.pagina = 5
            self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
            if not self.wait_for_loading():
                raise Exception("Timeout esperando carga inicial en captura_datos")
            optionsFinal = [
                ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p/text()[2]'],
                ['/html/body/div/strong/strong/div[3]/div[1]/div/button[2]'],
            ]
            functionListFinal = [
                self.errorTamañoDireccion,
                self.terminarPorta,
            ]
            self.poliedro.detectOption(optionsFinal, functionListFinal, NoneFunc=self.errorGeneral)
    
    def validado_web(self):
        """Versión Web de la captura de datos (visible en UI)"""
        #Saludo
        self.poliedro.tipoDoc('Sr', '//*[@id="select2-PersonalInfo_GreetingId-container"]')
 
        #Nombre
        nombre_actual = self.portas.value("PersonalInfo_Name",'id')
        if not nombre_actual.strip():    
            self.portas.write("PersonalInfo_Name", self.nombre, 'id')
        
        #Apellido
        apellido_actual = self.portas.value("PersonalInfo_LastName",'id')
        if not apellido_actual.strip():
            self.portas.write("PersonalInfo_LastName", self.apellido, 'id')

        correo_actual = self.portas.value("PersonalInfo_Email","id")
        if not correo_actual or not correo_actual.strip():
            self.portas.write("PersonalInfo_Email", self.correo, 'id')

        #Telefono
        telefono_actual = self.portas.value("PhoneId","id")
        if not telefono_actual or not telefono_actual.strip():
            
            #Tipo
            self.selectDropDown("PhoneClass","fijo")

            time.sleep(2)
            if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")

            #Indicativo
            self.selectDropDown("Prefix","7")

            #Numero
            self.portas.write("PhoneNumber","8883136","id")
        
        #Tipo documento
        self.poliedro.tipoDoc('Cedula', '//*[@id="select2-PersonalInfo_DocumentTypeId-container"]')
 
        #Cedula
        id_actual = self.portas.value("PersonalInfo_Document",'id')
        if not id_actual.strip() or id_actual.strip() == "0":
            campo = self.portas.browser.find_element_by_id("PersonalInfo_Document")
            campo.clear()
            self.portas.write("PersonalInfo_Document", self.idCliente, 'id')

        #Dirección
        direccion_actual = self.portas.value("AddressId","id")
        if not direccion_actual or not direccion_actual.strip():
            self.selectDropDown("AddressClassId","Otras")
            time.sleep(2)
            if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga después de validación")
            
            self.portas.write("Address", "central", "id")
            self.selectDropDown("Department","ANTIOQUIA")
            time.sleep(1)
            self.selectDropDown("City","MEDELLIN")
            self.portas.write("Town", "Central", "id")

        #Pospago o prepago
        checkboxes = self.portas.browser.find_elements_by_xpath('//*[@id="PersonalInfo_ProductDonorOperator"]')
        if self.tipoLinea.lower() == "pospago":
            checkboxes[0].click()
        elif self.tipoLinea.lower() == "prepago":
            checkboxes[1].click()
        
        time.sleep(2)
        if not self.wait_for_loading():
                raise Exception("Timeout esperando carga después de validación")

        self.portas.click("btnNext", "id")

        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga después de hacer clic en Siguiente")

    
    def validado_api(self):
        demographic_url = "https://traffic-md-webapp-prd01.traffic.claro.com.co/Demographic/Index1"
        demographic_data = {               
            "PersonalInfo.GreetingId": "M",
            "PersonalInfo.Name": self.nombre,
            "PersonalInfo.LastName": self.apellido,
            "PersonalInfo.Email": "master.33@gmail.com",
            "PersonalInfo.Phone.PhoneId": "526553",
            "PersonalInfo.Phone.PhoneClass": "",
            "PersonalInfo.Phone.Prefix": "7",
            "PersonalInfo.Phone.PhoneNumber": "8883136",
            "PersonalInfo.EmailInitial": "master.33@gmail.com",
            "PersonalInfo.DocumentTypeId": "1",
            "PersonalInfo.Document": self.idCliente,
            "PersonalInfo.Address.AddressId": "",
            "PersonalInfo.Address.AddressClassId": "Otras",
            "PersonalInfo.Address.Address": "central",
            "PersonalInfo.Address.Department": "ANTIOQUIA",
            "PersonalInfo.Address.City": "MEDELLIN",
            "PersonalInfo.Address.Town": "Central",
            "PersonalInfo.ProductDonorOperator": self.tipoLinea
        }

        self.cookie_header['Cookie'] = self.portas.getCookies()
        cookies = self.portas.browser.get_cookies()
        session = requests.Session()
        for cookie in cookies:
            session.cookies.set(cookie['name'], cookie['value'])
            
        headers = {'Cookie': self.cookie_header['Cookie']}

        demographic_response = session.post(demographic_url, data=demographic_data, headers = headers)

        if demographic_response.status_code != 200:
            self.excel.guardar(self.contador, 'Mensaje', "Error en la URL de Demographic/Index1",destino="src\portas\portabilidad.xlsx")
            raise Exception("Error en la URL de Demographic/Index1")
        
        self.portas.selectPage('https://traffic-md-webapp-prd01.traffic.claro.com.co/ProductService')
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga inicial en captura_datos")
        
    def selectDropDown(self, id, value):
        """
        Selecciona un valor de un dropdown. Funciona tanto para Select2 como para <select> normales.
        """
        try:
            el = self.portas.browser.find_element_by_id(id)
            classes = el.get_attribute("class") or ""

            # 🟢 Caso 1: Select2
            if "select2-hidden-accessible" in classes:
                self.portas.click(f"select2-{id}-container", "id")
                self.portas.write("/html/body/span/span/span[1]/input", value, "xpath")
                self.portas.write("/html/body/span/span/span[1]/input", Keys.ENTER, "xpath")

            # 🟢 Caso 2: <select> HTML normal
            else:
                select = Select(el)
                # intenta primero por texto visible (insensible a mayúsculas)
                matched = False
                for option in select.options:
                    if option.text.strip().lower() == value.strip().lower():
                        option.click()
                        matched = True
                        break
                if not matched:
                    select.select_by_value(value)
        except Exception as e:
            self.log_error(f"selectDropDown({id})", e)
        

    def tryInsert(self, path, text):
        try: self.portas.insert(path, text) 
        except: pass
    
    def errorGeneral(self):
        raise('error general')
    
    def terminarPorta(self):
        self.pagina = 6
        time.sleep(4)
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga inicial en captura_datos")
        self.portas.click('/html/body/div/strong/strong/div[3]/div[1]/div/button[2]')
        time.sleep(1)
        if not self.wait_for_loading():
            raise Exception("Timeout esperando carga inicial en captura_datos")
        self.msisdn = self.portas.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/div/fieldset[3]/div/div/strong')
        print(self.msisdn)
        self.excel.guardar(self.contador,'MSISDN',self.msisdn, destino='src\portas\portabilidad.xlsx')
        elapsed_time = time.time() - self.start_time
        self.excel.guardar(self.contador,'MENSAJE',str(round(elapsed_time,2)), destino='src\portas\portabilidad.xlsx')
        self.reinicio()
        self.contador += 1

    def errorTamañoDireccion(self):
        self.captarError('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p/text()[2]')
    
    def captarError(self, path, mensaje=None):
        if mensaje == None:
            validado = self.portas.read(path)
        else:
            validado = mensaje
        self.ventana_informacion.write(f'{self.min} {validado}')
        self.excel.guardar(self.contador, 'MENSAJE', validado, destino='src\portas\portabilidad.xlsx')
        self.excel.guardar(self.contador,'MSISDN','error', destino='src\portas\portabilidad.xlsx')
        self.reinicio()
        self.contador += 1
    
    def reinicio(self):
        try:
            if self.pagina == 6:
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[1]')
                time.sleep(2)
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[1]/div[1]/div[1]/div/div/ul/li[1]/span/input')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
            if self.pagina == 5:
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[1]')
                time.sleep(2)
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]')
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                self.poliedro.seleccionAcceso('290')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
            if self.pagina == 4:
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[1]')
                time.sleep(2)
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]')
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                self.poliedro.seleccionAcceso('290')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
            if self.pagina == 3:
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[1]')
                time.sleep(2)
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]')
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                self.poliedro.seleccionAcceso('290')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
            if self.pagina == 2:
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]')
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                self.poliedro.seleccionAcceso('290')
                if not self.wait_for_loading():
                    raise Exception("Timeout esperando carga inicial en captura_datos")
        except:
            try:
                self.poliedro.reinicio()
            except:
                try:
                    texto_pantalla = self.portas.read('titlesHeaderMainContent', 'id')
                    if 'Si va a dejar de utilizar el Módulo' not in texto_pantalla:
                        raise Exception('Error al reiniciar, no se pudo leer el texto de la pantalla')
                except:
                    self.poliedro_login_service = None
                    if not self.login():
                        self.ventana_informacion.write('❌ Error en login, verifique sus credenciales')
                        self.on_of(True)
                        raise Exception("Error crítico: Fallo en login de Poliedro")
                    
                    time.sleep(2)
                    try:
                        try:
                            if not self.tropas.get():
                                self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[last()]/a')
                        except:
                            pass
                        time.sleep(1)
                        self.portas.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[13]/a')
                        time.sleep(1)
                        self.poliedro.seleccionAcceso('290')
                    except Exception as e:
                        return

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
        if self.portas and not self.poliedro_login_service:
            self.poliedro_login_service = poliedro_login_service.LoginService(
                self.portas, 
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
    
    def wait_for_loading(self, timeout=120, sleep_interval=1, portas=True):
        """
        Método reutilizable para esperar que termine la carga.
        
        Args:
            timeout (int): Tiempo máximo de espera en segundos
            sleep_interval (float): Intervalo entre verificaciones
            portas (bool): True para usar self.portas, False para self.poliedro

        Returns:
            bool: True si terminó la carga, False si hubo timeout
        """
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                if portas:
                    try:
                        loading_style = self.portas.style('loading', 'id')
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