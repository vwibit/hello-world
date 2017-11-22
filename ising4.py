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

def minuseins(b):
	einsmatrix=[[-1 for x in range(b)] for y in range(b)]
	return einsmatrix




######HAMILTONIAN, Range und das zu untersuchende Gitter sind wählbar##############
def Hamiltonian(x,b):
	n=0

	for r in range(-1,b-1):

		for t in range(-1,b-1):


			#print(r,t)
			sum=x[r][t]*(x[r+1][t]+x[r][t+1]+x[r-1][t]+x[r][t-1])
			n+=sum

	return -n


###NORMALIZATION###



def summeallerspins(JT,b):
	summe=0
	gitter=eins(b)
	for f in range(b):
		for g in range(b):
			gitter[f][g]=-1
			#print(gitter)
			summe+=np.exp(-JT*Hamiltonian(gitter,b))
			#print(summe)
		#print(summe)
	#print("Die Energie ist " + repr(summe))
	return summe

#print(summeallerspins(5))


####Ein spezieller Spinzustand

def spinzustand(b,t):
	gitter = eins(b)
	spinsumme = 0
	for f in range(b):
		for g in range(b):

			if spinsumme < t:
				spinsumme += 1
				gitter[f][g]=-1
			else:
				#print(spinsumme)
				break

	return gitter

def WahrscheinlichkeiteinesSpinzustandes(b,t):
	h=spinzustand(b,t)
	P=np.exp(-0.5*Hamiltonian(h,b))/summeallerspins(b)
	return P

def HamInExp(JT,Z,b):
	P=math.exp(-JT*Hamiltonian(Z,b))
	return P
#print(WahrscheinlichkeiteinesSpinzustandes(20,14))


######MAGNETIZATION#########

def magnetisierung(b,t):
	r=b*b
	d=r-2*t
	m=d/(2*r)
	m=abs(m)
	return m

def magnetisierungZufall(Z,b):
	sum=0
	for x in range(b):
		for y in range(b):
			sum+=Z[x][y]
	return abs(sum/(b*b))
#print(magnetisierung(5,10))

def magnetisierungZufall2(Z,b):
	sum=0
	for x in range(b):
		for y in range(b):
			sum+=Z[x][y]
	return sum/(b*b)


#########Erwartungswert der Durchschnittsmagnetisierung
def avgmag(b):
	sum=0
	for t in range(b*b):
		sum+=WahrscheinlichkeiteinesSpinzustandes(b,t)*magnetisierung(b,t)
	return sum


#bis 18 gehts##
#print(avgmag(19))
#print(timeit.time.process_time())


######Erwartungswert mit zufällig gezählten Spinzuständen





def plotten(x):
	werte=[]
	for i in range(600):
		f=avgmagrandom(5,500)
		werte.append(f)
	plt.hist(werte)
	plt.title("Hits")
	plt.xlabel("Value")

	plt.show()





def metropolis(b,SpinConf):
	j=0
	z=0

	spinN = [eins(b) for x in range(SpinConf*b)]
	#gitter=spinzustand(b,8000)
	gitter=minuseins(b)
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
		for q in range(b):
			for w in range(b):

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
				Paccept=min(np.exp(DifH),1.)
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


		if j < r:

			return metropolisreturn(b,gitter,gitter2,j,r,spinN)


					#print(j,'no change')

def avgmagrandom(JT,b,spinN,N):
	sum=0
	summ=0
	for t in range(N):
		Z=spinN[t]
		#Z=Zufallsgitter(b)
		sum+=HamInExp(JT,Z,b)*magnetisierungZufall2(Z,b)
		summ+=HamInExp(JT,Z,b)
	return sum/summ


def AvgMagSimple(b,spinN,N):
	sum=0
	summ=0
	for t in range(N):
		Z=spinN[t]
		#Z=Zufallsgitter(b)
		sum+=magnetisierungZufall2(Z,b)
		summ+=1
	return sum/summ






#metropolis(4,5)#man bekommt die dreifache Anzahl an Spinzuständen..
print('Komplizierter Durchschnitt: ',avgmagrandom(0.00000002,33,metropolis(33,1000),1000))
print('Einfacher Durchschnitt: ',AvgMagSimple(33,metropolis(33,1000),1000))
print('Zeit: ',timeit.time.process_time())
#plt.hist(metropolis(3,10))
#plt.title("Hits")
#plt.xlabel("Value")

#plt.show()
