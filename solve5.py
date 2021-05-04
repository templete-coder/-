import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
table1 = pd.read_excel("附件1：各区域的人口、面积.xlsx")
table2 = pd.read_excel("处理后.xlsx")
table3 = pd.read_excel("距离.xlsx")
#相关列的取值范围
events = ["①","②","③","④","⑤","⑥","⑦"]
years = [2016,2017,2018,2019,2020]
areas=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","P"]
months=[1,2,3,4,5,6,7,8,9,10,11,12]
weeks=[i for i in range(261)]
#图的最短距离矩阵
matdis = table3.iloc[:,1:].values.tolist()
#区域：面积字典
mapas = {}
#区域：人口密度字典
mapad = {}
for i in range(0,table1.shape[0]):
    mapas[table1.iloc[i,0]] = table1.iloc[i,2]
    mapad[table1.iloc[i,0]] = (table1.iloc[i,1]/table1.iloc[i,2])

#将字典解为两个列表
def undict(dic):
    ret = [[],[]]
    sortkeys = sorted(dic.keys())
    for i in sortkeys:
        ret[0].append(i)
        ret[1].append(dic[i])
    return ret

#获取指定条件下的每个周中的事件出现次数
def getdata_byweek(event = False, area = False):
    nt = table2.copy(deep=True)
    if event != False:
        nt = nt[nt['事件类别']==event]
    if area != False:
        nt = nt[nt['事件所在的区域']==area]
    agg = nt.groupby('周数').agg('count')
    data = dict(zip(weeks,[0 for i in range(len(weeks))]))
    for i in range(0,agg.shape[0]):
        data[agg.index.tolist()[i]] = agg.iloc[i,0];
    return undict(data)

for e in events :
    #记录每个地区的事件密度的期望
    mapdd = {}
    #计算每个地区的事件密度的期望
    for a in areas :
        dstr = getdata_byweek(area = a,event = e)[1]
        dstr = [i/mapas[a] for i in dstr]
        mapdd[mapad[a]] = np.mean(dstr)
    #data是所有数据，data2是去除区域P的数据
    data = undict(mapdd)
    data2 = [data[0][0:-2],data[1][0:-2]]
    #设置use，可以使用对应数据进行拟合
    use = data
    p = np.poly1d(np.polyfit(use[0],use[1],1))
    print("事件%s的拟合结果：a1:%06.2f, a2:%06.2f"%(e,list(p)[0],list(p)[1]))
    plt.scatter(data2[0],data2[1],label = "ori evtnt:"+e)
    plt.plot(data2[0],p(data2[0]),label = "fit evtnt:"+e)
plt.legend()
plt.show()
#程序结束后暂停一下
input()
