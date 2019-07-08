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
        self.strinQunatity.trace('w', self.convertirDivisas)#w - cada vez que lo modificamos
        self.strInCurrency =StringVar()
        self.strOutCurrency = StringVar()

        #CREAMOS UN FRAME Y LOS EMPAQUETAMOS
        self.pack_propagate(0)
        frInCurrency = ttk.Frame(self)
        frInCurrency.pack_propagate(0)

        lblQ = ttk.Label(frInCurrency, text='Cantidad')
        lblQ.pack(side=TOP, fill=X, padx=DEFAULPADDING, pady=DEFAULPADDING)

        self.inQuantityEntry = ttk.Entry(frInCurrency, font=('Helvetica', 24, 'bold'), width=10, textvariable=self.strInQunatity)
        self.inQuantityEntry.pack(side = TOP, fill = X, padx=DEFAULPADDING, pady=DEFAULPADDING )
        #textvariable es la variable que se selecciona, combobox es un desplegable
        self.inCurrencyCombo = ttk.Combobox(frInCurrency, width = 25, height =5, values=currencies, textvariable=self.strInCurrency) 
        self.inCurrencyCombo.pack(side=TOP, fill=X, padx=DEFAULPADDING, pady=DEFAULPADDING)
        self.inCurrencyCombo.bind('<<ComboboxSelected>>', self.convertiDivisas)

        frInCurrency.pack(side=LEFT, fill=BOTH, expand = True)

        frOutCurrency = ttk.Frame(self)
        frOutCurrency.pack_propagate(0)

        frOutCurrency.pack(side = LEFT, fill=BOTH, expand = True)

        lblQ=ttk.Label(frOutCurrency, text='Cantidad')
        lblQ.pack (side=TOP, fill=X, padx=DEFAULPADDING, pady=DEFAULPADDING)

        self.outQuantityLbl = ttk.Label(frOutCurrency, font=('Helvetica', 24), anchor=E, width=10)
        self.outQuantityLbl.pack(side=TOP, fill=X)

        self.outCurrencyCombo = ttk.Combobox(frOutCurrency, width=25, height=5, values=currencies, textvariable=self.strOutCurrency)
        self.outCurrencyCombo.pack(side=TOP, fill= X, padx=DEFAULPADDING, pady=DEFAULPADDING, ipady=2)
        self.outCurrencyCombo.bind('<<ComboboxSelected>>', self.convertiDivisas)

        frOutCurrency.pack(side=LEFT, fill=BOTH, expand=True)

    def convertirDivisas(self,*args):
        print('in', self.strInCurrency.get())
        print('out', self.strOutCurrency.get())
        print('cantidad', self.strInQunatity.get())

    def getCurrencies(self):
        response = requests.get(self.all_symbols_ep.format(self.api_key))

        if response.status_code == 200:
            currencies = json.loads(response.text)
            result=[]
            for symbol in currencies['symbols']:
                text= '{} - {}'.format(symbol, currencies['symbols'], ['symbol'])
                result.append(text)
            return result
        else:
            print('se ha producido un error al consutar symbols:', response.status_code)

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