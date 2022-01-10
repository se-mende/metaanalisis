from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import pandas as pd
import time
from config.constants import BD
from pathlib import Path
import utils.helper as helper
import utils.bot as bot

columns = ['title', 'url', 'authors', 'description', 'plus', 'filter', 'page']
temp_folder = 'temp/'

def set_paths(output):
    Path(temp_folder).mkdir(parents=True, exist_ok=True)
    Path(output).unlink(missing_ok=True)

def login_scopus(browser, user, password):
    browser.find_element_by_id('fidname').send_keys(user)
    browser.find_element_by_css_selector('#formegre>font>input[type=password]:nth-child(4)').send_keys(password)
    browser.find_element_by_id('botingre').click()

def login_sciencedirect(browser, user, password):
    browser.find_element_by_id('egre').click()
    browser.find_element_by_id('fidname').send_keys(user)
    browser.find_element_by_id('pass2').send_keys(password)
    browser.find_element_by_id('botingre2').click()

def run(bd_input, pagefile, output_folder, url_general, output, user, password):
    set_paths(output_folder + output)
    browser = Chrome(executable_path='./chromedriver')
    browser.implicitly_wait(30)
    data_frame = pd.DataFrame(columns=columns)

    page = 1#helper.read_page(temp_folder + pagefile)
    browser.get(url_general)

    if user != '' and password != '':
        print('Es necesario loguearse. Intentando loguearse...')
        if bd_input == BD.SCOPUS.value:
            login_scopus(browser, user, password)
        elif bd_input == BD.SCIENCEDIRECT.value:
            login_sciencedirect(browser, user, password)
        elif bd_input == BD.WEBOFSCIENCE.value:
            login_sciencedirect(browser, user, password)
    
    my_html = BeautifulSoup(browser.page_source, 'lxml')

    has_result = True
    first = True
    while has_result:

        has_result, data_frame, my_html = bot.run(bd_input, my_html, data_frame, browser, page, first)
        first = False
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        data_frame.to_excel(output_folder + output)

        page = helper.set_page(temp_folder + pagefile, page)
        time.sleep(10)