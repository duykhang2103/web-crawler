import json
import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

# from crawl.tgdd_crawl import *

def getDetailTgdd():
    data = []
    with open("./static/json/tgdd-data.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        
    urls = [item['url'] for item in data]

    #Khai bao browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)

    for i in range(5):
    # for i in range(0, len(urls)):
        print(i)
        driver.get(urls[i])
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
            # print(len(system_box))
            # print("ssssss")
            for item in system_box:
                name = item.find_element(By.CLASS_NAME, "lileft").text
                infor = ""

                liRight = item.find_element(By.CLASS_NAME, "liright")
                inforEle = liRight.find_elements(By.CSS_SELECTOR, "span")
                # print(name)
                # print(len(inforEle))
                for x in inforEle:
                    infor = infor + ' ' + x.text

                if name[len(name) - 1] == ":":
                    systemItem = name + " " + infor
                else:
                    systemItem = name + ": " + infor
                newSystem.append(systemItem)
        except NoSuchElementException:
            newSystem = ""
        data[i].update({"rating":rating, "numOfRating":numOfRating, "newSystem": newSystem})

    with open("./static/json/11tgdd-data.json", "w", encoding ='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

getDetailTgdd()