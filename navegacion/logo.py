import customtkinter as ctk
from PIL import Image, ImageTk


class Logo:

    def __init__(self,master, on_of):
        image_path = "src\\team\logoTeamBlanco.png"
        image = Image.open(image_path)
        image = image.resize((500, 500))
        imagen = ImageTk.PhotoImage(image)
        # imagen = ctk.CTkImage(light_image=image)
        widget_imagen = ctk.CTkLabel(master, image=imagen, text='',)
        widget_imagen.image = imagen
        widget_imagen.pack(fill="both", expand=True)
        widget_imagen.place(relwidth=1, relheight=1)