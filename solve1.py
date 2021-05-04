import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")
table2 = pd.read_excel("处理后.xlsx")
#相关列的取值范围
areas=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","P"]
#计算安全度的函数
def safe(e,p) :
    if e == 0 :
        return float("inf")
    if p == 0:
        return 0.01/e
    return p/e
#寻找目前最不安全的时区
def find(e,p) :
    m = 0
    for i in range(len(e)) :
        if safe(e[i],p[i]) < safe(e[m],p[m]) :
            m = i
    return m

td = table2[table2['日']==1]
def solve_month(m) :
    print("月份:"+str(m))
    tm = td[td['月']==m]
    #e是每个时区的事件期望
    e = []
    for s in range(3) :
        tms = tm[tm['时间段']==s]
        for a in areas :
            e.append((tms[tms['事件所在的区域']==a].shape[0])/5)
    #p是安排到各个时区的人数
    p = [0 for i in range(45)]
    #首先为每个区域分配5人
    for i in range(3) :
        for j in range(5) :
            mx = find(e[i*15:(i+1)*15],p[i*15:(i+1)*15])
            p[i*15 + mx] += 1
    #然后将剩下的15人分配到所有区域中
    for i in range(15) :
        mx = find(e,p)
        p[mx] += 1
    #输出
    for i in range(3) :
        for j in range(15) :
            if p[i*15+j] != 0 :
                print("时段%d:地区%s,人数%d"%(i+1,areas[j],p[i*15+j]))
    m = find(e,p)
    print("最不安全的地区的安全度:%f"%safe(e[m],p[m]))

#处理每个月份
solve_month(2)
solve_month(5)
solve_month(8)
solve_month(11)
#程序结束后暂停一下
input()
