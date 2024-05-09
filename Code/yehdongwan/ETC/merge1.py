# -*- coding: utf-8 -*-
"""
Created on Mon May  6 12:33:20 2024

@author: DW
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import re


def classify_row(row):
    주거_flag = False
    상업_flag = False
    
    for value in row:
        if '주거' in value:
            주거_flag = True
            break
        if '상업' in value or '공업' in value:
            상업_flag = True
            break
    if 주거_flag and 상업_flag:
        return '혼합지역'
    elif 주거_flag:
        return '주거지역'
    elif 상업_flag:
        return '상업지역'
    else:
        return ' '
    

# utf-8

# cp949

data1  = pd.read_csv('데이터_대여소.csv',encoding='cp949')
data1[['용도지역_1','용도지역_2','용도지역_3','용도지역_4']] = data1[['용도지역_1','용도지역_2','용도지역_3','용도지역_4']].applymap(str)

for ii in range(0, len(data1)):
    data1['용도지역'][ii] = classify_row(data1[['용도지역_1','용도지역_2','용도지역_3','용도지역_4']].loc[ii])



data1.rename(columns={'용도지역': '분류'}, inplace=True)

data1[['대여소_ID', '주소1', '주소2','주소', '분류']].to_csv('용도지역_분류.csv')

