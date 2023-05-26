import csv
from copy import deepcopy


def get2(a):
    return a[1]


def readData():
    with open('anonymous-msweb.csv', encoding='utf-8-sig') as f:
        count = []
        for i in range(1000):
            count.append([])
        allSet = []
        newSet = []
        index = 0
        for row in csv.reader(f, skipinitialspace=True):
            if row[0] == "C":
                index += 1
                newSet = []
                allSet.append(newSet)
            elif row[0] == "V":
                nowNum = int(row[1])
                count[nowNum - 1000].append(index)
                newSet.append(nowNum)
        newSet.sort()
        allSet.append(newSet)
        while len(allSet[0]) == 0:
            allSet.pop(0)
    f.close()
    return allSet, count


supportMin = 50
confidenceMin = 0.5
# 定义最低支持度和置信度
infoSet, countSet = readData()
# countSet里面统计了每个元素出现的所有集合

sati = []
for i in range(1000):
    if len(countSet[i]) > 0:
        newSet = [i, len(countSet[i])]
        sati.append(newSet)
sati.sort(key=get2, reverse=True)
print(sati)

# 寻找频繁1项集
goodSet = []
for i in range(1000):
    count = len(countSet[i])
    if count > supportMin:
        goodSet.append([i, count])

# 寻找频繁2项集
goodSet2 = []
for i in goodSet:
    for j in goodSet:
        if i == j:
            continue
        sameItem = list(set(countSet[i[0]]) & set(countSet[j[0]]))
        # 这句用来寻找两个元素共同出现的集合
        count = len(sameItem)
        if count > supportMin:
            goodSet2.append([i[0], j[0], count])
answer = []
for i in goodSet2:
    conf = i[2] / len(countSet[i[0]])
    if conf > confidenceMin:
        lift = i[2] * 42711 / (len(countSet[i[0]]) * len(countSet[i[1]]))
        answer.append([i[0], i[1], conf, lift])
print(answer)
# 若存在x->y的强关联规则，则输出x,y,置信度，提升度
