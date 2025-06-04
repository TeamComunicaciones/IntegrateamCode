from navegacion import applicacion
from recursos import botones
from tkinter import messagebox
from funcionalidad.web_controller import  Web_Controller


def alertas(mensaje):
    root.root.attributes("-topmost", True)
    messagebox.showwarning(message=mensaje, title="Mensaje")   
    root.root.attributes("-topmost", False)



if __name__ == '__main__':
    app = applicacion.App
    driver_install = Web_Controller(0).edgedriver()
    root = app('1080x720', 'Team Comunicaciones', 'version: 3.6.6', alertas)
    root.start()