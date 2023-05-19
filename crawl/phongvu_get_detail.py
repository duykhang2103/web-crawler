import json
import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd

def getDetailPhongVu():
    data = []
    with open("./static/json/phongvu-data.json", "r", encoding='utf-8') as f:
        data = json.load(f)
        
    urls = [item['url'] for item in data]

    #Khai bao browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)

    for i in range(0, len(urls)):
    # for i in range(20):
        print(i)
        driver.get(urls[i])
        sleep(random.randint(1,3))

        try:    
            sysText = driver.find_element(By.CSS_SELECTOR, ".css-17aam1").text
            sys = sysText.split("\n");
        except NoSuchElementException:
            sys = ""

        if sys == [""]:
            sys = ""
        data[i].update({"system":sys})

    with open("./static/json/1.json", "w", encoding ='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

getDetailPhongVu()