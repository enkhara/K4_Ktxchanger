from tkinter import *
from tkinter import ttk

import configparser
import json

#peticion a fixer io desde paython
import requests

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