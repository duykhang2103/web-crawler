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
from multiprocessing.pool import ThreadPool

from cellphones_crawl import *


def crawl_detail(url,urls,data,result):
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver_service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=driver_service, options=options)
        
        driver.get(url)
        sleep(random.randint(1,3))
        rating = driver.find_element(By.CSS_SELECTOR,".title.is-4").text.split("/")[0]
        num_of_rates = driver.find_element(By.CLASS_NAME, "boxReview-score").find_element(By.TAG_NAME, "strong").text
        try:    
            items = driver.find_elements(By.CLASS_NAME, 'technical-content-item')
            product_info = []
            for item in items:         
                name = item.find_element(By.TAG_NAME,"p").text  
                value = item.find_element(By.TAG_NAME,"div").text
                product_info.append(name + ": " + value)  
        except NoSuchElementException:
            product_info = []
        data[urls.index(url)].update({"system": product_info , "rating": float(rating), "numOfRating": int(num_of_rates)})    
        result.append(data[urls.index(url)])
    except: 
        pass
    finally:
        driver.quit()
        
def getDetailCellPhones():
    with open("./static/json/cellphones-data.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    result = []
    urls = [item['url'] for item in data]
    pool = ThreadPool(5)
    for i in range (len(urls)) :
        url = urls[i]
        pool.apply_async(crawl_detail, (url,urls,data,result))       
        sleep(0.1) 
        
    pool.close()    
    pool.join()
    return result
def saveCellPhonesDetail(data):            
    with open("./static/json/cellphones-data.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def startCellphoneS():
    saveRawCellPhones(getCellPhones())
    saveCellPhonesDetail(getDetailCellPhones())
    

# saveGearvn(getDetailCellPhones())

#done 