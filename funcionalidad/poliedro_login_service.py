import time
import re
import traceback
from funcionalidad.web_controller import Web_Controller

class LoginService:
    """
    Servicio reutilizable para el login automatizado en Poliedro
    """
    
    def __init__(self, web_controller: Web_Controller, ventana_informacion=None):
        """
        Inicializa el servicio de login
        
        Args:
            web_controller: Instancia del controlador web (navegador)
            ventana_informacion: Ventana para mostrar mensajes (opcional)
        """
        self.web_controller: Web_Controller = web_controller
        self.ventana_informacion = ventana_informacion
        self.usuario = ""
        self.password = ""
        self.max_otp_attempts = 3
        self.otp_timeout = 60  # segundos para esperar OTP
        
        # ✅ CONFIGURACIÓN DE REINTENTOS
        self.max_login_attempts = 4  # Número máximo de intentos de login
        self.retry_interval = 120  # Intervalo entre reintentos (2 minutos)
        
    def configurar_credenciales(self, usuario, password):
        """
        Configura las credenciales de login
        
        Args:
            usuario (str): Usuario de Poliedro
            password (str): Contraseña de Poliedro
        """
        self.usuario = usuario
        self.password = password
        
    def login_automatico(self):
        """
        Ejecuta el proceso completo de login automatizado con reintentos
        
        Returns:
            bool: True si el login fue exitoso, False en caso contrario
        """
        # ✅ SISTEMA DE REINTENTOS
        for intento in range(self.max_login_attempts):
            try:
                self._log_message(f"🔄 Intento de login {intento + 1}/{self.max_login_attempts}")
                
                # Validar que se hayan configurado las credenciales
                if not self.usuario or not self.password:
                    self._log_message("❌ Error: Credenciales no configuradas", is_error=True)
                    return False
                    
                # Asegurarse de estar en la pantalla de login
                if not self._asegurar_pantalla_login():
                    self._log_message(f"❌ Error asegurando pantalla de login en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                
                # ✅ LIMPIAR ESTADO DEL FORMULARIO
                self._limpiar_estado_login()
                
                # Paso 1: Ingresar credenciales
                if not self._ingresar_credenciales():
                    self._log_message(f"❌ Error ingresando credenciales en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                    
                # Paso 2: Obtener código OTP
                codigo_otp = self._obtener_codigo_otp()
                if not codigo_otp:
                    self._log_message(f"❌ Error obteniendo código OTP en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                    
                # Paso 3: Ingresar código OTP
                if not self._ingresar_codigo_otp(codigo_otp):
                    self._log_message(f"❌ Error ingresando código OTP en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                    
                # Paso 4: Validar login exitoso
                if self._detectar_login_invalido():
                    self._log_message(f"❌ Login inválido en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                    
                # ✅ LOGIN EXITOSO
                self._log_message(f"✅ Login exitoso en intento {intento + 1}")
                return True
                
            except Exception as e:
                self._log_error(f"login_automatico_intento_{intento + 1}", e)
                if intento < self.max_login_attempts - 1:
                    self._log_message(f"⚠️ Error en intento {intento + 1}, reintentando...")
                    self._esperar_antes_reintentar()
                    continue
                
        # ❌ TODOS LOS INTENTOS FALLARON
        self._log_message(f"❌ Login falló después de {self.max_login_attempts} intentos", is_error=True)
        return False
    
    def _ingresar_credenciales(self):
        """
        Ingresa usuario y contraseña en el formulario de login
        
        Returns:
            bool: True si fue exitoso, False en caso contrario
        """
        try:
            self._log_message("🔐 Ingresando credenciales...")
            
            # Ingresar usuario
            self.web_controller.write('ctl00_ContentPlaceHolder1_txtUsuario', self.usuario, 'id')
            
            # Ingresar contraseña
            self.web_controller.write('ctl00_ContentPlaceHolder1_txtContraseña', self.password, 'id')
            
            # Esperar un momento antes de hacer clic
            time.sleep(2)
            
            # Hacer clic en el botón de login
            self.web_controller.click('btnIngresarUsuarioContraseña', 'id')
            
            # Esperar a que aparezca el formulario de OTP
            time.sleep(7)
            
            return True
            
        except Exception as e:
            self._log_error("_ingresar_credenciales", e)
            return False
    
    def _obtener_codigo_otp(self):
        """
        Obtiene el código OTP de la pestaña de MySMS
        
        Returns:
            str: Código OTP o None si no se pudo obtener
        """
        try:
            self._log_message("📱 Obteniendo código OTP...")
            
            # Cambiar a la pestaña de MySMS
            self.web_controller.cambiar_pestaña()
            
            # Esperar a que llegue el SMS
            time.sleep(3)
            
            # Intentar obtener el código OTP
            for intento in range(self.max_otp_attempts):
                try:
                    # Leer el contenido del SMS
                    sms_content = self.web_controller.read(
                        '//div[1]/span/span[2][contains(text(),"Su codigo OTP")]', 
                        'xpath'
                    )
                    
                    # Extraer el código usando regex
                    match = re.search(r"\b\d{6,10}\b", sms_content)
                    if match:
                        codigo = match.group()
                        self._log_message(f"✅ Código OTP obtenido: {codigo}")
                        return codigo
                        
                except Exception as e:
                    self._log_message(f"⚠️ Intento OTP {intento + 1}/{self.max_otp_attempts} fallido, reintentando...")
                    if intento < self.max_otp_attempts - 1:
                        time.sleep(10)  # Esperar antes de reintentar
                    
            self._log_message("❌ No se pudo obtener el código OTP después de varios intentos", is_error=True)
            return None
            
        except Exception as e:
            self._log_error("_obtener_codigo_otp", e)
            return None
    
    def _ingresar_codigo_otp(self, codigo_otp):
        """
        Ingresa el código OTP en el formulario
        
        Args:
            codigo_otp (str): Código OTP a ingresar
            
        Returns:
            bool: True si fue exitoso, False en caso contrario
        """
        try:
            self._log_message(f"🔑 Ingresando código OTP: {codigo_otp}")
            
            # Volver a la pestaña principal
            self.web_controller.volver_pestaña()
            time.sleep(2)
            
            # Ingresar el código OTP
            self.web_controller.write('ctl00_ContentPlaceHolder1_txtTokenEntrust', codigo_otp, 'id')
            time.sleep(1)
            
            # Hacer clic en el botón de login con OTP
            self.web_controller.click('ctl00_ContentPlaceHolder1_BtnLoginTokenEntrust', 'id')
            time.sleep(3)
            
            return True
            
        except Exception as e:
            self._log_error("_ingresar_codigo_otp", e)
            return False
    
    def _detectar_login_invalido(self):
        """
        Detecta si el login ha fallado por credenciales inválidas
        
        Returns:
            bool: True si el login es inválido, False en caso contrario
        """
        try:
            error_element = ''
            
            # Intentar leer el mensaje de error
            try:
                error_element = self.web_controller.read('ctl00_ContentPlaceHolder1_lbMensaje', 'id')
            except:
                try:
                    error_element = self.web_controller.read(
                        '//*[@id="ctl00_ContentPlaceHolder1_lbMensaje"][contains(text(), "invalid_user_response")]', 
                        'xpath'
                    )
                except:
                    pass
            
            # Si hay un error de usuario inválido
            if error_element and "invalid_user_response" in error_element:
                self._log_message(f"❌ Error en login: {error_element}", is_error=True)
                
                # Hacer clic en el botón de regresar
                try:
                    self.web_controller.click('ctl00_ContentPlaceHolder1_BtnRegresarMensaje', 'id')
                except:
                    pass
                    
                return True
                
            return False
            
        except Exception as e:
            self._log_error("_detectar_login_invalido", e)
            return False
    
    def _log_message(self, mensaje, is_error=False):
        """
        Registra un mensaje en la ventana de información
        
        Args:
            mensaje (str): Mensaje a registrar
            is_error (bool): Si es un mensaje de error
        """
        if self.ventana_informacion:
            self.ventana_informacion.write(mensaje)
        else:
            print(mensaje)
    
    def _log_error(self, contexto, error):
        """
        Registra un error en el log
        
        Args:
            contexto (str): Contexto donde ocurrió el error
            error (Exception): Excepción capturada
        """
        error_msg = f"Error en {contexto}: {str(error)}"
        self._log_message(error_msg, is_error=True)
        
        # Guardar en archivo de log
        with open("login_service_errors.txt", "a", encoding="utf-8") as f:
            f.write(f"\n[{contexto}] Error: {str(error)}\n")
            f.write(traceback.format_exc())
    
    def validar_sesion_activa(self):
        """
        Valida si la sesión sigue activa
        
        Returns:
            bool: True si la sesión está activa, False en caso contrario
        """
        try:
            # Verificar elementos que indican sesión activa
            # Esto deberías adaptarlo según los elementos específicos de tu aplicación
            session_indicators = [
                ("input", "botonLoginhomePoliedro")  # Si este elemento existe, no hay sesión
            ]
            
            html_content = self.web_controller.retornarHtml()
            from funcionalidad import scraping
            
            scrap = scraping.Scraping(html_content)
            soup = scrap.soup
            
            # Si encuentra elementos de login, la sesión no está activa
            for tag, id_value in session_indicators:
                if soup.find(tag, id=id_value):
                    return False
                    
            return True
            
        except Exception as e:
            self._log_error("validar_sesion_activa", e)
            return False
    
    def _esperar_antes_reintentar(self):
        """
        Espera antes de reintentar el login
        """
        minutos = self.retry_interval / 60
        self._log_message(f"⏳ Esperando {minutos:.1f} minutos antes del siguiente intento...")
        
        # Mostrar cuenta regresiva cada 30 segundos
        for i in range(self.retry_interval, 0, -30):
            if i <= 30:
                self._log_message(f"⏳ Reintentando en {i} segundos...")
                time.sleep(i)
                break
            else:
                self._log_message(f"⏳ Reintentando en {i//60}:{i%60:02d} minutos...")
                time.sleep(30)
    
    def configurar_reintentos(self, max_intentos=4, intervalo_minutos=2):
        """
        Configura los parámetros de reintentos
        
        Args:
            max_intentos (int): Número máximo de intentos
            intervalo_minutos (int): Intervalo entre reintentos en minutos
        """
        self.max_login_attempts = max_intentos
        self.retry_interval = intervalo_minutos * 60
        self._log_message(f"🔧 Configurados {max_intentos} intentos con intervalo de {intervalo_minutos} minutos")
    
    def _asegurar_pantalla_login(self):
        """
        Asegura que el navegador esté en la pantalla de login antes de intentar autenticar
        
        Returns:
            bool: True si está en la pantalla de login, False en caso contrario
        """
        try:
            self._log_message("🔍 Verificando pantalla de login...")
            
            # Verificar si ya estamos en la pantalla de login
            if self._detectar_pantalla_login():
                self._log_message("✅ Ya estoy en la pantalla de login")
                return True
            
            # Si no estamos en login, navegar a la página principal
            self._log_message("🔄 Navegando a la página de login...")
            
            # Navegar a la URL de login
            login_url = 'https://poliedrodist.comcel.com.co/'
            self.web_controller.selectPage(login_url)
            time.sleep(5)
            
            # Verificar que llegamos a la pantalla de login
            if self._detectar_pantalla_login():
                self._log_message("✅ Navegación exitosa a la pantalla de login")
                return True
            else:
                self._log_message("❌ No se pudo navegar a la pantalla de login", is_error=True)
                return False
                
        except Exception as e:
            self._log_error("_asegurar_pantalla_login", e)
            return False
    
    def _detectar_pantalla_login(self):
        """
        Detecta si estamos en la pantalla de login
        
        Returns:
            bool: True si estamos en la pantalla de login, False en caso contrario
        """
        try:
            # Obtener HTML actual
            html_content = self.web_controller.retornarHtml()
            from funcionalidad import scraping
            
            scrap = scraping.Scraping(html_content)
            soup = scrap.soup
            
            # Elementos que indican que estamos en la pantalla de login
            login_indicators = [
                ("input", "ctl00_ContentPlaceHolder1_txtUsuario"),
                ("input", "ctl00_ContentPlaceHolder1_txtContraseña"), 
                ("input", "btnIngresarUsuarioContraseña")
            ]
            
            # Verificar que todos los elementos de login estén presentes
            for tag, id_value in login_indicators:
                if not soup.find(tag, id=id_value):
                    return False
                    
            return True
            
        except Exception as e:
            self._log_error("_detectar_pantalla_login", e)
            return False
    
    def _limpiar_estado_login(self):
        """
        Limpia el estado del formulario de login para un nuevo intento
        """
        try:
            self._log_message("🧹 Limpiando estado del formulario...")
            
            # Limpiar campos de texto
            self.web_controller.write('ctl00_ContentPlaceHolder1_txtUsuario', '', 'id')
            self.web_controller.write('ctl00_ContentPlaceHolder1_txtContraseña', '', 'id')
            
            # Si hay campo de OTP, también limpiarlo
            try:
                self.web_controller.write('ctl00_ContentPlaceHolder1_txtTokenEntrust', '', 'id')
            except:
                pass  # El campo OTP podría no estar visible
                
            time.sleep(1)
            
        except Exception as e:
            self._log_error("_limpiar_estado_login", e)