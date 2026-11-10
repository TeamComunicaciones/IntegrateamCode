"""Manejo de errores de certificado en el navegador de la automatización.

Desde nov-2026 Claro sirve en poliedrodist.claro.com.co un certificado revocado
por GoDaddy (motivo "superseded"). En los equipos con Bitdefender, el antivirus
lo reemplaza por uno de "Bitdefender Untrusted CA" y Edge muestra "La conexión
no es privada", lo que detiene las automatizaciones.

Con True, el Edge que abre la automatización ignora los errores de certificado.
Riesgo: mientras esté en True ese navegador no valida certificados en NINGÚN
sitio, así que no avisaría si alguien suplantara una página. Volver a False en
cuanto Claro instale su certificado nuevo. No afecta el Edge normal del usuario
ni las consultas que la app hace por fuera del navegador.
"""

IGNORAR_ERRORES_CERTIFICADO = True
