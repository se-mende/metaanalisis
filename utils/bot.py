import re
from bs4 import BeautifulSoup
import config.keyphrases as keyphrases
import utils.helper as helper

#Scrap
def run(my_html, data_frame, browser):
    has_result = False
    resultados = my_html.find_all('div', class_='gs_ri')
    for article in resultados:
        has_result = True
        if article.find('h3', class_='gs_rt').a is None:
            print('***Articulo sin url***')
        else:
            title = article.find('h3', class_='gs_rt').a.text
            url = article.find('h3', class_='gs_rt').a['href']
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
    browser.find_element_by_class_name("gs_ico.gs_ico_nav_next").click()

    return has_result, data_frame, BeautifulSoup(browser.page_source, 'lxml')

def passes_filter(title, description):
    text = helper.prepare_text(title, description)
    has_word = helper.check_list_in_text(text, keyphrases.phrases)
    has_population = helper.check_list_in_text(text, keyphrases.population)

    return has_word and has_population

#Agrego metodología
def get_plus(title, description):
    text = helper.prepare_text(title, description)
    has_metodology = helper.check_list_in_text(text, keyphrases.methodology)

    return has_metodology

#Otro filtro
def otro_filtro(title, description):
    text = helper.prepare_text(title, description)
    has_filter = helper.check_list_in_text(text, keyphrases.test)

    return has_filter