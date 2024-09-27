from navegacion import sub_menu as sm, ventana_informacion 
from funcionalidad import  web_controller, poliedro, excel, clickImage
from recursos import botones, label, checkbox, colors
import threading
from subprocess import Popen
import pyperclip
from datetime import datetime, timedelta
import time
import tkinter as tk
import customtkinter as ctk


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
        self.label = label.Label().create_label(master, 'PORTABILIDADES', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.submenu= sm.Sub_menu(master, 3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.time = tk.StringVar()
        self.time.set('1.5')
        self.master = master
        boton = botones.Buttons()
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
        self.titulo = label.Label().create_label(self.submenu.submenu, 'Ciclos', 0.0, 0.78, 0.5,0.05, letterSize= 16)
        input_widget3 = ctk.CTkEntry(self.submenu.submenu, textvariable=self.repeticionesEdit)
        input_widget3.place(relx=0.5, rely=0.79, relheight=0.05, relwidth=0.2)
        self.okBotton3 = boton.create_button(self.submenu.submenu, 'OK', 0.7, 0.79, 0.15, 0.05, self.cambioCiclos)
        self.okBotton3.configure(fg_color= color.team, text_color= 'white')
        
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
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.portas = Abrir_pagina1(float(self.time.get()))
        self.portas.openEdge()
        self.portas.selectPage(self.link)
        self.titulo = label.Label().create_label(self.submenu.submenu, 'Intervalos', 0.0, 0.65, 0.5,0.2, letterSize= 16)
        input_widget = ctk.CTkEntry(self.submenu.submenu, textvariable=self.time)
        input_widget.place(relx=0.5, rely=0.73, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.submenu.submenu, 'OK', 0.7, 0.73, 0.15, 0.05, self.cambioIntervalo)
        self.okBotton.configure(fg_color= color.team, text_color= 'white')
    
    def ejecuccionHilo(self):
        hilo_portas = threading.Thread(target=self.ejecuccion)
        hilo_portas.start()
    
    def ejecuccion(self):
        try:
            self.on_of(False)
            self.ventana_informacion.write('Empezando ejecuccion')
            self.poliedro.definirBrowser(self.portas)
            self.poliedro.seleccionAcceso('290')
            self.excel.leer_excel('src\portas\portabilidad.xlsx','CC CLIENTE')
            self.excel.quitarFormatoCientifico('SERIAL')
            for i in range(int(self.repeticiones)):
                self.ciclo = True
                self.contador = 0
                self.iteraciones()
            self.ventana_informacion.write('Proceso terminado')
            self.on_of(True)
        except Exception as e:
            self.ventana_informacion.write(f'se detiene el programa error: {e}')
            
            self.alertas('se detiene el programa error')
            raise('se detiene el programa')
        


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

    def crearVariablesExcel(self,i):
        self.idCliente = str(self.excel.excel['CC CLIENTE'][i])
        self.fechaExpedicion = str(self.excel.excel['FECHA EXPEDICION'][i])
        self.apellido = str(self.excel.excel['APELLIDO CLIENTE'][i])
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
        if len(self.idCliente) == 9:
            self.captarError('','No se admite cedula de 9 digitos')
        else:
            self.portas.eraseLetter('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[4]/div[3]/div/input', 20)
            self.portas.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[4]/div[3]/div/input', self.iccid, enter=True)
            if str(self.iccid2) != 'nan':
                try:
                    self.portas.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[4]/div[4]/div/input', self.iccid2)
                    minpre = False
                except: minpre = False
            else:
                try:
                    self.portas.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[4]/div[4]/div/input', write=True)
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
                    ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[2]/div/div[1]/div/input', self.idVendedor],
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
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[5]/input[1]')
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
        validado = self.portas.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span')
        if 'Validación Correcta' in validado: pass
        else: raise('invalido')
        time.sleep(0.5)
        self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[3]')
        self.pagina = 3
        self.poliedro.tipoDoc('sr', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[1]/div/span/span[1]/span/span[1]')
        self.tryInsert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[2]/div/input', self.nombre)
        self.tryInsert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[3]/div/input', self.apellido)
        correo= self.portas.value('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[4]/div/input')
        if correo == '':
            self.tryInsert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[4]/div/input', self.correo)
        try: self.poliedro.tipoDoc('cedula', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[1]/div/span/span[1]/span/span[1]')
        except: pass
        try: self.poliedro.rellenoNumero2()
        except:pass
        try: self.poliedro.rellenoDireccion2()
        except:pass
        try: self.portas.eraseLetter('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[2]/div/input', 1, move=True)
        except: pass
        self.tryInsert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[2]/div/input', self.idCliente)
        if self.tipoLinea.lower() == 'prepago':
            self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[2]/div[1]/div/div/div[2]/span/span/input')
        else:
            self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[2]/div[1]/div/div/div[1]/span/span/input')
        self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[2]')
        self.portas.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]')
        self.pagina = 4
        self.poliedro.tipoDoc('al', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[2]/div/span/span[1]/span/span[1]')
        self.poliedro.tipoDoc('w', '/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div/div[1]/div[3]/div/span/span[1]/span/span[1]')
        self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[2]')
        self.portas.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
        self.pagina = 5
        self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
        optionsFinal = [
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p/text()[2]'],
            ['/html/body/div/strong/strong/div[3]/div[1]/div/button[2]'],
        ]
        functionListFinal = [
            self.errorTamañoDireccion,
            self.terminarPorta,
        ]
        self.poliedro.detectOption(optionsFinal, functionListFinal, NoneFunc=self.errorGeneral)
    
    def tryInsert(self, path, text):
        try: self.portas.insert(path, text) 
        except: pass
    
    def errorGeneral(self):
        raise('error general')
    
    def terminarPorta(self):
        self.pagina = 6
        self.portas.click('/html/body/div/strong/strong/div[3]/div[1]/div/button[2]')
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
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[1]/div[1]/div[1]/div/div/ul/li[1]/span/input')
            if self.pagina == 5:
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
            if self.pagina == 4:
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[3]/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
            if self.pagina == 3:
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[1]')
                time.sleep(2)
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
            if self.pagina == 2:
                self.portas.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
        except:
            self.poliedro.reinicio()