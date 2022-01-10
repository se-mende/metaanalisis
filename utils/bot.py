import re
import time
from bs4 import BeautifulSoup
import config.keyphrases as keyphrases
import utils.helper as helper
from config.constants import BD
import config.scopus as scopus
import config.sciencedirect as sciencedirect

#Scrap
def run (bd_input, my_html, data_frame, browser, page, first):
    if bd_input == BD.GOOGLE.value:
        return google_run(my_html, data_frame, browser, page)
    elif bd_input == BD.SCOPUS.value:
        if first:
            browser.find_element_by_css_selector('#documents-tab-panel>div>form>div:nth-child(2)>div>div.keyword-wrapper.DocumentSearchForm-module__CqSqZ.DocumentSearchForm-module___dnnI>els-input>div>label>input').send_keys(scopus.search_term)
            browser.find_element_by_css_selector('#documents-tab-panel>div>form>div.DocumentSearchForm-module__1S2LH.DocumentSearchForm-module__3fwOu.DocumentSearchForm-module__3dDdf.margin-size-16-t>div:nth-child(2)>button').click()
            time.sleep(5)
            my_html = BeautifulSoup(browser.page_source, 'lxml')
        return scopus_run(my_html, data_frame, browser, page)
    elif bd_input == BD.SCIENCEDIRECT.value:
        if first:
            browser.find_element_by_id('qs-searchbox-input').send_keys(sciencedirect.search_term)
            browser.find_element_by_css_selector('#aa-srp-search-submit-button>button').click()
            browser.find_element_by_css_selector('#srp-facets>div.facet-container>form>div:nth-child(2)>div:nth-child(2)>fieldset>ol>li:nth-child(2)>div>label>span.checkbox-check.checkbox-small.checkbox-label-indent').click()
            time.sleep(5)
            my_html = BeautifulSoup(browser.page_source, 'lxml')
        return sciencedirect_run(my_html, data_frame, browser, page)

def sciencedirect_run(my_html, data_frame, browser, page):
    has_result = False
    results = my_html.find_all('div', class_='result-item-content')
    matching_counter = 0
    counter = 1
    for article in results:
        has_result = True
        article_url = sciencedirect.article_base_url + article.find('a', class_='result-list-title-link')['href']
        browser.get(article_url)
        title = browser.find_element_by_css_selector('#screen-reader-main-title>span').text
        url = article_url
        author_spans = article.find_all('span', class_='author')
        authors = ''
        for span in author_spans:
            authors += span.text + ', '
        try:
            abstract = browser.find_element_by_class_name('abstract.author').text
            abstract = re.sub('\xa0','',re.sub('\n',' ', abstract))
        except:
            abstract = ''
        
        print(str(counter) + '. ' + title)
        print(str(counter) + '. ' + abstract)
        counter += 1

        if passes_filter(title, abstract):
            matching_counter += 1
            plus = get_plus(title, abstract)
            filtro = otro_filtro(title, abstract)
            data_frame = data_frame.append({'title': title,
                                            'url': url,
                                            'authors': authors,
                                            'description': abstract,
                                            'plus': plus,
                                            'filter': filtro,
                                            'page': page},
                                            ignore_index=True)
        browser.back()
        time.sleep(3)
    next_url = f'{sciencedirect.next_url}=FLA&offset={25*page}'
    browser.get(next_url)

    print(f'Encontrados {matching_counter} resultados en página {page}')
    time.sleep(5)

    return has_result, data_frame, BeautifulSoup(browser.page_source, 'lxml')


def scopus_run(my_html, data_frame, browser, page):    
    has_result = False
    results = my_html.find_all('tr', class_='searchArea')
    matching_counter = 0
    counter = 1
    for article in results:
        has_result = True
        article_url = article.find('a', class_='ddmDocTitle')['href']
        browser.get(article_url)
        title = browser.find_element_by_class_name('Highlight-module__1p2SO').text
        url = browser.current_url
        authors_span = article.find('span', class_='ddmAuthorList')
        author_anchors = authors_span.find_all('a')
        authors = ''
        for anchor in author_anchors:
            authors += anchor.text
        abstract = browser.find_element_by_css_selector('#profileleftinside>micro-ui>scopus-document-details-page>div>els-stack>article>div:nth-child(4)>section>div>div.margin-size-4-t.margin-size-16-b').text
        abstract = re.sub('\xa0','',re.sub('\n',' ', abstract))
        
        print(str(counter) + '. ' + title)
        counter += 1

        if passes_filter(title, abstract):
            matching_counter += 1
            plus = get_plus(title, abstract)
            filtro = otro_filtro(title, abstract)
            data_frame = data_frame.append({'title': title,
                                            'url': url,
                                            'authors': authors,
                                            'description': abstract,
                                            'plus': plus,
                                            'filter': filtro,
                                            'page': page},
                                            ignore_index=True)
        browser.back()
        time.sleep(3)
    
    browser.execute_script("return setSelectedLink('NextPageButton');")

    print(f'Encontrados {matching_counter} resultados en página {page}')

    return has_result, data_frame, BeautifulSoup(browser.page_source, 'lxml')

def google_run(my_html, data_frame, browser, page):
    has_result = False
    resultados = my_html.find_all('div', class_='gs_ri')
    matching_counter = 0
    for article in resultados:
        has_result = True
        if article.find('h3', class_='gs_rt').a is not None:
            title = article.find('h3', class_='gs_rt').a.text
            url = article.find('h3', class_='gs_rt').a['href']
            authors = article.find('div', class_='gs_a').text
            abstract = article.find('div', class_='gs_rs').text
            abstract = re.sub('\xa0','',re.sub('\n',' ', abstract))
            if passes_filter(title, abstract):
                matching_counter += 1
                plus = get_plus(title, abstract)
                filtro = otro_filtro(title, abstract)
                data_frame = data_frame.append({'title': title,
                                                'url': url,
                                                'authors': authors,
                                                'description': abstract,
                                                'plus': plus,
                                                'filter': filtro,
                                                'page': page},
                                               ignore_index=True)
    
    browser.find_element_by_class_name("gs_ico.gs_ico_nav_next").click()

    print(f'Encontrados {matching_counter} resultados en página {page}')

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