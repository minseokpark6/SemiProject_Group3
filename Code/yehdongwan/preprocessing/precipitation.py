import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


plt.close('all')


def categorize_value(value):
    if pd.isna(value):
        return 0
    
    if value < 5:
        return 5
    elif value < 10:
        return 10
    elif value < 20:
        return 20
    elif value < 30:
        return 30
    elif value < 50:
        return 50
    elif value < 80:
        return 80
    else:
        return 100


Data_path1 = f"..\..\..\Data\기상청\강수량.csv"

# Data = pd.read_csv(Data_path1,skiprows=7,encoding='cp949')
Data = pd.read_csv(Data_path1,skiprows=7)

Data.columns

# Data['강수량(mm)'].max()




Data["강수량"] = Data['강수량(mm)'].apply(categorize_value)
Data['날짜'] = pd.to_datetime(Data['날짜'])
precipi = Data["강수량"]
date = Data['날짜']



### plot

bottomspace = 3

fig, ax = plt.subplots(figsize=(12, 4))


ax.set_ylim(-bottomspace, 100)
ax.bar(date, precipi+bottomspace, align='edge', bottom = -bottomspace)  


ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonthday=15, interval=1))


ax.tick_params(axis='x', rotation=45)
ax.grid(axis='y')


#ax.set_xlim(date.iloc[0], date.iloc[-1])
# ax.set_xlim('tight')
plt.show()