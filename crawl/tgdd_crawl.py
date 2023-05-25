import numpy as np
from selenium import webdriver
from time import sleep
import random
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import threading

#Cao laptop
def Crawl_Laptop(res):
    #Khai bao browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    #Mo lien ket den trang
    driver.get("https://www.thegioididong.com/laptop-ldp")
    sleep(random.randint(1,3))

    #Cao laptop
    ##Lay url cua tung loai may tinh
    links_elements = driver.find_elements(By.CSS_SELECTOR, ".quick-link [href]")
    button_links = [link.get_attribute("href") for link in links_elements]
    data = []

    for button in button_links:
        driver.get(button)
        sleep(random.randint(1,3))
        
        try:
            view_more_button = driver.find_element(By.CSS_SELECTOR, ".view-more ")
            view_more_button.click()
            sleep(random.randint(1,3))
            try:
                view_more_button.click()
                sleep(random.randint(1,3))  
            except ElementNotInteractableException:
                pass     
        except ElementNotInteractableException:
            pass

        #Lay thong tin ve urls, name, curPrice, brand
        elements = driver.find_elements(By.CSS_SELECTOR, ".listproduct .main-contain")
        urls = [url.get_attribute("href") for url in elements]
        names = [name.get_attribute("data-name") for name in elements]
        curPrices = [curPrice.find_element(By.CLASS_NAME, "price").text for curPrice in elements]
        brands = [brand.get_attribute("data-brand") for brand in elements]

        elements_sys = driver.find_elements(By.CSS_SELECTOR, ".utility")
        # systems = [system.text for system in elements_sys]

        l = len(urls)
        # l = 5
        #Lay thong tin ve discount
        discounts = []
        isSales = []
        for i in range(1, l+1):
            try:
                discount_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[{}]/a[1]/div[4]/span".format(i))
            except NoSuchElementException:
                try:
                    discount_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[{}]/a[1]/div[5]/span".format(i))
                except NoSuchElementException:
                    discounts = discounts + [""]
                    isSales = isSales + [0]
                    continue
            discounts = discounts + [discount_element.text]
            isSales = isSales + [1]
            
        #Lay gia goc
        oriPrices = []
        for i in range(1, l+1):
            try:
                oriPrice_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[{}]/a[1]/div[4]/p".format(i))
            except NoSuchElementException:
                try:
                    oriPrice_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[{}]/a[1]/div[5]/p".format(i))
                except NoSuchElementException:
                    oriPrices = oriPrices + [""]
                    continue
            oriPrices = oriPrices + [oriPrice_element.text]

        #Lay thong tin ve anh
        imgs = []
        for i in range(1, l+1):
            try:
                img_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[%i]/a[1]/div[2]/img" % (i))
            except NoSuchElementException:
                try:
                    img_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[%i]/a[1]/div[2]/img[1]" % (i))
                except:
                    print("sos")
                    print(button)
                    print(i)
                    pass
                # /html/body/div[6]/section/div[3]/ul/li[1]/a[1]/div[2]/img
                # /html/body/div[6]/section/div[3]/ul/li[2]/a[1]/div[2]/img[1]
                # /html/body/div[6]/section/div[3]/ul/li[3]/a[1]/div[2]/img[1]
            img = img_element.get_attribute("src")
            if img is None:
                img = img_element.get_attribute("data-src")
            imgs = imgs + [img]

        #Chuan hoa thong tin
        for i in range(0, len(discounts)):
            discounts[i] = discounts[i][0 : len(discounts[i])-1]
        for i in range(0, len(oriPrices)):
            oriPrices[i] = oriPrices[i][0 : len(oriPrices[i])-1]
        # systems_list = []
        # for system in systems:
        #     systems_list = systems_list + [system.split('\n')]

        for i in range(0, l):
            print(i)
            print(urls[i])
            print(curPrices[i])
            print(curPrices[i][0 : len(curPrices[i]) - 1].replace(".",""))

            res.append({"tag": "laptop",
                            "img": imgs[i],        
                            "url": urls[i],
                            "brand": brands[i],   
                            "name": names[i],
                            "system": "",
                            "discount": discounts[i].replace("-",""),
                            "oriPrice": oriPrices[i].replace(",", "."),
                            "curPrice": curPrices[i],
                            "curPrice1": int(curPrices[i][0 : len(curPrices[i]) - 1].replace(".","")),
                            "isSale": isSales[i],
                            "shopName": 'thegioididong',
                            "shopName1": 'Thế giới di động',
                            })


        #Tro ve trang chinh -> tiep tuc vao cac loai may tinh khac    
        driver.get("https://www.thegioididong.com/laptop-ldp")
        sleep(random.randint(1,3))
    
    # saveRawTgdd("laptop.json", data)
    #Dong url
    driver.close()
    return res

