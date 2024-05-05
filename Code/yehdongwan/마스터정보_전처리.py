import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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
        if '상업' in value:
            상업_flag = True
    if 주거_flag and 상업_flag:
        return '혼합지역'
    elif 주거_flag:
        return '주거지역'
    elif 상업_flag:
        return '상업지역'
    else:
        return '분류안됨'


data= pd.read_csv('../../Data/따릉이/서울시 따릉이대여소 마스터 정보.csv',encoding='cp949')

대여소_data = data[['대여소_ID', '주소1', '주소2', '위도', '경도']]
대여소_data['isin강서'] = data['주소1'].str.extract(r'(\S+)구')
강서_temp = 대여소_data[대여소_data['isin강서'] == '강서'].reset_index(drop=True)
print(강서_temp.loc[2])

강서_temp['주소'] = None


#주소 전처리

driver.get("https://search.naver.com/search.naver?where=nexearch&sm=top_sly.hst&fbm=0&acr=4&ie=utf8&query=%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C+%EA%B0%95%EC%84%9C%EA%B5%AC+%EB%A7%88%EA%B3%A1%EC%A4%91%EC%95%99%EB%A1%9C+201+%EB%A1%AF%EB%8D%B0%EC%A4%91%EC%95%99%EC%97%B0%EA%B5%AC%EC%86%8C")

for ii,item in enumerate(강서_temp['주소1']):
    
    item = item.replace("지하","")
    input_adress = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/form/fieldset/div[1]/input')
    input_adress.clear()
    input_adress.send_keys(item)
    
    search_key = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[1]/div[1]/div/form/fieldset/button/i')
    search_key.click()
    time.sleep(1)
    try:
        target_주소 = driver.find_element(By.CLASS_NAME, "GA0XP")
        강서_temp.at[ii,'주소'] =  target_주소.text
    except:
        강서_temp.at[ii,'주소'] =  None
    if ii == 60 or ii == 120 or ii == 180:
        time.sleep(30)
    
    
강서_temp.to_csv('강서_tempv1.csv', index=False)


강서_temp['용도지역_1'] = None
강서_temp['용도지역_2'] = None
강서_temp['용도지역_3'] = None
강서_temp['용도지역_4'] = None
##################################################################################

driver.get("https://www.eum.go.kr/web/mp/mpMapDet.jsp")
print(' ')
print('*'*30)
print('*'*30)

for ii,item in enumerate(강서_temp['주소']):
    print(ii)
    if ii==5:
        break
    input_adress = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/input')
    input_adress.clear()
    input_adress.send_keys(item)
    search_key = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/a[2]')
    search_key.click()
    driver.maximize_window()
    time.sleep(1)
    
    try:
        if driver.find_element(By.CLASS_NAME, "scrollbar-outer scroll-content").text == "입력하신 지번이 검색되지 않습니다.":
            continue    
    except:
        pass
   
    
    see_more_key = driver.find_element(By.CSS_SELECTOR,'#overchk')
    see_more_key.click()
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
    강서_temp.at[ii,'용도지역_1'] = 용도지역_1
    강서_temp.at[ii,'용도지역_2'] = 용도지역_2
    강서_temp.at[ii,'용도지역_3'] = 용도지역_3
    강서_temp.at[ii,'용도지역_4'] = 용도지역_4
    
    close_key = driver.find_element()(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/a/img')
    close_key.click()
    

driver.quit()
강서_temp['용도지역'] = 강서_temp[['용도지역_1','용도지역_2','용도지역_3','용도지역_4']].apply(classify_row, axis=1)

print(강서_temp['용도지역'])