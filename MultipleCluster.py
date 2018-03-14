import random
import timeit
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.setrecursionlimit(1000)
import csv


#################################
Grid=100

########################################################Random Cluster####################
cluster=[[0 for x in range(Grid)] for y in range(Grid)]

g=[]

integer=0
for x in range(Grid-1):
    for y in range(Grid-1):
        f = random.random()
        if f >= 0.95:
            if cluster[(x+1)%Grid][y] ==0 and cluster[(x+1)%Grid][(y+1)%Grid]==0 and cluster[(x+1)%Grid][y-1]==0 and cluster[x-1][(y+1)%Grid]==0 and cluster[x-1][y-1]==0 and cluster[x][(y+1)%Grid] == 0 and cluster[x-1][y] == 0 and cluster[x][y-1]==0:
                cluster[x][y] = 1

        if cluster[x][y] == 1:
            g.append([])
            g[integer].append([x,y])
            integer += 1

Startlaenge=len(g)

cluster=[[0 for x in range(Grid)] for y in range(Grid)]

############################################ randomwalk ##############
def randomwalk(i):
    #l= len(g[i])
    #if random.random() > 1/l:
    #    return i

    rand = random.randint(0,3)

    if rand == 0:
        for j in range(len(g[i])):
            g[i][j][0] = (g[i][j][0] + 1)%Grid
    if rand == 1:
        for j in range(len(g[i])):
            g[i][j][1] = (g[i][j][1] + 1)%Grid
    if rand == 2:
        for j in range(len(g[i])):
            g[i][j][0] = (g[i][j][0] - 1)%Grid
    if rand == 3:
        for j in range(len(g[i])):
            g[i][j][1] = (g[i][j][1] - 1)%Grid

    return i

#################################Routine#############

for p in range(8000000):
    x=random.randint(0,len(g)-1)

    z=randomwalk(x)

    Number=[]
    for h in range(len(g[z])):
        x,y = g[z][h][0],g[z][h][1]
        for i in range(len(g)):
            if i != z:
                for j in range(len(g[i])):

                    if g[i][j] == [(x+1)%Grid,y] or g[i][j] == [(x-1)%Grid,y] or g[i][j] == [x,(y+1)%Grid] or g[i][j] == [x,(y-1)%Grid] or g[i][j] == [(x-1)%Grid,(y+1)%Grid] or g[i][j] == [(x+1)%Grid,(y+1)%Grid] or g[i][j] == [(x+1)%Grid,(y-1)%Grid] or g[i][j] == [(x-1)%Grid,(y-1)%Grid]:
                        for j in range(len(g[i])):
                            g[z].append([g[i][j][0],g[i][j][1]])
                        Number.append(i)
                    
                        break

        if len(g) == 1:
            break



##################### double entries will be deleted #####################
    #print(Number)
    Number.sort(reverse=True)
    NumberOut=[]
    if len(Number) > 1:
        NumberOut.append(Number[0])
        for i in range(len(Number)-1):
            if Number[i] != Number[i+1]:
                NumberOut.append(Number[i+1])
        ##print(NumberOut)
        #print(len(g))
        for i in range(len(NumberOut)):
            del g[NumberOut[i]]
        #print(len(g))
    if len(Number) == 1:
        del g[Number[0]]
        #print(len(g))

    for e in range(len(g)):
        Count=0
        g[e].sort()
        for r in range(len(g[e])):
            R=len(g[e])-1-r
            if g[e][R-1] == g[e][R] and len(g[e]) != 1:
                del g[e][R]
                g[e].append(0)
                Count+=1
        if Count != 0:
            for i in range(Count):
                g[e].pop()

    if len(g) == 1:
        break



print('Ziellaenge ist '+str(len(g[0])))
print('Startlaenge ist '+str(Startlaenge))

for j in range(len(g[0])):
    cluster[g[0][j][0]][g[0][j][1]] = 1

myData=cluster
myFile = open('Multi_3_'+str(len(g[0])) +'.csv','w')
with myFile:
    writer = csv.writer(myFile,lineterminator = '\n')
    writer.writerows(myData)

print(timeit.time.process_time())
plt.imshow(cluster)
#cax = plt.axes([0.85, 0.1, 0.075, 0.8])
#plt.colorbar(cax=cax)
plt.show()
