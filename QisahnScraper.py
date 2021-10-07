
import os
import time
import urllib
import urllib.request

import pandas as pd
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
# quisahn SCRIPT................................................................
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

driver = webdriver.Chrome()

master_list = []
main_url = "https://www.qisahn.com/products/the-legend-of-zelda-skyward-sword-hd#"


driver.get(main_url)
time.sleep(1)
imgs= []
img = driver.find_elements_by_xpath('//*[@id="tmb-#i.id.to_s"]/img')
for x in img:
    temp = x.get_attribute('src')
    temp = temp.replace('mini','product')
    imgs.append(temp)
print(imgs)
stock_status=""
stock_count="" 
try:
    price = driver.find_element_by_id('product_price').text
    if price =='Sold Out':
        stock_status = "Sold Out"

except:
    price = "Not Found"
print(price)

main_list = []
r = requests.get(main_url)
soup  = BeautifulSoup(r.text,'html.parser')

name = soup.find('h1',{'id':'product_base_name'}).text.strip()
print(name)
try:
    description = soup.find('div',class_='product_text').text.strip()
except:     
    description ="Not Found"



condition = soup.find_all('div',class_='product-variation-option-container')
for x in condition:
    print(x.text)

edition = soup.find('div',{'id':'edition_variation'}).text.strip()
print(edition)


platform = soup.find('div',{'id':'platform_variation'}).text.strip()
print(platform)

add_to = driver.find_element_by_id('add-to-cart-button').text.strip()
release_date = "Not Found"
if add_to == 'Pre-order':
    release_date = driver.find_element_by_xpath('//*[@id="inside-product-cart-form"]/div[3]/div/div')
    release_date = release_date.split(':')
    release_date = release_date[1]

rating=''
rating_count=0

item_parent = {
            'name':  name,
            'description' : description,
            'rating' : rating,
            'rating_count': rating_count,
            'url' : main_url,

        }


item_variants ={
        'stock_status': stock_status,
        'stock_count': stock_count,
        'images' : imgs,
        }


item_variants1 = []
item_variants1.append(item_variants)
main_dir = {
        "item_parent": item_parent,
        "item_variants": item_variants1,
        }
main_list.append(main_dir)
df = pd.DataFrame(main_list)
df.to_json('theomnideskOutput.json', orient='records', lines=True)


print("scrip run Successfully")


driver.quit()