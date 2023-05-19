from sched import scheduler

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
import json
import time 
from selenium.webdriver.common.action_chains import ActionChains
import threading

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome()

driver.get('https://gearvn.com/')
html = driver.page_source

# Trích xuất thông tin sản phẩm và lưu vào một danh sách

# Cào laptop windows, bàn phím, chuột, tai nghe
def crawl1(tag, sidebar_dropdown_index,dropdown_container_index, driver,products):
    sidebar_dropdowns = driver.find_elements(By.CSS_SELECTOR,".sidebar-submenu")
    sidebar_dropdown = sidebar_dropdowns[sidebar_dropdown_index]
    dropdown_containers = sidebar_dropdown.find_elements(By.CSS_SELECTOR,".dropdown-container")
    dropdown_container = dropdown_containers[dropdown_container_index]
    sub_cat_items = dropdown_container.find_elements(By.CSS_SELECTOR,"a.sub-cat-item-filter")

    brand_links = dropdown_container.find_elements(By.TAG_NAME, 'a')
    brands = []
    for link in brand_links:
        brand_name = link.get_attribute('textContent')
        brands.append(brand_name)
    
    item_links = [link.get_attribute("href") for link in sub_cat_items]
    for i, link in enumerate(item_links):      
        driver.get(link)
        brand = brands[i]
        max_pages = 10  
        pages_scraped = 0  
        while pages_scraped < max_pages:
            product_rows = driver.find_elements(By.CSS_SELECTOR, '#collection .product-row')
            for row in product_rows:
                try:
                    name = row.find_element(By.CSS_SELECTOR, '.product-row-name').text
                    url = row.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
 
                    price = row.find_element(By.CSS_SELECTOR, '.product-row-price .product-row-sale').text.replace("₫","").replace(",",".")
                    oriprice = row.find_element(By.CSS_SELECTOR, '.product-row-price > del').text.replace("₫","").replace(",",".")
                    discount = row.find_element(By.CSS_SELECTOR, '.new-product-percent').text.replace("%","").replace("-","")
                    img = row.find_element(By.CSS_SELECTOR, '.product-row-thumbnail').get_attribute('src')
                    
                except NoSuchElementException:
                    continue
                products.append({'tag': tag,'brand':brand,'name': name, 'url': url,'oriPrice': oriprice, 'curPrice': price, 'discount': discount, 'img': img})
                
            pages_scraped += 1
            try:
                next_page_link_selector = '.pagination li:nth-child(3) a'
                next_page_link = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_page_link_selector))).get_attribute('href')
                driver.get(next_page_link)
            except:
                break
          
# Cào macbook
def crawlMacbook(tag, sidebar_dropdown_index,dropdown_container_index, driver,products):
    sidebar_dropdowns = driver.find_elements(By.CSS_SELECTOR,".sidebar-submenu")
    sidebar_dropdown = sidebar_dropdowns[sidebar_dropdown_index]
    dropdown_containers = sidebar_dropdown.find_elements(By.CSS_SELECTOR,".dropdown-container")
    dropdown_container = dropdown_containers[dropdown_container_index]
    sub_cat_items = dropdown_container.find_elements(By.CSS_SELECTOR,"a.sub-cat-item-filter")
    brand = "Apple"
    
    item_links = [link.get_attribute("href") for link in sub_cat_items]
    for i, link in enumerate(item_links):
        driver.get(link)
        max_pages = 10  
        pages_scraped = 0  
        while pages_scraped < max_pages:
            product_rows = driver.find_elements(By.CSS_SELECTOR, '#collection .product-row')
            for row in product_rows:
                try:
                    name = row.find_element(By.CSS_SELECTOR, '.product-row-name').text
                    link = row.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    price = row.find_element(By.CSS_SELECTOR, '.product-row-price .product-row-sale').text.replace("₫","").replace(",",".")
                    oriprice = row.find_element(By.CSS_SELECTOR, '.product-row-price > del').text.replace("₫","").replace(",",".")
                    discount = row.find_element(By.CSS_SELECTOR, '.new-product-percent').text.replace("%","").replace("-","")
                    img = row.find_element(By.CSS_SELECTOR, '.product-row-thumbnail').get_attribute('src')
                except NoSuchElementException:
                    continue
                products.append({'tag': tag,'brand':brand,'name': name, 'url': link,'oriPrice': oriprice, 'curPrice': price, 'discount': discount, 'img': img})
            pages_scraped += 1
            try:
                next_page_link_selector = '.pagination li:nth-child(3) a'
                next_page_link = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_page_link_selector))).get_attribute('href')
                driver.get(next_page_link)
            except:
                break

