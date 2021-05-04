import pandas as pd
import numpy as np
import cvxpy as cp
import math
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

def calcpoly(x,p) :
    a = 0
    for i in range(len(p)) :
        a  = a*x+p[i]
    return a

def cps(x,p) :
    
    return [calcpoly(i,p) for i in x]

#拟合全部事件
r = 6
for e in events :
    data = getdata(event = e)
    a = []
    b = []
    for i in range(len(data[1])) :
        data[1][i] /= 5
    for i in range(r) :
        x = np.mean(data[0][i*2:i*2+2])
        y = np.mean(data[1][i*2:i*2+2])
        ax = []
        for j in range(r) :
            ax.append(pow(x,j))
        a.append(ax)
        b.append(y)
    a = np.array(a)
    b = np.array(b).reshape(r,1)
    c = np.ones(r)
    x = cp.Variable((r,1))
    objective = cp.Minimize((c @(a @ x - b)))
    constraints = [
        a @ x >= b
    ]
    prob = cp.Problem(objective, constraints)
    prob.solve()
    p = x.value.reshape(1,r).tolist()[0]
    p.reverse()
    print("事件%s的函数：y="%e,end="")
    for i in range(len(p) - 2) :
        if i != 0 :
            print("+",end="")
        print("%4.2f*x^%d"%(p[i],len(p)-i-1),end="")
    print("+%4.2f*x+%4.2f"%(p[-2],p[-1]))
    plt.plot(months,cps(months,p),label = "fit")
    '''
    for y in years :
        data = getdata(event = e,year = y)
        plt.plot(data[0],data[1],label = "ori year:"+str(y))
    '''
    plt.plot(data[0],data[1],label = "ori")
    plt.title("event:"+e)
    plt.legend()
    plt.show()
#程序结束后暂停一下
input()
