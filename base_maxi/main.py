import logging
from selenium import webdriver
from pprint import pprint
import time 
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import cfg_load
from datetime import datetime
import os
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import cfg_load
config_db = cfg_load.load("credential.yaml")
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = config_db["token"]
org = config_db["organisation"]
bucket = config_db["bucket"]
price_list = []

webpages = cfg_load.load("website.yaml")
for page_name, page_link in webpages._dict.items():
    
    driver = webdriver.Chrome(ChromeDriverManager().install())
    config = cfg_load.load("maxi_config.yml")
    driver.get(page_link)

    javaScript = "window.scrollBy(0,1000);"
    driver.execute_script(javaScript)
    time.sleep(15)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    results = soup.find(id="site-layout")

    page_detail = results.find_all("div", class_="product-details-page-details__content__name")

    for job_element in page_detail:
        product_detail = []
        before_price = None
        in_special = "Regular price"
        try:
            before_price = job_element.find("del", "price__value selling-price-list__item__price selling-price-list__item__price--was-price selling-price-list__item__price--__value").text.split()
        except AttributeError:
            pass   #Product not in special so variable is empty
        if before_price is not None: # Product is in special
            in_special = "In special"
        current_regular_price = job_element.find("span", class_="price__value selling-price-list__item__price selling-price-list__item__price--now-price selling-price-list__item__price--__value").text.split()
        relative_price = job_element.find("span", class_="price__value comparison-price-list__item__price__value").text.split()
        relative_price_unit = job_element.find("span", class_="price__unit comparison-price-list__item__price__unit").text.split()
        # product_name = job_element.find("h1", class_="product-name__item product-name__item--name").text.split()
        price_list.append([page_name, in_special, current_regular_price, before_price, relative_price, relative_price_unit])

        with InfluxDBClient(url="https://us-central1-1.gcp.cloud2.influxdata.com", token=token, org=org) as client:
            write_api = client.write_api(write_options=SYNCHRONOUS)
            point = Point(page_name) \
            .tag("food", "food2") \
            .field(f"Current Price", float(current_regular_price[0].replace(',','.'))) \
            .time(datetime.utcnow(), WritePrecision.NS)
            write_api.write(bucket, org, point)

            if before_price is not None:
                write_api = client.write_api(write_options=SYNCHRONOUS)
                point = Point(page_name) \
                .tag("food", "food2") \
                .field(f"Before price", float(before_price[0].replace(',','.'))) \
                .time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket, org, point)
            point = Point(page_name) \
            .tag("food", "food2") \
            .field(f"Relative Price {relative_price_unit}", float(relative_price[0].replace(',','.'))) \
            .time(datetime.utcnow(), WritePrecision.NS)

            write_api.write(bucket, org, point)

        client.close()



    driver.quit()
    print("Closing driver")

    time.sleep(5)
    print("wait ended")
for elem in price_list:
    print(elem)





