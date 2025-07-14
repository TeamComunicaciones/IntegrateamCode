
from navegacion import sub_menu as sm, ventana_informacion
from recursos import create_frame, label, botones
from funcionalidad import  web_controller, poliedro, excel
from subprocess import Popen
import threading
import time

class Revisar_equipos:

    def __init__(self,master, on_of):
        self.on_of = on_of
        self.poliedro = poliedro.Poliedro()
        self.excel = excel.Excel_controller()
        self.titulo = label.Label().create_label(master, 'CONSULTA TRIPLETAS KIT PREPAGO', 0.2, 0.0, 0.5,0.2, letterSize=25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR LISTA', self.abrir_excel], boton2=['ABRIR PAGINA', self.abrir_pagina], boton3=['START', self.ejecuccionHilo])
        self.link= 'https://poliedrodist.comcel.com.co/'

    def abrir_excel(self):
        self.ventana_informacion.write('excel revisión abierto recuerde cerrar antes de iniciar')
        p = Popen("src\\revisar_equipos\openExcel.bat")
        stdout, stderr = p.communicate()

    def abrir_pagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.revision = Abrir_pagina1(0)
        self.revision.openEdge()
        self.revision.selectPage(self.link)
    
    def ejecuccionHilo(self):
        hilo_equipos = threading.Thread(target=self.ejecuccion)
        hilo_equipos.start()
    
    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write('Empezando ejecuccion')
        self.poliedro.definirBrowser(self.revision)
        self.revision.click('/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[1]/div[9]')
        self.revision.click('/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[1]/div[10]/div[2]')
        self.revision.click('/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[1]/div[10]/div[3]/div/a')
        self.excel.leer_excel('src\\revisar_equipos\\revisar_equipos.xlsx', 'Serial')
        self.excel.quitarFormatoCientifico('Serial')
        self.excel.quitarFormatoCientifico('Iccid')
        self.ciclo = True
        self.contador = 0

        while self.ciclo:
            if self.contador == self.excel.cantidad:
                self.ciclo = False
            else:
                self.revisionInd()
        self.ventana_informacion.write('Proceso terminado')
        self.on_of(True)

    def revisionInd(self):
        self.ventana_informacion.write(f'Revisando {self.contador+1} de {self.excel.cantidad}')
        self.imei = str(self.excel.excel['Serial'][self.contador])
        self.codigo = str(self.excel.excel['Codigo'][self.contador])
        if str(self.codigo) != 'nan' or str(self.imei) == '':
            pass
            self.ventana_informacion.write('Codigo ya encontrado')
            self.contador += 1
        else:
            self.revision.eraseLetter('/html/body/table/tbody/tr[3]/td/form/table/tbody/tr/td[2]/div/table/tbody/tr[4]/td[2]/input', 20)
            self.revision.insert('/html/body/table/tbody/tr[3]/td/form/table/tbody/tr/td[2]/div/table/tbody/tr[4]/td[2]/input', self.imei)
            self.revision.click('/html/body/table/tbody/tr[3]/td/form/table/tbody/tr/td[2]/div/table/tbody/tr[8]/td[2]/input')
            self.poliedro.detectOption([['/html/body/div/table[2]/tbody/tr[2]/td[1]/b']], [self.exitoso], NoneFunc=self.fallido)
            self.revision.browser.back()
    
    def exitoso(self):
        msisdn = self.revision.read('/html/body/div/table[2]/tbody/tr[2]/td[1]/b')
        iccid = self.revision.read('/html/body/div/table[2]/tbody/tr[2]/td[2]/b')
        codigo = self.revision.read('/html/body/div/table[1]/tbody/tr[2]/td[2]/b')
        self.excel.guardar(self.contador, 'Msisdn', msisdn, destino='src\\revisar_equipos\\revisar_equipos.xlsx')
        self.excel.guardar(self.contador, 'Iccid', iccid, destino='src\\revisar_equipos\\revisar_equipos.xlsx')
        self.excel.guardar(self.contador, 'Codigo', codigo, destino='src\\revisar_equipos\\revisar_equipos.xlsx')
        self.contador += 1

    def fallido(self):
        observaciones = self.excel.excel['Observacion'][self.contador]
        codigo = self.revision.read('/html/body/div/table[1]/tbody/tr[2]/td[2]/b')
        observacion = f'{observaciones}, {codigo}'
        observacion = observacion.replace('nan,', '')
        self.excel.guardar(self.contador, 'Observacion', observacion, destino='src\\revisar_equipos\\revisar_equipos.xlsx')
        self.contador += 1