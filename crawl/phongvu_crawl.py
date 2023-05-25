import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, NoSuchElementException 
from selenium.webdriver.common.by import By
import pandas as pd
import json
import threading
import time
#Khai bao browser
options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])


# driver = webdriver.Chrome(service=driver_service)

#Mo lien ket den trang

urlList = [
    "https://phongvu.vn/c/laptop",
    "https://phongvu.vn/c/chuot",
    "https://phongvu.vn/c/ban-phim-van-phong",
    "https://phongvu.vn/c/tai-nghe",
    "https://phongvu.vn/c/loa",
    "https://phongvu.vn/c/microphone",
    "https://phongvu.vn/c/vga-card-man-hinh",
    "https://phongvu.vn/c/pin-laptop",
    "https://phongvu.vn/c/sac-laptop",
    "https://phongvu.vn/c/usb",
    "https://phongvu.vn/c/ram",
    "https://phongvu.vn/c/o-cung",
    "https://phongvu.vn/c/webcam"
]

tagNameList = [
    "laptop", 
    "mouse", 
    "keyboard", 
    "headphone", 
    "loudspeaker", 
    "mic", 
    "vga", 
    "battery", 
    "charger", 
    "usb", 
    "ram", 
    "harddisk", 
    "webcam"    
]

mainUrl = "https://phongvu.vn"
##Lay link cua tung loai may tinh

def crawlPhongVu(url, tag, res):
    
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service, options=options)
    impUrl = "?page="
    page = 1
    data = []
    while True:
        link = url + impUrl + f'{page}'
        page = page + 1
        driver.get(link)
        sleep(random.randint(1,3))
        
        if page == 3:
            break

        try:
            checkImg = driver.find_element(By.CSS_SELECTOR, ".css-1tg24kl")
            print(page)
            break
        except NoSuchElementException :
            items = driver.find_elements(By.CSS_SELECTOR, ".css-1y2krk0 .css-pxdb0j")
            for item in items:
                tempTag = tag
                tempImg = "<img class item-img src=" + item.find_element(By.TAG_NAME, "img").get_attribute('src') + ">"
                tempUrl = item.get_attribute("href")
                tempBrand = item.find_element(By.CSS_SELECTOR, ".css-rwi43z").text
                tempName = item.find_element(By.TAG_NAME, "img").get_attribute('alt')
                tempSystem = ''

                try:
                    tempDiscount = item.find_element(By.CSS_SELECTOR, ".css-1f8jk2s").text
                    tempIsSale = 1
                except NoSuchElementException:
                    tempDiscount = ''
                    tempIsSale = 0

                try:
                    tempOriPrice = item.find_element(By.CSS_SELECTOR, ".att-product-detail-retail-price").text
                    tempOriPrice1 = item.find_element(By.CSS_SELECTOR, ".att-product-detail-retail-price").text.replace(".","")
                except NoSuchElementException:
                    tempOriPrice = ""
                    tempOriPrice1 = "0"

                try:
                    tempCurPrice = item.find_element(By.CSS_SELECTOR, ".att-product-detail-latest-price").text
                    tempCurPrice1 = item.find_element(By.CSS_SELECTOR, ".att-product-detail-latest-price").text.replace(".","")
                except NoSuchElementException:
                    tempCurPrice = item.find_element(By.CSS_SELECTOR, ".css-quss1").text
                    tempCurPrice1 = item.find_element(By.CSS_SELECTOR, ".css-quss1").text.replace(".", "").split(" - ")[0] +"X"

                data.append({
                    'tag': tempTag,
                    'img': tempImg,
                    'url': tempUrl,
                    'brand': tempBrand,
                    'name': tempName,
                    'system': tempSystem,
                    'discount': tempDiscount[1:len(tempDiscount) - 1],
                    'oriPrice': tempOriPrice[0:len(tempOriPrice) - 2],
                    'curPrice': tempCurPrice[0:len(tempCurPrice) - 2] + ' ₫',
                    'curPrice1': int(tempCurPrice1[0:len(tempCurPrice1) - 2]),
                    'isSale': tempIsSale,
                    'shopName': 'phongvu',
                    'shopName1': 'Phong Vũ',
                })
                # sleep(random.randint(1,3))
    # print(len(items))
    res.extend(data)
    driver.close()


def saveRawPhongVu(filename, data):
    with open(filename, 'w', encoding='utf8') as file:
        json.dump(data, file, ensure_ascii=False, indent = 4)

def runProgramPhongVu(urlList, tagNameList):
    threads = []
    res = []

    for i in range(len(urlList)):
        t = threading.Thread(target=crawlPhongVu, args=(urlList[i], tagNameList[i], res))
        threads.append(t)
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return res

# saveRawPhongVu("./static/json/phongvu-data.json", runProgramPhongVu(urlList, tagNameList))

#done