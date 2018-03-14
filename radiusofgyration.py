import numpy as np
import sys
import csv
import math


a=np.loadtxt(open(sys.argv[1], "rb"), delimiter=",", skiprows=1)

gyr=[]


def radiusCM(a):
    radi=0
    radj=0
    item=0
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j]==1:
                radi+=i
                radj+=j
                item+=1
    radi=radi/item
    radj=radj/item

    return [radi,radj]



def radiusofgration(a):
    counter=0
    sumofr=0
    z=radiusCM(a)
    #z[0]=int(z[0]-len(a)*0.5)
    #z[1]=int(z[1]-len(a)*0.5)
    #h=(z[0]**2+z[1]**2)**0.5
    for i in range(len(a)):
        for j in range(len(a)):
            if a[i][j]==1:
                r=(i-z[0])**2+(j-z[1])**2

                #r=(r-h)**2
                sumofr += r
                counter += 1
                rofgyr = format((sumofr)**0.5/counter,'.2f')
                lncounter=math.log(counter)
                lnrofgyr=math.log((sumofr)**0.5/counter)
                gyr.append(str(counter)+str(" ")+str(rofgyr)+str(" ")+str((lncounter))+str(" ")+str(lnrofgyr))
    return gyr
#print(radiusCM(a))
list=radiusofgration(a)
file=open('radofgyr_neu_'+ sys.argv[1] + '.txt','w')
for item in list:
    file.write("%s\n" % item)
file.close()
