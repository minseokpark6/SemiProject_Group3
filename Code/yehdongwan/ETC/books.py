from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

# 주소의 위치로 이동
driver.get("https://product.kyobobook.co.kr/bestseller/online?period=001&per=50")

book_elements = driver.find_elements(By.CLASS_NAME, 'prod_item')

for index, book in enumerate(book_elements):
    rank = index + 1
    title = book.find_element(By.CLASS_NAME, 'prod_info').text
    author = book.find_element(By.CLASS_NAME, 'prod_author').text
    price = book.find_element(By.CLASS_NAME, 'price').text
    print(rank, title, author, price)
