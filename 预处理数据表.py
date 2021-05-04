import numpy as py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import warnings
warnings.filterwarnings("ignore")
table2 = pd.read_excel("附件2：某地消防救援出警数据.xlsx")
#定义要添加的数据
start = min(table2.iloc[:,1])
year = []
month = []
day = []
weekcount = []
section = []
#计算数据
for i in range(0,table2.shape[0]):
    time = table2.iloc[i,1]
    year.append(time.year)
    month.append(time.month)
    day.append(time.day)
    weekcount.append(int((time-start).days/7))
    section.append(int(table2.iloc[i,2].hour/8))
#将数据添加到对应列
table2['年'] = year
table2['月'] = month
table2['日'] = day
table2['周数'] = weekcount
table2['时间段'] = section
#保存结果
table2.to_excel('./处理后.xlsx')
