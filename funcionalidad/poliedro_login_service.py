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
        self.max_otp_attempts = 2  # Número máximo de intentos para obtener el OTP
        self.otp_timeout = 60  # segundos para esperar OTP
        
        # CONFIGURACIÓN DE REINTENTOS
        self.max_login_attempts = 2  # Número máximo de intentos de login
        self.retry_interval = 120  # Intervalo entre reintentos (2 minutos)

        # Configuracion del portal para extraer la OPT
        self.mysms_portal = False  # Si se usa MySMS para obtener el OTP
        self.google_messages_portal = False  # Si se usa Google Messages para obtener el OTP

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
        # SISTEMA DE REINTENTOS
        for intento in range(self.max_login_attempts):
            try:
                self._log_message(f"🔄 Intento de login {intento + 1}/{self.max_login_attempts}")
                
                # Validar que se hayan configurado las credenciales
                if not self.usuario or not self.password:
                    self._log_message("Error: Credenciales no configuradas", is_error=True)
                    return False
                    
                # Asegurarse de estar en la pantalla de login
                if not self._asegurar_pantalla_login():
                    self._log_message(f"Error asegurando pantalla de login en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                
                # LIMPIAR ESTADO DEL FORMULARIO
                self._limpiar_estado_login()
                
                # Paso 1: Ingresar credenciales
                if not self._ingresar_credenciales():
                    self._log_message(f"Error ingresando credenciales en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                    
                # Paso 2: Obtener código OTP
                codigo_otp = None

                if self.mysms_portal:
                    codigo_otp = self._obtener_codigo_otp()
                elif self.google_messages_portal:
                    codigo_otp = self._obtener_codigo_otp_google()
                else:
                    self._log_message("Error: No se ha configurado el portal para obtener el OTP", is_error=True)
                    return False
                
                if not codigo_otp:
                    self._log_message(f"Error obteniendo código OTP en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                    
                # Paso 3: Ingresar código OTP
                if not self._ingresar_codigo_otp(codigo_otp):
                    self._log_message(f"Error ingresando código OTP en intento {intento + 1}")
                    if intento < self.max_login_attempts - 1:
                        self._esperar_antes_reintentar()
                        continue
                    return False
                
                # Paso 4: Validar login exitoso
                if not self.detectar_login_valido():
                    if self._detectar_login_invalido():
                        self._log_message(f"Login inválido en intento {intento + 1}")
                        if intento < self.max_login_attempts - 1:
                            self._esperar_antes_reintentar()
                            continue
                        return False
                    
                # LOGIN EXITOSO
                self._log_message(f"Login exitoso en intento {intento + 1}")
                return True
                
            except Exception as e:
                self._log_error(f"login_automatico_intento_{intento + 1}", e)
                if intento < self.max_login_attempts - 1:
                    self._log_message(f"⚠️ Error en intento {intento + 1}, reintentando...")
                    self._esperar_antes_reintentar()
                    continue
                
        # TODOS LOS INTENTOS FALLARON
        self._log_message(f"Login falló después de {self.max_login_attempts} intentos", is_error=True)
        return False
    
    def _ingresar_credenciales(self):
        """
        Ingresa usuario y contraseña en el formulario de login.

        Si aparece el mensaje:
        'Actualmente existe un usuario en el sistema. Por favor verifique'
        aplica workaround (1 intento con credenciales incorrectas) y reintenta login normal.
        """
        try:
            self._log_message("Ingresando credenciales...")

            # Ingresar usuario/contraseña (IDs fijos)
            self.web_controller.write('ctl00_ContentPlaceHolder1_txtUsuario', self.usuario, 'id')
            self.web_controller.write('ctl00_ContentPlaceHolder1_txtContraseña', self.password, 'id')
            time.sleep(2)

            # Clic en ingresar
            self.web_controller.click('btnIngresarUsuarioContraseña', 'id')
            time.sleep(2)

            # ✅ Si el sistema responde "usuario en el sistema", aplicar workaround
            if self._usuario_en_sistema_detectado():
                self._log_message("⚠️ Login bloqueado: 'Actualmente existe un usuario en el sistema...'")

                if self._forzar_expiracion_por_credenciales_incorrectas():
                    self._log_message("🔁 Reintentando login normal después del workaround...")

                    # reingresar credenciales correctas
                    self.web_controller.write('ctl00_ContentPlaceHolder1_txtUsuario', self.usuario, 'id')
                    self.web_controller.write('ctl00_ContentPlaceHolder1_txtContraseña', self.password, 'id')
                    time.sleep(2)

                    self.web_controller.click('btnIngresarUsuarioContraseña', 'id')
                    time.sleep(2)
                else:
                    self._log_message("❌ Workaround falló. No pude forzar expiración.")
                    return False

            # Esperar a que aparezca el formulario OTP
            self._log_message("Esperando formulario OTP...")
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
            time.sleep(2)
            # Cambiar a la pestaña de MySMS
            self.web_controller.cambiar_pestaña()
            
            # Esperar a que llegue el SMS
            time.sleep(10)
            
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
                        self._log_message(f"Código OTP obtenido: {codigo}")
                        return codigo
                        
                except Exception as e:
                    self._log_message(f"Intento OTP {intento + 1}/{self.max_otp_attempts} fallido, reintentando...")
                    if intento < self.max_otp_attempts - 1:
                        time.sleep(10)  # Esperar antes de reintentar
                    
            self._log_message("No se pudo obtener el código OTP después de varios intentos", is_error=True)
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
            self._log_message(f"Ingresando código OTP: {codigo_otp}")
            
            # Volver a la pestaña principal
            self.web_controller.volver_pestaña()
            time.sleep(2)
            
            # Ingresar el código OTP
            self.web_controller.write('ctl00_ContentPlaceHolder1_txtTokenEntrust', codigo_otp, 'id')
            time.sleep(1)
            
            # Hacer clic en el botón de login con OTP
            self.web_controller.click('ctl00_ContentPlaceHolder1_BtnLoginTokenEntrust', 'id')
            time.sleep(2)
            
            return True
            
        except Exception as e:
            self._log_error("_ingresar_codigo_otp", e)
            return False
        
    def detectar_login_valido(self):
        """
        Detecta si el login fue exitoso
        
        Returns:
            bool: True si el login es válido, False en caso contrario
        """
        try:
            # Verificar elementos que indican inicio de sesión exitoso
            session_indicators = [
                'si va a dejar de utilizar'
            ]

            textoInicio = self.web_controller.read('//*[@id="titlesHeaderMainContent"]/small/span[contains(text(),"Si va a dejar")]', 'xpath')
            if textoInicio:
                texto_normalizado = textoInicio.lower()
                if any(indicator in texto_normalizado for indicator in session_indicators):
                    self._log_message("Login detectado como válido")
                    return True

        except Exception as e:
            self._log_error("detectar_login_valido", e)
            return False
        
        return False
    
    def _detectar_login_invalido(self):
        """
        Detecta si el login ha fallado por credenciales inválidas
        
        Returns:
            bool: True si el login es inválido, False en caso contrario
        """
        try:
            error_element = ''
            error_indicators = [
                'invalid_user_response',
                'Las credenciales no corresponden',
                'Actualmente existe un usuario en el sistema. Por favor verifique',
                'El usuario se encuentra actualmente en el sistema.',
                'Token inválido',
                '-'
            ]
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
            
            # Verificar si hay algún indicador de error
            if error_element:
                for indicator in error_indicators:
                    if indicator in error_element:
                        self._log_message(f"Error detectado: {error_element}", is_error=True)
                        
                        # Hacer clic en el botón de regresar si existe
                        try:
                            self.web_controller.click('ctl00_ContentPlaceHolder1_BtnRegresarMensaje', 'id')
                            time.sleep(2)
                        except:
                            pass
                            
                        return True

            # Si no se encontró ningún error, el login fue exitoso   
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
    
    def _looks_like_login_page(self, html: str | None = None) -> bool:
        try:
            wc = self.web_controller

            if html is None:
                html = str(wc.retornarHtml() or "")
            h = html.lower()

            try:
                current_url = str(getattr(wc.browser, "current_url", "") or "").lower()
            except Exception:
                current_url = ""

            # señales fuertes por URL
            if ("wpolps03" in current_url) or ("/pol_login/" in current_url):
                return True

            # si seguimos dentro de traffic, no marcar login solo por una pista débil
            in_traffic = "prod-md.azpol.claro.com.co" in current_url

            # señales HTML
            login_ids = [
                "ctl00_ContentPlaceHolder1_txtUsuario",
                "ctl00_ContentPlaceHolder1_txtContraseña",
                "btnIngresarUsuarioContraseña",
            ]

            found_login_marker = False
            for _id in login_ids:
                if wc.elementExists(_id, by="id"):
                    found_login_marker = True
                    break

            if found_login_marker and not in_traffic:
                return True

            if (("wpolps03" in h) or ("/pol_login/" in h) or ("pol_login" in h)) and not in_traffic:
                return True

            return False
        except Exception:
            return False
    
    def validar_sesion_activa(self):
        """
        True = parece que seguimos dentro de la app
        False = login, red caída o estado no confiable
        """
        try:
            wc = self.web_controller

            try:
                url = str(getattr(wc, "browser", None).current_url or "").lower()
                if url.startswith("chrome-error://") or url.startswith("edge://"):
                    return False
            except Exception:
                pass

            try:
                html = str(wc.retornarHtml() or "")
                h = html.lower()
                if ("dns_probe_finished_nxdomain" in h) or ("err_name_not_resolved" in h):
                    return False
            except Exception:
                pass

            if self._looks_like_login_page():
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
    
    def configurar_reintentos(self, max_intentos=2, intervalo_minutos=2):
        """
        Configura los parámetros de reintentos
        
        Args:
            max_intentos (int): Número máximo de intentos
            intervalo_minutos (int): Intervalo entre reintentos en minutos
        """
        self.max_login_attempts = max_intentos
        self.retry_interval = intervalo_minutos * 60
        self._log_message(f"🔧 Configurados {max_intentos} intentos con intervalo de {intervalo_minutos} minutos")

    def configurar_portales_otp(self, mysms=False, google_messages=False):
        """
        Configura los portales para obtener el código OTP
        
        Args:
            mysms (bool): Si se usa MySMS para obtener el OTP
            google_messages (bool): Si se usa Google Messages para obtener el OTP
        """
        if not mysms and not google_messages:
            self._log_message("⚠️ Advertencia: No se ha configurado ningún portal OTP. El login podría fallar.", is_error=True)
            return
        if mysms and google_messages:
            self._log_message("⚠️ Advertencia: Ambos portales OTP están habilitados. Se utilizará el primero disponible.")
            self.mysms_portal = True
            self.google_messages_portal = False
        else:
            self.mysms_portal = mysms
            self.google_messages_portal = google_messages

        self._log_message(f"Configurados portales OTP: MySMS={self.mysms_portal}, Google Messages={self.google_messages_portal}")

    def _asegurar_pantalla_login(self):
        """
        Asegura que el navegador esté en la pantalla de login antes de intentar autenticar
        
        Returns:
            bool: True si está en la pantalla de login, False en caso contrario
        """
        try:
            # Navegar a la página principal
            self._log_message("🔄 Navegando a la página de login...")
            # Verificar que llegamos a la pantalla de login
            if self._detectar_pantalla_login():
                self._log_message("Navegación exitosa a la pantalla de login")
                return True
            
            url_actual = self.web_controller.getCurrentUrl()
            if url_actual and 'poliedro' not in url_actual:
                self.web_controller.volver_pestaña()
                time.sleep(2)
            
            # Navegar a la URL de login
            login_url = 'https://poliedrodist.comcel.com.co/'
            self.web_controller.selectPage(login_url)
            time.sleep(5)
            
            # Verificar que llegamos a la pantalla de login
            if self._detectar_pantalla_login():
                self._log_message("Navegación exitosa a la pantalla de login")
                return True
            else:
                self._log_message("No se pudo navegar a la pantalla de login", is_error=True)
                return False
                
        except Exception as e:
            self._log_error("_asegurar_pantalla_login", e)
            return False
    
    def _detectar_pantalla_login(self):
        """
        Detecta si estamos en la pantalla de login de manera más robusta
        
        Returns:
            bool: True si estamos en la pantalla de login, False en caso contrario
        """
        try:
            # Verificar múltiples indicadores de la pantalla de login
            indicadores_login = [
                ('ctl00_ContentPlaceHolder1_txtUsuario', 'id'),        # Campo de usuario
                ('ctl00_ContentPlaceHolder1_txtContraseña', 'id'),     # Campo de contraseña
                ('btnIngresarUsuarioContraseña', 'id')                 # Botón de ingreso
            ]
            
            # Verificar la URL actual
            url_actual = self.web_controller.getCurrentUrl()
            if url_actual and ('LoginPoliedro' in url_actual or 'poliedro' in url_actual):
                # Verificar al menos 2 de los elementos para mayor seguridad
                elementos_encontrados = 0
                for elemento_id, tipo in indicadores_login:
                    try:
                        # Usar read o waitExist que no interactúan con el elemento
                        if tipo == 'id':
                            self.web_controller.waitExist(elemento_id, 'id', write=False)
                            elementos_encontrados += 1
                    except Exception:
                        pass  # Ignorar si no se encuentra un elemento específico
                        
                # Si encontramos al menos 2 elementos, consideramos que es la pantalla de login
                if elementos_encontrados >= 2:
                    self._log_message("✅ Detectada pantalla de login")
                    return True
                
            self._log_message("❌ No se detectó la pantalla de login")
            return False
            
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

    def _obtener_codigo_otp_google(self):
        """
        Obtiene el código OTP de la pestaña de messages de Google
        
        Returns:
            str: Código OTP o None si no se pudo obtener
        """
        try:
            self._log_message("📱 Obteniendo código OTP...")
            time.sleep(2)
            # Cambiar a la pestaña de MySMS
            self.web_controller.cambiar_pestaña()
            
            # Esperar a que llegue el SMS
            time.sleep(10)
            
            # El listado de conversaciones ya muestra el texto del ultimo
            # mensaje, asi que el OTP se puede leer sin abrir el chat. Se
            # prueban varias rutas porque el DOM de Google Messages cambia
            # entre versiones y antes solo se buscaba la conversacion abierta.
            #
            # Se filtra por "OTP" y no por la frase completa: el operador ya
            # mando el mensaje como "Su codigo OTP", "Su cdigo OTP" y
            # "Su codigo OTP", y cualquier variante rompia la lectura. El
            # translate() ignora mayusculas. Lo que descarta un mensaje que
            # solo mencione la palabra es el regex de 6-10 digitos de abajo.
            clave = 'contains(translate(%s, "otp", "OTP"), "OTP")'
            rutas = [
                # Listado de conversaciones (no requiere abrir el chat)
                '(//mws-conversation-snippet[%s])[1]' % (clave % '.'),
                # Conversacion abierta
                '(//div[contains(@class, "text-msg")][%s])[last()]' % (clave % '.'),
                # DOM anterior
                '(//mws-message-wrapper[.//div[%s]])[last()]//div[%s]' % (clave % 'text()', clave % 'text()'),
            ]

            # Intentar obtener el código OTP
            for intento in range(self.max_otp_attempts):
                for ruta in rutas:
                    try:
                        # Leer el contenido del SMS
                        sms_content = self.web_controller.read(ruta, 'xpath')
                    except Exception:
                        continue

                    # Extraer el código usando regex
                    match = re.search(r"\b\d{6,10}\b", sms_content or "")
                    if match:
                        codigo = match.group()
                        self._log_message(f"Código OTP obtenido: {codigo}")
                        return codigo

                self._log_message(f"Intento OTP {intento + 1}/{self.max_otp_attempts} fallido, reintentando...")
                if intento < self.max_otp_attempts - 1:
                    time.sleep(10)  # Esperar antes de reintentar
                    
            self._log_message("No se pudo obtener el código OTP después de varios intentos", is_error=True)
            return None
            
        except Exception as e:
            self._log_error("_obtener_codigo_otp", e)
            return None

    def _page_contains_text(self, text: str) -> bool:
        try:
            html = str(self.web_controller.retornarHtml() or "")
            return text.lower() in html.lower()
        except Exception:
            return False


    def _usuario_en_sistema_detectado(self) -> bool:
        # Texto EXACTO / estable que me diste
        return self._page_contains_text("Actualmente existe un usuario en el sistema")

    def _credenciales_no_corresponden_detectado(self) -> bool:
        return self._page_contains_text("Las credenciales no corresponden")

    def _forzar_expiracion_por_credenciales_incorrectas(self) -> bool:
        """
        Workaround:
        Si aparece 'Actualmente existe un usuario en el sistema...', primero volvemos al login con "Regresar",
        luego hacemos 1 intento con credenciales incorrectas, y cuando salga "Las credenciales no corresponden",
        volvemos a dar "Regresar" para quedar listos para el login normal.
        """
        try:
            self._log_message(
                "Detectado 'usuario en el sistema'. Forzando expiración con credenciales incorrectas (1 intento)..."
            )

            # 0) Pantalla 1: "Actualmente existe un usuario..." -> Regresar
            if self._usuario_en_sistema_detectado():
                self.web_controller.click("ctl00_ContentPlaceHolder1_BtnRegresarMensaje", "id")
                time.sleep(2)

            # 1) En login: credenciales incorrectas
            wrong_user = f"{self.usuario}a"
            wrong_pass = f"{self.password}a"

            self.web_controller.write("ctl00_ContentPlaceHolder1_txtUsuario", wrong_user, "id")
            self.web_controller.write("ctl00_ContentPlaceHolder1_txtContraseña", wrong_pass, "id")
            time.sleep(2)

            self.web_controller.click("btnIngresarUsuarioContraseña", "id")
            time.sleep(2)

            # 2) Pantalla 2: "Las credenciales no corresponden" -> Regresar
            if self._credenciales_no_corresponden_detectado():
                self.web_controller.click("ctl00_ContentPlaceHolder1_BtnRegresarMensaje", "id")
                time.sleep(2)

            self._log_message("✅ Workaround aplicado: listo para reintentar login normal.")
            return True

        except Exception as e:
            self._log_error("_forzar_expiracion_por_credenciales_incorrectas", e)
            return False