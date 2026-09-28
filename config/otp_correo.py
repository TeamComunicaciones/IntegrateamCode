"""
Configuración de la lectura del código OTP de Poliedro desde el correo del operario.

Claro manda el OTP a un buzón por operario (<cédula>@teamcomunicaciones.com.co).
El webmail es Roundcube, que por dentro lee el buzón por IMAP; la aplicación se
conecta al mismo servidor IMAP, sin navegador.

Si Claro cambia el remitente o el asunto del correo, se corrige aquí.
"""

# Servidor IMAP del buzón. Se usa "mail." y no "webmail." porque el certificado
# TLS de "webmail." no corresponde a ese nombre y la verificación falla.
SERVIDOR_IMAP = "mail.teamcomunicaciones.com.co"
PUERTO_IMAP = 993

# Tiempo máximo de cada operación de red contra el servidor (segundos).
TIMEOUT_RED = 20

# Cómo se reconoce el correo del OTP.
REMITENTE = "no-reply@gpin.com.co"
# Palabra que debe aparecer en el asunto (se compara sin mayúsculas ni tildes).
# Hace falta porque el mismo remitente manda otros correos, p. ej. "Generacion Pin".
PALABRA_ASUNTO = "OTP"

# El código es el único grupo de estos dígitos en el texto del correo.
# El año del pie ("© 2026") tiene 4 y queda fuera.
DIGITOS_MIN = 6
DIGITOS_MAX = 10

# Si el correo trae varios números de ese largo, se toma el más cercano a una
# de estas palabras (se comparan sin mayúsculas ni tildes).
PALABRAS_CERCANAS = ["codigo", "otp"]

# Espera del correo, en segundos.
TIMEOUT_ESPERA = 120
INTERVALO_SONDEO = 3

# Carpetas donde se busca si el OTP no llegó a la bandeja de entrada, solo para
# avisar al operario (no se toma el código de ahí).
CARPETAS_EXTRA = ["Junk", "Spam", "INBOX.Junk", "INBOX.Spam"]
