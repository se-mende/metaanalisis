from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
import pandas as pd
import time
from pathlib import Path
import utils.helper as helper
import utils.bot as bot

columns = ['title', 'url', 'authors', 'description', 'plus', 'filter', 'page']
temp_folder = 'temp/'

def run(pagefile, output_folder, url_general, output):
    Path(temp_folder).mkdir(parents=True, exist_ok=True)
    Path(output_folder + output).unlink(missing_ok=True)

    browser = Chrome(executable_path='./chromedriver')
    data_frame = pd.DataFrame(columns=columns)

    page = helper.read_page(temp_folder + pagefile)
    browser.get(url_general)
    my_html = BeautifulSoup(browser.page_source, 'lxml')

    has_result = True
    while has_result:

        has_result, data_frame, my_html = bot.run(my_html, data_frame, browser, page)

        Path(output_folder).mkdir(parents=True, exist_ok=True)
        data_frame.to_excel(output_folder + output)

        page = helper.set_page(temp_folder + pagefile, page)
        time.sleep(10)