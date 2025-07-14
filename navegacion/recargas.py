from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors, checkbox, combobox
from funcionalidad import  web_controller, excel, scraping
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
from datetime import datetime


class Recargas:

    def __init__(self,master, on_of):
        self.prueba = 'prueba'
        self.on_of = on_of
        self.titulo = label.Label().create_label(master, 'RECARGAS', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.link= 'https://atiendo.claro.com.co/pretups/'
        # self.link2='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_factura.asp'
        # self.link3='https://190.144.217.66/Front_PortalComercial/Portal/consultas/con_seriales_factura.asp'
        self.menu = sm.Sub_menu(master,3, boton1=['ARCHIVO', self.abrir_excel], boton2=['CUENTAS', self.abrir_excel2], boton3=['START', self.ejecuccionHilo])
        self.recargas = ''
        grupo = {
            'Paquetes Todo Incluido':'a0c6d71e0b4f-0',
            'Paquetes de datos':'a0c6d71e0b4f-1',
            'Paquete de Bienvenida Prepago':'a0c6d71e0b4f-2',
            'Reventa ':'a0c6d71e0b4f-3',
            'Aplicaciones y Redes':'a0c6d71e0b4f-4',
            'Paquetes de Voz':'a0c6d71e0b4f-5',
            'Paquetes de LDI':'a0c6d71e0b4f-6',
            'Paquetes GAMERS':'a0c6d71e0b4f-7',
            'Paquetes Salud en Linea':'a0c6d71e0b4f-8',
        }
        servicio = [
            'VZ - Paq 300 Min - 1 Dia - $2,000',
            'VZ - Paq 1000 Min - 20 Dias - $16,500',
            'VZ - Paq 300 Min - 2 Dias - $2,500',
            'Paq Instagram 1 Dia $3,000',
            'Paq WAZE 1 dia $1,500',
            'Paq Youtube 1 hora $3,500',
            'Chat WhatsApp 15 Dias $9,500',
            'Chat WhatsApp 30 Dias $18,500',
        ]

        self.paquetes = tk.BooleanVar()
        self.grupoSelect = tk.StringVar()
        self.paqueteSelect = tk.StringVar()
        self.entry_paginas = tk.StringVar()
        self.entry_paginas.set('1')
        self.visible = tk.BooleanVar()
        self.entry_tiempo = tk.StringVar()
        self.entry_tiempo.set('0')
        self.entry_pin = tk.StringVar()
        # self.entry_pin.set('0147')
        self.entry_user = tk.StringVar()
        # self.entry_user.set('cotalvaro')
        self.entry_password = tk.StringVar()
        # self.entry_password.set('Team26+')

        self.title_paquetes = label.Label().create_label(self.menu.submenu, 'Paquetes: ', 0.0, 0.47, 0.30,0.05, letterSize= 14)
        self.title_paginas = label.Label().create_label(self.menu.submenu, 'Grupo: ', 0.0, 0.53, 0.25,0.05, letterSize= 14)
        self.title_paginas = label.Label().create_label(self.menu.submenu, 'Servicio: ', 0.0, 0.59, 0.25,0.05, letterSize= 14)
        self.title_paginas = label.Label().create_label(self.menu.submenu, 'Paginas: ', 0.0, 0.65, 0.25,0.05, letterSize= 14)
        self.title_pin = label.Label().create_label(self.menu.submenu, 'Invisible: ', 0.0, 0.71, 0.25,0.05, letterSize= 14)
        self.title_pin = label.Label().create_label(self.menu.submenu, 'Tiempo: ', 0.0, 0.77, 0.25,0.05, letterSize= 14)
        self.title_pin = label.Label().create_label(self.menu.submenu, 'Pin: ', 0.0, 0.83, 0.25,0.05, letterSize= 14)
        self.title_user = label.Label().create_label(self.menu.submenu, 'Usuario: ', 0.0, 0.89, 0.3,0.05, letterSize= 14)
        self.title_password = label.Label().create_label(self.menu.submenu, 'Clave: ', 0.0, 0.95, 0.25,0.05, letterSize= 14)
  
        self.checkbox_tropas =  checkbox.Checkbox().create_checkbox(self.menu.submenu, '', self.on_checkbox_change_paquetes, self.paquetes, place=True, x=0.3, y= 0.47, widht=0.50, height=0.05, letterSize=14)
        self.grupo =  combobox.Combobox().create_combobox(self.menu.submenu, list(grupo.keys()), x=0.3, y= 0.53, widht=0.60, height=0.05, letterSize=14, textvariable=self.grupoSelect)
        self.servicio =  combobox.Combobox().create_combobox(self.menu.submenu, servicio, x=0.3, y= 0.59, widht=0.60, height=0.05, letterSize=14)
        input_paginas= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_paginas)
        input_paginas.place(relx=0.3, rely=0.65, relheight=0.05, relwidth=0.6)
        self.checkbox_visible =  checkbox.Checkbox().create_checkbox(self.menu.submenu, '', self.on_checkbox_change_visible, self.visible, place=True, x=0.3, y= 0.71, widht=0.50, height=0.05, letterSize=14)
        input_tiempo= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_tiempo)
        input_tiempo.place(relx=0.3, rely=0.77, relheight=0.05, relwidth=0.6)
        input_pin= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_pin)
        input_pin.place(relx=0.3, rely=0.83, relheight=0.05, relwidth=0.6)
        input_user= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_user)
        input_user.place(relx=0.3, rely=0.89, relheight=0.05, relwidth=0.6)
        input_password= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_password)
        input_password.place(relx=0.3, rely=0.95, relheight=0.05, relwidth=0.6)
        
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.excel = excel.Excel_controller()
        self.excel2 = excel.Excel_controller()
    
    def ejecuccionHilo(self):
        self.ventana_informacion.write('ejecutando hilos')
        self.on_of(False)
        self.ventana_informacion.write(f'Empezando ejecuccion con {self.grupo.get()} paginas')
        self.enlistar_data()
        self.enlistar_cuentas()
        if self.entry_paginas.get().isnumeric():
            if int(self.entry_paginas.get()) > 10:
                self.entry_paginas.set('10')
        else:
            self.entry_paginas.set('1')
        threads = []
        self.datos_excel = []
        n = int(self.entry_paginas.get())
        rows_per_df = self.excel.cantidad // n
        remainder = self.excel.cantidad % n
        self.dfs = []
        start_index = 0
        for i in range(n):
            if i < remainder:
                end_index = start_index + rows_per_df + 1
            else:
                end_index = start_index + rows_per_df
            temp_df = self.excel.excel.iloc[start_index:end_index].reset_index(drop=True)
            self.dfs.append(temp_df)
            start_index = end_index
        self.excel.borrar('src\\recargas\\recargas.xlsx')
        for i in range(n):
            thread = threading.Thread(target=self.ejecuccion, args=(i,))
            threads.append(thread)
            thread.start()
        # # Esperar a que todos los hilos terminen
        # for thread in threads:
        #     thread.join()
        # print("Todas las ejecuciones han terminado.")
    
    def abrir_excel(self):
        self.ventana_informacion.write('excel recargas abierto recuerde cerrar antes de iniciar')
        p = Popen("src\\recargas\openExcel.bat")
        stdout, stderr = p.communicate()

    def abrir_excel2(self):
        self.ventana_informacion.write('excel cuentas abierto recuerde cerrar antes de iniciar')
        p = Popen("src\\recargas\openExcel2.bat")
        stdout, stderr = p.communicate()
    
    def on_checkbox_change_paquetes(self):
        if self.paquetes.get():
            self.ventana_informacion.write('Cambiando modalidad a Paquetes')
        else:
            self.ventana_informacion.write('Cambiando modalidad a Estandar')
        
    def on_checkbox_change_visible(self):
        if self.visible.get():
            self.ventana_informacion.write('Cambiando modalidad a Invisible')
        else:
            self.ventana_informacion.write('Cambiando modalidad a Visible')
        
    def ejecuccion(self, i):
        self.abrirPagina(i)
    
    def abrirPagina(self, i):
        ciclo = True
        contador = 0
        intentos = 0
        self.ventana_informacion.write(f'Navegador {i+1} abierto')   
        class Abrir_pagina1(web_controller.Web_Controller):pass
        recargas = Abrir_pagina1(1)
        try:
            recargas.openEdge(headless=self.visible.get())
            recargas.selectPage(self.link)
            recargas.insert('loginID', self.excel2.excel['cuenta'][i], 'id')
            recargas.insert('password', self.entry_password.get(), 'id')
            recargas.click('/html/body/form[2]/table[3]/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/input[1]')
            time.sleep(10)
            try:
                recargas.readShort2('login_id', 'id')
                recargas.insert('login_id', self.excel2.excel['cuenta'][i], 'id')
                recargas.insert('pwd', self.entry_password.get(), 'id')
                recargas.click('/html/body/app-root/div/app-login/div/div/div[2]/form/div[9]/button')
                time.sleep(10)
            except:
                pass
            # time.sleep(10)
            recargas.click('/html/body/app-root/div/app-layout/app-sidebar/nav/div/div[2]/a[2]')
            if self.paquetes.get():
                recargas.click('/html/body/app-root/div/app-layout/section/claro-app-recharge/div/div/div[3]/div/claro-header-recharge/ul/div[2]/li/a')
        except: pass
        while ciclo:
                if contador == len(self.dfs[i]):
                    ciclo = False
                else:
                    try:
                        min =self.dfs[i]['linea'][contador]
                        value =self.dfs[i]['valor'][contador]
                        while True:
                            if recargas.value('msisdnInput', 'id') == f'{min}':
                                break
                            recargas.eraseLetter('msisdnInput', 20, 'id')
                            recargas.insert('msisdnInput', f'{min}', 'id')
                        if self.paquetes.get():
                            while True:
                                if recargas.read('groupSelect', 'id') == self.grupo.get():
                                    break
                                recargas.click('groupSelect', 'id')
                                recargas.click(f".//span[text()='{self.grupo.get()}']",)
                            while True:
                                if recargas.read('subServiceSelect', 'id') == self.servicio.get():
                                    break
                                recargas.click('subServiceSelect', 'id')
                                recargas.click(f".//span[text()='{self.servicio.get()}']",)
                        else:
                            recargas.eraseLetter('amountInput', 20, 'id')
                            recargas.insert('amountInput', f'{value}', 'id')
                        recargas.click('recharge', 'id')
                        contador += 1
                        recargas.eraseLetter('no-partitioned', 20, 'id')
                        recargas.insert('no-partitioned', self.entry_pin.get(), 'id')
                        recargas.click('rechargebutton2', 'id')
                        self.ventana_informacion.write(f'Pagina {i+1} {round(contador/len(self.dfs[i]) *100)}% completado')
                        recargas.click('anotherRecharge', 'id')
                        intentos = 0
                        
                    except:
                        intentos += 1
                        if intentos > 20:
                            ciclo = False
                            self.ventana_informacion.write(f'Se detiene por exceso en intentos fallidos')
                        try:
                            recargas.cerrar()
                            recargas = Abrir_pagina1(1)
                            recargas.openEdge(headless=self.visible.get())
                            recargas.selectPage(self.link)
                            recargas.insert('loginID', self.excel2.excel['cuenta'][i], 'id')
                            recargas.insert('password', self.entry_password.get(), 'id')
                            recargas.click('/html/body/form[2]/table[3]/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/input[1]')
                            time.sleep(10)
                            try:
                                recargas.readShort2('login_id', 'id')
                                recargas.insert('login_id', self.excel2.excel['cuenta'][i], 'id')
                                recargas.insert('pwd', self.entry_password.get(), 'id')
                                recargas.click('/html/body/app-root/div/app-login/div/div/div[2]/form/div[9]/button')
                                time.sleep(10)
                            except:
                                pass
                            recargas.click('/html/body/app-root/div/app-layout/app-sidebar/nav/div/div[2]/a[2]')
                            if self.paquetes.get():
                                recargas.click('/html/body/app-root/div/app-layout/section/claro-app-recharge/div/div/div[3]/div/claro-header-recharge/ul/div[2]/li/a')
                        except: pass
        self.ventana_informacion.write(f'Proceso terminado para navegador {i+1}')
        
        
    def enlistar_data(self):
        self.excel.leer_excel('src\\recargas\\recargas.xlsx','linea')

    def enlistar_cuentas(self):
        self.excel2.leer_excel('src\\recargas\\cuentas.xlsx','numero')



    