import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


data= pd.read_csv('../../../Data/따릉이/서울시 따릉이대여소 마스터 정보.csv',encoding='cp949')

data



대여소_data = data[['대여소_ID', '주소1', '주소2', '위도', '경도']]
대여소_data['isin강서'] = data['주소1'].str.extract(r'(\S+)구')
강서_temp = 대여소_data[대여소_data['isin강서'] == '강서'].reset_index(drop=True)
print(강서_temp)
