from enum import Enum
import utils.scrapper as scrapper
import config.google as google

class BD(Enum):
    GOOGLE = 1
    
output_folder = 'output/'
output = ''
pagefile = ''
url_general = ''

if __name__ == '__main__':

    print('***** Metaanálisis - Andrea Alvarez Ojeda *****\n')
    print('¿Qué base de datos desea buscar?')
    print(f'1. Google ({google.url})')
    bd_input = int(input())

    if(bd_input > 0 and bd_input <= 1):

        if bd_input == BD.GOOGLE.value:
            pagefile = google.page
            url_general = google.url + google.search_term
            output = google.output

        scrapper.run(pagefile, output_folder, url_general, output)
    else:
        print('Opción no válida. Intente de nuevo.')
