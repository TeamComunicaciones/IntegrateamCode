# import socketio
# import requests
# import time

# # response = requests.get('http://190.85.173.37:8003/')

# # Crear una instancia del cliente Socket.IO
# sio = socketio.Client()

# # Evento para manejar la conexión al servidor
# @sio.event
# def connect():
#     print('Conectado al servidor.')

# # Evento para manejar la solicitud de la primera palabra clave
# @sio.on('request_keyword')
# def on_request_keyword(data):
#     print(data['message'])
#     # Enviar la primera palabra clave al servidor
#     time.sleep(4)
#     usuario = 'sebas'
#     contraseña = '123'
#     sio.emit('send_keyword', {'usuario': usuario, 'contraseña': contraseña})

# # Evento para manejar la solicitud de la segunda palabra clave
# @sio.on('request_second_word')
# def on_request_second_word(data):
#     print(data['message'])
#     # Enviar la segunda palabra clave al servidor
#     second_word = input("Ingresa la segunda palabra clave: ")
#     sio.emit('send_second_word', {'keyword': second_word})

# # Evento para manejar la respuesta del servidor con la concatenación
# @sio.on('result')
# def on_result(data):
#     print('Concatenación recibida del servidor:', data['message'])

# # Evento para manejar la desconexión
# @sio.event
# def disconnect():
#     print('Desconectado del servidor.')

# # Conectar al servidor en la URL y puerto especificados
# sio.connect('http://190.85.173.37:8003/')

# # Mantener la conexión abierta
# sio.wait()



import os
from selenium import webdriver

options = webdriver.IeOptions()
options.ignore_zoom_level = True
options.attach_to_edge_chrome = True
# options.edge_executable_path = os.getenv("EDGE_PATH") # only for "IE Mode (old)" section
driver = webdriver.Ie(options=options)

# Maximizar la ventana del navegador
driver.maximize_window()

# Intentar cargar la página
driver.get('https://www.google.com/')

# Asegurarse de que el navegador pueda interactuar
try:
    driver.implicitly_wait(10)  # Espera implícita
    print("Página cargada correctamente.")
except Exception as e:
    print(f"Error al cargar la página: {e}")

# Cerrar el navegador
driver.quit()
pass

