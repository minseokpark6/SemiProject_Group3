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

import branca

bycolor = ["#FF858D","#85BEFF"]

legend_html = """
{% macro html(this, kwargs) %}
<div style="
    position: fixed;
    # bottom: 100px;
    top : 950px;
    left: 50px;
    width: 250px;
    height: 80px;
    z-index:9999;
    font-size:25px;
    ">
    <p><a style="color:#FF8200;font-size:150%;margin-left:20px;">◼</a>&emsp;주거지역</p>
    <p><a style="color:#84CAE7;font-size:150%;margin-left:20px;">◼</a>&emsp;상업지역</p>
    <p><a style="color:#D56062;font-size:150%;margin-left:20px;">◼</a>&emsp;대여량</p>
    <p><a style="color:#067BC2;font-size:150%;margin-left:20px;">◼</a>&emsp;반납량</p>
</div>
<div style="
    position: fixed;
    # bottom: 10px;
    top : 950px;
    left: 50px;
    width: 200px;
    height: 250px;
    z-index:9998;
    font-size:14px;
    background-color: #ffffff;
    opacity: 1;
    ">
</div>
{% endmacro %}
"""

legend = branca.element.MacroElement()
legend._template = branca.element.Template(legend_html)





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
타겟_대여소 = pd.read_csv(상위20)

lonlat = pd.merge(타겟_대여소, masterlonlat, left_on='대여소_ID', right_on='대여소_ID', how='left')

# 새로운 컬럼 추가
타겟_대여소[['경도','위도']] = lonlat[['경도','위도']]
위경도 = []
for index, row in 타겟_대여소.iterrows():
    위경도.append([row['위도'], row['경도']])

    
타겟_대여소['위경도'] = 위경도

#%%

강서따릉이 = folium.Map(
    location=[37.55956763970192, 126.82985152724713], 
    zoom_start=15,
    # tiles='cartodb dark_matter'
    )

import io
import matplotlib.pyplot as plt

bar_charts_data1 = zip(타겟_대여소.출근대여량, 타겟_대여소.출근반납량)

fig = plt.figure(figsize=(0.1,0.8))  # 배경을 투명하게 설정
fig.patch.set_alpha(0)
ax = fig.add_subplot(111)

# 테두리를 제거하기 위해 spines를 비활성화합니다.
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)


plots = []
bar_width = 1
for 대여량,반납량 in bar_charts_data1:
    bar1 = ax.bar(0-bar_width/2, 대여량, bar_width, label='출근대여량', color='#e6194b')
    bar2 = ax.bar(0+bar_width/2, 반납량, bar_width, label='출근반납량', color='#19e6b4')
    ax.set_ylim(0,28000)
    ax.set_xlim(-2,2)
    ax.set_xticks([])
    ax.set_yticks([])
    buff = io.StringIO()
    plt.savefig(buff, format="SVG",transparent = True)
    buff.seek(0)
    svg = buff.read()
    svg = svg.replace("\n", "")
    plots.append(svg)
    plt.cla()
plt.clf()
plt.close()

#%%

출근그룹 = folium.FeatureGroup(name='출근시간')

for i, lon_lat in enumerate(타겟_대여소['위경도']):
    marker = folium.Marker(lon_lat)
    icon = folium.DivIcon(html=plots[i])
    marker.add_child(icon)
    popup = folium.Popup(
        "대여량: {}<br>\반납량: {}".format(타겟_대여소.출근대여량[i], 타겟_대여소.출근반납량[i])
    )
    marker.add_child(popup)
    marker.add_to(출근그룹)
    # 출근그룹.add_child(marker)


출근그룹.add_to(강서따릉이)


#%% 

bar_charts_data2 = zip(타겟_대여소.퇴근대여량, 타겟_대여소.퇴근반납량)

fig = plt.figure(figsize=(0.1,0.8))  # 배경을 투명하게 설정
fig.patch.set_alpha(0)
ax = fig.add_subplot(111)

# 테두리를 제거하기 위해 spines를 비활성화합니다.
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)


plots = []
bar_width = 1
for 대여량,반납량 in bar_charts_data2:
    bar1 = ax.bar(0-bar_width/2, 대여량, bar_width, label='퇴근대여량', color='#e6194b')
    bar2 = ax.bar(0+bar_width/2, 반납량, bar_width, label='퇴근반납량', color='#19e6b4')
    ax.set_ylim(0,28000)
    ax.set_xlim(-2,2)
    ax.set_xticks([])
    ax.set_yticks([])
    buff = io.StringIO()
    plt.savefig(buff, format="SVG",transparent = True)
    buff.seek(0)
    svg = buff.read()
    svg = svg.replace("\n", "")
    plots.append(svg)
    plt.cla()
plt.clf()
plt.close()

#%%

퇴근그룹 = folium.FeatureGroup(name='퇴근시간')

for i, lon_lat in enumerate(타겟_대여소['위경도']):
    marker = folium.Marker(lon_lat)
    icon = folium.DivIcon(html=plots[i])
    marker.add_child(icon)
    popup = folium.Popup(
        "대여량: {}<br>\반납량: {}".format(타겟_대여소.퇴근대여량[i], 타겟_대여소.퇴근반납량[i])
    )
    marker.add_child(popup)
    marker.add_to(퇴근그룹)
    # 출근그룹.add_child(marker)

퇴근그룹.add_to(강서따릉이)

강서따릉이.get_root().add_child(legend)

#%%

st_2031 = [37.566925,126.827438]

# 강서구url = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_gangseo.geojson"


# Folium 지도 객체 생성



#########기본 레이어 생성##########
folium.GeoJson(
    'data/final_boundaries.geojson',
    name='구역경계',
    style_function=lambda feature: {
       'fillColor': 'gray',  # A 구역을 회색으로 표시
       'fillOpacity': 0.3,
       'color': 'gray',
       'weight': 1,
   }
    ).add_to(강서따릉이)
####################


subway_group = folium.FeatureGroup(name='지하철')
bicycle_group = folium.FeatureGroup(name='따릉이')



for lat1, lon1, 역명 in zip(지하철lonlat['convY'], 지하철lonlat['convX'], 지하철lonlat['역명']):
    subway_marker = folium.Marker(
        location = [lat1,lon1],
        tooltip=역명,
        popup=역명,
        icon=folium.Icon(color='gray', icon_color='white', icon='subway', angle=0, prefix='fa'),
        )
    subway_marker.add_to(subway_group)



##따릉이 spot
for lat,lon, 최종용도 in zip(타겟_대여소['위도'],타겟_대여소['경도'], 타겟_대여소['최종용도']):
    if 최종용도 == "상업":
        color = 'blue'
        bicycle_marker = folium.Marker(
            location = [lat,lon],
            popup="상업지역",
            tooltip=최종용도 + "지역",
            icon=folium.Icon(color=color, icon_color='white', icon='bicycle', angle=0, prefix='fa'),
            )
        
    elif 최종용도 == "주거":
        color = 'orange'
        bicycle_marker = folium.Marker(
            location = [lat,lon],
            popup="주거지역",
            tooltip=최종용도 + "지역",
            icon=folium.Icon(color=color, icon_color='white', icon='bicycle', angle=0, prefix='fa'),
            )
        
    else:
        color = 'gray'
        bicycle_marker = folium.Marker(
            location = [lat,lon],
            popup="분류안됨",
            tooltip="분류안됨",
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



강서따릉이.save('Data/00_지도_ver03.html')



