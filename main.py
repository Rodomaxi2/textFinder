from bs4 import BeautifulSoup
import requests
from requests.exceptions import ConnectionError
import os

# link = 'https://docs.python.org/3.8/library/tkinter.html'
# link = 'https://www.larepublica.co/'
directorio = 'textDir'


# Esta funcion borra todos los archivos de ejecuciones pasadas
def eraseCache():
    for root, dirs, files in os.walk(directorio):
        for name in files:
            os.unlink(os.path.join(root, name))


def formatString(link):
    link = link.replace('<title>', '')
    link = link.replace('</title>', '')
    link = link.replace(' ', '')
    link = link.replace('|', '')
    link = link.replace('?', '')
    link = link.replace('¿', '')
    link = link.replace('\"', '')
    link = link.replace('\\', '')
    link = link.replace('/', '')
    link = link.replace('\n', '')
    return link


def extractText(link, directorio):
    try:
        response = requests.get(link, timeout=(3, 27))
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if(soup.title == None):
                # Si el link actual no tiene una etiqueta de titulo, el titulo sera el propio link formateado
                title = link
                title = formatString(title)
            else:
                try:
                    title = soup.title.string
                    title = formatString(title)

                except ValueError as ve:
                    print('El titulo no contiene el atributo string', ve)
                    return

            # Por cada una de las noticias se creara un archivo con el contenido siguiente
            with open(f'{directorio}/{title}.txt', 'w', encoding='utf-8') as f:
                f.write(title)
                # f.white(link)
                for text in soup.stripped_strings:
                    f.write(text)
                    f.write('\n')

        else:
            return
            # raise ValueError(f'Error: {response.status_code} con link: {link}')

        response.close()
    except requests.exceptions.Timeout:
        print('El tiempo se agoto')

    except ConnectionError:
        print('Link caido')


def searchLinks(link):
    try:
        response = requests.get(link)  # se accede a la pagina principal
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            if not os.path.isdir(directorio):
                os.mkdir(directorio)
            else:
                eraseCache()

            for newLink in soup.find_all('a'):
                try:
                    if(newLink.get('href')):
                        parsedLink = newLink.get('href').replace(' ', '')
                        #print("se encontro el link: ", parsedLink)
                        if parsedLink.find('_blank') > 0:
                            continue
                        elif parsedLink.find('sic') > 0:
                            continue
                        elif parsedLink[0:4] == 'http':
                            pass
                        else:
                            parsedLink = link + parsedLink

                        print(parsedLink)
                        extractText(parsedLink, directorio)
                    else:
                        print('Link no valido')

                except ValueError as ve:
                    print(ve)

        else:
            raise ValueError(f'Error{response.status_}')
    except ValueError as ve:
        print('Un error ocurrio:', ve)