# Cào ram, ổ cứng
def crawl2(tag, sidebar_dropdown_index,dropdown_container_index, driver,products):
    sidebar_dropdowns = driver.find_elements(By.CSS_SELECTOR,".sidebar-submenu")
    sidebar_dropdown = sidebar_dropdowns[sidebar_dropdown_index]
    dropdown_containers = sidebar_dropdown.find_elements(By.CSS_SELECTOR,".dropdown-container")
    dropdown_container = dropdown_containers[dropdown_container_index]
    sub_cat_items = dropdown_container.find_elements(By.CSS_SELECTOR,"a.sub-cat-item-filter")
    
    item_links = [link.get_attribute("href") for link in sub_cat_items]
    for i, link in enumerate(item_links):
        if i <=3 : continue
        driver.get(link)
        max_pages = 10  
        pages_scraped = 0  
        while pages_scraped < max_pages:
            product_rows = driver.find_elements(By.CSS_SELECTOR, '#collection .product-row')
            for row in product_rows:
                try:
                    name = row.find_element(By.CSS_SELECTOR, '.product-row-name').text
                    brand = name.split()[1]
                    link = row.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                    price = row.find_element(By.CSS_SELECTOR, '.product-row-price .product-row-sale').text.replace("₫","").replace(",",".")
                    oriprice = row.find_element(By.CSS_SELECTOR, '.product-row-price > del').text.replace("₫","").replace(",",".")
                    discount = row.find_element(By.CSS_SELECTOR, '.new-product-percent').text.replace("%","").replace("-","")
                    img = row.find_element(By.CSS_SELECTOR, '.product-row-thumbnail').get_attribute('src')
                except NoSuchElementException:
                    continue
                products.append({'tag': tag,'img': img,'url': link,'brand':brand,'name': name ,'discount': discount,'oriPrice': oriprice, 'curPrice': price })
            pages_scraped += 1
            try:
                next_page_link_selector = '.pagination li:nth-child(3) a'
                next_page_link = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.CSS_SELECTOR, next_page_link_selector))).get_attribute('href')
                driver.get(next_page_link)
            except:
                break

def crawl_detail(products,url,urls):
    driver = webdriver.Chrome()
    driver.get(url)
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
    products[urls.index(url)].update({"system": product_info }) 
    driver.close() 
        
def run_program(driver):
    products = []
    crawl1("laptop",0,0,driver,products)  
    crawl1("laptop",1,0,driver,products)
    crawlMacbook("laptop",7,0,driver,products)
    crawl1("keyboard",9,0,driver,products)
    crawl1("keyboard",9,1,driver,products)
    crawl1("mouse",10,0,driver,products)
    crawl1("mouse",10,1,driver,products)
    crawl1("headphone",11,0,driver,products)
    crawl1("headphone",11,1,driver,products)
    crawl2("ram",6,4,driver,products)
    crawl2("harddisk",6,5,driver,products)
    
    # đa luồng cào system
    urls = [item['url'] for item in products]
    for i in range(0, len(urls), 5):
        threads_detail = []
        for url in urls[i:i+5]:
            thread = threading.Thread(target=crawl_detail, args=(products,url,urls))
            threads_detail.append(thread)
            thread.start()  
        for thread in threads_detail:
            thread.join()
    return products

def saveData(link, data):
    with open(link, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

saveData("GearVn.json",run_program(driver))

# Đóng trình duyệt
driver.quit()
