from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service

# Crear opciones para Edge
options = EdgeOptions()
options.add_argument("--start-maximized")

# Crear servicio especificando la ruta del driver
service = Service(executable_path='msedgedriver.exe')

try:
    # Crear instancia del navegador
    driver = webdriver.Edge(service=service, options=options)
    
    # Navegar a una página de prueba
    driver.get("https://www.google.com")
    
    print("EdgeDriver funcionando correctamente!")
    print(f"Título de la página: {driver.title}")
    
    # Esperar un momento
    import time
    time.sleep(3)
    
    # Cerrar el navegador
    driver.quit()
    
except Exception as e:
    print(f"Error al inicializar EdgeDriver: {e}")
