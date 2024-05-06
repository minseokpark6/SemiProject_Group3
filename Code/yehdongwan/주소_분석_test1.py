import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

##################
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=chrome_options)

####################################

def classify_row(row):
    주거_flag = False
    상업_flag = False
    for value in row.values:
        if '주거' in value:
            주거_flag = True
        if '상업' in value or '공업' in value:
            상업_flag = True
    if 주거_flag and 상업_flag:
        return '혼합지역'
    elif 주거_flag:
        return '주거지역'
    elif 상업_flag:
        return '상업지역'
    else:
        return '분류안됨'



강서_temp = pd.read_csv('강서_tempv4.csv', encoding='cp949')


강서_temp['용도지역_1'] = None
강서_temp['용도지역_2'] = None
강서_temp['용도지역_3'] = None
강서_temp['용도지역_4'] = None
##################################################################################

driver.get("https://www.eum.go.kr/web/mp/mpMapDet.jsp")
print(' ')
print('*'*30)
print('*'*30)
driver.maximize_window()
input_adress = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/input')
search_key = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/a[2]')

# body > div.mpmap_wrap > div.map_left > div.map_header > div > div > div.scroll-wrapper.scrollbar-outer > ul > li:nth-child(1) > a




for ii,item in enumerate(강서_temp['주소']):
    if ii == 37:
        break
    print(ii)
    input_adress.clear()
    input_adress.send_keys(item)
    search_key.click()
    time.sleep(2)
    try:
        print("주소가 존재합니다.")
        see_more_key = driver.find_element(By.CSS_SELECTOR,'#overchk')
        see_more_key.click()
        
    except:
        if driver.find_element(By.CLASS_NAME, "scrollbar-outer.scroll-content").text == "입력하신 지번이 검색되지 않습니다.":
            continue
        
        
        elif driver.find_element(By.CLASS_NAME, "ico01"):
            
            print("123")
            count = -1
            count_ = -1
            새주소 = []
            for index, adress in enumerate(driver.find_elements(By.CSS_SELECTOR, "div.scroll-wrapper.scrollbar-outer > ul > li")):
                print("12")
                if item in driver.find_element(By.CSS_SELECTOR, f"li:nth-child({int(index)+1}) > a").text:
                    count+= 1
                    if "(" in driver.find_element(By.CSS_SELECTOR, f"li:nth-child({int(index)+1}) > a").text:
                        count_ += 1
                        새주소 = driver.find_element(By.CSS_SELECTOR, f"li:nth-child({int(index)+1}) > a").text
                        괄호안의주소 = re.search(r'\((.*?)\)', 새주소).group(1)
                
                
            if count == 0:
                input_adress.clear()
                input_adress.send_keys(괄호안의주소)
                search_key.click()
                if driver.find_element(By.CLASS_NAME, "scrollbar-outer.scroll-content").text == "입력하신 지번이 검색되지 않습니다.":
                    continue
                
            elif count >= 1:
                actions = ActionChains(driver)

                # 마우스를 요소로 이동
                actions.move_to_element(driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > a"))
                
                # 클릭
                actions.click()
                
                # 동작 실행
                actions.perform()
                
            
            
            print("주소가 존재합니다.")
            # see_more_key = driver.find_element(By.CSS_SELECTOR,'#overchk')
            see_more_key = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[2]/p[2]/input')
            print("여기1")
            
            time.sleep(2)
            see_more_key = driver.find_element(By.CSS_SELECTOR,'#overchk')
            see_more_key.click()
            
            # print("여기2")
            # 용도지역_1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[1]/div')
            # 용도지역_2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[2]/div')
            # 용도지역_3 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[3]/div')
            # 용도지역_4 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[4]/div')
            # print(item)
            # print(용도지역_1.text)
            # print(용도지역_2.text)
            # print(용도지역_3.text)
            # print(용도지역_4.text)
            # print(' ')
            # 강서_temp.at[ii,'용도지역_1'] = 용도지역_1.text
            # 강서_temp.at[ii,'용도지역_2'] = 용도지역_2.text
            # 강서_temp.at[ii,'용도지역_3'] = 용도지역_3.text
            # 강서_temp.at[ii,'용도지역_4'] = 용도지역_4.text
            
            # close_key = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/a/img')
            # close_key.click()
                
                    
            
            
            
        # click_key = driver.find_element(By.CSS_SELECTOR, "li:nth-child(1) > a")
        # click_key.click()
        # time.sleep(1)
    
        
        
        
    time.sleep(1)
    용도지역_1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[1]/div')
    용도지역_2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[2]/div')
    용도지역_3 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[3]/div')
    용도지역_4 = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/div[3]/ul/li[4]/div')
    print(item)
    print(용도지역_1.text)
    print(용도지역_2.text)
    print(용도지역_3.text)
    print(용도지역_4.text)
    print(' ')
    강서_temp.at[ii,'용도지역_1'] = 용도지역_1.text
    강서_temp.at[ii,'용도지역_2'] = 용도지역_2.text
    강서_temp.at[ii,'용도지역_3'] = 용도지역_3.text
    강서_temp.at[ii,'용도지역_4'] = 용도지역_4.text
    see_more_key.click()
    close_key = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/a/img')
    close_key.click()


    

driver.quit()
강서_temp['용도지역'] = 강서_temp[['용도지역_1','용도지역_2','용도지역_3','용도지역_4']].apply(classify_row, axis=1)

print(강서_temp['용도지역'])