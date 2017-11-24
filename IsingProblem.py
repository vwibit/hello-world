import numpy as np
import random
import timeit
import matplotlib.pyplot as plt
import math
import sys
sys.setrecursionlimit(10000)

##b ist Dim. der erstellten Gitter, t die Anzahl umgepolter Spins


######ZUFALLSMATRIX ERSTELLEN UND MATRIX DRUCKEN#######
def Zufallsgitter(b):

	a = [[1 for x in range(b)] for y in range(b)]

	for x in range(b):
		for y in range(b):
			i = random.randint(-1, 1)
			while i == 0:
				i = random.randint(-1, 1)
			a[x][y]=i
	return a



##einsermatrix###
def eins(b):
	einsmatrix=[[1 for x in range(b)] for y in range(b)]
	return einsmatrix

def Hamiltonian(x,b):
  	n=0

  	for r in range(-1,b-1):

  		for t in range(-1,b-1):


  			#print(r,t)
  			sum=x[r][t]*(x[r+1][t]+x[r][t+1]+x[r-1][t]+x[r][t-1])
  			n+=sum

  	return -n

def HamInExp(JT,Z,b):
    P=math.exp(-JT*Hamiltonian(Z,b))
	  return P

def magnetisierungZufall(Z,b):
  	sum=0
  	for x in range(b):
  		for y in range(b):
  			sum+=Z[x][y]
  	return abs(sum/(b*b))


def metropolis(b,SpinConf):
	j=0
	z=0

	spinN = [eins(b) for x in range(SpinConf*b)]
	#gitter=spinzustand(b,800)
	#gitter=minuseins(b)
	gitter=Zufallsgitter(b)
	gitter2=eins(b)
	r=SpinConf-1

	metropolisreturn(b,gitter,gitter2,j,r,spinN)
	#print(j,len(spinN))

	for h in range(SpinConf):
		if spinN[h]==spinN[h+1]:
			spinN.pop(h)
			#spinN.append(0)
			#print(h)

	for h in range(len(spinN)-SpinConf):
		spinN.pop()

	#print(len(spinN))
	return spinN


def metropolisreturn(b,gitter,gitter2,j,r,spinN):
				#It needs zufallspin:
				i = random.randint(0,b*b-1)
				q=int((i-i%b)/b)
				w=i%b
				for x in range(b):
					for y in range(b):
						gitter2[x][y]=gitter[x][y]


				gitter2[q][w]=-gitter2[q][w]
				H1=Hamiltonian(gitter,b)
				H2=Hamiltonian(gitter2,b)
				DifH=H2-H1
				#print(H1,H2,DifH)
				#print(gitter)
				#print(gitter2)
				Paccept=min(math.exp(-DifH),1.)
				i = random.randint(0, 100)/100.
				#print(i,Paccept)
				if i < Paccept:
					for x in range(b):
						for y in range(b):
							#print(j)
							spinN[j][x][y]=gitter2[x][y]
							gitter[x][y]=gitter2[x][y]
					j+=1
					#print(j,'change')

				else:
					for x in range(b):
						for y in range(b):
							#print(j)
							spinN[j][x][y]=gitter[x][y]
					j+=1


				if j < r*2:
					return metropolisreturn(b,gitter,gitter2,j,r,spinN)


def avgmagrandom(JT,b,spinN,N):
	sum1=0
	summ=0
	for t in range(N):
		Z=spinN[t]
		#Z=Zufallsgitter(b)
		sum1+=HamInExp(JT,Z,b)*magnetisierungZufall2(Z,b)
		summ+=HamInExp(JT,Z,b)
	return sum1/summ


def AvgMagSimple(b,spinN,N):
	sum=0
	summ=0
	for t in range(N):
		Z=spinN[t]
		#Z=Zufallsgitter(b)
		sum+=magnetisierungZufall(Z,b)
		summ+=1
	return sum/summ


z=[]
for j in range(300):
	z.append(avgmagrandom(0.2,12,metropolis(12,100),100))

plt.hist(z,bins=50)
plt.title("Hits")
plt.xlabel("Value")

plt.show()
