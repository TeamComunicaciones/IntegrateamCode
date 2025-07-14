from funcionalidad import web_controller
import time

data = []
class Abrir_pagina1(web_controller.Web_Controller): pass
facebook = Abrir_pagina1(int(0))
facebook.openEdge()
#facebook.selectPage('facebook.com/100087558304955/videos/4039444366315523')
for i in range(1,489):
    # if i%10 == 2:
    #     try:
    #         facebook.click(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[5]/div[1]/div[2]/div[{i+1}]/div[1]/div/div/div/span/span')

    #     except:
    #         pass
    #     time.sleep(3)
    try:
        comentario = facebook.read(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[5]/div[1]/div[2]/div[{i}]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/div/span/div/div')
    except:
        try:
            comentario = facebook.read(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[5]/div[1]/div[2]/div[{i}]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/div/span/div/div')
        except:
            comentario = 'no se pudo guardar'
            pass

    try:
        autor = facebook.read(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[5]/div[1]/div[2]/div[{i}]/div/div[1]/div[2]/div[2]/div[1]/div[1]/div/div/span/span/a/span')
    except:
        try:
            autor = facebook.read(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[5]/div[1]/div[2]/div[{i}]/div/div[1]/div/div[2]/div[1]/div[1]/div/div/span/span/a/span')
        except:
            autor = 'no se pudo guardar'
            pass

    try: 
        respuesta = facebook.read(f'')
    except:
        respuesta = 'no se pudo guardar'
    
    data.append({
        'name': autor,
        'date': autor,
        'text': comentario,
    })
pass