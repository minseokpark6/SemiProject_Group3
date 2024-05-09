# -*- coding: utf-8 -*-
"""
Created on Wed May  8 19:50:05 2024

@author: DW
"""

import folium
import random

longit = 37.671053
latitu = 126.713676
m = folium.Map(location=[longit, latitu], zoom_start=14)

from folium.plugins import MarkerCluster
marker_cluster = MarkerCluster().add_to(m)

iconColor = [ 'red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred',
     'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white',
     'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
iconLenMinusOne = len(iconColor) - 1

# glyphicon 아이콘
#     prefix='glyphicon'  , https://getbootstrap.com/docs/3.3/components/
#     ... icon=folium.Icon(color=iColor,icon='gift', prefix='glyphicon')
# font-awesome 아이콘
#    prefix='fa',   https://fontawesome.com/v4/icons/

# font-awesome 사이트에서 아이콘 리스트를 미리 뽑아왔다.
with open('fontAwesomeIcons.txt', 'r') as f:
    res = f.readlines()



icons = []
for ll in res:
    if ll[0] == '#': continue
    ll2 = ll.rstrip()
    if ll2 not in icons: icons.append(ll.rstrip())



nIcons = len(icons)
print(f'Total {nIcons}')

for i in range(nIcons):
    iColor = iconColor[random.randint(0, iconLenMinusOne)]
    while 'blue' in iColor:
        iColor = iconColor[random.randint(0, iconLenMinusOne)]
    if i % 200 == 0: latitu += 0.01

    folium.Marker(
        location=[longit, latitu],
        popup=folium.Popup(icons[i]+"ddddd", max_width='100'),
        icon=folium.Icon(color='blue', icon_color=iColor,
                                    icon=icons[i], angle=0, prefix='fa')
        ).add_to(marker_cluster)

m.save('map2.html')
