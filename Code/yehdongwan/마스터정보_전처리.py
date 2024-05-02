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


data= pd.read_csv('../../Data/따릉이/서울시 따릉이대여소 마스터 정보.csv',encoding='cp949')

대여소_data = data[['대여소_ID', '주소1', '주소2', '위도', '경도']]
대여소_data['isin강서'] = data['주소1'].str.extract(r'(\S+)구')
강서_temp = 대여소_data[대여소_data['isin강서'] == '강서'].reset_index(drop=True)
print(강서_temp.loc[2])





# 주소의 위치로 이동

# driver.get("https://www.eum.go.kr/web/mp/mpMapDet.jsp")

# for item in 강서_temp['주소1']:
#     input_adress = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/input"))).send_keys(f"{item}")
#     search_key = wait.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[1]/input"))).click()
#     see_more_key = wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div[1]/div[1]/a[2]'))).click()
    

# /html/body/div[1]/div[1]/div[1]/input
# /html/body/div[1]/div[1]/div[1]/a[2]
# /html/body/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/p[2]/input
##################################################################################

driver.get("https://www.eum.go.kr/web/mp/mpMapDet.jsp")
print(' ')
print('*'*30)
print('*'*30)

for ii,item in enumerate(강서_temp['주소1']):
    if ii==10:
        break
    input_adress = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/input')
    input_adress.clear()
    input_adress.send_keys(item)
    search_key = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/a[2]')
    search_key.click()
    driver.maximize_window()
    time.sleep(0.5)
    
    see_more_key = driver.find_element(By.CSS_SELECTOR,'#overchk')
    see_more_key.click()
    time.sleep(0.5)
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
    

#overchk
# /html/body/div[6]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div[2]/p[2]/input



#gisMapLayer > div.overPop > ul




# driver.quit()

