import pandas as pd
import numpy as np
import math
from scipy.optimize import curve_fit
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
for i in range(0,table1.shape[0]):
    mapas[table1.iloc[i,0]] = table1.iloc[i,2]

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

#需要拟合的函数形式
def func(x,a,b,c) :
    return abs(a)/(x+b) + c
#批量调用上一个函数
def funcarr(x,a) :
    return [func(i,a[0],a[1],a[2]) for i in x]


#计算每个地区和事件上的分布
#记录所有事件的相关性与距离的对应关系
data = {}
for e in events :
    dstrs = []
    for a in areas :
        dstr = getdata_byweek(area = a,event = e)[1]
        dstr = [i/mapas[a] for i in dstr]
        #为了防止全0
        dstr[0] += 0.001
        dstrs.append(dstr)
    #相关矩阵
    matcor = np.corrcoef(dstrs)
    dicdata = {}
    for i in range(15) :
        for j in range(15) :
            dicdata[matdis[i][j]] = matcor[i][j]
    data[e] = undict(dicdata)

#对记录的数据进行拟合
for e in events :
    args, cov = curve_fit(func, data[e][0], data[e][1])
    args[0] = abs(args[0])
    print("事件%s的参数:a1:%06.2f, a2:%06.2f, a3:%06.2f"%(e,args[0],args[1],args[2]))
    plt.plot(data[e][0],data[e][1],label = "ori")
    vals = funcarr(data[e][0],args)
    plt.plot(data[e][0],vals,label = "fit")
    plt.title("event:"+e)
    plt.legend()
    plt.show()

#此次的重复拟合用于下一步
for e in events :
    args, cov = curve_fit(func, data[e][0], data[e][1])
    vals = funcarr(data[e][0],args)
    plt.plot(data[e][0],vals,label = "fit evtnt:"+e)

plt.legend()
plt.show()
#程序结束后暂停一下
input()

