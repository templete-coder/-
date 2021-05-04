import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from pandas.core.frame import DataFrame
import warnings
warnings.filterwarnings("ignore")
table1 = pd.read_excel("附件1：各区域的人口、面积.xlsx")
table2 = pd.read_excel("处理后.xlsx")
#相关列的取值范围
events = ["①","②","③","④","⑤","⑥","⑦"]
years = [2016,2017,2018,2019,2020]
areas=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","P"]
months=[1,2,3,4,5,6,7,8,9,10,11,12]

#将字典解为两个列表
def undict(dic):
    ret = [[],[]]
    for i in dic.keys():
        ret[0].append(i)
        ret[1].append(dic[i])
    return ret

#获取指定条件下的12个月中的事件出现次数
def getdata(event = False,year = False,years = False, area = False):
    nt = table2.copy(deep=True)
    if event != False:
        nt = nt[nt['事件类别']==event]
    if year != False:
        nt = nt[nt['年']==year]
    if area != False:
        nt = nt[nt['事件所在的区域']==area]
    if years != False:
        nt = nt[nt['年'].isin(years)]
    agg = nt.groupby('月').agg('count')
    data = dict(zip([i for i in range(1,13)],[0 for i in range(12)]))
    for i in range(0,agg.shape[0]):
        data[agg.index.tolist()[i]] = agg.iloc[i,0];
    return undict(data)

#获取指定条件下的5年中的事件
def getdata_byyear(event = False,month = False, area = False):
    nt = table2.copy(deep=True)
    if event != False:
        nt = nt[nt['事件类别']==event]
    if month != False:
        nt = nt[nt['月']==month]
    if area != False:
        nt = nt[nt['事件所在的区域']==area]
    agg = nt.groupby('年').agg('count')
    data = dict(zip(years,[0 for i in range(5)]))
    for i in range(0,agg.shape[0]):
        data[agg.index.tolist()[i]] = agg.iloc[i,0];
    return undict(data)

#拟合一个月份，一个事件的函数，返回最优的拟合
def fitem(e,m,usenum,maxk = 2,mincor = 0.3):
    data = getdata_byyear(event = e,month = m)
    d0 = data[0][0:usenum]
    d1 = data[1][0:usenum]
    a = np.polyfit(d0,d1,1)
    p = np.poly1d(a)
    v = p(d0)
    #
    if np.corrcoef(v,d1)[0][1] < mincor:
        p = np.poly1d([np.mean(d1)])
    if len(p) == 2 and abs(list(p)[0]) > maxk :
        p = np.poly1d([ list(p)[0]/abs(list(p)[0])*maxk, list(p)[1] ])
    return p


pem = {}
def fity(yn):
    global pem
    for e in events :
        pm = {}
        for m in months :
            pm[m] = fitem(e,m,yn)
        pem[e] = pm

def calc(year,event):
    data = [[],[]]
    for i in months :
        data[0].append(i)
        data[1].append(max([0,pem[event][i](year)]))
    return data

#使用前四年进行拟合
fity(4)
y = years[4]
for e in events :
    ori = getdata(event = e, year = y)[1]
    fit = calc(y,e)[1]
    print("事件{0}的预测相关性:{1}".format( e, np.corrcoef(ori,fit)[0][1] ))
    print("事件{0}的预测协方差:{1}".format( e, np.cov(ori,fit)[0][1] ))
    #输出函数图像
    plt.plot(months, ori, label = "ori")
    plt.plot(months, fit, label = "fit")
    plt.title( "evnet:" + e)
    plt.legend()
    plt.show()

#使用所有五年进行拟合
fity(5)
y = 2021
en = [0 for i in range(12)]
for e in events :
    fit = calc(y,e)[1]
    for i in range(0,len(fit)) :
        en[i]+=fit[i]
for i in range(0,len(en)) :
    print("月份{0}的预测事件数:{1}".format(months[i],en[i]))
plt.plot(months, en)
plt.title("predict")
plt.show()
#程序结束后暂停一下
input()
