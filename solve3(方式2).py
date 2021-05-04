#禁忌的拟合法：混沌拟合
#不需要函数原型，参数也只需要一个
#通过组合基础函数，得到大量的函数原型，进行拟合
import pandas as pd
import numpy as np
import math 
from math import sin,log,sqrt,pow
import copy
from scipy import optimize
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
table1 = pd.read_excel("附件1：各区域的人口、面积.xlsx")
table2 = pd.read_excel("处理后.xlsx")
#相关列的取值范围
events = ["①","②","③","④","⑤","⑥","⑦"]
years = [2016,2017,2018,2019,2020]
areas=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","P"]
months=[1,2,3,4,5,6,7,8,9,10,11,12]

#方差的计算
def dif(a,b) :
    return sum([pow(a[i]-b[i],2) for i in range(len(a))])

#定义公式的所有变化方式
fs1 = [
    "{0}",
    "1/({0})",
    "sin({0})"
]
#定义公式的所有结合方式
fs2 = [
    "({0})+({1})",
    "({0})*({1})",
    "({1})/({0})",
    "{0}"
]

#用于进行最小化的函数
#输入参数，输出应用该参数的模型，与原数据的方差
func = 0
ori = 0
def minz(a) :
    try :
        return dif([func(m,a) for m in months],ori)
    except:
        return 10000000

#拟合过程，对函数原型fs进行拟合
bd = float("inf")
ba = 0
bf = 0
def fit(fs) :
    global func
    global bd
    global ba
    global bf
    func = eval("lambda x,a:" + fs)
    #print(fs)
    #print(minz(1.001))
    a=optimize.fminbound(minz,-100,100)
    if minz(a) < bd :
        bd = minz(a)
        ba = a
        bf = fs

#将所有公式进行结合，并穿插参数
fn = 2
fs = ['x','x']
def fortow() :
    global fs
    if len(fs) == 1 :
        fit(fs[0])
    tmp = copy.deepcopy(fs)
    for i in range(len(fs)-1) :
        for f21 in fs2 :
            for f22 in fs2 :
                nfs = f21.format(fs[i],fs[i+1])
                nfs = f22.format(nfs,'a')
                del fs[i]
                del fs[i]
                fs.insert(i,nfs)
                fortow()
                fs = copy.deepcopy(tmp)

#将所有公式进行变化，并穿插参数
def forone(n):
    global fs
    if n < 0:
        fortow()
    else :
        for f1 in fs1 :
            for f21 in fs2 :
                for f22 in fs2 :
                    tmp = fs[n]
                    fs[n] = f21.format(fs[n],"a")
                    fs[n] = f1.format(fs[n])
                    fs[n] = f22.format(fs[n],"a")
                    forone(n-1)
                    fs[n] = tmp

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

#求解过程
print("程序处理较慢，请耐心等待")
for e in events :
    data = getdata(event = e)
    ori = data[1]
    #print(ori)
    bd = float("inf")
    ba = 0
    bf = 0
    forone(fn-1)
    print("事件%s的预测标准差:%f,参数%f\n函数:y=%s"%(e,sqrt(bd),ba,bf))
    func = eval("lambda x,a:" + bf)
    vals = [func(m,ba) for m in months]
    plt.plot(data[0],data[1],label = "ori")
    plt.plot(months,vals,label = "fit")
    plt.title("event:"+e)
    plt.legend()
    plt.show()

#程序结束后暂停一下
input()
