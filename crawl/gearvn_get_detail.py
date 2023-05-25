import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import json
import time 
from selenium.webdriver.common.action_chains import ActionChains
import threading
from itertools import islice
from selenium.webdriver.chrome.service import Service
from time import sleep
import random

from gearvn_crawl import *


def crawl_detail_gearvn(url,urls, products,result):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    driver.get(url)
    sleep(random.randint(1,3))
    try:    
        table = driver.find_element(By.CLASS_NAME, 'table')
        rows = table.find_elements(By.TAG_NAME, 'tr')
        product_info = []
        for rowss in rows:
            cells = rowss.find_elements(By.TAG_NAME, 'td')
            if len(cells) == 2:
                key = cells[0].text.strip()
                value = cells[1].text.strip()
                product_info.append(key + ": " + value)  
    except NoSuchElementException:
        product_info = []
    products[urls.index(url)].update({"system": product_info, , "rating": -1, "numOfRating":-1 })
    result.append(products[urls.index(url)]) 
    driver.close() 

def getDetailGearvn():
    with open("./static/json/gearvn-data.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    result = []
    urls = [item['url'] for item in data]
    pool = ThreadPool(5)
    for i in range (len(urls)) :
        url = urls[i]
        pool.apply_async(crawl_detail_gearvn, (url,urls,data,result))       
        sleep(0.1) 
        
    pool.close()    
    pool.join()
    return result
def saveGearvnDetail(data):            
    with open("./static/json/gearvn-data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def startGearvn():
    saveRawGearvn("./static/json/gearvn-data.json",run_program())
    saveGearvnDetail(getDetailGearvn())
# saveGearvnDetail(getDetailGearvn())