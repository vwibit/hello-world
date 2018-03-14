import random
import timeit
import numpy as np
import sys
import matplotlib.pyplot as plt
sys.setrecursionlimit(1000)
import csv


def RANDOMSTART(b,RMAX):
    #x=random.randint(int(-(RMAX(CLUSTER,b)+2)+b*0.5),int(RMAX(CLUSTER,b)+2+b*0.5))
    x=  random.randint(-(RMAX+2),(RMAX+2))

    z= -x**2 + (RMAX+2)**2
    z=  z**0.5*(-1)**random.randint(0,1)
    x=x+int(b*0.5)
    z=z+int(b*0.5)
    #print(x,int(z))
    return x, int(z)





def RANDOMSTEP(x,y,b):
    i=random.random()
    if i<0.25:
        x=(x+1)%(b)
    elif i>0.25 and i<0.5:
        y=(y+1)%(b)
    elif i>0.5 and i<0.75:
        x=(x-1)%(b)
    elif i > 0.75:
        y=(y-1)%(b)
    return x,y

def NEXTNEIGHBORCHECK(x,y,b,CLUSTER,k,RMAX):
    CHECK=0
    if (x-int(b*0.5))**2+(y-int(b*0.5))**2 < (RMAX+2)**2:

        a = CLUSTER[(x+1)%(b+1)][y] + CLUSTER[x][(y+1)%(b+1)] + CLUSTER[(x-1)%(b+1)][y] + CLUSTER[x][(y-1)%(b+1)]
    #hier fehlt Pnm
        a=a*0
        if a>0:
            r=random.random()
            if r > 1.0:
                CLUSTER[x][y]=1
                CHECK+=1
        else:
            a = CLUSTER[(x+1)%(b+1)][(y+1)%(b+1)] + CLUSTER[(x+1)%(b+1)][(y-1)%(b+1)] + CLUSTER[(x-1)%(b+1)][(y+1)%(b+1)] + CLUSTER[(x-1)%(b+1)][(y-1)%(b+1)]
            #a=a*0   #hier fehlt Psnm
            if a>0:
            #    r=random.random()
            #    if r > 0.5:
                CLUSTER[x][y]=1
                CHECK+=1
    if CHECK>0:
        T=(x-int(b*0.5))**2+(y-int(b*0.5))**2
        T=T**0.5
        if T > RMAX:
            RMAX=int(T)
        z=RANDOMSTART(b,RMAX)
        x,y=z[0],z[1]
        CHECK=0
        k=k+1
    return x,y,CLUSTER,k,RMAX

def TOOFARAWAY(x,y,b,RMAX,CLUSTER):
    if (x-int(b*0.5))**2+(y-int(b*0.5))**2 > (2*RMAX)**2:
        z=RANDOMSTART(b,RMAX)
        x,y=z[0],z[1]
        a=0
    return x,y,CLUSTER



def DLA(b,N,ParticleNr):
    CLUSTER=[[0 for n in range(b+1)] for m in range(b+1)]
    CLUSTER[int(b*0.5)][int(b*0.5)]=1
    RMAX=1
    z=RANDOMSTART(b,RMAX)
    x,y=z[0],z[1]
    k=0
    for n in range(N):
        #if (x-int(b*0.5))**2+(y-int(b*0.5))**2 < (2*RMAX)**2:
        K = NEXTNEIGHBORCHECK(x,y,b,CLUSTER,k,RMAX)
        x,y,CLUSTER = K[0],K[1],K[2]
        k=K[3]
        RMAX=K[4]
        #print(x,y,'neighbor')
        L = TOOFARAWAY(x,y,b,RMAX,CLUSTER)
        x,y,CLUSTER = L[0],L[1],L[2]
        #print(x,y,'toofar')
        z=RANDOMSTEP(x,y,b)
        #print(z)
        x,y=z[0],z[1]
        #print(x,y,'random')
        if k == int(ParticleNr):
            print(k)
            return CLUSTER
            break
    print(k)
    return CLUSTER

#print(DLA(10,5,1000))

myData=DLA(500,600000000,sys.argv[1])
myFile = open('Fractals_3_'+ sys.argv[1] + sys.argv[2]+'.csv','w')
with myFile:
    writer = csv.writer(myFile,lineterminator = '\n')
    writer.writerows(myData)


#with open('csvFractals.csv', newline='') as myFile:
#    reader = csv.reader(myFile)
#    for row in reader:
#        print(row)

plt.imshow(myData)
#cax = plt.axes([0.85, 0.1, 0.075, 0.8])
#plt.colorbar(cax=cax)

plt.show()

print(timeit.time.process_time())
