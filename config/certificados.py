"""Manejo de errores de certificado en el navegador de la automatización.

Desde nov-2026 Claro sirve en poliedrodist.claro.com.co un certificado revocado
por GoDaddy (motivo "superseded"). En los equipos con Bitdefender, el antivirus
lo reemplaza por uno de "Bitdefender Untrusted CA" y Edge muestra "La conexión
no es privada", lo que detiene las automatizaciones.

Con True:
  - El Edge que abre la automatización ignora los errores de certificado.
  - Las consultas a Poliedro que la app hace por fuera del navegador (Volantes y
    Consulta de seriales) tampoco validan el certificado.
Riesgo: mientras esté en True ese navegador no valida certificados en NINGÚN
sitio, ni esas consultas el de Poliedro, así que no avisarían si alguien
suplantara la página. Volver a False en cuanto Claro instale su certificado
nuevo. No afecta el Edge normal del usuario.
"""

import urllib3

IGNORAR_ERRORES_CERTIFICADO = True

# Valor para el parámetro `verify` de requests en las consultas a Poliedro.
VERIFICAR_CERTIFICADO_POLIEDRO = not IGNORAR_ERRORES_CERTIFICADO

if IGNORAR_ERRORES_CERTIFICADO:
    # Sin esto, cada consulta con verify=False imprime un aviso en la consola.
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
