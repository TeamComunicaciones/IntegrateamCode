from selenium.webdriver.chrome.service import Service as ChromeService
import chromedriver_autoinstaller
from selenium import webdriver
from tkinter import *
import time
import requests
import urllib.request
import os
import zipfile
import winreg
import subprocess
from io import BytesIO
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.edge.service import Service
import random
import traceback
import threading # <-- 1. Importar threading

# --- 2. Añadir un Lock global ---
# Este "candado" se asegurará de que solo un hilo a la vez
# pueda ejecutar la sección de "descargar driver".
driver_lock = threading.Lock()

# --- 3. NUEVO: Variable Caché ---
# Guardará la ruta del driver una vez que el primer hilo la verifique.
driver_path_cache = None


class Web_Controller:

    def __init__(self, sleeptime):
        global sleep
        sleep = sleeptime
        global aleatorio
        aleatorio = False
        self.browser = None
    
    def actualizarIntervalo(self, valor, aleatorio_value=False):
        global sleep
        sleep = valor
        global aleatorio
        aleatorio = aleatorio_value

    def script(self, str):
        self.browser.execute_script(str)
    
    def retornarHtml(self):
        return self.browser.page_source

    def chromedriver(self):
        chromedriver_autoinstaller.install()

    def get_edge_version(self):
        """Obtiene la versión de Microsoft Edge instalada"""
        # Intenta primero con HKEY_CURRENT_USER
        try:
            path = r"SOFTWARE\Microsoft\Edge\BLBeacon"
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
            version, _ = winreg.QueryValueEx(registry_key, "version")
            winreg.CloseKey(registry_key)
            return version
        except FileNotFoundError:
            # Fallback a HKEY_LOCAL_MACHINE si la primera clave no existe
            try:
                path = r"SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{56EB18F8-B008-4CBD-B6D2-8C97FE7E9062}"
                registry_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ)
                version, _ = winreg.QueryValueEx(registry_key, "pv")
                winreg.CloseKey(registry_key)
                return version
            except Exception as e:
                print(f"[ERROR] No se pudo obtener la versión de Edge desde el registro: {e}")
                return None
    
    def get_driver_version(self, driver_path):
        """Obtiene la versión del driver si ya existe"""
        try:
            result = subprocess.run([driver_path, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                 # La salida es algo como "Microsoft Edge WebDriver 120.0.2210.133 ..."
                return result.stdout.split()[3]
        except Exception:
            return None
        return None
    
    def ensure_msedgedriver(self):
        """Verifica si el driver es compatible con Edge; si no, lo descarga"""
        
        # --- 4. Acceder a la variable caché global ---
        global driver_path_cache
        
        # --- 5. Usar el Lock ---
        # Solo un hilo puede "sostener el candado" a la vez.
        with driver_lock:
            # --- 6. Comprobar la caché PRIMERO ---
            # Si el primer hilo ya verificó el driver, los otros hilos
            # simplemente obtendrán la ruta y saldrán inmediatamente.
            if driver_path_cache:
                return driver_path_cache

            # --- Si la caché está vacía, este es el PRIMER HILO ---
            project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            dest_folder = os.path.join(project_root, "drivers")
            os.makedirs(dest_folder, exist_ok=True)

            edge_version = self.get_edge_version()
            if not edge_version:
                 raise Exception("No se pudo detectar la versión de Microsoft Edge.")
                 
            major_edge = edge_version.split(".")[0]
            driver_path = os.path.join(dest_folder, "msedgedriver.exe")

            # Si ya existe y es compatible
            if os.path.exists(driver_path):
                driver_version = self.get_driver_version(driver_path)
                if driver_version and driver_version.split(".")[0] == major_edge:
                    # --- 7. Guardar en caché y retornar ---
                    driver_path_cache = driver_path # Guardar en caché
                    return driver_path
                else:
                    print(f"[INFO] Driver desactualizado (Driver: {driver_version}, Edge: {edge_version}), descargando nuevo...")

            # (Lógica de descarga...)
            url = f"https://msedgedriver.azureedge.net/{edge_version}/edgedriver_win64.zip"
            resp = requests.get(url, stream=True)

            if resp.status_code != 200:
                print(f"[WARN] No se encontró el driver exacto {edge_version}, buscando LATEST_STABLE para {major_edge}...")
                # URL alternativa para obtener la última versión estable del major
                latest_url = f"https.msedgedriver.azureedge.net/LATEST_RELEASE_{major_edge}_WIN"
                latest_resp = requests.get(latest_url)
                
                if latest_resp.status_code != 200:
                     # Fallback aún más genérico si el major falla
                     latest_url = "https.msedgedriver.azureedge.net/LATEST_STABLE"
                     print(f"[WARN] No se encontró LATEST_RELEASE para {major_edge}, buscando LATEST_STABLE...")
                     latest_resp = requests.get(latest_url)
                     if latest_resp.status_code != 200:
                         raise Exception(f"No se pudo obtener driver para Edge {major_edge}")
                
                # El contenido de la respuesta puede tener caracteres extra (BOM)
                driver_version = latest_resp.content.decode('utf-16-le', errors='ignore').strip()
                print(f"[INFO] Versión del driver a descargar: {driver_version}")

                url = f"https://msedgedriver.azureedge.net/{driver_version}/edgedriver_win64.zip"
                resp = requests.get(url, stream=True)

            if resp.status_code != 200:
                raise Exception(f"No se pudo descargar driver desde {url}")

            zip_path = os.path.join(dest_folder, "edgedriver.zip")
            with open(zip_path, "wb") as f:
                for chunk in resp.iter_content(1024):
                    f.write(chunk)

            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(dest_folder)
            except zipfile.BadZipFile:
                 raise Exception(f"El archivo descargado de {url} está corrupto o no es un ZIP.")
            
            os.remove(zip_path)

            # --- 8. Guardar en caché después de descargar y retornar ---
            driver_path_cache = driver_path
            return driver_path
        # El "lock" se libera automáticamente aquí
    
    #def edgedriver(self):
    #     response = requests.get('https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/LATEST_STABLE')
    #     latest_version = response.text.strip()
    #     print(latest_version)
    #     url = f'https://msedgedriver.azureedge.net/{latest_version}/edgedriver_win64.zip'
    #     response = urllib.request.urlopen(url)
    #     zipfile.ZipFile(BytesIO(response.read())).extractall(os.getcwd())
    #     os.environ['PATH'] += os.pathsep + os.getcwd()

    # def get_driver(self, headless: bool = False):
    #     opts = Options()
    #     if self.headless:
    #         opts.add_argument("--headless=new")

    #     return webdriver.Edge(options=opts)

    def validate(funcion):
        def execute(self,*args, **kwargs):
            proof = True
            contador = 1
            while proof:
                try:
                    data = funcion(self,*args, **kwargs)
                    proof= False
                    if aleatorio:
                        randomTime = round(random.uniform(-0.15,1.15),2)
                    else:
                        randomTime = 0
                    
                    # Asegurarnos de que sleep no sea negativo si randomTime es -0.15 y sleep es 0.1
                    sleep_time = float(sleep) + randomTime
                    if sleep_time < 0:
                        sleep_time = 0
                        
                    time.sleep(sleep_time)
                    return data
                except Exception as err:
                    if contador < 8:
                        time.sleep(1)
                        contador +=1
                    else:
                        print(f'Excedio los intentos para la funcion con argumentos: {args}')
                        raise err
        return execute
    
    def validateShort(funcion):
        def execute(self,*args, **kwargs):
            proof = True
            contador = 1
            while proof:
                try:
                    data = funcion(self,*args, **kwargs)
                    proof= False
                    time.sleep(float(sleep)) # Usar float() para aceptar decimales
                    return data
                except Exception as e:
                    if contador < 5:
                        print(f'intento numero {contador}')
                        time.sleep(1)
                        contador +=1
                    else:
                        raise Exception('Excedio el numero de intentos (short)') from e
        return execute
    
    def validateShort2(funcion):
        def execute(self,*args, **kwargs):
            proof = True
            contador = 1
            while proof:
                try:
                    data = funcion(self,*args, **kwargs)
                    proof= False
                    time.sleep(float(sleep)) # Usar float() para aceptar decimales
                    return data
                except Exception as e:
                    if contador < 3:
                        print(f'intento numero {contador}')
                        time.sleep(1)
                        contador +=1
                    else:
                        raise Exception('Excedio el numero de intentos (short2)') from e
        return execute
    
    def openEdgeModeExplorer(self):
        options = webdriver.IeOptions()
        driver = webdriver.Ie(options=options)
        driver.get("http://www.google.com")
        driver.quit()
    
    def openChrome(self):
        service = ChromeService('chromedriver')
        options =  webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(chrome_options= options)
    
    def isBrowserOpen(self):
        try:
            self.browser.title
            return True
        except WebDriverException:
            return False
    
    def openEdge(self, headless = False):
        driver_path = self.ensure_msedgedriver()

        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Evitar logs innecesarios en la consola
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        if headless:
            options.add_argument("--headless=new")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        
        # Usar 'executable_path' que es lo que 'msedge.selenium_tools' espera
        self.browser = Edge(executable_path=driver_path, options=options)
        self.browserOriginal = self.browser
        return self.browser

    def openEdgeModeIE(self, headless = False):
        ieOptions = webdriver.IeOptions()
        ieOptions.add_additional_option("ie.edgechromium", True)
        ieOptions.add_additional_option("ie.edgepath",'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
        
        # Usar 'executable_path' para IEDriverServer
        self.browser = webdriver.Ie(executable_path='IEDriverServer.exe', options=ieOptions)
        self.browserOriginal = self.browser
    
    def crearNavegador(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("start-maximized")
        
        # Usar 'executable_path'
        driver_path = self.ensure_msedgedriver()
        return Edge(executable_path=driver_path, options=options)

    @validateShort2
    def listarElemetos(self, byStr, by='xpath', click=None):
        list_data = []
        if by == "xpath": find = self.browser.find_elements_by_xpath(byStr)
        elif by == "id": find = self.browser.find_elements_by_id(byStr)
        elif by == "name": find = self.browser.find_elements_by_name(byStr)
        else: find = [] # Asegurar que 'find' sea iterable
            
        if find is not None:
            for item in find:
                name = item.text
                if click is not None:
                    if name == click:
                        item.click()
                        break
                list_data.append(name)
        return list_data

    @validate
    def selectPage(self, link):
        self.browser.get(link)

    def getCookies(self):
        cookies = self.browser.get_cookies()
        if cookies:
            cookie_text = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        return cookie_text
    
    @validate
    def insert(self, byStr, text, by='xpath', enter =False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            find.send_keys(text)
            if enter:
                find.send_keys(Keys.ENTER)

    # --- CAMBIO IMPORTANTE: Disparar eventos de JS ---
    @validate
    def fast_insert(self, byStr, text, by='xpath'):
        """Inserta texto instantáneamente usando JavaScript y dispara eventos."""
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
        
        if find is not None:
            # Establecer el valor
            self.browser.execute_script("arguments[0].value = arguments[1];", find, text)
            # Disparar evento 'input' para que la página (React/Angular) detecte el cambio
            self.browser.execute_script("arguments[0].dispatchEvent(new Event('input', { 'bubbles': true }));", find)
            # Disparar evento 'change' por si acaso
            self.browser.execute_script("arguments[0].dispatchEvent(new Event('change', { 'bubbles': true }));", find)


    @validate
    def select(self, byStr, text, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            selection = Select(find)
            selection.select_by_value(text)
    
    @validate
    def click(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            find.click()

    @validate
    def js_click(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
        if find is not None:
            self.browser.execute_script("arguments[0].click();", find)
    
    @validate
    def click_ctr(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
        if find is not None:
            ActionChains(self.browser).key_down(Keys.CONTROL).click(find).key_up(Keys.CONTROL).perform()
    
    def cambiar_pestaña(self):
        if len(self.browser.window_handles) > 1:
            self.browser.switch_to.window(self.browser.window_handles[-1])
    
    def volver_pestaña(self):
        if len(self.browser.window_handles) > 0:
            self.browser.switch_to.window(self.browser.window_handles[0])
    
    def cerrar_pestaña(self):
        self.browser.close()
    
    @validateShort2
    def leer_txt(self):
        texto_elemento = self.browser.find_element_by_xpath("/html/body/pre")
        return texto_elemento.text

    @validateShort2
    def readShort2(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        elif by == "class": find = self.browser.find_element_by_class_name(byStr)
        else: find = None

        if find is not None:
            return find.text
        else: return "none"
    
    @validateShort
    def readShort(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None

        if find is not None:
            return find.text
        else: return "none"
    
    @validate
    def read(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        elif by == "class": find = self.browser.find_element_by_class_name(byStr)
        else: find = None

        if find is not None:
            return find.text
        else: return "none"

    @validate
    def readMulty(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_elements_by_xpath(byStr)
        elif by == "id": find = self.browser.find_elements_by_id(byStr)
        elif by == "name": find = self.browser.find_elements_by_name(byStr)
        elif by == "class": find = self.browser.find_elements_by_class_name(byStr)
        else: find = [] # Asegurar que 'find' sea iterable
            
        if find is not None:
            return [i.text for i in find]
        else: return "none"
    
    @validate
    def value(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None

        if find is not None:
            return find.get_attribute('value')
        else: return "none"

    @validate
    def style(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None

        if find is not None:
            return find.get_attribute('style')
        else: return "none"

    def readNoValidate(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None

        if find is not None:
            return find.text
        else: return "none"
    
    @validateShort2
    def waitExist2(self, byStr, by='xpath', write=False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
            
        if find is not None:
            if write:
                find.send_keys('')
            pass
        else: raise Exception(f"Elemento no encontrado: {byStr}") # Levantar excepción

    @validateShort
    def waitExist(self, byStr, by='xpath', write=False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
            
        if find is not None:
            if write:
                find.send_keys('')
            pass
        else: raise Exception(f"Elemento no encontrado: {byStr}") # Levantar excepción

    @validate
    def waitExistRobust(self, byStr, by='xpath', write=False):
        """Versión de waitExist con el decorador @validate (más reintentos)."""
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
            
        if find is not None:
            if write:
                find.send_keys('')
            pass
        else: raise Exception(f"Elemento no encontrado (Robust): {byStr}") # Levantar excepción

    @validate
    def wait(self, byStr, condition ,by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
            
        if find is not None:
            if find.text is not None:
                if condition in find.text:
                    raise Exception(f"Condición de espera encontrada: {condition}") # Levantar excepción
    
    # --- CAMBIO IMPORTANTE: Disparar eventos de JS ---
    @validate
    def erase(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            #find.clear() <-- 'clear()' a veces no dispara eventos
            # Usar la misma técnica que fast_insert para borrar
            self.browser.execute_script("arguments[0].value = '';", find)
            self.browser.execute_script("arguments[0].dispatchEvent(new Event('input', { 'bubbles': true }));", find)
            self.browser.execute_script("arguments[0].dispatchEvent(new Event('change', { 'bubbles': true }));", find)

    
    @validate
    def eraseLetter(self, byStr, cantidad, by='xpath', move=False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            for i in range(0,cantidad):
                if move:
                    find.send_keys(Keys.ARROW_RIGHT)
                find.send_keys(Keys.BACKSPACE)

    @validate
    def write(self, byStr, keys, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None and keys is not None:
            find.send_keys(keys)

    @validate
    def getCurrentUrl(self):
        """Retorna la URL actual del navegador con validación"""
        if self.browser is not None:
            return self.browser.current_url
        return None # Retornar None si el navegador no existe
    
    def readonly(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
            
        if find is not None:
            readonly_value = find.get_attribute('readonly')
            if readonly_value == 'readonly' or readonly_value == 'true': # Ser más flexible
                return True
            else:
                return False
        else: return None
    
    def selectDown(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
            
        if find is not None:
            find.send_keys(Keys.ARROW_DOWN)
            find.send_keys(Keys.ENTER)
    
    def browserGet(self):
        return self.browser
    
    def elementExists(self, byStr, by='xpath'):
        """
        Verifica si un elemento existe en la página sin lanzar excepciones.
        
        Args:
            byStr (str): El identificador del elemento (xpath, id, name)
            by (str): Tipo de búsqueda ('xpath', 'id', 'name'). Por defecto 'xpath'
            
        Returns:
            bool: True si el elemento existe, False si no existe
        """
        try:
            if by == "xpath": 
                self.browser.find_element_by_xpath(byStr)
            elif by == "id": 
                self.browser.find_element_by_id(byStr)
            elif by == "name": 
                self.browser.find_element_by_name(byStr)
            else:
                return False
            return True
        except:
            return False
    
    def cerrar(self):
        # --- 9. Mejora de seguridad ---
        # Verificar si el navegador existe antes de cerrarlo
        if self.browser:
            try:
                self.browser.close()
                self.browser.quit()
            except WebDriverException as e:
                print(f"[WARN] Excepción al cerrar el navegador (puede ser normal si ya estaba cerrado): {e}")
            finally:
                self.browser = None