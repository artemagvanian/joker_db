from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

import datetime
import json

scrape_categories = {'bakerivarer': 'https://joker.no/nettbutikk/varer/bakerivarer',
                     'barneprodukter': 'https://joker.no/nettbutikk/varer/barneprodukter',
                     'dessert': 'https://joker.no/nettbutikk/varer/dessert',
                     'drikkevarer': 'https://joker.no/nettbutikk/varer/drikkevarer',
                     'dyreprodukter': 'https://joker.no/nettbutikk/varer/dyreprodukter',
                     'fisk-skalldyr': 'https://joker.no/nettbutikk/varer/fisk-skalldyr',
                     'frokost-palegg': 'https://joker.no/nettbutikk/varer/frokost-palegg',
                     'frukt-gront': 'https://joker.no/nettbutikk/varer/frukt-gront',
                     'hus-hjem-artikler': 'https://joker.no/nettbutikk/varer/hus-hjem-artikler',
                     'kaker-bakevarer': 'https://joker.no/nettbutikk/varer/kaker-bakevarer',
                     'kioskvarer': 'https://joker.no/nettbutikk/varer/kioskvarer',
                     'kjott': 'https://joker.no/nettbutikk/varer/kjott',
                     'meieriprodukter': 'https://joker.no/nettbutikk/varer/meieriprodukter',
                     'middag': 'https://joker.no/nettbutikk/varer/middag',
                     'middagstilbehor': 'https://joker.no/nettbutikk/varer/middagstilbehor',
                     'ost': 'https://joker.no/nettbutikk/varer/ost',
                     'personlige-artikler': 'https://joker.no/nettbutikk/varer/personlige-artikler',
                     'snacks-godteri': 'https://joker.no/nettbutikk/varer/snacks-godteri'}

driver = webdriver.Chrome()

product_list = []

for category, url in scrape_categories.items():
    driver.get(url)

    while True:
        try:
            view_more = WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.XPATH, r"//button[contains(text(),'Vis flere')]"))
            )
            view_more.click()
        except TimeoutException:
            break

    raw_product_list = driver.find_elements_by_class_name('ws-product-vertical')

    html_to_data_mapper = {'price': 'ws-product-vertical__price',
                           'unit_price': 'ws-product-vertical__price-unit',
                           'title': 'ws-product-vertical__title',
                           'description': 'ws-product-vertical__subtitle'}

    for raw_item in raw_product_list:
        item = {}
        for key, html_class in html_to_data_mapper.items():
            try:
                item[key] = raw_item.find_element_by_class_name(html_class).text
            except NoSuchElementException:
                item[key] = ''
        item['category'] = category
        product_list.append(item)

driver.quit()

with open(f'joker_prices_{datetime.date.today().isoformat()}.json', 'w') as f:
    json.dump(product_list, f)
