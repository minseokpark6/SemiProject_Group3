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



############
# open API로 받아오기
# API_key = 'OA-1120'
# service = 'SearchFAQOfGUListService' 
# gu_url = f'http://openapi.seoul.go.kr:8088/{API_key}/json/{service}/1/5'
# gu_list = requests.get(gu_url).json()
# print(gu_list)

gu_list = {'SearchFAQOfGUListService': {'list_total_count': 25, 'RESULT': {'CODE': 'INFO-000', 'MESSAGE': '정상 처리되었습니다'}, 'row': [{'CODE': '315', 'CD_DESC': '강서구'}]}}






df_gu = pd.DataFrame(gu_list['SearchFAQOfGUListService']['row'])
df_gu

gu_json = []
vwolrd_key = '43CA47D5-0AEC-31E0-B596-F219E84702E5'
for gu in df_gu['CD_DESC']:
    url_vworld = f'https://api.vworld.kr/req/data?service=data&version=2.0&request=GetFeature&format=json&errorformat=json&size=10&page=1&data=LT_C_ADSIGG_INFO&attrfilter=sig_kor_nm:like:{gu}&columns=sig_cd,full_nm,sig_kor_nm,sig_eng_nm,ag_geom&geometry=true&attribute=true&key={vwolrd_key}&domain=https://localhost'
    result_dict = requests.get(url_vworld).json()
    gu_json.append(result_dict)
    
    
gu_json


# 서울시 25개 구의 경계 데이터 수집 및 합치기   ->1개 구만 받아오기
features = []
for gu_data in gu_json:  # gu_json 25개 구의 API 응답 데이터 리스트   ->1개구만
   gu_name = gu_data['response']['result']['featureCollection']['features'][0]['properties']['sig_kor_nm']
   feature = {
       "type": "Feature",
       "id": gu_name,  # 구명을 id로 추가
       "geometry": gu_data['response']['result']['featureCollection']['features'][0]['geometry'],
       "properties": {
           "name": gu_name
       }
   }
   features.append(feature)


geojson_data = {
   "type": "FeatureCollection",
   "features": features
}

# GeoJSON 파일 저장
#강서구
with open('data/seoul_gu_boundaries.geojson', 'w', encoding='cp949') as f:
    json.dump(geojson_data, f, ensure_ascii=False)


#korea
rfile = open('Data/skorea-geo.json', 'r', encoding='utf-8').read()
jsonData = json.loads(rfile)
with open('data/korea_boundaries.geojson', 'w',encoding='utf-8') as f:
    json.dump(jsonData, f, ensure_ascii=False)



gdf_ko = gpd.read_file('data/korea_boundaries.geojson')
gdf_gs = gpd.read_file('data/seoul_gu_boundaries.geojson', encoding='cp949')

# A 파일의 구역에서 B 파일의 구역을 뺀 새로운 GeoDataFrame 생성
except_gs = gdf_ko.difference(gdf_gs.unary_union)

# 새로운 GeoDataFrame을 GeoJSON 파일로 저장
except_gs.to_file('data/final_boundaries.geojson', driver='GeoJSON')

#%%   
###########################################
###########################################
###########################################

# def style_function_외곽(feature):
#     return {
#         'opacity': 0.1,
#         'weight': 1,
#         'color': 'gray',
#         'fillOpacity': 0.5,
#         'dashArray': '5, 5',
#     }
# def style_function_강서(feature):
#     return {
#         'fillOpacity': 1,  # 행정 구역의 투명도는 유지
#         'weight': 1,
#         'dashArray': '5, 5',
#     }


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

pie_charts_data = zip(data.consonants, data.vowels)  #######

fig = plt.figure(figsize=(0.5, 0.5))
fig.patch.set_alpha(0)
ax = fig.add_subplot(111)
plots = []
for sizes in pie_charts_data:
    ax.pie(sizes, colors=("#e6194b", "#19e6b4"))
    buff = io.StringIO()
    plt.savefig(buff, format="SVG")
    buff.seek(0)
    svg = buff.read()
    svg = svg.replace("\n", "")
    plots.append(svg)
    plt.cla()
plt.clf()
plt.close()



m = folium.Map(location=(0, 0), zoom_start=2)

for i, coord in enumerate(data.coordinates):
    marker = folium.Marker(coord)
    icon = folium.DivIcon(html=plots[i])
    marker.add_child(icon)
    popup = folium.Popup(
        "Consonants: {}<br>\nVowels: {}".format(data.consonants[i], data.vowels[i])
    )
    marker.add_child(popup)
    m.add_child(marker)






for lat1, lon1, 역명 in zip(지하철lonlat['convY'], 지하철lonlat['convX'], 지하철lonlat['역명']):
    folium.Marker(
        location = [lat1,lon1],
        popup=역명,
        icon=folium.Icon(color='blue', icon_color='white', icon='subway', angle=0, prefix='fa'),
        ).add_to(강서따릉이)

dfdfasdf

##따릉이 spot
for lat,lon, 최종용도 in zip(target_st['위도'],target_st['경도'], target_st['최종용도']):
    if 최종용도 == "상업":
        color = 'orange'
        folium.Marker(
            location = [lat,lon],
            popup="상업지역",
            icon=folium.Icon(icon='Bicycle'),
            ).add_to(강서따릉이)
        
    elif 최종용도 == "주거":
        color = 'blue'
        folium.Marker(
            location = [lat,lon],
            popup="주거지역",
            icon=folium.Icon(icon='Bicycle',icon_color='white',color=color),
            ).add_to(강서따릉이)
        
    else:
        color = 'gray'
        folium.Marker(
            location = [lat,lon],
            popup="분류안됨",
            icon=folium.Icon(color=color),
            ).add_to(강서따릉이)

folium.Marker(
    location = st_2031,
    tooltip = "Click me!",
    popup="HOT PLACE",
    icon=folium.Icon(color='red'),
    ).add_to(강서따릉이)




# url = "https://leafletjs.com/examples/custom-icons/{}".format
# icon_image = url("leaf-red.png")
# shadow_image = url("leaf-shadow.png")

# icon = folium.CustomIcon(
#     icon_image,
#     icon_size=(38, 95),
#     icon_anchor=(22, 94),
#     )

# folium.Marker(
#     location=[37.55956763970192, 126.82985152724713], icon=icon, popup="Mt. Hood Meadows"
# ).add_to(강서따릉이)




        

강서따릉이.save('Data/00_지도_ver01.html')



