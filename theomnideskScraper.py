import os
import re
import time
import urllib.request

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# theomnidesk SCRIPT................................................................
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

# driver = webdriver.Chrome()

master_list = []
# main_url = "https://theomnidesk.com/collections/omnidesk-ecosystem/products/titus"
main_url = "https://theomnidesk.com/collections/omnidesk-ecosystem/products/flokkgalaxy?variant=40706669478057"
# main_url = "https://theomnidesk.com/collections/omnidesk-ecosystem/products/flokk8020?variant=40691715702953"
main_url = "https://theomnidesk.com/products/switch-pro?pr_prod_strat=description&pr_rec_pid=4352448888875&pr_ref_pid=4509325131819&pr_seq=uniform"
# driver.get(main_url)
# time.sleep(3)

main_list = []
r = requests.get(main_url)
soup = BeautifulSoup(r.text,'html.parser')
try:
    rateing_count = soup.find('span',class_='stamped-summary-text').text
    rateing_count = rateing_count.split(' ')
    rateing_count = int(rateing_count[2])
except:
    rateing_count = 0
try:
    rating = soup.find('span',class_='stamped-summary-text-1').text
    rating = float(rating)
except:
    rating = "Not Found"
# print(rateing_count,rating)
main_url = main_url.split("?")
main_url = main_url[0]
url  = f'{main_url}.json'
# print(url)
data = requests.get(url).json()

# print(data)
name = data['product']['title']
# print(name)

item_id = data['product']['id']
tags = data['product']['tags']

product_type = data['product']['product_type']

template_suffix  = data['product']['template_suffix']

description = data['product']['body_html']
soup = BeautifulSoup(description,'html.parser')
  
for data in soup(['style', 'script']):
    # Remove tags
    data.decompose()

# return data by retrieving the tag content
decs=  ' '.join(soup.stripped_strings)
# js = soup.find_all('p')
# # print(js)
# decs = ""
# for x in js:
#     decs = decs + x.text+" "

val1 = []
val2 = []
vatiants = []
variants = data['product']['variants']
# print(len(variants))

for x in variants:
    option1 = x['option1']
    option2 = x['option2']
    val1.append(option1)
    
    print(option2)
    vari = {
        'color':option1,

    }
    if option2 != None:
        vari['size'] = option2
        val2.append(option2)


    variant_price = x['compare_at_price']
    # print(variant_price)
    if variant_price == '':
        variant_price = float(x['price'])
    final_price =  x['price']
    final_price = float(final_price)
    stock_status = 'available'
    stock_count = 'null'


    mains_dir = {
                'original_price':variant_price,
                'final_price':final_price,
                'stock_status':stock_status,
                'stock_count':stock_count,
                'variant':vari,
                }
    vatiants.append(mains_dir)
    print(mains_dir)


# nm = soup.find_all('div',class_='option_title')
# kk = []
# for x in nm:
#     kk.append(x.text)
#     print(x)

val1 = set(val1)
val2 = set(val2)
jj = []
for x in val2:
    jj.append(x)
vvs = {
    'color':val1,
}
try:
    if jj[0] != None:
        vvs['size'] = val2
except:
    pass



# color = []
# size = []
# for x in variants:
#     variants_id = x['product_id']
#     variants_title = x['title']
#     variants_original_price = float(x['price'])
#     variants_final_price = float(x['compare_at_price'])
#     temp =  variants_title.split('/')
#     if variants_title == 'Default Title':
#         size = "Not Found"
#         color = "Not Found"

#     if len(temp) == 2:
#         color.append(temp[0])
#         size.append(temp[1])
#     variant = {
#         'variants_id':variants_id,
#         'variants_title':variants_title,
#         'variants_original_price':variants_original_price,
#         'variants_final_price':variants_final_price,
#     }
#     variantss.append(variant)
    
# color_size = []
# if color == 'Not Found' or size == 'Not Found':
#     color_size = "not found"
# else:
#     for x in color:
#         for y in size:
#             color_size.append(f'Color: {x}, Size: {y}')




img = data['product']['images']
imgs = []
for x in img:
    imgs.append(x['src'])





item_parent = {
            'item_id':item_id,
            'name':  name,
            'description' : decs,
            'rating' : rating,
            'rating_count': rateing_count,
            'url' : main_url,
            'variants':vvs,
            'images' : imgs,

        }


# item_variants ={
#          'size':size,
#         'color':color,
#         'stock_status': stock_status,
#         'stock_count': stock_count,
#         'template_suffix':template_suffix,
#         # 'Color Family': color_size,
#         # 'variant' :variantss,
        
#         }


# item_variants1 = []
# item_variants1.append(item_variants)
main_dir = {
        "item_parent": item_parent,
        "item_variants": vatiants,
        }
main_list.append(main_dir)
df = pd.DataFrame(main_list)
df.to_json('theomnideskOutput.json', orient='records', lines=True)


print("scrip run Successfully")






