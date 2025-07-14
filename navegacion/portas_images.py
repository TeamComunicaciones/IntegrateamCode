from navegacion import sub_menu as sm, ventana_informacion 
from funcionalidad import  web_controller, poliedro, excel, clickImage
from recursos import botones, label, checkbox
import threading
from subprocess import Popen
import pyperclip
from datetime import datetime, timedelta
import time
import tkinter as tk
import customtkinter as ctk

class Portas:

    def __init__(self,master, cambioTamaño, ventanaSuperior):
        self.errorCorreo=False
        self.cambioTamaño = cambioTamaño
        self.ventanaSuperior = ventanaSuperior
        self.master = master
        self.label = label.Label().create_label(master, 'PORTABILIDADES', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.controlador =clickImage.ClickImage()
        self.submenu= sm.Sub_menu(master, 2, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['START', self.ejecuccionHilo])
        self.master = master
        self.excel = excel.Excel_controller()
        self.checkbox = checkbox.Checkbox()
        self.checkbox2 = checkbox.Checkbox()
        self.checkbox_var = tk.BooleanVar()
        self.tropas = tk.BooleanVar()
        self.validacionImgs = tk.BooleanVar()
        self.checkbox_validacionImgs =  checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Configurar Imagenes.', self.on_checkbox_change_configuracion, self.validacionImgs)
        self.checkbox_festivo = checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Lunes Festivo.', self.on_checkbox_change, self.checkbox_var)
        self.checkbox_tropas =  checkbox.Checkbox().create_checkbox(self.submenu.submenu, 'Tropas.', self.on_checkbox_change_tropas, self.tropas)
        
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

    def on_checkbox_change_configuracion(self):
        if self.validacionImgs.get():
            self.ventana_informacion.write('Activando el modo Debug')
        else:
            self.ventana_informacion.write('Desactivando el modo Debug')
        self.controlador.debug(self.validacionImgs.get(), self.ventanaSuperior)
    
    def abrir_excel(self):
        self.ventana_informacion.write('excel portabilidad abierto recuerde cerrar antes de iniciar')
        p = Popen("src\portas\openExcel.bat")
        stdout, stderr = p.communicate()
    
    def ejecuccionHilo(self):
        hilo_legalizador = threading.Thread(target=self.ejecuccion)
        hilo_legalizador.start()
    
    def ejecuccion(self):
        self.cambioTamaño(False)
        self.ventana_informacion.write('cambio tamaño')
        self.submenu.submenu.destroy()
        self.submenu= sm.Sub_menu(self.master, 1, boton1=['STOP', self.stop], agrandar=True)
        self.controlador.definirInformes(self.ventana_informacion)
        self.controlador.detener = False
        self.excel.leer_excel('src\portas\portabilidad.xlsx','CC CLIENTE')
        self.excel.quitarFormatoCientifico('SERIAL')
        self.seleccionOpcion()
        

    def copiarMin(self, i):
        self.controlador.copiarMin('referenciaMin')
        self.msisdn = pyperclip.paste()
        print(self.msisdn)
        self.excel.guardar(i,'MSISDN',self.msisdn, destino='src\portas\portabilidad.xlsx')
    
    def stop(self):
        self.cambioTamaño(True)
        self.ventana_informacion.write('Restablece tamaño')
        self.submenu.submenu.destroy()
        self.submenu= sm.Sub_menu(self.master, 2, boton2=['START', self.ejecuccionHilo])
        self.controlador.debugBool = False
        self.controlador.detener = True
    
    def seleccionOpcion(self):
        self.ventana_informacion.write(f'Iniciando ejecución')
        self.ingresoOpcionRapida()

    def iteraciones(self):
        for i in range(self.excel.cantidad):
            self.i = i
            try:
                self.ventana_informacion.write(f'operacion {i+1} de {self.excel.cantidad}')
                self.crearVariablesExcel(i)
                if 'el MSISDN asignado es' in self.msisdn:
                    continue
                start_time = time.time()
                self.rellenoPrimerFormulario()
                self.copiarMin(i)
                elapsed_time = time.time() - start_time
                self.excel.guardar(i,'MENSAJE',str(round(elapsed_time,2)), destino='src\portas\portabilidad.xlsx')
                self.reinicio()
            except:
                if self.controlador.detener:
                    pass
                else:
                    self.ventana_informacion.write(f'Reiniciando para intentar con la siguiente')
                    if self.errorCorreo:
                        self.excel.guardar(i,'MENSAJE','Error Correo', destino='src\portas\portabilidad.xlsx')
                    else:
                        self.excel.guardar(i,'MENSAJE','error', destino='src\portas\portabilidad.xlsx')
                    self.errorCorreo = False
                    self.reinicio()
        self.iteraciones()
        
    
    def reinicio(self):
        try:
            self.controlador.scroll(800)
            self.controlador.clickImg('reinicio1',1, extra=True, excel=[self.excel,self.i])
            if self.tropas.get():
                pass
            else:
                self.controlador.clickImg('reinicio2',1, extra=True, excel=[self.excel,self.i])
            self.ingresoOpcionRapida()
        except:
            try:
                self.controlador.clickImg('reinicio1',1, extra=True, excel=[self.excel,self.i])
            except:
                pass
            try:
                if self.tropas.get():
                    pass
                else:
                    self.controlador.clickImg('reinicio2',1, extra=True, excel=[self.excel,self.i])
            except:
                pass
            try:
                self.ingresoOpcionRapida()
            except:
                pass

    

    def ingresoOpcionRapida(self):
        if self.tropas.get():
            self.controlador.clickImg('tropas1', 1)
            self.controlador.clickImg('tropas2', 1)
        else:
            self.controlador.clickImg('paso1', 1)
            self.controlador.clickImg('paso2', 1)
        self.controlador.clickImg('paso3', 1, region='region3')
        self.controlador.write('290', enter=True)
    
    def crearVariablesExcel(self,i):
        self.idCliente = str(self.excel.excel['CC CLIENTE'][i])
        self.fechaExpedicion = str(self.excel.excel['FECHA EXPEDICION'][i])
        self.apellido = str(self.excel.excel['APELLIDO CLIENTE'][i])
        self.idVendedor = str(self.excel.excel['CEDULA VENDEDOR'][i])
        self.min = str(self.excel.excel['NUMERO MOVIL'][i])
        self.iccid = str(self.excel.excel['SERIAL'][i])[-12:]
        self.iccid2 = str(self.excel.excel['SERIAL2'][i])[-12:]
        self.nip = str(self.excel.excel['NIP'][i])
        self.nombre = str(self.excel.excel['NOMBRE CLIENTE'][i])
        self.correo = str(self.excel.excel['CORREO'][i])
        self.tipoLinea = str(self.excel.excel['TIPO DE LINEA'][i])
        self.tipo = 'cedula'
        self.msisdn = str(self.excel.excel['MSISDN'])

    def rellenoPrimerFormulario(self):
        self.controlador.clickImg('paso4',1, region='region4', desplazar=True, excel=[self.excel,self.i])
        self.controlador.write(self.tipo, enter=True)
        self.controlador.clickImg('paso5',1, region='region5', excel=[self.excel,self.i], confidenceImg=0.9)
        self.controlador.write(self.idCliente)
        self.controlador.clickImg('paso6',1, region='region6', excel=[self.excel,self.i])
        self.controlador.write(self.apellido)
        self.controlador.clickImg('paso7',1, region='region7', excel=[self.excel,self.i])
        self.controlador.write(self.idVendedor)
        try:
            self.controlador.wait('regionExpedicion', menos=True, confidence=0.90)
            self.controlador.clickImg('pasoExpedicion',1, region='regionExpedicion', seleccionar=True, excel=[self.excel,self.i])
            self.controlador.write(self.fechaExpedicion)
        except:
            pass
        
        self.controlador.clickImg('paso8',1, region='region8', excel=[self.excel,self.i])
        self.controlador.write(self.min)
        self.controlador.scroll(-600)
        self.controlador.clickImg('paso9',1, region='region9', desplazar=True, excel=[self.excel,self.i])
        tamañoNip = len(self.nip)
        while (tamañoNip<5):
            self.controlador.write('0')
            tamañoNip += 1
        self.controlador.write(self.nip)
        self.controlador.clickImg('paso10',1, region='region10', seleccionar=True, copiar=True, excel=[self.excel,self.i])
        contenido_portapapeles = pyperclip.paste()
        fecha = datetime.strptime(contenido_portapapeles, '%d/%m/%Y')
        if 3 <= fecha.weekday() <= 7:
            print("La fecha cae entre jueves y domingo.")
            if self.checkbox_var.get():
                festivo = 1
            else:
                festivo = 0
            dias_hasta_lunes = (0 + festivo - fecha.weekday()) % 7
            proximo_lunes = fecha + timedelta(days=dias_hasta_lunes)
            newfecha = proximo_lunes.strftime('%d/%m/%Y')
            print(newfecha)
            self.controlador.write(newfecha, enter=True)
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
            self.controlador.write(newfecha, enter=True)

        else:
            print("La fecha no cae entre jueves y domingo.")
        self.controlador.clickImg('paso11',1, region='region11')
        self.controlador.write(self.iccid, enter=True, pausa=True)
        if str(self.iccid2) != 'nan':
            self.controlador.clickImg('paso12',1, region='region12', excel=[self.excel,self.i])
            self.controlador.write(self.iccid2)
        self.controlador.clickImg('paso13',1, excel=[self.excel,self.i])
        self.controlador.wait('wait6', extra=True)
        self.controlador.clickImg('paso14',1, excel=[self.excel,self.i])
        self.controlador.wait('wait1')
        self.controlador.scroll(-300)
        self.ventana_informacion.write('moviendo mouse')
        try:
            self.controlador.quitarMouse()
        except:
            pass
        self.ventana_informacion.write('movido')
        try:
            self.controlador.wait('wait2', menos=True, confidence=0.90)
            intentoBasico = True
        except:
            intentoBasico = False
        if intentoBasico:
            self.rellenarDatosBasicos()
        try:
            self.controlador.wait('regionBasica1', menos=True, confidence=0.90)
            intentoSr = True
        except:
            intentoSr = False
        if intentoSr:
            self.rellenarSr()
        try:
            self.controlador.wait('regionBasica4', menos=True)
            intentoCorreo = True
        except:
            intentoCorreo = False
        if intentoCorreo:
            self.rellenarCorreo()
        try:
            # self.controlador.scroll(-300) # solo para bogota
            self.controlador.wait('wait3', menos=True)
            intentoTelefono = True
        except:
            intentoTelefono = False
        if intentoTelefono:
            self.rellenarTelefono()
        try:
            self.controlador.wait('wait3-2', menos=True)
            intentoTelefono2 = True
        except:
            intentoTelefono2 = False
        if intentoTelefono2:
            self.rellenarTelefono2()
        try:
            self.controlador.wait('wait4', menos=True, confidence=0.90)
            intentoDocumento = True
        except:
            intentoDocumento = False
        if intentoDocumento:
            self.rellenarDocumento()
        try:
            self.controlador.wait('wait5', menos=True)
            intentoDireccion = True
        except:
            intentoDireccion = False
        if intentoDireccion:
            self.rellenarDireccion()
        try:
            self.controlador.wait('wait5-2', menos=True)
            intentoDireccion2 = True
        except:
            intentoDireccion2 = False
        if intentoDireccion2:
            self.rellenarDireccion2()

        self.opcion1()
        try:
            self.controlador.wait('errorCorreo', menos=True)
            self.errorCorreo = True
        except:
            pass
        if self.errorCorreo:
            raise('Error Correo')

        self.controlador.wait('wait7', extra=True)
        self.controlador.clickImg('paso17', 1, 'region17', desplazar=True, excel=[self.excel,self.i], confidenceImg=0.7, confidenceReg=0.7)
        self.controlador.write('a', enter=True)
        self.controlador.clickImg('paso18', 1, 'region18', excel=[self.excel,self.i])
        self.controlador.write('w', enter=True)
        self.controlador.clickImg('paso19', 1, excel=[self.excel,self.i])
        self.controlador.scroll(-600)
        self.controlador.clickImg('paso20', 1, excel=[self.excel,self.i])
        self.controlador.clickImg('paso21', 1, excel=[self.excel,self.i])
    
    def rellenarSr(self):
        self.controlador.clickImg('pasoBasica1', 1, 'regionBasica1', excel=[self.excel,self.i])
        self.controlador.write('sr', enter=True)

    def rellenarDatosBasicos(self):
        self.controlador.clickImg('pasoBasica2', 1, 'regionBasica2', excel=[self.excel,self.i])
        self.controlador.write(self.nombre, desplazarClick=True)
        self.controlador.clickImg('pasoBasica3', 1, 'regionBasica3', excel=[self.excel,self.i])
        self.controlador.write(self.apellido, desplazarClick=True)

    def rellenarCorreo(self):
        self.controlador.clickImg('pasoBasica4', 1, 'regionBasica4', excel=[self.excel,self.i])
        self.controlador.write(self.correo, desplazarClick=True, correo=True)

    def rellenarCorreo2(self):
        self.controlador.clickImg('pasoBasica4-2', 1, 'regionBasica4-2', excel=[self.excel,self.i])
        self.controlador.write(self.correo, desplazarClick=True, correo=True)
    
    def rellenarTelefono(self):
        self.controlador.clickImg('pasoTel1', 1, 'regionTel1', excel=[self.excel,self.i])
        self.controlador.write('fij', enter=True)
        self.controlador.clickImg('pasoTel2', 1, 'regionTel2', excel=[self.excel,self.i])
        self.controlador.write('604', enter=True)
        self.controlador.clickImg('pasoTel3', 1, 'regionTel3', excel=[self.excel,self.i])
        self.controlador.write('6046679', enter=True, backspase=True)
    
    def rellenarTelefono2(self):
        self.controlador.clickImg('pasoTel1-2', 1, 'regionTel1-2', excel=[self.excel,self.i])
        self.controlador.write('fij', enter=True)
        self.controlador.clickImg('pasoTel2-2', 1, 'regionTel2-2', excel=[self.excel,self.i])
        self.controlador.write('604', enter=True)
        self.controlador.clickImg('pasoTel3-2', 1, 'regionTel3-2', excel=[self.excel,self.i])
        self.controlador.write('6046679', enter=True, backspase=True)
    
    def rellenarDocumento(self):
        self.controlador.clickImg('pasoCc1', 1, 'regionCc1', excel=[self.excel,self.i])
        self.controlador.write(self.tipo, enter=True)
        self.controlador.clickImg('pasoCc2', 1, 'regionCc2', excel=[self.excel,self.i])
        self.controlador.write(self.idCliente, enter=True, backspase=True)
    
    def rellenarDireccion(self):
        self.controlador.clickImg('pasoDireccion1', 1, 'regionDireccion1', excel=[self.excel,self.i])
        self.controlador.write('otras', enter=True)
        time.sleep(3)
        self.controlador.clickImg('pasoDireccion2', 1, 'regionDireccion2', excel=[self.excel,self.i])
        self.controlador.write('centro', enter=True, desplazarClick=True)
        self.controlador.clickImg('pasoDireccion3', 1, 'regionDireccion3', excel=[self.excel,self.i])
        self.controlador.write('ant', enter=True)
        self.controlador.clickImg('pasoDireccion4', 1, 'regionDireccion4', excel=[self.excel,self.i])
        self.controlador.write('medel', enter=True)
        self.controlador.clickImg('pasoDireccion5', 1, 'regionDireccion5', excel=[self.excel,self.i])
        self.controlador.write('central', enter=True, desplazarClick=True)
    
    def rellenarDireccion2(self):
        self.controlador.clickImg('pasoDireccion1-2', 1, 'regionDireccion1-2', excel=[self.excel,self.i])
        self.controlador.write('otras', enter=True)
        time.sleep(3)
        self.controlador.clickImg('pasoDireccion2-2', 1, 'regionDireccion2-2', excel=[self.excel,self.i])
        self.controlador.write('centro', enter=True, desplazarClick=True)
        self.controlador.clickImg('pasoDireccion3-2', 1, 'regionDireccion3-2', excel=[self.excel,self.i])
        self.controlador.write('ant', enter=True)
        self.controlador.clickImg('pasoDireccion4-2', 1, 'regionDireccion4-2', excel=[self.excel,self.i])
        self.controlador.write('medel', enter=True)
        self.controlador.clickImg('pasoDireccion5-2', 1, 'regionDireccion5-2', excel=[self.excel,self.i])
        self.controlador.write('central', enter=True, desplazarClick=True)
    

    def opcion1(self):
        self.controlador.scroll(-3000)
        if self.tipoLinea == 'prepago':
            self.controlador.clickImg('paso15', 1, 'region15-prepago', excel=[self.excel,self.i])
        else:
            self.controlador.clickImg('paso15', 1, 'region15-postpago', excel=[self.excel,self.i])
        self.controlador.clickImg('paso16', 1, excel=[self.excel,self.i])


        
        
    


