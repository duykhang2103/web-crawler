from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException,ElementClickInterceptedException
import time
import random
import json
from time import sleep
import threading
from queue import Queue
from multiprocessing.pool import ThreadPool
options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])

urlList = [
    "https://cellphones.com.vn/laptop.html",
    "https://cellphones.com.vn/phu-kien/chuot-ban-phim-may-tinh/chuot.html",
    "https://cellphones.com.vn/phu-kien/chuot-ban-phim-may-tinh/ban-phim.html",
    "https://cellphones.com.vn/thiet-bi-am-thanh/tai-nghe.html",
    "https://cellphones.com.vn/linh-kien/ram.html",
    "https://cellphones.com.vn/linh-kien/o-cung.html",
    "https://cellphones.com.vn/thiet-bi-am-thanh/micro-thu-am.html"
]

tagNameList = [
    "laptop", "mouse", "keyboard","headphone","ram" , "harddisk","mic"  
]

def crawl(url, tag, data):
    driver_service = Service(executable_path='chromedriver.exe')
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.get(url)
    sleep(random.randint(1,3))
    
    # nut xem them cac brand
    load_more_btn = driver.execute_script("return document.querySelector('.button__link.px-2')") 
    if load_more_btn is not None:
        load_more_btn.click()
    
    brand_links = driver.find_elements(By.CSS_SELECTOR, "a.list-brand__item")
    item_links = [link.get_attribute("href") for link in brand_links]
    brands = []
    for link in brand_links:
        brand_name_element = link.find_elements(By.CSS_SELECTOR, 'img')
        if brand_name_element: 
            brand_name = brand_name_element[0].get_attribute('alt')
        else :
            brand_name = ""
        brands.append(brand_name)

    for i in range(len(item_links)):
        driver.get(item_links[i])
        brand = brands[i]
        sleep(random.randint(1,3))

        while(True):
            try:
                sleep(random.randint(1,3))
                load_more_button = driver.execute_script("return document.querySelector('.btn-show-more')")
                load_more_button.click()
            except (ElementClickInterceptedException, ElementNotInteractableException):
                break
        products = driver.find_elements(By.CSS_SELECTOR, ".product__link")
        for product in products:
            product_url = product.get_attribute('href')
            product_img = product.find_element(By.CSS_SELECTOR, ".product__image > img").get_attribute("src")
            product_name = product.find_element(By.CSS_SELECTOR, ".product__name > h3").text

            product_curprice = product.find_element(By.CSS_SELECTOR, "p.product__price--show").text
            if (product_curprice != "Giá Liên Hệ") :
                product_curprice1 = product_curprice.replace("₫","").replace(".","")
            else : product_curprice1 = '0'

            product_oriprice_element = product.find_elements(By.CSS_SELECTOR, "p.product__price--through")
            product_oriprice = product_oriprice_element[0].text.replace("₫","").replace(" ", "") if product_oriprice_element else ""

            product_discount_element = product.find_elements(By.CSS_SELECTOR, "p.product__price--percent-detail")
            isSale = 1 if product_discount_element else 0
            product_discount = product_discount_element[0].text.replace("Giảm ","").replace("%","") if product_discount_element else ""
            data.append({
                "tag" : tag,
                "img" : product_img,
                "url" : product_url,
                "brand" : brand,                
                "name" : product_name,
                "discount" : product_discount,
                "oriPrice" : product_oriprice,
                "curPrice" : product_curprice,
                "curPrice1" : int(product_curprice1),
                "isSale" : isSale,
                "shopName" : "cellphones",
                "shopName1" : "CellphoneS".
                "rating": -1,
                "numOfRating": -1
            })
            
    driver.close()

def getCellPhones():
    url_groups = [
        urlList[0:3], 
        urlList[3:6], 
        urlList[6:]
        ]
    i = 0
    data = []
    for url_group in url_groups:
        threads = []
        for url in url_group:
            t = threading.Thread(target=crawl, args=(url, tagNameList[i],data))
            i = i + 1
            threads.append(t)
        for t in threads:
            t.start()        
        for t in threads:
            t.join()
    return data
def saveRawCellPhones(data):
    with open("./static/json/cellphones-data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
# saveRawCellPhones(getCellPhones())

#modify Giá liên hệ

