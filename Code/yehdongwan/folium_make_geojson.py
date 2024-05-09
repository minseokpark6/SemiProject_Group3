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


# 서울시 25개 구의 경계 데이터 수집 및 합치기
features = []
for gu_data in gu_json:  # gu_json 25개 구의 API 응답 데이터 리스트
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
with open('data/seoul_gu_boundaries.geojson', 'w', encoding='cp949') as f:
    json.dump(geojson_data, f, ensure_ascii=False)
    
    
###########################################
###########################################
###########################################

def outside_style_function(feature):
    gu_name = feature['properties']['name']
    if gu_name == '강서구':  # 강서구는 어두운 스타일 적용하지 않음
        return {
            'opacity': 0.7,
            'weight': 1,
            'color': 'white',
            'fillOpacity': 0,
        }
    else:  # 강서구 외의 지역은 어둡게 표시
        return {
            'opacity': 0.7,
            'weight': 1,
            'color': 'black',
            'fillOpacity': 0.2,
            'fillColor': 'darkgray',  # 배경 색상을 어둡게 변경
            'dashArray': '5, 5',
        }

# Folium 지도 객체 생성
m = folium.Map(
    location=[37.5651, 126.98955], 
    zoom_start=11
)

# 강서구를 기본 타일로 추가
folium.GeoJson(
    'data/seoul_gu_boundaries.geojson',
    style_function=lambda feature: {
        'opacity': 0.7,
        'weight': 1,
        'color': 'black',
        'fillOpacity': 0.7,
        'fillColor': 'yellow',
        'dashArray': '5, 5',
    }
).add_to(m)

# 강서구 외의 지역을 'cartodb dark_matter' 타일로 추가
folium.GeoJson(
    'data/seoul_gu_boundaries.geojson',
    style_function=outside_style_function
).add_to(m)

# 타일 변경
# folium.TileLayer('cartodb dark_matter').add_to(m)

m


#%%

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

# m = folium.Map(location=st_2031, zoom_start=14)

for lat,lon, 최종용도 in zip(target_st['위도'],target_st['경도'], target_st['최종용도']):
    if 최종용도 == "상업":
        color = 'red'
    elif 최종용도 == "주거":
        color = 'blue'
    else:
        color = 'gray'
    folium.Marker(
        location = [lat,lon],
        tooltip = "Click me!",
        popup="Timberline Lodge",
        icon=folium.Icon(color=color),
        ).add_to(m)

folium.Marker(
    location = st_2031,
    tooltip = "Click me!",
    popup="Timberline Lodge",
    icon=folium.Icon(color='gray'),
    ).add_to(m)



m
m.save('00_지도_ver01.html')




#%%

# 서울내지하철 = pd.read_csv('Data/서울교통공사 역주소 및 전화번호_20240331.csv', encoding='cp949')



# 강서구에 해당하는 역만 추려냅니다.
강서구지하철목록 = ['개화','김포공항','공항시장','신방화','마곡나루','양천향교','가양','증미','등촌','염창','방화','개화산','송정','마곡','발산','우장산','화곡','까치산']
강서구지하철 = pd.DataFrame(강서구지하철목록, columns=['역명'])

위경도api = requests.get('http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/TaimsKsccDvSubwayStationGeom/1.0?apikey=c222bd7a-fc22-47c6-8c34-3d0c144d797c').json()
지하철위경도 = pd.DataFrame(위경도api)
지하철위경도.columns

지하철lonlat = pd.merge(강서구지하철, 지하철위경도, left_on='역명', right_on='stnKrNm', how='left')


for lat,lon, 역명 in zip(지하철lonlat['convY'],지하철lonlat['convX'], 지하철lonlat['역명']):
    folium.Marker(
        location = [lat,lon],
        tooltip = "Click me!",
        popup=역명,
        icon=folium.Icon(color='gray'),
        ).add_to(m)


        




