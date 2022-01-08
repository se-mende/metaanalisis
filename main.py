import pandas as pd
import time
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from pathlib import Path
import utils.helper as helper
import config.google as google
import utils.bot as bot

output_folder = 'output/'
columns = ['title', 'url', 'authors', 'description', 'plus', 'filter']
data_frame = pd.DataFrame(columns=columns)
browser = Chrome(executable_path='./chromedriver')
page = 1

if __name__ == '__main__':

    pagefile = google.page

    helper.read_page(pagefile)
    url_general = google.url + google.search_term
    browser.get(url_general)
    my_html = BeautifulSoup(browser.page_source, 'lxml')

    has_result = True
    while has_result:

        has_result, data_frame, my_html = bot.run(my_html, data_frame, browser)

        Path(output_folder).mkdir(parents=True, exist_ok=True)
        data_frame.to_excel(output_folder + google.output)

        page = helper.set_page(pagefile, page)
        time.sleep(10)


