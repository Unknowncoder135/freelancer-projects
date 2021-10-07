
import os
import re
import time
import urllib
import urllib.request

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# stealplug SCRIPT................................................................
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


main_list = []
driver = webdriver.Chrome()


# main_url = "https://stealplug.com.my/adidas_yeezy/yeezy_500_stone"
# main_url = "https://stealplug.com.my/travis_scott_collaborations/aj1_low_travis"
main_url = "https://stealplug.com.my/adidas/Adidas_ultra_4d_black_purple"



driver.get(main_url)
time.sleep(2)

r = requests.get(main_url)
soup = BeautifulSoup(r.text,'html.parser')

soups = soup.find('div',class_='in_stock')
add_slit = []
code  =soup.find_all('p',class_='info')
for x in code:
    print(x.text)
    add_slit.append(x.text)

for x in add_slit:
    try:
        bs = x.split('Product Code:')
        bbs = bs[1]
    except:
        pass
code = bbs.strip()
print(code)


sub_diss = []

# try:
#     sub_dis =  soup.find_all('p',class_='info')
#     for x in sub_dis:
#         sub_diss.append(x.text)
#     try:
#         avaliblity = sub_diss[3].split(':')
#         avaliblity =avaliblity[1]
#     except:
#         avaliblity = "Not Found"
#     try:
#         brand = sub_diss[4]
#         brand = brand.replace('Brands','')
#     except:
#         brand = "Not Found"
#     try:
#         code = sub_diss[5]
#         code = code.split(':')
#         code = code[1]
#     except:
#         code = "Not Found"

# except:
#     pass




name = driver.find_element_by_id("page-title").text
# print(name)

price = driver.find_element_by_class_name("live-price").text
# print(price)
price =price.replace(',','')
price = float(price[2:])



description = driver.find_element_by_class_name("meta_description").text



lable1 = driver.find_element_by_xpath('//*[@id="product"]/div[1]/div/div[1]').text
lable1 =  lable1.lower()
print(lable1)


pricess = []
vatians = []


val1=[]
# val2 = []
try:
    for x in range(3,10):
      
        size = driver.find_element_by_xpath(f'//*[@class="form-control"]/option[{x}]')
        names = size.text
        val1.append(names)              
        size.click()

        time.sleep(2)
        prices = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div/ul/li/span').text
        prices = prices.replace(',','')
        prices = prices.split('M')[1]
        print(prices)
        # print(names)
        stock = driver.find_element_by_id("button-cart").text
        stock_count = 'null'
        if stock == 'Sold out':
            stock_status = "Sold out"
            stock_count = 0
        else:
            stock_status = 'available'
        
        variant = {
            f'{lable1}':names,
        }

        mains_dir = {
                'original_price':'null',
                'final_price':float(prices),
                'currency':'RM',
                'stock_status':stock_status,
                'stock_count':stock_count,
                'variant':variant,
                }
        vatians.append(mains_dir)
        print(vatians)
except:
    print("aks")
    pass

if len(vatians) ==  0:
    prices = driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[2]/div/ul/li/span').text
    print(prices)
    print(names)
    stock = driver.find_element_by_id("button-cart").text
    stock_count = 'null'
    if stock == 'Sold out':
        stock_status = "Sold out"
        stock_count = 0
    else:
        stock_status = 'available'


    mains_dir = {
            'original_price':prices,
            'final_price':prices,
            'stock_status':stock_status,
            'stock_count':stock_count,
            'variant':'null',
            }
    vatians.append(mains_dir)
    print(vatians)

# try:
#     ma = driver.find_elements_by_class_name("form-control")
#     ma = ma[2]
#     drp = Select(ma)
#     lens = drp.options
#     for x in lens:
#         ss = x.text
#         x.click()
#         pric = driver.find_element_by_xpath("//*[@id='content']/div[1]/div[2]/div/ul/li/span").text
#         print(pric)
#         size.append(ss)                     
#     size = size[1:]
# except:
#     size = "Not Found"
# size = size[1:]



color = []
finder = driver.find_element_by_class_name("control-label").text
if finder == 'Color':
    color = size
    size = "Not Found"
else:
    color = "Not Found"



rating_count = 0
rating = 0.0

imgs=[]

try:
    for x in range(1,10):
        img = driver.find_element_by_xpath(f'//*[@id="gallery"]/ul/div/div/li[{x}]/a')
        img = img.get_attribute('href')
        imgs.append(img)
except:
    pass


vvs = {
    f'{lable1}':val1
}
item_parent = {
            'item_id':code,
            'name':  name,
            'description' : description,
            'rating' : rating,
            'rating_count': rating_count,
            'url' : main_url,
            'variant':vvs,
            'images' : imgs,
            

        }




main_dir = {
        "item_parent": item_parent,
        "item_variants": vatians,
        }
main_list.append(main_dir)
df = pd.DataFrame(main_list)
df.to_json('stealplugOutput.json', orient='records', lines=True)


print("scrip run Successfully")



driver.quit()