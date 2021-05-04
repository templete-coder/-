import pandas as pd
import numpy as np
import copy
import math
import warnings
table3 = pd.read_excel("距离.xlsx")
#图的最短距离矩阵
matdis = table3.iloc[:,1:].values.tolist()

areas=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","P"]
#新建的消防站数量
cn = 3

#算法所需要使用的全局变量
left = set([i for i in range(15)])
left.remove(9)
left.remove(13)
choice = {9,13}
best = {}
far = 100000

#应用策略cs时，计算max(da)
def maxdis(cs = choice) :
    mn = [100000 for i in range(15)]
    for c in cs :
        for i in range(15) :
            if matdis[c][i] < mn[i] :
                mn[i] = matdis[c][i]
    return max(mn)

#枚举所有的策略，选取max(da)最小的策略
def func(num) :
    global left
    global choice
    global best
    global far
    if num == 0:
        mx = maxdis()
        if mx < far :
            far = mx
            best = copy.deepcopy(choice)
    else :
        cl = copy.deepcopy(left)
        for l in cl :
            left.remove(l)
            choice.add(l)
            func(num-1)
            left.add(l)
            choice.remove(l)
#计算最终的最优策略
func(cn)
#计算抵达最终策略的分步最优策略
best.remove(9)
best.remove(13)
wait = copy.deepcopy(best)
choice = {9,13}
while len(wait) > 0 :
    left = copy.deepcopy(wait)
    best = {}
    far = 100000
    func(1)
    choice = copy.deepcopy(best)
    for i in best:
        if i in wait:
            print(areas[i])
            wait.remove(i)
print(maxdis(best))
#程序结束后暂停一下
input()




