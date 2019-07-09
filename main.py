from tkinter import *
from tkinter import ttk

import configparser
import json

#peticion a fixer io desde paython
import requests

DEFAULPADDING =4
class Exchanger(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, width = '400', height = '150')

        config = configparser.ConfigParser()
        config.read('config.ini')

        self.api_key = config['fixer.io']['API_KEY']
        self.all_symbols_ep = config['fixer.io']['ALL_SYMBOLS_EP']
        self.rate_ep = config['fixer.io']['RATE_LATEST_EP']

        currencies = self.getCurrencies()

        #variables de control
        self.strInQunatity= StringVar(value='')
        self.strInQunatity.trace('w', self.convertirDivisas)#w - cada vez que lo modificamos
        
        self.strInCurrency =StringVar()
        self.strOutCurrency = StringVar()

        #CREAMOS UN FRAME Y LOS EMPAQUETAMOS
        self.pack_propagate(0)
        frInCurrency = ttk.Frame(self)
        frInCurrency.pack_propagate(0)

        frErrorMessages = ttk.Frame(self, height = 40)
        frErrorMessages.pack(side = BOTTOM, fill=X)#lo empaquetamos abajo i que expanda por el eje x ocupando todo el espacio
        frErrorMessages.pack_propagate(0)#para que mande mas que sus hijos
        self.lblErrorMessages = ttk.Label(frErrorMessages, text='Texto de preba',width = 50 foreground ='red', anchor=CENTER)
        self.lblErrorMessages.pack(side=TOP, fill=BOTH, expand=True )


        lblQ = ttk.Label(frInCurrency, text='Cantidad')
        lblQ.pack(side=TOP, fill=X, padx=DEFAULPADDING, pady=DEFAULPADDING)

        self.inQuantityEntry = ttk.Entry(frInCurrency, font=('Helvetica', 24, 'bold'), width=10, textvariable=self.strInQunatity)
        self.inQuantityEntry.pack(side = TOP, fill = X, padx=DEFAULPADDING, pady=DEFAULPADDING )
        #textvariable es la variable que se selecciona, combobox es un desplegable
        self.inCurrencyCombo = ttk.Combobox(frInCurrency, width = 25, height =5, values=currencies, textvariable=self.strInCurrency) 
        self.inCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULPADDING, pady=DEFAULPADDING)
        self.inCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)

        frInCurrency.pack(side=LEFT, fill=BOTH, expand = True)

        frOutCurrency = ttk.Frame(self)
        frOutCurrency.pack_propagate(0)

        frOutCurrency.pack(side = LEFT, fill=BOTH, expand = True)

        

        lblQ=ttk.Label(frOutCurrency, text='Cantidad')
        lblQ.pack (side=TOP, fill=X, padx=DEFAULPADDING, pady=DEFAULPADDING)

        self.outQuantityLbl = ttk.Label(frOutCurrency, font=('Helvetica', 24), anchor=E, width=10)
        self.outQuantityLbl.pack(side=TOP, fill=X,padx=DEFAULPADDING, pady=DEFAULPADDING)

        self.outCurrencyCombo = ttk.Combobox(frOutCurrency, width=25, height=5, values=currencies, textvariable=self.strOutCurrency)
        self.outCurrencyCombo.pack(side=TOP, fill= X, padx=DEFAULPADDING, pady=DEFAULPADDING,  ipady=2)
        self.outCurrencyCombo.bind('<<ComboboxSelected>>', self.convertirDivisas)

        frOutCurrency.pack(side=LEFT, fill=BOTH, expand=True)

    def ValidarCantidad(self, *args):
        try:
            v=float(self.strInQunatity.get())
            self.oldInQuantity =v
            self.convertirDivisas()
        except:
            self.str

    def convertirDivisas(self,*args):
        print('in', self.strInCurrency.get())
        print('out', self.strOutCurrency.get())
        print('cantidad', self.strInQunatity.get())

        base= 'EUR'
        _from=self.strInCurrency.get()
        #para coger solo las siglas de la moneda seleccionada
        _from = _from[:3]
        _to=self.strOutCurrency.get()
        _to = _to[:3]
        symbols= _from + ',' +_to
        self.strInCurrency.get()
        if self.strInCurrency.get() and self.strInQunatity.get() and self.strOutCurrency.get():

            self.lblErrorMessages.confi(text='Conectando...')

            response = requests.get(self.all_symbols_ep.format(self.api_key, base,symbols))
            
            if response.status_code == 200:
                data = json.loads(response.text)
                if data['success']:
                    tasa_conversion = data['rates'][_from]
                    tasa_conversion = data['rates'][_top]
                    self.lblErrorMessages.config(text='')
                else:
                    msgError= '{} - {}'.format(data['error']['code'], data['error']['type'])
                    print(msgError)

                    self.lblErrorMessages.config(text=msgError)#para pintar el mensaje en la label
                    return

            else:
                msgError = 'Se ha producido un error en la consulta API:'+response.status_code
                print(msgError)

                self.lblErrorMessages.config(text=msgError)#para pintar el mensaje en la label
                return

                
            
            #valor_label = Cantidad / tasa_conversion * tasa_conversion2

            valor_label = round(float(self.strInQunatity.get())/ tasa_conversion * tasa_conversion2, 5)
            #para modificar los atributos de una label que ya esta creada, se usa el config)
            self.outQuantityLbl.config(text=valor_label)


    def getCurrencies(self):
        response = requests.get(self.all_symbols_ep.format(self.api_key))

        if response.status_code == 200:
            currencies = json.loads(response.text)#usamos json para formatear el arichivo
            result=[] #creamos la lista vacía
            for symbol in currencies['symbols']:
                text = " {} - {} ".format(symbol, currencies['symbols'][symbol])
                result.append(text)
            return result
        else:
            msgError = 'Se ha producido un error en la consulta API:'+response.status_code
            print(msgError)

            self.lblErrorMessages.config(text=msgError)#para pintar el mensaje en la label
            return


class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry('400x150')
        self.title('Exchanger fixer.io')
        self.exchanger= Exchanger(self)
        self.exchanger.place(x=0, y=0)

    def start(self):
        self.mainloop()

if __name__ == '__main__':
    exchanger = MainApp()
    exchanger.start()

'''
config = configparser.ConfigParser()
config.read('config.ini')

inSymbol = input('que moneda quieres convertir: ')
outSymbol = input('en qué otra moneda: ')

url = config['fixer.io']['RATE_LATEST_EP']
apy_key = config['fixer.io']['API_KEY']

url=url.format(apy_key, inSymbol, outSymbol)
#peticion http para obtener (get)
response = requests.get(url)
if response.status_code == 200:
    #interpretamos el fichero con la libreria json
    print (response.text)
else:
    print('Se ha producido un error en la peticion:', response.status_code)
'''