from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import time
import random
import json
from time import sleep
import threading

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
    "laptop", "mouse", "keyboard",
    "headphone",
     "ram"    
    ,"harddisk", 
    "mic"  
]
data = []
def crawl(url, tag):
    driver_service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.get(url)
    sleep(random.randint(1,3))
    
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
        
    for i, link in enumerate(item_links):
        driver.get(link)
        brand = brands[i]
        sleep(random.randint(1,3))

        while(True):
            try:
                sleep(random.randint(1,3))
                load_more_button = driver.execute_script("return document.querySelector('.btn-show-more')")
                load_more_button.click()
            except ElementNotInteractableException:
                break
        products = driver.find_elements(By.CSS_SELECTOR, ".product__link")
        for product in products:
            product_url = product.get_attribute('href')
            product_img = product.find_element(By.CSS_SELECTOR, ".product__image > img").get_attribute("src")
            product_name = product.find_element(By.CSS_SELECTOR, ".product__name > h3").text
            product_curprice = product.find_element(By.CSS_SELECTOR, "p.product__price--show").text.replace(" ₫","")

            product_oriprice_element = product.find_elements(By.CSS_SELECTOR, "p.product__price--through")
            product_oriprice = product_oriprice_element[0].text.replace(" ₫","") if product_oriprice_element else ""

            product_discount_element = product.find_elements(By.CSS_SELECTOR, "p.product__price--percent-detail")
            product_discount = product_discount_element[0].text.replace("Giảm ","").replace("%","") if product_discount_element else ""
            data.append({
                "tag" : tag,
                "img" : product_img,
                "url" : product_url,
                "brand" : brand,                
                "name" : product_name,
                "discount" : product_discount,
                "oriPrice" : product_oriprice,
                "curPrice" : product_curprice
            })
            
    driver.close()
    
threads = []

for i, url in enumerate(urlList):
    t = threading.Thread(target=crawl, args=(url, tagNameList[i]))
    threads.append(t)

for t in threads:
    t.start()

for t in threads:
    t.join()

# đa luồng cào system
urls = [item['url'] for item in data]
def crawl_detail(url):
    driver = webdriver.Chrome()
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
    data[urls.index(url)].update({"system": product_info , "rating": rating, "numOfRating": num_of_rates})    
    driver.close()
for i in range(0, len(urls), 5):
    threads_detail = []
    for url in urls[i:i+5]:
        thread = threading.Thread(target=crawl_detail, args=(url,))
        threads_detail.append(thread)
        thread.start()  
    for thread in threads_detail:
        thread.join()
        
with open("Cellphone.json", 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)