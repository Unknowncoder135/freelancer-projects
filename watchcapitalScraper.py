
import os
import time
import urllib
import urllib.request
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# watchcapital SCRIPT................................................................
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

main_list = []

url = "https://www.watchcapital.com.sg/product/rolex-sea-dweller-126600"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')
main_url = f'{url}.js'

r = requests.get(main_url)
data = r.json()

rating = 'not Found'
rating_count = 0
product_id = data['id']


name = data['name']


originalPrice = data['price']


img_list = []
img = data['images']
for x in img:
    img_list.append(x['url'])


create_date = data['created_at']


try:
    description = soup.find('div', class_='product_description').text
    description = description.split('\n')
    # print(description)
    Details = description[1]
    year_Purchase = description[2]
    Reference_Number = description[3]
    Box_Papers = description[4]
except:
    description = "Not found"
    Details = "Not found"
    year_Purchase = "Not found"
    Reference_Number = "Not found"
    Box_Papers = "Not found"


# categories = []

# category = data['categories']
# for x in category:
#     id = x['id']
#     names = x['name']
#     cat_url = x['url']
#     small_dir = {
#         'cat_id': id,
#         'cat_name': names,
#         'cat_url': cat_url,
#     }
#     categories.append(small_dir)

stock_status = "avalable"
stock_count = 'null'

item_parent = {
    'item_id': product_id,
    'name':  name,
    'description': description,
    'rating':rating,
    'rating_count': rating_count,
    'url': url,
    'images': img_list,

}


item_variants = {
    'originalPrice': originalPrice,
    'final_price': originalPrice,
    'stock_status':  stock_status,
    'stock_count': stock_count,
    'details': Details,
    'year_Purchase': year_Purchase,
    'Reference_Number': Reference_Number,
}


item_variants1 = []
item_variants1.append(item_variants)
main_dir = {
    "item_parent": item_parent,
    "item_variants": item_variants1,
}

main_list.append(main_dir)
df = pd.DataFrame(main_list)
df.to_json('watchcapitalOutput.json', orient='records', lines=True)
print("script run succecfully")

