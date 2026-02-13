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

    def __init__(self, master, on_of):
        self.prueba = 'prueba'
        self.on_of = on_of
        self.titulo = label.Label().create_label(master, 'RECARGAS', 0.2, 0.0, 0.5, 0.2, letterSize=25)
        self.link = 'https://atiendo.claro.com.co/pretups/'
        self.menu = sm.Sub_menu(master, 3,
                                boton1=['ARCHIVO', self.abrir_excel],
                                boton2=['CUENTAS', self.abrir_excel2],
                                boton3=['START', self.ejecuccionHilo])
        self.recargas = ''

        # Mapa de grupos de paquetes
        grupo = {
            'Paquetes de LDI': 'a0c6d71e0b4f-6',
        }

        servicio = [
            'LDI- Paq LDI 7 Min Venezuela - $2,000',
            'LDI- Paq 10 Min USA CAN PR MEX-$2,000',
            
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
        self.entry_user = tk.StringVar()
        self.entry_password = tk.StringVar()

        self.title_paquetes = label.Label().create_label(self.menu.submenu, 'Paquetes: ', 0.0, 0.47, 0.30, 0.05,
                                                         letterSize=14)
        self.title_paginas = label.Label().create_label(self.menu.submenu, 'Grupo: ', 0.0, 0.53, 0.25, 0.05,
                                                        letterSize=14)
        self.title_paginas = label.Label().create_label(self.menu.submenu, 'Servicio: ', 0.0, 0.59, 0.25, 0.05,
                                                        letterSize=14)
        self.title_paginas = label.Label().create_label(self.menu.submenu, 'Paginas: ', 0.0, 0.65, 0.25, 0.05,
                                                        letterSize=14)
        self.title_pin = label.Label().create_label(self.menu.submenu, 'Invisible: ', 0.0, 0.71, 0.25, 0.05,
                                                    letterSize=14)
        self.title_pin = label.Label().create_label(self.menu.submenu, 'Tiempo: ', 0.0, 0.77, 0.25, 0.05,
                                                    letterSize=14)
        self.title_pin = label.Label().create_label(self.menu.submenu, 'Pin: ', 0.0, 0.83, 0.25, 0.05,
                                                    letterSize=14)
        self.title_user = label.Label().create_label(self.menu.submenu, 'Usuario: ', 0.0, 0.89, 0.3, 0.05,
                                                     letterSize=14)
        self.title_password = label.Label().create_label(self.menu.submenu, 'Clave: ', 0.0, 0.95, 0.25, 0.05,
                                                         letterSize=14)

        self.checkbox_tropas = checkbox.Checkbox().create_checkbox(
            self.menu.submenu, '', self.on_checkbox_change_paquetes, self.paquetes,
            place=True, x=0.3, y=0.47, widht=0.50, height=0.05, letterSize=14
        )
        self.grupo = combobox.Combobox().create_combobox(
            self.menu.submenu, list(grupo.keys()),
            x=0.3, y=0.53, widht=0.60, height=0.05,
            letterSize=14, textvariable=self.grupoSelect
        )
        self.servicio = combobox.Combobox().create_combobox(
            self.menu.submenu, servicio,
            x=0.3, y=0.59, widht=0.60, height=0.05, letterSize=14
        )
        input_paginas = ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_paginas)
        input_paginas.place(relx=0.3, rely=0.65, relheight=0.05, relwidth=0.6)

        self.checkbox_visible = checkbox.Checkbox().create_checkbox(
            self.menu.submenu, '', self.on_checkbox_change_visible, self.visible,
            place=True, x=0.3, y=0.71, widht=0.50, height=0.05, letterSize=14
        )
        input_tiempo = ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_tiempo)
        input_tiempo.place(relx=0.3, rely=0.77, relheight=0.05, relwidth=0.6)

        input_pin = ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_pin)
        input_pin.place(relx=0.3, rely=0.83, relheight=0.05, relwidth=0.6)

        input_user = ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_user)
        input_user.place(relx=0.3, rely=0.89, relheight=0.05, relwidth=0.6)

        input_password = ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_password)
        input_password.place(relx=0.3, rely=0.95, relheight=0.05, relwidth=0.6)

        self.ventana_informacion = ventana_informacion.Ventana_informacion(master)
        self.excel = excel.Excel_controller()
        self.excel2 = excel.Excel_controller()

        # Progreso por navegador: índice de la siguiente fila a procesar en self.dfs[i]
        self.progreso_navegador = {}  # se llena en ejecuccionHilo

    def ejecuccionHilo(self):
        self.ventana_informacion.write('ejecutando hilos')
        self.on_of(False)
        self.ventana_informacion.write(f'Empezando ejecuccion con {self.entry_paginas.get()} paginas')

        self.enlistar_data()
        self.enlistar_cuentas()

        # Validar número de páginas
        if self.entry_paginas.get().isnumeric():
            if int(self.entry_paginas.get()) > 10:
                self.entry_paginas.set('10')
        else:
            self.entry_paginas.set('1')

        threads = []
        self.datos_excel = []
        n = int(self.entry_paginas.get())

        # Dividir el dataframe en n partes
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

        # Inicializar progreso de cada navegador (siguiente índice a procesar)
        self.progreso_navegador = {i: 0 for i in range(n)}

        # Limpiar archivo de recargas
        self.excel.borrar('src\\recargas\\recargas.xlsx')

        # Crear hilos
        for i in range(n):
            thread = threading.Thread(target=self.ejecuccion, args=(i,))
            threads.append(thread)
            thread.start()

    def abrir_excel(self):
        self.ventana_informacion.write('excel recargas abierto recuerde cerrar antes de iniciar')
        p = Popen("src\\recargas\\openExcel.bat")
        stdout, stderr = p.communicate()

    def abrir_excel2(self):
        self.ventana_informacion.write('excel cuentas abierto recuerde cerrar antes de iniciar')
        p = Popen("src\\recargas\\openExcel2.bat")
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

    # =========================
    # Wrapper con reintentos
    # =========================
    def ejecuccion(self, i):
        """
        Ejecuta abrirPagina(i, start_index) con reintentos.
        No repite recargas ya exitosas porque reanuda desde self.progreso_navegador[i].
        """
        intento = 0
        while True:
            try:
                start = self.progreso_navegador.get(i, 0)

                if start >= len(self.dfs[i]):
                    self.ventana_informacion.write(
                        f'Navegador {i+1}: ya no hay más líneas por procesar (todo completado).'
                    )
                    break

                self.ventana_informacion.write(
                    f'Navegador {i+1}: iniciando/reanudando desde la línea {start + 1} '
                    f'de {len(self.dfs[i])}.'
                )

                self.abrirPagina(i, start)
                # Si abrirPagina termina sin lanzar excepción, significa que ya terminó
                # correctamente ese bloque de recargas.
                break

            except Exception as e:
                intento += 1
                self.ventana_informacion.write(
                    f'Navegador {i+1}: FALLO GENERAL (intento {intento}). '
                    f'Se reintentará desde la línea '
                    f'{self.progreso_navegador.get(i, 0) + 1}. Error: {e}'
                )
                time.sleep(5)  # breve pausa para no saturar

    # ==================================================
    # abrirPagina: ahora recibe start_row para reanudar
    # ==================================================
    def abrirPagina(self, i, start_row):
        ciclo = True
        contador = start_row  # índice de fila actual
        intentos = 0
        self.ventana_informacion.write(f'Navegador {i+1} abierto')

        class Abrir_pagina1(web_controller.Web_Controller):
            pass

        # --- CAMBIO 1: Reducir el sleep de 1 a 0.1 ---
        recargas = Abrir_pagina1(0.1)

        try:
            recargas.openEdge(headless=self.visible.get())
            recargas.selectPage(self.link)
            recargas.insert('loginID', self.excel2.excel['cuenta'][i], 'id')
            recargas.insert('password', self.entry_password.get(), 'id')
            recargas.click('/html/body/form[2]/table[3]/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/input[1]')

            # --- CAMBIO 2: Lógica de Login Inteligente ---
            self.ventana_informacion.write(
                f'Navegador {i+1}: Primer login enviado, verificando siguiente página...'
            )

            login_exitoso = False
            for _ in range(10):
                # Escenario A: Apareció el segundo login
                if recargas.elementExists('login_id', 'id'):
                    self.ventana_informacion.write(f'Navegador {i+1}: Segundo login detectado.')
                    recargas.insert('login_id', self.excel2.excel['cuenta'][i], 'id')
                    recargas.insert('pwd', self.entry_password.get(), 'id')
                    recargas.click('/html/body/app-root/div/app-login/div/div/div[2]/form/div[9]/button')

                    # Esperar al dashboard DESPUÉS del segundo login
                    recargas.waitExistRobust(
                        '/html/body/app-root/div/app-layout/app-sidebar/nav/div/div[2]/a[2]'
                    )
                    login_exitoso = True
                    break

                # Escenario B: Se saltó el segundo login y ya está en el dashboard
                if recargas.elementExists(
                    '/html/body/app-root/div/app-layout/app-sidebar/nav/div/div[2]/a[2]'
                ):
                    self.ventana_informacion.write(
                        f'Navegador {i+1}: Login directo al dashboard detectado.'
                    )
                    login_exitoso = True
                    break

                time.sleep(1)  # Esperar 1 seg antes de volver a comprobar

            if not login_exitoso:
                raise Exception(
                    "No se pudo detectar ni el segundo login ni el dashboard después de 10 seg."
                )

            self.ventana_informacion.write(
                f'Navegador {i+1}: Dashboard cargado. Accediendo a recargas.'
            )

            # Navegación al formulario de recargas
            recargas.click('/html/body/app-root/div/app-layout/app-sidebar/nav/div/div[2]/a[2]')
            if self.paquetes.get():
                recargas.click(
                    '/html/body/app-root/div/app-layout/section/claro-app-recharge/div/div/div[3]/div'
                    '/claro-header-recharge/ul/div[2]/li/a'
                )

        except Exception as e:
            self.ventana_informacion.write(
                f'Navegador {i+1}: Error grave durante el login o navegación inicial. {e}'
            )
            try:
                recargas.cerrar()
            except:
                pass
            # Lanzamos excepción para que ejecuccion() pueda reintentar
            raise

        # ==================================================================
        # ESPERA EXPLÍCITA ANTES DEL BUCLE
        # ==================================================================
        try:
            self.ventana_informacion.write(
                f'Navegador {i+1}: Esperando a que cargue el formulario de recarga...'
            )
            recargas.waitExist('msisdnInput', 'id')
            self.ventana_informacion.write(
                f'Navegador {i+1}: Formulario cargado. Iniciando recargas.'
            )
        except Exception as e:
            self.ventana_informacion.write(
                f'Navegador {i+1}: ERROR. No se pudo encontrar el formulario (msisdnInput) después de esperar.'
            )
            self.ventana_informacion.write(
                f'Navegador {i+1}: Se reintentará navegador completo. Error: {e}'
            )
            try:
                recargas.cerrar()
            except:
                pass
            raise
        # ==================================================================
        # FIN ESPERA
        # ==================================================================

        # ============================
        # Bucle principal de recargas
        # ============================
        while ciclo:
            if contador >= len(self.dfs[i]):
                ciclo = False
                continue

            try:
                # Fila actual a procesar
                min_str = str(self.dfs[i]['linea'][contador])
                value_str = str(self.dfs[i]['valor'][contador])

                # Ingresar MSISDN
                while True:
                    if recargas.value('msisdnInput', 'id') == min_str:
                        break
                    recargas.erase('msisdnInput', 'id')
                    recargas.fast_insert('msisdnInput', min_str, 'id')

                # Si es modalidad paquetes
                if self.paquetes.get():
                    # Seleccionar grupo
                    while True:
                        if recargas.read('groupSelect', 'id') == self.grupo.get():
                            break
                        recargas.click('groupSelect', 'id')
                        recargas.click(f".//span[text()='{self.grupo.get()}']")

                    # Seleccionar servicio
                    while True:
                        if recargas.read('subServiceSelect', 'id') == self.servicio.get():
                            break
                        recargas.click('subServiceSelect', 'id')
                        recargas.click(f".//span[text()='{self.servicio.get()}']")
                else:
                    # Monto libre
                    recargas.erase('amountInput', 'id')
                    recargas.fast_insert('amountInput', value_str, 'id')

                recargas.click('recharge', 'id')

                # Esperar a que aparezca el campo del PIN
                recargas.waitExistRobust('no-partitioned', 'id')

                # Ingresar PIN
                recargas.erase('no-partitioned', 'id')
                recargas.fast_insert('no-partitioned', self.entry_pin.get(), 'id')

                recargas.click('rechargebutton2', 'id')

                # Esperar confirmación y botón de otra recarga
                recargas.waitExistRobust('anotherRecharge', 'id')
                recargas.click('anotherRecharge', 'id')

                # Si llegó hasta aquí, la recarga se considera exitosa
                contador += 1
                self.progreso_navegador[i] = contador  # guardar el siguiente índice a procesar
                intentos = 0

                self.ventana_informacion.write(
                    f'Pagina {i+1} {round(contador / len(self.dfs[i]) * 100)}% completado'
                )

            except Exception as e:
                intentos += 1
                self.ventana_informacion.write(
                    f'Navegador {i+1}: Error en el bucle (intento {intentos}). Error: {e}'
                )

                # Si hay demasiados errores seguidos en este navegador, lanzamos excepción
                # para que el wrapper ejecuccion() rehaga todo el flujo de login.
                if intentos > 20:
                    self.ventana_informacion.write(
                        f'Navegador {i+1}: Se detiene este ciclo por exceso en intentos fallidos. '
                        f'Se reintentará navegador completo.'
                    )
                    try:
                        recargas.cerrar()
                    except:
                        pass
                    # Lanzar excepción para que ejecuccion() reintente desde self.progreso_navegador[i]
                    raise RuntimeError('Demasiados intentos consecutivos en recarga')

                # Reintento local: reiniciar sólo el navegador dentro de la misma función
                try:
                    recargas.cerrar()
                except:
                    pass

                try:
                    recargas = Abrir_pagina1(0.1)
                    recargas.openEdge(headless=self.visible.get())
                    recargas.selectPage(self.link)
                    recargas.insert('loginID', self.excel2.excel['cuenta'][i], 'id')
                    recargas.insert('password', self.entry_password.get(), 'id')
                    recargas.click(
                        '/html/body/form[2]/table[3]/tbody/tr/td/table[2]/tbody/tr[5]/td[2]/input[1]'
                    )

                    # Re-aplicar la Lógica de Login Inteligente
                    login_exitoso_reinicio = False
                    for _ in range(10):
                        if recargas.elementExists('login_id', 'id'):
                            recargas.insert('login_id', self.excel2.excel['cuenta'][i], 'id')
                            recargas.insert('pwd', self.entry_password.get(), 'id')
                            recargas.click(
                                '/html/body/app-root/div/app-login/div/div/div[2]/form/div[9]/button'
                            )
                            recargas.waitExistRobust(
                                '/html/body/app-root/div/app-layout/app-sidebar/nav/div/div[2]/a[2]'
                            )
                            login_exitoso_reinicio = True
                            break

                        if recargas.elementExists(
                            '/html/body/app-root/div/app-layout/app-sidebar/nav/div/div[2]/a[2]'
                        ):
                            login_exitoso_reinicio = True
                            break

                        time.sleep(1)

                    if not login_exitoso_reinicio:
                        raise Exception("Fallo al reiniciar el login.")

                    recargas.click(
                        '/html/body/app-root/div/app-layout/app-sidebar/nav/div/div[2]/a[2]'
                    )
                    if self.paquetes.get():
                        recargas.click(
                            '/html/body/app-root/div/app-layout/section/claro-app-recharge/div/div/div[3]/div'
                            '/claro-header-recharge/ul/div[2]/li/a'
                        )

                    recargas.waitExist('msisdnInput', 'id')
                    self.ventana_informacion.write(
                        f'Navegador {i+1}: Reinicio de navegador completado.'
                    )

                except Exception as e_reinicio:
                    self.ventana_informacion.write(
                        f'Navegador {i+1}: Fallo crítico durante el reinicio local. {e_reinicio}'
                    )
                    # Dejamos que el while continúe e intente de nuevo,
                    # o termine alcanzando intentos > 20 y levante excepción.

        self.ventana_informacion.write(f'Proceso terminado para navegador {i+1}')
        try:
            recargas.cerrar()
        except:
            pass

    def enlistar_data(self):
        self.excel.leer_excel('src\\recargas\\recargas.xlsx', 'linea')

    def enlistar_cuentas(self):
        self.excel2.leer_excel('src\\recargas\\cuentas.xlsx', 'numero')
