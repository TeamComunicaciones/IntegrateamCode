from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors
from funcionalidad import  web_controller, poliedro, excel
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time

class Legalizador:

    def __init__(self,master, on_of):
        self.etapa = 0
        self.on_of = on_of
        self.poliedro = poliedro.Poliedro(legalizador=True)
        self.excel = excel.Excel_controller()
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.titulo = label.Label().create_label(master, 'LEGALIZADOR', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.legalizador = ''
        self.time = tk.StringVar()
        self.time2 = 3
        self.time.set('0')
        self.titulo = label.Label().create_label(self.menu.submenu, 'Intervalos', 0.0, 0.65, 0.5,0.2, letterSize= 16)
        self.titulo = label.Label().create_label(self.menu.submenu, 'Ciclos', 0.0, 0.78, 0.5,0.05, letterSize= 16)
        self.titulo2 = label.Label().create_label(self.menu.submenu, 'Correo', 0.25, 0.83, 0.5,0.05, letterSize= 16)
        input_widget = ctk.CTkEntry(self.menu.submenu, textvariable=self.time)
        input_widget.place(relx=0.5, rely=0.73, relheight=0.05, relwidth=0.2)
        boton = botones.Buttons()
        color = colors.Colors()
        self.okBotton = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.73, 0.15, 0.05, self.cambioIntervalo)
        self.okBotton.configure(fg_color= color.team, text_color= 'white')
        self.correo = 'acruz@teamcomunicaciones.com'
        self.correoEdit = tk.StringVar()
        self.correoEdit.set(self.correo) 
        self.repeticiones = '1'
        self.repeticionesEdit = tk.StringVar()
        self.repeticionesEdit.set(self.repeticiones) 
        input_widget2 = ctk.CTkEntry(self.menu.submenu, textvariable=self.correoEdit)
        input_widget2.place(relx=0.15, rely=0.89, relheight=0.05, relwidth=0.7)
        input_widget3 = ctk.CTkEntry(self.menu.submenu, textvariable=self.repeticionesEdit)
        input_widget3.place(relx=0.5, rely=0.79, relheight=0.05, relwidth=0.2)
        self.okBotton2 = boton.create_button(self.menu.submenu, 'confirmar', 0.3, 0.95, 0.40, 0.05, self.cambioCorreo)
        self.okBotton2.configure(fg_color= color.team, text_color= 'white')
        self.okBotton3 = boton.create_button(self.menu.submenu, 'OK', 0.7, 0.79, 0.15, 0.05, self.cambioCiclos)
        self.okBotton3.configure(fg_color= color.team, text_color= 'white')
        
    
    def abrir_excel(self):
        self.ventana_informacion.write('excel legalizador abierto recuerde cerrar antes de iniciar')
        p = Popen("src\legalizador\openExcel.bat")
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
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.legalizador = Abrir_pagina1(int(self.time.get()))
        self.legalizador.openEdge()
        self.legalizador.selectPage(self.link)
    
    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()
        
    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        self.poliedro.definirBrowser(self.legalizador)
        self.poliedro.seleccionAcceso('362')
        for i in range(int(self.repeticiones)):
            self.ciclo = True
            self.contador = 0
            self.excel.leer_excel('src\legalizador\legalizador.xlsx','iccid')
            self.excel.quitarFormatoCientifico('iccid')
            self.ventana_informacion.write(f'Ciclo {i+1}')
            while self.ciclo:
                if self.contador == self.excel.cantidad:
                    self.ciclo = False
                else:
                    try:
                        self.min = str(self.excel.excel['min'][self.contador])
                        self.mensaje= str(self.excel.excel['Mensaje'][self.contador])
                        if str(self.mensaje) != 'nan' and str(self.mensaje) != 'error':
                            self.ventana_informacion.write(f'Legalizacion {self.min} ya realizada o con error ya detectado')
                            self.contador += 1
                        else:
                            self.mensaje = ''
                            self.min = ''
                            self.legalizadorInd()
                    except:
                        self.ventana_informacion.write(f'Siguiente por error en legalizacion de {self.min}')
                        if f'{len(self.cedula)}' == '9' and self.tipoDoc != 'nit':
                            self.excel.guardar(self.contador, 'Mensaje', 'error por cedula de 9 digitos')
                        else:
                            self.excel.guardar(self.contador, 'Mensaje', 'error')
                        self.contador += 1
                        try:
                            self.reinicio()
                        except:
                            try:
                                self.poliedro.reinicio(start=False)
                            except:
                                self.poliedro.reinicio()
            self.ventana_informacion.write('Proceso terminado')
            self.ventana_informacion.write(f'Ciclo {i+1} finalizado')
        self.on_of(True)
    

    def legalizadorInd(self):
        self.ventana_informacion.write(f'legalizando numero {self.contador+1} de {self.excel.cantidad}')
        self.iccid = str(self.excel.excel['iccid'][self.contador])[-12:] 
        self.cedulaVendedor = str(self.excel.excel['idvendedor'][self.contador]).replace('.0','')
        self.imei = str(self.excel.excel['imei'][self.contador])
        self.min = str(self.excel.excel['min'][self.contador])
        self.nombre = str(self.excel.excel['nombre'][self.contador])
        self.apellido = str(self.excel.excel['apellido'][self.contador])
        self.cedula = str(self.excel.excel['cedula'][self.contador])
        self.tipoDoc = str(self.excel.excel['tipodoc'][self.contador])
            

        primerFormulario = [
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[2]/div/div[1]/div/input', self.cedulaVendedor],
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[2]/div/div[2]/div/input', self.min],
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[3]/div[1]/div/input', self.imei],
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[3]/div[2]/div/input', self.iccid],
        ]

        if self.excel.excel['tipodoc'][self.contador].lower().replace(" ","") == 'nit':
            self.poliedro.seleccionNit()
            primerFormulario.append(['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[2]/div/input', self.cedula[:9]])
            self.poliedro.rellenoFormulario(5, primerFormulario)
        else:
            primerFormulario.append(['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[2]/div/input', self.cedula])
            primerFormulario.append(['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[3]/div/input', self.apellido])
            self.poliedro.rellenoFormulario(6, primerFormulario)
        time.sleep(self.time2)
        self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[5]/input[1]')
        self.etapa = 1
        options = [
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span'],
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div'],
        ]
        functionList = [
            self.validado,
            self.errorKitRegistrado,
        ]
        self.poliedro.detectOption(options, functionList, NoneFunc=self.errorGeneral)


    def validado(self):
        validado = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[6]/div/span')
        if 'Validación Correcta' in validado: pass
        else: raise('invalido')
        time.sleep(0.5)
        time.sleep(self.time2)
        self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[3]')
        self.etapa = 2
        options = [
            ['/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/ul/li']
        ]
        self.poliedro.detectOption(options,[self.errorConsultaDemografica], NoneFunc=self.terminarValidado)

    def terminarValidado(self):
        self.poliedro.saludo()
        if self.excel.excel['tipodoc'][self.contador].lower().replace(" ","") == 'nit':
            self.poliedro.tipoDoc('nit')
        else:
            self.poliedro.tipoDoc('cedula')
            self.poliedro.rellenoApellido(self.apellido)
        self.poliedro.rellenoNombre(self.nombre)
        self.poliedro.rellenoCedula(self.cedula)
        self.poliedro.correo(self.correo)
        self.poliedro.rellenoNumero()
        self.poliedro.rellenoDireccion(legalizador=True)
        time.sleep(self.time2)
        self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[5]/input[2]')
        self.etapa = 3
        time.sleep(self.time2)
        self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/input[2]')
        self.etapa = 4
        time.sleep(self.time2)
        self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/strong/strong/div/input[2]')
        self.etapa = 5
        activado = True
        while activado:
            try:
                mensaje = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p')
                if 'Solicitud fue enviada satisfactoriamente' in mensaje:
                    activado = False
            except:
                time.sleep(1)
        #/html/body/div/div[2]/section/div/div[2]/div[2]/main/div/div/div/strong/strong/div/div/div/p
        # Su Solicitud fue enviada satisfactoriamente.
        self.ventana_informacion.write(f'Legalizacion exitosa de {self.min}')
        self.excel.guardar(self.contador, 'Mensaje', 'legalizada')
        self.reinicio()
        self.contador += 1
    
    def errorConsultaDemografica(self):
        validado = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/ul/li')
        self.ventana_informacion.write(f'{self.min} {validado}')
        self.excel.guardar(self.contador, 'Mensaje', validado)
        self.reinicio()
        self.contador += 1
    
    def errorKitRegistrado(self):
        validado = self.legalizador.read('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[4]/div[2]/div[1]/div/div/div')
        self.ventana_informacion.write(f'{self.min} {validado}')
        self.excel.guardar(self.contador, 'Mensaje', validado)
        # self.legalizador.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[7]/input[1]')
        self.reinicio()
        self.contador += 1

    def errorGeneral(self):
        raise('error general')
    
    def reinicio(self):
        if self.etapa == 0:
            pass
        if self.etapa == 5:
            time.sleep(self.time2)
            self.legalizador.click('btnPrev', 'id')
            self.poliedro.seleccionAcceso('362', start=False)
        else:
            for i in range(self.etapa):
                time.sleep(self.time2)
                self.legalizador.click('btnPrev', 'id')
        self.etapa == 0

        

    