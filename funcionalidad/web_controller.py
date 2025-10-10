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
        path = r"SOFTWARE\Microsoft\Edge\BLBeacon"
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_READ)
        version, _ = winreg.QueryValueEx(registry_key, "version")
        return version
    
    def get_driver_version(self, driver_path):
        """Obtiene la versión del driver si ya existe"""
        try:
            result = subprocess.run([driver_path, "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.split()[1]
        except Exception:
            return None
        return None
    
    def ensure_msedgedriver(self):
        """Verifica si el driver es compatible con Edge; si no, lo descarga"""
        # --- Carpeta drivers en la raíz del proyecto ---
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        dest_folder = os.path.join(project_root, "drivers")
        os.makedirs(dest_folder, exist_ok=True)

        edge_version = self.get_edge_version()
        major_edge = edge_version.split(".")[0]
        driver_path = os.path.join(dest_folder, "msedgedriver.exe")

        # Si ya existe y es compatible
        if os.path.exists(driver_path):
            driver_version = self.get_driver_version(driver_path)
            if driver_version and driver_version.split(".")[0] == major_edge:
                return driver_path
            else:
                print("[INFO] Driver desactualizado, descargando nuevo...")

        # Intentar descargar el driver de la misma versión de Edge
        url = f"https://msedgedriver.microsoft.com/{edge_version}/edgedriver_win64.zip"
        resp = requests.get(url, stream=True)

        # Si no está disponible, descargar el último release del mismo major version
        if resp.status_code != 200:
            print(f"[WARN] No encontrado driver exacto {edge_version}, buscando LATEST_RELEASE_{major_edge}...")
            latest_url = f"https://msedgedriver.microsoft.com/LATEST_RELEASE_{major_edge}"
            latest_resp = requests.get(latest_url)
            if latest_resp.status_code != 200:
                raise Exception(f"No se pudo obtener driver para Edge {major_edge}")
            driver_version = latest_resp.text.strip()
            url = f"https://msedgedriver.microsoft.com/{driver_version}/edgedriver_win64.zip"
            resp = requests.get(url, stream=True)

        if resp.status_code != 200:
            raise Exception(f"No se pudo descargar driver desde {url}")

        # Guardar zip temporal
        zip_path = os.path.join(dest_folder, "edgedriver.zip")
        with open(zip_path, "wb") as f:
            for chunk in resp.iter_content(1024):
                f.write(chunk)

        # Extraer
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(dest_folder)
        os.remove(zip_path)

        return driver_path
    
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
                    time.sleep(int(float(sleep) + randomTime))
                    return data
                except Exception as err:
                    if contador < 8:
                        time.sleep(1)
                        contador +=1
                    else:
                        print(f'Excedio los intentos para la funcion con argumentos: {args}')
                        # <-- CAMBIO: Se corrige el 'raise' para lanzar una excepción válida.
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
                    time.sleep(int(sleep))
                    return data
                except Exception as e: # <-- CAMBIO: Captura la excepción para poder relanzarla.
                    if contador < 5:
                        print(f'intento numero {contador}')
                        time.sleep(1)
                        contador +=1
                    else:
                        # <-- CAMBIO: Se corrige el 'raise' para lanzar una excepción válida.
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
                    time.sleep(int(sleep))
                    return data
                except Exception as e: # <-- CAMBIO: Captura la excepción para poder relanzarla.
                    if contador < 3:
                        print(f'intento numero {contador}')
                        time.sleep(1)
                        contador +=1
                    else:
                        # <-- CAMBIO: Se corrige el 'raise' para lanzar una excepción válida.
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
        if headless:
            options.add_argument("--headless=new")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        self.browser = Edge(executable_path=driver_path, options=options)
        self.browserOriginal = self.browser
        return self.browser

    def openEdgeModeIE(self, headless = False):
        ieOptions = webdriver.IeOptions()
        ieOptions.add_additional_option("ie.edgechromium", True)
        ieOptions.add_additional_option("ie.edgepath",'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
        self.browser = webdriver.Ie(executable_path='IEDriverServer.exe', options=ieOptions)
        self.browserOriginal = self.browser
    
    def crearNavegador(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("start-maximized")
        return Edge(executable_path='msedgedriver.exe', options=options)

    @validateShort2
    def listarElemetos(self, byStr, by='xpath', click=None):
        list_data = []
        if by == "xpath": find = self.browser.find_elements_by_xpath(byStr)
        elif by == "id": find = self.browser.find_elements_by_id(byStr)
        elif by == "name": find = self.browser.find_elements_by_name(byStr)
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

    # <-- NUEVA FUNCIÓN: Se añade js_click para manejar clics interceptados.
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
        self.browser.switch_to.window(self.browser.window_handles[-1])
    
    def volver_pestaña(self):
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
        if find is not None:
            return find.text
        else: return "none"
    
    @validateShort
    def readShort(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            return find.text
        else: return "none"
    
    @validate
    def read(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        elif by == "class": find = self.browser.find_element_by_class_name(byStr)
        if find is not None:
            return find.text
        else: return "none"

    @validate
    def readMulty(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_elements_by_xpath(byStr)
        elif by == "id": find = self.browser.find_elements_by_id(byStr)
        elif by == "name": find = self.browser.find_elements_by_name(byStr)
        elif by == "class": find = self.browser.find_elements_by_class_name(byStr)
        if find is not None:
            return [i.text for i in find]
        else: return "none"
    
    @validate
    def value(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            return find.get_attribute('value')
        else: return "none"

    @validate
    def style(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            return find.get_attribute('style')
        else: return "none"

    def readNoValidate(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            return find.text
        else: return "none"
    
    @validateShort2
    def waitExist2(self, byStr, by='xpath', write=False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            if write:
                find.send_keys('')
            pass
        else: raise('')

    @validateShort
    def waitExist(self, byStr, by='xpath', write=False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            if write:
                find.send_keys('')
            pass
        else: raise('')

    @validate
    def wait(self, byStr, condition ,by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            if find.text is not None:
                if condition in find.text:
                    raise('error')
    
    @validate
    def erase(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            find.clear()
    
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
    
    def readonly(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            readonly_value = find.get_attribute('readonly')
            if readonly_value == 'readonly':
                return True
            else:
                return False
        else: return None
    
    def selectDown(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
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
        self.browser.close()
        self.browser.quit()