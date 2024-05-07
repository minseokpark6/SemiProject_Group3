import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.font_manager as fm
import os
font_path = 'C:\\Windows\\Fonts\\gulim.ttc'
font = fm.FontProperties(fname=font_path).get_name()
mpl.rc('font', family=font)

path = "C:\\Windows\\Fonts"
file_list = os.listdir(path)

강서_데이터1 = pd.read_csv('../../Data/따릉이/강서_따릉이_데이터_01.csv',encoding='utf-8')
강서_데이터2 = pd.read_csv('../../Data/따릉이/강서_따릉이_데이터_02.csv',encoding='utf-8')
강서_데이터 = pd.concat([강서_데이터1,강서_데이터2])
# print(강서_데이터)




#####################


aa = 강서_데이터.sort_values(by=['기준_날짜','기준_시간대'],ascending=[True, True])
aa['time'] = aa['기준_날짜']  +" "+ (aa['기준_시간대'] // 100).astype(str).str.zfill(2) + ':' + (aa['기준_시간대']%100).astype(str).str.zfill(2)
aa['time'] = pd.to_datetime(aa['time'])

aa1 = aa.set_index('time')
aa1.columns


######################


fig, axs = plt.subplots(6,2,figsize=(12, 10))

ax_count = -1
for month, divided_data in aa1.groupby(pd.Grouper(freq='M')):
    ax_count += 1
    print(f"Data for {month}:")
    
    
    min_date = divided_data.index.min()
    max_date = divided_data.index.max()
    total_days = (max_date - min_date).days + 1
        
    시간별이용량 = divided_data.groupby(divided_data.index.hour)['전체_건수'].sum()/total_days

    시간별이용량.plot(kind='bar', ax=axs[ax_count%6,ax_count//6])
    axs[ax_count%6,ax_count//6].set_title(f'{month.month}월')
    axs[ax_count%6,ax_count//6].set_ylim(0, 1500)


plt.tight_layout()

# 그래프 보이기
plt.show()

    
