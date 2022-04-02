from __future__ import print_function
from logging import error

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import time 
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
#from __future__ import print_function

link_list = {"https://www.maxi.ca/pain-100-ble-entier-sans-gras-ni-sucre-ajout-s/p/20315894_EA": "https://www.maxi.ca/pain-100-ble-entier-sans-gras-ni-sucre-ajout-s/p/20315894_EA"}

DRIVER_PATH = '/usr/local/bin/chromedriver'

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

# driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver = webdriver.Chrome(ChromeDriverManager().install())


# for website in link_list:
# print(website)
driver.get("https://www.maxi.ca/bifteck-de-contre-filet-de-boeuf/p/21407452_EA")

#h1 = driver.find_element_by_id("faceted-grid")
#lass="product-card-price"
javaScript = "window.scrollBy(0,1000);"
driver.execute_script(javaScript)

#h1 = driver.find_element_by_class_name('product-price__markdown')
#print(h1.text)
time.sleep(15)

soup = BeautifulSoup(driver.page_source, "html.parser")
results = soup.find(id="site-layout")
#print(results.prettify())

page_detail = results.find_all("div", class_="product-details-page-details__content__name")
#print(page_detail)
price_list = []

class_search_current_regular_price = class_="price__value selling-price-list__item__price selling-price-list__item__price--now-price selling-price-list__item__price--__value"
class_search_relative_price = class_="price__value comparison-price-list__item__price__value"
class_search_relative_price_unit = class_="price__unit comparison-price-list__item__price__unit"
class_special_tag = "text text--small3 text--left global-color-black product-promo__badge__content"
class_before_price = "price__value selling-price-list__item__price selling-price-list__item__price--was-price selling-price-list__item__price--__value"

special_tag = None
in_special = False

for job_element in page_detail:
    special_tag = job_element.find(class_=class_special_tag)
    if special_tag is not None: # Product is in special
        before_price = job_element.find("del", class_before_price)
        in_special == True
    current_regular_price = job_element.find("span", class_search_current_regular_price)
    relative_price = job_element.find("span", class_search_relative_price)
    relative_price_unit = job_element.find("span", class_search_relative_price_unit)

    product_name = job_element.find("h1", class_="product-name__item product-name__item--name")

    if in_special is True:
        output = print(product_name.text + ' ' + before_price.text + ' ' + current_regular_price.text )
    else:
        print(product_name.text + ' ' + current_regular_price.text)

driver.close()