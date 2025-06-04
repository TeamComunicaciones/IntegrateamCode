from navegacion import sub_menu as sm, ventana_informacion
from recursos import  label, botones, colors
from funcionalidad import  web_controller, poliedro, excel
from subprocess import Popen
import threading
import tkinter as tk
import customtkinter as ctk
import time
from bs4 import BeautifulSoup
import requests
import pandas as pd

class Volantes:

    def __init__(self,master, on_of):
        self.etapa = 0
        self.on_of = on_of
        self.volantes = ''
        self.excel = excel.Excel_controller()
        self.link= 'https://poliedrodist.comcel.com.co/'
        self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        self.titulo = label.Label().create_label(master, 'VOLANTES', 0.2, 0.0, 0.5,0.2, letterSize= 25)
        self.ventana_informacion =  ventana_informacion.Ventana_informacion(master)
        self.menu = sm.Sub_menu(master,3, boton1=['ABRIR PAGINA', self.abrir_pagina], boton2=['COOKIE', self.ejecuccionHilo], boton3=['START', self.consulta_hilo])
        self.legalizador = ''
        self.time = tk.StringVar()
        self.time2 = 3
        self.time.set('0')
        self.entry_first_date = tk.StringVar()
        self.title_first_date = label.Label().create_label(self.menu.submenu, 'Fecha : ', 0.0, 0.55, 0.45,0.05, letterSize= 14)
        input_first_date= ctk.CTkEntry(self.menu.submenu, textvariable=self.entry_first_date)
        input_first_date.place(relx=0.4, rely=0.55, relheight=0.05, relwidth=0.6)
        boton = botones.Buttons()
        color = colors.Colors()
        self.resultados = []
        self.__url = url = "https://poliedrodist.comcel.com.co/Recaudo.PS/VolantesNIT/ResumenVolantes"
        self.__headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "es-US,es-419;q=0.9,es;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://poliedrodist.comcel.com.co/Recaudo.PS/VolantesNIT/Index",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "Cookie": '',
        }
        self.__codigos_pendientes = {
            "D2146.00001": [
                "11855", "11894", "11896", "11898", "12498", "14819", "15002", "18249", "23090", "44914",
                "44916", "44920", "54542", "54554", "56084", "60478", "63827", "63831", "63834", "63837",
                "63839", "63841", "63843", "68064", "68068", "68072", "68076", "69026", "70037", "71332",
                "71336", "71340", "71346", "71697", "73884", "78215", "78628", "87858", "75022",
                "95581", "53000", "64695", "65103", "67985", "67983", "68360", "68544", "68681", "68977",
                "68979", "68981", "74389", "93894","88751"
            ],
            "D1632.00001": [
                "51180", "61972", "63262", "69998", "71009", "80459", "80858", "84342", "61409"
            ],
            "D1399.00001": [
                "79134", "79988", "82315", "82403", "83071", "90226", "92343", "92785", "92861",
                "96725", "96822", "99451", "99508"
            ],
            "D2731.00001": [
                "75767", "75837", "76113", "76877", "83123", "90868", "93909", "93911", "93913"
            ],
            "D1816.00002": [
                "97914"
            ]
        }
        
        
    
    def abrir_excel(self):
        self.ventana_informacion.write('excel legalizador abierto recuerde cerrar antes de iniciar')
        p = Popen("src\\volantes\openExcel.bat")
        stdout, stderr = p.communicate()
    
    
    def abrir_pagina(self):
        self.ventana_informacion.write('Navegador abierto')
        class Abrir_pagina1(web_controller.Web_Controller):pass
        self.volantes = Abrir_pagina1(int(self.time.get()))
        self.volantes.openEdge()
        self.volantes.selectPage(self.link)
    
    def ejecuccionHilo(self):
        self.ejecuccion()
        
    def ejecuccion(self):
        self.on_of(False)
        self.ventana_informacion.write(f"Generando cookie...")
        self.ventana_informacion.write('Empezando ejecuccion')
        self.volantes.script("location.href='/activaciones/http/REDUCCION%20CUENTAS/Inicio.asp';")
        self.volantes.script("location.href='/ACTIVACIONES/Http/REINGENIERIA/DispatcherPoliedroRecaudo/DispacherEntrada.ASP?Site=1'")
        self.volantes.script("location.href='/Recaudo.PS/Dispatcher/EntranceVolantes'")
        self.volantes.select("/html/body/div/div[2]/section/div/div[2]/div/div[3]/main/form/div/div[1]/div[2]/div/select", "D")
        self.volantes.write("idinitialDate", "24/12/2024", "id")
        self.volantes.write("idfinalDate", "24/12/2024", "id")
        self.volantes.click("btnConsultar", "id")
        time.sleep(3)
        self.__headers['Cookie'] = self.volantes.getCookies()
        
        response_distr = requests.get(self.__url, headers=self.__headers)
        soup_distr = BeautifulSoup(response_distr.text, 'html.parser')
        select_distr = soup_distr.find('select', {'id': 'Distr'})
        options_distr = select_distr.find_all('option')
        self.codigos_distr = {option['value'].replace('-',''):option.text  for option in options_distr}
        self.ventana_informacion.write(f"cookie generada...")

    def consulta_hilo(self):
        hilo_legalizador = threading.Thread(target=self.consulta)
        hilo_legalizador.start()
        
    def consulta(self):
        for codigo, items in self.__codigos_pendientes.items():
            for item in items:
                for volantetype in ['R', 'V']:
                    volante = 'Reposición' if volantetype == 'R' else 'Voz'
                    self.ventana_informacion.write(f"Haciendo consulta para: {item} con Volantetype {volantetype}...")
                    data = {
                        "SelectedDistr": f"-{item}",
                        "Volantetype": volantetype,
                        "Initialdate": self.entry_first_date.get(),
                        "FinalDate": self.entry_first_date.get(),
                    }
                    response = requests.post(self.__url, headers=self.__headers, data=data)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, 'html.parser')
                        if soup.find('form', {'id': 'frmConsultaVolantes'}):
                            table = soup.find('form', {'id': 'frmConsultaVolantes'}).find('table')
                            rows = []
                            for row in table.find_all('tr')[1:]:
                                cols = row.find_all('td')
                                if len(cols) >= 3:
                                    secuencia = cols[0].get_text(strip=True)
                                    valor_efectivo = cols[1].get_text(strip=True)
                                    valor_cheque = cols[2].get_text(strip=True)
                                    usuario = cols[3].get_text(strip=True) if len(cols) > 3 else "Desconocido"
                                    self.resultados.append({
                                        "Código Maestro": codigo,
                                        "Distribuidor": item,
                                        "Fecha de Consulta": self.entry_first_date.get(),
                                        "Tipo de Volante": volante,
                                        "Secuencia": secuencia,
                                        "Valor Efectivo": valor_efectivo,
                                        "Valor Cheque": valor_cheque,
                                        "Usuario": usuario,
                                        "Mensaje": '',
                                    })

                        elif soup.find('div', {'id': 'MessageSinReg'}):
                                self.resultados.append({
                                    "Código Maestro": codigo,
                                    "Distribuidor": item,
                                    "Fecha de Consulta": self.entry_first_date.get(),
                                    "Tipo de Volante": volante,
                                    "Secuencia": '',
                                    "Valor Efectivo": '',
                                    "Valor Cheque": '',
                                    "Usuario": '',
                                    "Mensaje": "No existe ningún Volante asociado a los filtros de búsqueda."
                                })
                        else:
                            self.resultados.append({
                                "Código Maestro": codigo,
                                "Distribuidor": item,
                                "Fecha de Consulta": self.entry_first_date.get(),
                                "Tipo de Volante": volante,
                                "Secuencia": '',
                                "Valor Efectivo": '',
                                "Valor Cheque": '',
                                "Usuario": '',
                                "Mensaje": "Respuesta inesperada, no se pudo procesar el HTML correctamente."
                            })
        self.codigos_distr = {
            "11855": "D2146.00001", "11894": "D2146.00002", "11896": "D2146.00003", "11898": "D2146.00004", 
            "12498": "D2146.00005", "14819": "D2146.00006", "15002": "D2146.00007", "18249": "D2146.00008", 
            "23090": "D2146.00010", "44914": "D2146.00011", "44916": "D2146.00012", "44920": "D2146.00014", 
            "54542": "D2146.00024", "54554": "D2146.00027", "56084": "D2146.00028", "60478": "D2146.00029", 
            "63827": "D2146.00030", "63831": "D2146.00031", "63834": "D2146.00032", "63837": "D2146.00033", 
            "63839": "D2146.00034", "63841": "D2146.00035", "63843": "D2146.00036", "68064": "D2146.00037", 
            "68068": "D2146.00038", "68072": "D2146.00039", "68076": "D2146.00040", "69026": "D2146.00041", 
            "70037": "D2146.00042", "71332": "D2146.00043", "71336": "D2146.00044", "71340": "D2146.00045", 
            "71346": "D2146.00046", "71697": "D2146.00047", "73884": "D2146.00048", "75022": "D2146.00050", 
            "78215": "D2146.00051", "78628": "D2146.00052", "87858": "D2146.00054", "88751": "D2146.00055", 
            "95581": "D2146.00057", "53000": "D2575.00001", "64695": "D2575.00002", "65103": "D2575.00003", 
            "67985": "D2575.00004", "67983": "D2575.00006", "68360": "D2575.00007", "68544": "D2575.00008", 
            "68681": "D2575.00009", "68977": "D2575.00010", "68979": "D2575.00011", "68981": "D2575.00012", 
            "74389": "D2575.00015", "93894": "D2575.00016", "51180": "D1632.00001", "61972": "D1632.00002", 
            "63262": "D1632.00003", "69998": "D1632.00004", "71009": "D1632.00005", "80459": "D1632.00006", 
            "80858": "D1632.00007", "84342": "D1632.00008", "61409": "D1669.00001", "79134": "D1399.00001", 
            "79988": "D1399.00002", "82315": "D1399.00003", "82403": "D1399.00004", "83071": "D1399.00005", 
            "90226": "D1399.00006", "92343": "D1399.00007", "92785": "D1399.00008", "92861": "D1399.00010", 
            "96725": "D1399.00012", "96822": "D1399.00013", "75767": "D2731.00001", "75837": "D2731.00002", 
            "76113": "D2731.00003", "76877": "D2731.00004", "83123": "D2731.00005", "90868": "D2731.00006", 
            "93909": "D2731.00007", "93911": "D2731.00008", "93913": "D2731.00009", "97914": "D1816.00002",
            "99451": "D1399.00014", "99508": "D1399.00015"
        }
        data_df = pd.DataFrame(self.resultados)
        data_df['Distribuidor'] = data_df['Distribuidor'].replace(self.codigos_distr)
        self.resultados = []
        data_df.to_excel('src/volantes/volantes.xlsx', index=False)
        self.abrir_excel()