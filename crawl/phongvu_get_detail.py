import json
import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import threading
from multiprocessing.pool import ThreadPool

from phongvu_crawl import *

def crawlDetailPhongVu(url, urls, data, res):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)

    driver.get(url)
    sleep(random.randint(1,3))

    try:    
        sysText = driver.find_element(By.CSS_SELECTOR, ".css-17aam1").text
        sys = sysText.split("\n");
    except NoSuchElementException:
        sys = ""

    try:
        nameText = driver.find_element(By.CSS_SELECTOR, ".css-4kh4rf").text
        nameText = nameText.replace("Liên hệ đặt hàng\n", "")
    except NoSuchElementException:
        nameText = ""

    if sys == [""]:
        sys = ""
    # textt = sys
    data[urls.index(url)].update({"name": nameText, "system":sys, "rating": -1, "numOfRating":-1})
    res.append(data[urls.index(url)])
    # print(res)
    driver.close()


def getDetailPhongVu():
    with open("./static/json/phongvu-data.json", "r", encoding='utf-8') as f:
        data = json.load(f)
    result = []
    urls = [item['url'] for item in data]
    pool = ThreadPool(5)
    for i in range (len(urls)) :
        url = urls[i]
        pool.apply_async(crawlDetailPhongVu, (url,urls,data,result))       
        sleep(0.1) 
        
    pool.close()    
    pool.join()
    return result

    # data = []
    # with open("./static/json/phongvu-data.json", "r", encoding='utf-8') as f:
    #     data = json.load(f)
    # urls = [item['url'] for item in data]
    # res = []
    # # Define a list to hold thread objects
    # threads = []

    # # Define the number of threads to run at a time
    # num_threads = 3

    # # Loop through the files and start a thread for each set of 5 files
    # # for i in range(len(urls) - 30, len(urls), num_threads):
    # for i in range(0, len(urls), num_threads):
    # # for i in range(0, 20, num_threads):
    #     files = urls[i:i+num_threads]

    #     # Create a thread for each file and start it
    #     for index, file_name in enumerate(files):
    #         print(file_name)
    #         t = threading.Thread(target=crawlDetailPhongVu, args=(file_name, index, data, res))
    #         threads.append(t)
    #         t.start()

    #     # Wait for all threads to finish
    #     for t in threads:
    #         t.join()
    # # print(textt)
    # return res

def savePhongVuDetail(data):
    with open("./static/json/phongvu-data.json", "w", encoding ='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def startPhongVu():
    saveRawPhongVu("./static/json/phongvu-data.json", runProgramPhongVu(urlList, tagNameList))
    savePhongVuDetail(getDetailPhongVu())

# startPhongVu()
# savePhongVuDetail(getDetailPhongVu())

#done