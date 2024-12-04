from selenium.webdriver.common.keys import Keys
import time

class Poliedro:

    def __init__(self, legalizador=False):
        self.tropas = False
        self.legalizador = legalizador
    
    def manejoTropas(self,tropas):
        self.tropas = tropas

    def definirBrowser(self, browser):
        self.browser = browser

    def seleccionAcceso(self, opcion, start = True):
        # self.link2='https://poliedrodist.comcel.com.co/activaciones/http/REINGENIERIA/pagDispatcherEntradaModernizacion.asp?Site=1'
        # self.browser.selectPage(self.link2)
        if self.tropas:
            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td/div/div/div[2]/a') #/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[1]/div[1]/div[2]/div/span/span[1]/span/span[1]
            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr/td/div/div/div[3]/div[5]/a')
            
        else:
            if start:
                self.browser.click('/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[1]/div[5]')
                self.browser.click('/html/body/table/tbody/tr[5]/td/table/tbody/tr/td[1]/div[1]/div[1]/div[6]/div[2]/a')
        self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[1]/div[1]/div[2]/div/span/span[1]/span/span[1]')
        self.browser.write('/html/body/span/span/span[1]/input', opcion)
        self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
        self.opcion = opcion

    def seleccionNit(self):
        self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div[2]/div[1]/div[1]/div[1]/div/span/span[1]/span/span[1]')
        self.browser.write('/html/body/span/span/span[1]/input', 'nit')
        self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
        
    
    def rellenoFormulario(self,campos,lista):

        for i in range (campos):
            if len(lista[i]) == 2: lista[i].append('xpath')
            self.browser.eraseLetter(lista[i][0], 20, by=lista[i][2])
            time.sleep(1) 
            self.browser.insert(lista[i][0],lista[i][1],lista[i][2])
            time.sleep(1) 
    
    def detectOption(self, options, functions, NoneFunc = None, short2 = False):
        self.selectOption = None
        for i in range (len(options)):
            if len(options[i]) == 1: options[i].append('xpath')
            try:
                if short2:
                    self.browser.readShort2(options[i][0], options[i][1])
                else:
                    self.browser.readShort(options[i][0], options[i][1])
                self.selectOption = i
                break
            except:
                pass
        if self.selectOption is not None:
            func = functions[self.selectOption]
            func()
        else:
            if NoneFunc is not None:
                NoneFunc()
    
    def reinicio(self, start = True):
        try:
            if self.legalizador:                       
                self.browser.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]/a/span')
                self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[12]/td[1]/a')
            else:
                self.browser.click('/html/body/div/div[2]/section/div/div[1]/aside/nav/div[2]/ul/li[12]/a')
                if self.tropas == False:
                    if self.legalizador:
                        try:
                            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[13]/td[1]/a')
                        except:
                            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[12]/td[1]/a')
                    else:
                        try:
                            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[13]/td[1]/a')
                        except:
                            self.browser.click('/html/body/p/table[2]/tbody/tr[2]/td[1]/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[12]/td[1]/a')
        except: 
            pass
        self.seleccionAcceso(self.opcion, start)
    
    def saludo(self):
        self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[1]/div/span/span[1]/span/span[1]')
        self.browser.write('/html/body/span/span/span[1]/input', 'r')
        self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)

    def correo(self, correo):
        self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[4]/div/input',correo)

    def tipoDoc(self, tipo, xpath='/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[1]/div/span/span[1]/span/span[1]'):
        tipoDoc = self.browser.read(xpath)
        if 'Seleccione' in tipoDoc:
            self.browser.click(xpath)
            self.browser.write('/html/body/span/span/span[1]/input', tipo)
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)

    def rellenoNombre(self, nombre):
        readonly = self.browser.readonly('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[2]/div/input')
        if readonly != True:
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[2]/div/input', nombre)

    def rellenoApellido(self, apellido):
        readonly = self.browser.readonly('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[3]/div/input')
        if readonly != True:
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[3]/div/input', apellido)
    
    def rellenoCedula(self, cedula):
        readonly = self.browser.readonly('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[2]/div/input')
        if readonly != True:
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[2]/div/input', cedula)

    def rellenoNumero(self):
        try:
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/span/span[1]/span/span[1]')
            self.browser.write('/html/body/span/span/span[1]/input', 'fijo')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.click('//html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/span/span[1]/span/span[1]')
            time.sleep(1)
            self.browser.write('/html/body/span/span/span[1]/input', '604')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
        except:
            try:
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/select', 'fijo')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select', '604')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
            except:
                raise('No logra ingresar datos de Numero')

    def rellenoNumero2(self):
        try: 
            self.browser.waitExist('PhoneClass', 'id', write=True)
            self.browser.select('PhoneClass', '2', 'id')
            self.browser.select('Prefix', '604', 'id')
            # self.browser.erase('Prefix', 'id')
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
        except:
            self.browser.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/span/span[1]/span/span[1]', write=True)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/span/span[1]/span/span[1]')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/select', 'fijo')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[1]/div/select', Keys.ENTER)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select')
            time.sleep(1)
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select', '604')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[2]/div/select', Keys.ENTER)
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[1]/div[5]/div[2]/fieldset/div/div[3]/div/input', '3131234')
     
    def rellenoDireccion(self, legalizador=False):
        try:
            if legalizador:
                self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/span/span[1]/span/span[1]')
                self.browser.write('/html/body/span/span/span[1]/input', 'otras')
                self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            else:
                self.browser.select('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/span/span[1]/span/span[1]','otras')
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/span/span[1]/span/span[1]')
            self.browser.write('/html/body/span/span/span[1]/input', 'otras')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'central')
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[3]/div/span/span[1]/span/span[1]')
            self.browser.write('/html/body/span/span/span[1]/input', 'antio')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[4]/div/span/span[1]/span/span[1]')
            self.browser.write('/html/body/span/span/span[1]/input', 'mede')
            self.browser.write('/html/body/span/span/span[1]/input', Keys.ENTER)
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'central')
        except:
            try:
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', 'otras')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'central')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[3]/div/select', 'ANTIOQUIA')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[4]/div/select', 'MEDELLIN')
                time.sleep(1)
                self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[1]/div/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'central')
            except:
                raise('No logra ingresar datos Direccion')

    def rellenoDireccion2(self):
        try:
            self.browser.waitExist('AddressClassId', 'id', write=True)
            self.browser.select('AddressClassId', 'Otras', 'id')
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'central')
            self.browser.select('Department', 'ANTIOQUIA', 'id')
            self.browser.select('City', 'MEDELLIN', 'id')
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'central')
        except:
            self.browser.waitExist('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', write=True)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', 'otras')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[1]/div[1]/select', Keys.ENTER)
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[2]/div/input', 'central')
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[3]/div/select')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[3]/div/select', 'antio')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[3]/div/select', Keys.ENTER)
            self.browser.click('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[4]/div/select')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[4]/div/select', 'mede')
            self.browser.write('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[4]/div/select', Keys.ENTER)
            self.browser.insert('/html/body/div/div[2]/section/div/div[2]/div[2]/main/form/div/div[2]/div[1]/div[2]/div[3]/div[2]/fieldset/div[5]/div/input', 'central')