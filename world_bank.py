from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

search_term = 'scholar?hl=es&as_sdt=0%2C5&q=%28"all-day+schooling"+OR+"ampliación+de+la+jornada+escolar"+OR+"attend+school+full+time"+OR+"complete+double+schooling"+OR+"complete+school+day"+OR+"doble+escolaridad"+OR+"doble+jornada+escolar"+OR+"double+shift+schools"+OR+"escuela+tiempo+completo"+OR+"extended+school+day"+OR+"extended+school+hours"+OR+"extending+the+school+day"+OR+"full+school+days"+OR+"full+time+school"+OR+"jornada+escolar+completa"+OR+"jornada+escolar+completa"+OR+"jornada+escolar+extendida"+OR+"jornada+única"+OR+"lengthening+the+School+Day"+OR+"long+school+day"+OR+"school+full+time"+OR+"school+full-time"+OR+"the+school+day+extension"%29+&btnG='

words = ['all-day schooling',
'ampliación de escuelas de jornada',
'ampliación de la jornada escolar',
'attend school full time',
'complete double schooling',
'complete school day',
'doble escolaridad',
'doble jornada escolar',
'double schooling',
'double shift schooling',
'double shift schools',
'double-shifting in schools',
'escuela tiempo completo',
'extended school day',
'extended school hours',
'extending the school day',
'extension of all-day schools',
'extension of school coverage',
'extension of the school day',
'full engagement in school',
'full school days',
'full time school',
'full time school day',
'full-time education',
'full-time School Day',
'full-time schools',
'JEC',
'jornada escolar completa',
'jornada escolar completa',
'jornada escolar extendida',
'jornada única',
'lengthening the School Day',
'long school day',
'longer School Day',
'school full time',
'school full time',
'school full-time',
'the school day extension'
]

methodology = ['randomized',
'impact evaluations',
'experiments',
'randomized controlled trials',
'evaluación de impacto',
'experimentos aleatorios',
'RCT',
'experimentos sociales controlados',
'experimentos naturales',
'experimentos aleatorios',
'experimentos sociales',
'cuasi experimentos',
'diferencias en diferencias',
'método de emparejamiento',
'variables instrumentales',
'regresión discontinua',
'RD',
'estudio aleatorio',
'evaluaciones de impacto',
'ensayos controlados aleatorios',
'ECA',
'ensayos aleatorios controlados',
'estudios controlados al azar',
'social experiments',
'controlled experiments',
'economic experiments' ,
'randomized experiments',
'quasi-experiments',
'difference in differences',
'propensity-score matching',
'PSM',
'instrumental variables'
]

population = ['school',
'school students',
'estudiantes de colegio',
'básica',
'media',
'secundaria',
'middle school',
'secondary',
'secondary education',
'secondary school',
'high school',
'basic school',
'elementary school',
'primary school'
]

test = ['math', 'reading', 'mathematics', 'language', 'standard deviation', 'academic achievement', 'matematicas',
        'desviacion estandar', 'lenguaje', 'logro academico']

# CAMBIAR NOMBRE output por output123
excel = 'ouptut_google.xlsx'
columns = ['title', 'url', 'authors', 'description', 'plus', 'filter']


def prepare_text(title, description):
    text = title + ' ' + description
    return text.lower()

def check_list_in_text(text, search_list):
    if any(ext in text for ext in search_list):
        return True
    else:
        return False

def passes_filter(title, description):
    text = prepare_text(title, description)
    has_word = check_list_in_text(text, words)
    has_population = check_list_in_text(text, population)

    return has_word and has_population

#Agrego metodología
def get_plus(title, description):
    text = prepare_text(title, description)
    has_metodology = check_list_in_text(text, methodology)

    return has_metodology

#Otro filtro
def otro_filtro(title, description):
    text = prepare_text(title, description)
    has_filter = check_list_in_text(text, test)

    return has_filter


#Scrap
def bot(my_html, data_frame, browser):
    has_result = False
    resultados = my_html.find_all('div', class_='gs_ri')
    for article in resultados:
        has_result = True
        if article.find('h3', class_='gs_rt').a is None:
            print('***Articulo sin url***')
        else:
            title = article.find('h3', class_='gs_rt').a.text
            url = 'https://scholar.google.es/' + article.find('h3', class_='gs_rt').a['href']
            authors = article.find('div', class_='gs_a').text
            abstract = article.find('div', class_='gs_rs').text
            abstract = re.sub('\xa0','',re.sub('\n',' ', abstract))
            print(abstract)
            if passes_filter(title, abstract):
                print(abstract)
                plus = get_plus(title, abstract)
                filtro = otro_filtro(title, abstract)
                data_frame = data_frame.append({'title': title,
                                                'url': url,
                                                'authors': authors,
                                                'description': abstract,
                                                'plus': plus,
                                                'filter': filtro},
                                               ignore_index=True)
    #browser.find_element_by_class_name("gs_btnPR.gs_in_ib.gs_btn_lrge.gs_btn_half.gs_btn_lsu").click()
    browser.find_element_by_class_name("gs_ico.gs_ico_nav_next").click()

    return has_result, data_frame, BeautifulSoup(browser.page_source, 'lxml')

if __name__ == '__main__':

    #page = int(81211/15)

    try:
        with open('page_google.txt', 'r') as f_page:
            page = int(f_page.read())
    except:
        page = 1

    has_result = True
    browser = Chrome(executable_path='./chromedriver')
    data_frame = pd.DataFrame(columns=columns)
    url_general = f'https://scholar.google.es/{search_term}'
    browser.get(url_general)
    my_html = BeautifulSoup(browser.page_source, 'lxml')

    while has_result:

        has_result, data_frame, my_html = bot(my_html, data_frame, browser)

        #try:
        #    with pd.ExcelWriter(excel, engine='openpyxl') as writer:
        #        writer.book = load_workbook(excel)
        #        data_frame.to_excel(writer, columns=columns)
        #except:
        #    data_frame.to_excel(excel)

        data_frame.to_excel(excel)

        """
        wb = Workbook()
        ws = wb.active
        with pd.ExcelWriter(excel, engine="openpyxl") as writer:
            writer.book = wb
            writer.sheets = dict((ws.title, ws) for ws in wb.worksheets)
            writer.save()
        """

        with open('page_google.txt', 'w') as f_page:
            f_page.write(str(page))

        page += 1

        time.sleep(3)


