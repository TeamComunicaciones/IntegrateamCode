import pyautogui
import random
import time
import pyperclip
from datetime import datetime, timedelta
from PIL import Image as Im
from PIL import ImageTk as ImTk
from tkinter import PhotoImage, Tk, Label


class ClickImage:

    def __init__(self):
        self.detener = False
        self.debug_value = False
    
    def definirInformes(self, informes):
        self.informes = informes
    
    def debug(self, debug, ventanaSuperior):
        self.debug_value = debug
        self.ventanaSuperior = ventanaSuperior

    def contadorPrueba(self):
        contador = 0
        while True:
            if self.detener: raise('Detener programa')
            print(f'intento numero {contador}')
            time.sleep(1)
            contador += 1

    def clickImg(self, img, tiempo, region=None, desplazar=False, seleccionar=False, copiar=False, extra=False, excel=None, confidenceImg=0.8, confidenceReg=0.8):
        if self.detener: raise('Detener programa')
        if region is not None:
            self.wait(region, extra=extra, excel=excel)
            region = f'src\portas\imgs\{region}.png'
            region = pyautogui.locateOnScreen(region, confidence=confidenceReg)
        self.wait(img, extra=extra, excel=excel)
        img2 = f'src\portas\imgs\{img}.png'
        element_location = pyautogui.locateOnScreen(img2, confidence=confidenceImg, region=region)
        if element_location is None:
            print(f'no esta imagen {img}')
            self.informes.write(f'problema con imagen {img}')
        print(element_location)
        self.minX = element_location.left
        self.minY = element_location.top
        self.maxX =  self.minX + element_location.width
        self.maxY = self.minY + element_location.height
        self.ancho = element_location.width
        self.alto = element_location.height
        self.reducirBorde()
        self.time = tiempo
        self.randomPausa()
        extraTime = 6 if self.pausa else 0
        pause = random.randint(0,extraTime)
        if pause > 0:
            print(f'se pausa {pause} segundos')
            time.sleep(pause)
        randomTime = round(random.uniform(self.time-0.12, self.time+1),2)
        x = random.randint(self.minX,self.maxX)
        y = random.randint(self.minY,self.maxY)
        pyautogui.moveTo(x,y,duration=randomTime, tween=pyautogui.easeInOutQuad, logScreenshot=False)
        pyautogui.click()
        if desplazar:
            pyautogui.moveRel(-200,-200, 1)
        if seleccionar:
            x, y = pyautogui.position()
            new_x = x - 500
            pyautogui.dragTo(new_x, y, duration=1, button='left')
        if copiar:
            pyautogui.hotkey('ctrl', 'c')
        

    def reducirBorde(self):
        self.minX = int(self.minX + self.ancho/4)
        self.minY = int(self.minY + self.alto/4)
        self.maxX = int(self.maxX - self.ancho/4)
        self.maxY = int(self.maxY - self.alto/4)

    def seleccionarPuntoAleatorio(self):
        x = random.randint(self.minX,self.maxX)
        y = random.randint(self.minY,self.maxY)
        self.randomPausa()
        extraTime = 10 if self.pausa else 0
        pause = random.randint(0,extraTime)
        if pause > 0:
            print(f'se pausa {pause} segundos')
            time.sleep(pause)
        randomTime = round(random.uniform(self.time, self.time+1.5),2)
        pyautogui.moveTo(x,y,duration=randomTime, tween=pyautogui.easeInOutQuad, logScreenshot=False)
        pyautogui.click()

    def write(self, palabra, enter=False, pausa=False, backspase=False, desplazarClick = False, correo=False):
        if backspase:
            pyautogui.press('backspace')
            pyautogui.press('delete')
        if correo:
            antes, despues = palabra.split('@')
            pyautogui.typewrite(antes,0.25)
            pyperclip.copy('@')
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.typewrite(despues,0.25)
            pyautogui.hotkey('esc')
        else:
            pyautogui.typewrite(palabra,0.25)
        if enter:
            pyautogui.press('enter')
        time.sleep(1)
        if pausa:
            time.sleep(2)
        if desplazarClick:
            pyautogui.moveRel(-300,0, 1)
            pyautogui.click()
            time.sleep(1)
    
    def scroll(self, cantidad):
        time.sleep(1)
        pyautogui.scroll(cantidad)
        time.sleep(3)
 
    def randomPausa(self):
        numero = random.randint(1,10)
        self.pausa = True if numero>=8 else False
    
    def marcarBorde(self):
        pyautogui.moveTo(self.minX,self.minY,0.5)
        pyautogui.click()
        pyautogui.dragTo(self.maxX,self.minY,0.5)
        pyautogui.dragTo(self.maxX,self.maxY,0.5)
        pyautogui.dragTo(self.minX,self.maxY,0.5)
        pyautogui.dragTo(self.minX,self.minY,0.5)

    def wait(self, img, extra=False, menos =False , confidence= 0.8, excel=None):
        contador = 0
        img2 = f'src\portas\imgs\{img}.png'
        self.rutaImg = img2
        continuar = True
        self.debugBool = True
        timeExtra = 0
        timeMenos = 0
        if extra:
            timeExtra = 200
        if menos:
            timeMenos = -50

        if self.debug_value:
            self.subventana = self.ventanaSuperior(img2, self.pantallazo, self.nextDebug)
            contador3 = 1
            while(self.debugBool):
                pass
                # print(contador3)
                # contador3 += 1


        while (continuar):
            # busca una imagen específica en la pantalla y devuelve sus coordenadas
            element_location = pyautogui.locateOnScreen(img2, confidence=confidence)
            if element_location is None:
                print(f'no esta imagen {img} {contador}')
                time.sleep(0.1)
                contador += 1

                if contador == 100 + timeExtra + timeMenos:
                    if self.informes != None and menos==False: 
                        self.informes.write(f'problema con imagen {img}')
                        if excel != None:
                            excelFile = excel[0]
                            i = excel[1]
                            excelFile.guardar(i,'FALLA',img, destino='src\portas\portabilidad.xlsx')
                    raise('excede tiempo')
            else:
                continuar = False

    def copiarMin(self, img):
        self.wait(img)
        img2 = f'src\portas\imgs\{img}.png'
        element_location = pyautogui.locateOnScreen(img2, confidence=0.8)
        pyautogui.moveTo(element_location,duration=1)
        pyautogui.click()
        x, y = pyautogui.position()
        new_x = x + 30
        pyautogui.dragTo(new_x, y, duration=1, button='left')
        pyautogui.hotkey('ctrl', 'c')

    def quitarMouse(self):
         pyautogui.moveRel(-1800,-300, 1)
        
    def nextDebug(self):
        self.subventana.destroy()
        self.debugBool = False
    
    def pantallazo(self):
        self.posiciones = {}
        def capture_area(event):
            self.posiciones[f'{self.contadorClicks}'] = [self.tomarPantalla.winfo_pointerx(),self.tomarPantalla.winfo_pointery()]
            self.contadorClicks +=1
            print(self.posiciones)
            if self.contadorClicks >2:
                self.tomarPantalla.destroy()
                self.tomarPantalla.quit()
        screen_width, screen_height = pyautogui.size()
        screenshot = pyautogui.screenshot()
        self.contadorClicks = 1
        self.tomarPantalla = Tk()
        self.tomarPantalla.attributes("-transparentcolor", "white")
        self.tomarPantalla.attributes("-alpha", 0.3)
        self.tomarPantalla.overrideredirect(True)
        screen_width, screen_height = pyautogui.size()
        self.tomarPantalla.geometry(f'{screen_width}x{screen_height}')
        self.tomarPantalla.bind("<Button-1>", capture_area)
        self.tomarPantalla.mainloop()
        preview = screenshot.crop((self.posiciones['1'][0], self.posiciones['1'][1], self.posiciones['2'][0], self.posiciones['2'][1]))
        preview.show()
        preview.save(self.rutaImg)
