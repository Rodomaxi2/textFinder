from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import re
from tkinter import *
import tkinter.ttk as ttk
import threading
from palabras import *

# Logica y algoritmo


contadorGlobal = 0
contadorAltas = 0
contadorMedias = 0
contadorBajas = 0


palabrasPrueba = prueba
alta = categoriaAlta
media = categoriaMedia
baja = categoriaBaja

# Esta funcion cuenta las palabras dentro de un texto que coincidan con el array dado


def actualizarTabla(contadorAltas, contadorMedias, contadorBajas):
    if (contadorAltas > 5):
        mensajeAltas = "Se sugiere que no se visite la pagina web"
    else:
        mensajeAltas = "No se encontraron palabras de esta categoria"
    if (contadorMedias > 5):
        mensajeMedias = "La pagina puede contener vilencia se sugiere que sea visitada con un adulto"
    else:
        mensajeMedias = "No se encontraron palabras de esta categoria"
    if (contadorBajas > 5):
        mensajeBajas = "La pagina puede ser visitada por menores, sin embargo no se puede"
    else:
        mensajeBajas = "No se encontraron palabras de esta categoria"

    tableDraw.item(0, text='',
                   values=(str(contadorAltas), 'Alta', mensajeAltas))
    tableDraw.item(1, text='',
                   values=(str(contadorMedias), 'Media', mensajeMedias))
    tableDraw.item(2, text='',
                   values=(str(contadorBajas), 'Baja', mensajeBajas))


def actualizarEstado(estado):
    if (estado == "Trabajando..."):
        taskLabel.config(text=estado)
        buttonAnalizar.config(state=DISABLED)
    else:
        taskLabel.config(text=estado)
        buttonAnalizar.config(state=NORMAL)


def contarPalabras(texto, palabras):
    contador = 0
    for palabra in palabras:
        coincidencias = re.findall(r'(?i)\w*' + palabra + '\w*', texto)
        contador += len(coincidencias)
    return contador

# Esta funcion borra todos los archivos de ejecuciones pasadas


def formatString(link):
    link = link.replace('<title>', '')
    link = link.replace('</title>', '')
    link = link.replace(' ', '')
    link = link.replace('|', '')
    link = link.replace('?', '')
    link = link.replace('??', '')
    link = link.replace('\"', '')
    link = link.replace('\\', '')
    link = link.replace('/', '')
    link = link.replace('\n', '')
    return link


def extractText(link):
    global contadorAltas, contadorMedias, contadorBajas
    try:
        response = requests.get(link, timeout=(3, 27))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if(soup.title == None):

                title = link
                title = formatString(title)
            else:
                try:
                    title = soup.title.string

                except ValueError as ve:
                    print('El titulo no contiene el atributo string', ve)
                    return

            contadorAltas += contarPalabras(title, palabrasPrueba)
            contadorMedias += contarPalabras(title, media)
            contadorBajas += contarPalabras(title, baja)

            for text in soup.strings:
                contadorAltas += contarPalabras(text, palabrasPrueba)
                contadorMedias += contarPalabras(text, media)
                contadorBajas += contarPalabras(text, baja)
            print(contadorAltas)

        else:
            return
            # raise ValueError(f'Error: {response.status_code} con link: {link}')

        response.close()
    except requests.exceptions.Timeout:
        print('El tiempo se agoto')

    except ConnectionError:
        print('Link caido')


def searchLinks(link):
    global contadorAltas, contadorMedias, contadorBajas
    try:

        response = requests.get(link)  # se accede a la pagina principal
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            actualizarEstado("Trabajando...")

            for newLink in soup.find_all('a'):
                try:
                    if(newLink.get('href')):
                        parsedLink = newLink.get('href').replace(' ', '')
                        # print("se encontro el link: ", parsedLink)
                        if parsedLink.find('_blank') > 0:
                            continue
                        elif parsedLink.find('sic') > 0:
                            continue
                        elif parsedLink[0:4] == 'http':
                            pass
                        else:
                            parsedLink = link + parsedLink

                        print(parsedLink)
                        extractText(parsedLink)
                    else:
                        print('Link no valido')

                except ValueError as ve:
                    print(ve)

        else:
            raise ValueError(f'Error {response.status_code}')
        actualizarTabla(contadorAltas, contadorMedias, contadorBajas)
        actualizarEstado("Hecho")
    except ValueError as ve:
        print('Un error ocurrio:', ve)


# Interfaz de usuario e interaccion
window = Tk()
window.title("Analizador de paginas")
window.geometry("400x400")


linkLabel = Label(window, text="Ingresa el link a evaluar:", font=10)
linkLabel.place(x=10, y=30)

textAreaLink = Entry(window, font=30, width=35)
textAreaLink.place(x=10, y=60)

global buttonAnalizar
buttonAnalizar = Button(window, text="Analizar", command=lambda: threading.Thread(
    target=searchLinks(textAreaLink.get())).start())

buttonAnalizar.place(x=335, y=57)

estadoLabel = Label(window, text="Estado:", font=20)
estadoLabel.place(x=80, y=100)

global taskLabel
taskLabel = Label(window, text="Listo para trabajar", font=20)
taskLabel.place(x=150, y=100)

global tableDraw
tableDraw = ttk.Treeview(window, columns=3)
tableDraw.place(x=10, y=160)
tableDraw['columns'] = ('numero', 'categoria', 'consejo')
tableDraw.column("#0", width=0,  stretch=True)
tableDraw.column("numero", anchor=CENTER, width=40, stretch=True)
tableDraw.column("categoria", anchor=CENTER, width=100)
tableDraw.column("consejo", anchor=CENTER, width=240)

tableDraw.heading("#0", text="", anchor=CENTER)
tableDraw.heading("numero", text="Num", anchor=CENTER)
tableDraw.heading("categoria", text="Categoria", anchor=CENTER)
tableDraw.heading("consejo", text="Consejo", anchor=CENTER)

tableDraw.insert(parent='', index='end', iid=0, text='',
                 values=('0', 'Alta', ""))
tableDraw.insert(parent='', index='end', iid=1, text='',
                 values=('0', 'Media', ""))
tableDraw.insert(parent='', index='end', iid=2, text='',
                 values=('0', 'Baja', ""))


window.mainloop()
