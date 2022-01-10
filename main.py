import utils.scrapper as scrapper
import config.google as google
import config.scopus as scopus
import config.sciencedirect as sciencedirect
import config.webofscience as webofscience
from config.constants import BD
    
output_folder = 'output/'
output = ''
pagefile = ''
url_general = ''
user = ''
password = ''

if __name__ == '__main__':

    print('***** Metaanálisis - Andrea Alvarez Ojeda *****\n')
    print('¿Qué base de datos desea buscar?')
    print(f'1. Google ({google.url})')
    print(f'2. Scopus ({scopus.url})')
    print(f'3. Science Direct ({sciencedirect.url})')
    print(f'4. Web of Science ({webofscience.url})')
    bd_input = int(input())

    if(bd_input > 0 and bd_input <= 4):

        if bd_input == BD.GOOGLE.value:
            pagefile = google.page
            url_general = google.url + google.search_term
            output = google.output
        elif bd_input == BD.SCOPUS.value:
            pagefile = scopus.page
            url_general = scopus.url
            output = scopus.output
            user = scopus.user
            password = scopus.password
        elif bd_input == BD.SCIENCEDIRECT.value:
            pagefile = sciencedirect.page
            url_general = sciencedirect.url
            output = sciencedirect.output
            user = sciencedirect.user
            password = sciencedirect.password
        elif bd_input == BD.WEBOFSCIENCE.value:
            pagefile = webofscience.page
            url_general = webofscience.url
            output = webofscience.output
            user = webofscience.user
            password = webofscience.password

        scrapper.run(bd_input, pagefile, output_folder, url_general, output, user, password)
    else:
        print('Opción no válida. Intente de nuevo.')

    input()