#Cao phu kien
def Crawl_Accessory(accessory_link, accessory_tag, res):
    #Khai bao browser
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service)
    # data = []
    #Truy cap link
    driver.get(accessory_link)
    sleep(random.randint(1,3))

    #Hien thi tat ca san pham
    while True:
        try:
            view_more_button = driver.find_element(By.CSS_SELECTOR, ".view-more ")
            view_more_button.click()
            sleep(random.randint(1,3))   
        except ElementNotInteractableException:
            break

    #Lay thong tin
    elements = driver.find_elements(By.CSS_SELECTOR, ".listproduct .main-contain")
    urls = [url.get_attribute("href") for url in elements]
    names = [name.get_attribute("data-name") for name in elements]
    curPrices = [curPrice.find_element(By.CLASS_NAME, "price").text for curPrice in elements]
    brands = [brand.get_attribute("data-brand") for brand in elements]

    l = len(urls)

    #Lay thong tin ve discount
    discounts = []
    isSales = []
    for i in range(1, l+1):
        try:
            discount_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[{}]/a[1]/div[3]/span".format(i))
        except NoSuchElementException:
            discounts = discounts + [""]
            isSales = isSales + [0]
            continue
        discounts = discounts + [discount_element.text]
        isSales = isSales + [1]
            
    #Lay gia goc
    oriPrices = []
    for i in range(1, l+1):
        try:
            oriPrice_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[{}]/a[1]/div[3]/p".format(i))
        except NoSuchElementException:
            oriPrices = oriPrices + [""]
            continue
        oriPrices = oriPrices + [oriPrice_element.text]

    #Lay thong tin ve anh
    imgs = []
    for i in range(1, l+1):
        img_element = driver.find_element("xpath","/html/body/div[6]/section/div[3]/ul/li[{}]/a[1]/div[2]/img".format(i))
        img = img_element.get_attribute("src")
        if img is None:
            img = img_element.get_attribute("data-src")
        imgs = imgs + [img]

    #Chuan hoa thong tin
    for i in range(0, len(discounts)):
        discounts[i] = discounts[i][0 : len(discounts[i])-1]
    for i in range(0, len(oriPrices)):
        oriPrices[i] = oriPrices[i][0 : len(oriPrices[i])-1]

    #Tao data de ghi vao json
    for i in range(0, l):
        res.append({"tag": accessory_tag,
                    "img": imgs[i],        
                    "url": urls[i],
                    "brand": brands[i],   
                    "name": names[i],
                    "system": "",
                    "discount": discounts[i].replace("-",""),
                    "oriPrice": oriPrices[i].replace(",", "."),
                    "curPrice": curPrices[i].replace(",", "."),
                    "curPrice1": int(curPrices[i][0 : len(curPrices[i]) - 1].replace(".","")),
                    "isSale": isSales[i],
                    "shopName": 'thegioididong',
                    "shopName1": 'Thế giới di động',               
                    })
    
    # saveRawTgdd(accessory_tag + ".json", data)
    #Dong driver
    driver.close()
    return res


accessory_links = [
    "https://www.thegioididong.com/chuot-may-tinh",
    "https://www.thegioididong.com/ban-phim", 
    "https://www.thegioididong.com/tai-nghe", 
    "https://www.thegioididong.com/o-cung-di-dong"
]
accessory_tags = [
    "mouse",
    "keyboard",
    "headphone", 
    "harddisk"
]

# Đa luồng
def runProgramTgdd(accessory_links, accessory_tags):
    threads = []
    res1 = []
    res = Crawl_Laptop(res1)
    for i in range(0, len(accessory_links)):
        threads.append(threading.Thread(target=Crawl_Accessory, args = (accessory_links[i], accessory_tags[i], res)))

    for t in threads:
        t.start()

    # Đợi cho tất cả các thread kết thúc
    for t in threads:
        t.join()
    
    return res

#Ghi file json
def saveRawTgdd(filename, data):
    with open(filename, "w", encoding ='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# saveRawTgdd("./static/json/test-crawl-tgdd-data.json", runProgramTgdd(accessory_links, accessory_tags)

# test laptop
#test at home