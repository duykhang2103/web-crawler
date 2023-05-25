import json
import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import threading
from multiprocessing.pool import ThreadPool

from tgdd_crawl import *


def crawlDetailTgdd(url, urls, data, res):
    #Khai bao browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--ignore-certificate-errors-spki-list')
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)

    driver.get(url)
    print(url)
    sleep(random.randint(1,3))
    try:    
        rating_element = driver.find_element(By.CSS_SELECTOR, ".rating-top .point")
        rating = float(rating_element.text)
        total_rating_element = driver.find_element(By.CSS_SELECTOR, ".rating-total")
        total_rating = total_rating_element.text
        numOfRating = int(total_rating.split()[0])
    except NoSuchElementException:
        rating = 0
        numOfRating = 0

    newSystem = []
    try:
        system_box = driver.find_elements(By.CSS_SELECTOR, ".parameter__list li")
        # print("ssssss")
        for item in system_box:
            name = item.find_element(By.CLASS_NAME, "lileft").text
            infor = ""

            liRight = item.find_element(By.CLASS_NAME, "liright")
            inforEle = liRight.find_elements(By.CSS_SELECTOR, "span")
            # print(name)
            # print(len(inforEle))
            for x in inforEle:
                # print(x.text[len(x.text) - 18 : len(x.text)])
                if x.text[len(x.text) - 18 : len(x.text)] == "Xem thông tin hãng":
                    infor = infor + ' ' + x.text[:len(x.text) - 18]
                else:
                    infor = infor + ' ' + x.text

            if name[len(name) - 1] == ":":
                systemItem = name + " " + infor
            else:
                systemItem = name + ": " + infor
            newSystem.append(systemItem)
    except NoSuchElementException:
        newSystem = ""
    data[urls.index(url)].update({"rating":rating, "numOfRating":numOfRating, "system": newSystem})
    res.append(data[urls.index(url)])
    # print(res)
    driver.close()


def getDetailTgdd():
    with open("./static/json/1tgdd-data.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    result = []
    urls = [item['url'] for item in data]
    pool = ThreadPool(5)
    for i in range (len(urls)) :
        url = urls[i]
        pool.apply_async(crawlDetailTgdd, (url,urls,data,result))       
        sleep(0.1) 
        
    pool.close()    
    pool.join()
    return result


def saveTgddDetail(data):
    with open("./static/json/tgdd-data.json", "w", encoding ='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def startTgdd():
    saveRawTgdd("./static/json/tgdd-data.json", runProgramTgdd(accessory_links, accessory_tags))
    saveTgddDetail(getDetailTgdd())

# startTgdd()