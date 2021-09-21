import requests
import lxml.html as html
import os
import datetime

#Se crean las constantes que contienen las diferentes expresiones en Xpath y el link

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a[@*]/@href' #Se cambia h2 por "text-fill"
XPATH_TITLE = '//div[@class="mb-auto"]/text-fill/span/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY = '//div[@class="html-content"]/p[not(@class)]/text()'

def parse_notice(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH_TITLE)[0]
                title = title.replace('\"','') #se elimina las comillas dobles de los titulos
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)
            except IndexError: #algunas noticias no tienen resumen asi que aun se deben almacenar
                return
            
            with open(f'{today}/{title}.txt', 'w', encoding='utf-8') as f: #Por cada una de las noticias se creara un archivo con el contenido siguiente
                f.write(title)
                f.write('\n\n')
                f.write(summary)
                f.write('\n\n')
                for p in body:
                    f.write(p)
                    f.write('\n')

        else:
             raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL) #se accede a la pagina principal
        if response.status_code == 200:
            home = response.content.decode('utf-8') #La codificacon se cambia para un mejor manejo de caracteres latinos
            parsed = html.fromstring(home) #se obtiene el documento HTML
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            #print(links_to_notices)
            today = datetime.date.today().strftime('%d-%m-%Y') #Se obtiene la fecha del dia de ejecuacion con el formato especificado
            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)
        else:
            raise ValueError(f'Error{response.status_code}')
    except ValueError as ve:
        print(ve)

def run():
    parse_home()

if __name__ == '__main__':
    run()