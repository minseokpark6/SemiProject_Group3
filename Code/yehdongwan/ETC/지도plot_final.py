# -*- coding: utf-8 -*-
"""
Created on Tue May  7 17:35:01 2024

@author: DW
"""
import pandas as pd
import folium
import requests
import json
import time
import geopandas as gpd



#%%  지하철 위치

# 강서구에 해당하는 역만 추려냅니다.
강서구지하철목록 = ['개화','김포공항','공항시장','신방화','마곡나루','양천향교','가양','증미','등촌','염창','방화','개화산','송정','마곡','발산','우장산','화곡','까치산']
강서구지하철 = pd.DataFrame(강서구지하철목록, columns=['역명'])

위경도api = requests.get('http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/TaimsKsccDvSubwayStationGeom/1.0?apikey=c222bd7a-fc22-47c6-8c34-3d0c144d797c').json()
지하철위경도 = pd.DataFrame(위경도api)
지하철위경도.columns

지하철lonlat = pd.merge(강서구지하철, 지하철위경도, left_on='역명', right_on='stnKrNm', how='left')
지하철lonlat = 지하철lonlat.drop_duplicates(subset=['역명'])






#%%  따릉이 위치

마스터_정보 = "강서_tempv1.csv"
상위20 = "Data/쏠림정도_top20_대여소.csv"

masterlonlat = pd.read_csv(마스터_정보, encoding="cp949")
target_st = pd.read_csv(상위20)

lonlat = pd.merge(target_st, masterlonlat, left_on='대여소_ID', right_on='대여소_ID', how='left')

# 새로운 컬럼 추가
target_st[['경도','위도']] = lonlat[['경도','위도']]


#%%

st_2031 = [37.566925,126.827438]

# 강서구url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_gangseo.geojson"


# Folium 지도 객체 생성

강서따릉이 = folium.Map(
    location=[37.55956763970192, 126.82985152724713], 
    zoom_start=14,
    # tiles='cartodb dark_matter'
    )

#########레이어 추가##########

folium.GeoJson(
    'data/final_boundaries.geojson',
    name='Korea',
    style_function=lambda feature: {
       'fillColor': 'gray',  # A 구역을 회색으로 표시
       'fillOpacity': 0.3,
       'color': 'gray',
       'weight': 1,
   }
    ).add_to(강서따릉이)


#####
import io

import matplotlib.pyplot as plt





subway_group = folium.FeatureGroup(name='지하철')
bicycle_group = folium.FeatureGroup(name='따릉이')



for lat1, lon1, 역명 in zip(지하철lonlat['convY'], 지하철lonlat['convX'], 지하철lonlat['역명']):
    subway_marker = folium.Marker(
        location = [lat1,lon1],
        popup=역명,
        icon=folium.Icon(color='gray', icon_color='white', icon='subway', angle=0, prefix='fa'),
        )
    subway_marker.add_to(subway_group)



##따릉이 spot
for lat,lon, 최종용도 in zip(target_st['위도'],target_st['경도'], target_st['최종용도']):
    if 최종용도 == "상업":
        color = 'orange'
        bicycle_marker = folium.Marker(
            location = [lat,lon],
            popup="상업지역",
            icon=folium.Icon(color=color, icon_color='white', icon='bicycle', angle=0, prefix='fa'),
            )
        
    elif 최종용도 == "주거":
        color = 'blue'
        bicycle_marker = folium.Marker(
            location = [lat,lon],
            popup="주거지역",
            icon=folium.Icon(color=color, icon_color='white', icon='bicycle', angle=0, prefix='fa'),
            )
        
    else:
        color = 'gray'
        bicycle_marker = folium.Marker(
            location = [lat,lon],
            popup="분류안됨",
            icon=folium.Icon(color=color),
            )
    bicycle_marker.add_to(bicycle_group)
    

hot = folium.Marker(
    location = st_2031,
    tooltip = "Click me!",
    popup="HOT PLACE",
    icon=folium.Icon(color='red', icon_color='white', icon='bicycle', angle=0, prefix='fa'),
    )
hot.add_to(bicycle_group)


subway_group.add_to(강서따릉이)
bicycle_group.add_to(강서따릉이)


folium.LayerControl().add_to(강서따릉이)



강서따릉이.save('Data/00_지도_ver02.html')



