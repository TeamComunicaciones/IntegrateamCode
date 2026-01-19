from navegacion import applicacion
from recursos import botones
from tkinter import messagebox
from funcionalidad.web_controller import  Web_Controller


def alertas(mensaje):
    root.root.attributes("-topmost", True)
    messagebox.showwarning(message=mensaje, title="Mensaje")   
    root.root.attributes("-topmost", False)

if __name__ == '__main__':

    try:
        driver = Web_Controller(0).openEdge(headless=True)
    except Exception as e:
        print(f'[WARN] Inicialización del driver falló: {e}')
    else:
        if driver is not None:
            driver.quit()

    app = applicacion.App
    root = app('1080x720', 'Team Comunicaciones', 'version: 3.6.29', alertas)
    root.start()