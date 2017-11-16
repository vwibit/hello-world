import numpy as np
import random
import timeit
import matplotlib.pyplot as plt

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



def summeallerspins(b):
	summe=0
	gitter=eins(b)
	for f in range(b):
		for g in range(b):
			gitter[f][g]=-1
			#print(gitter)
			summe+=np.exp(-0.5*Hamiltonian(gitter,b))
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

def HamInExp(Z,b):
	P=np.exp(-0.5*Hamiltonian(Z,b))
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
def avgmagrandom(b,N):
	sum=0
	summ=0
	#Random in auswahl des spinzustandes
	#N zufällige Spinzustände

	for t in range(N):

		Z=Zufallsgitter(b)
		sum+=HamInExp(Z,b)*magnetisierungZufall(Z,b)
		#print(sum)
		summ+=HamInExp(Z,b)

	return sum/summ

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
	spinvektor = [[eins(b) for x in range(2)] for y in range(SpinConf)]
	spinvektor[0][0]=Zufallsgitter(b)


	for x in range(b):
		for y in range(b):
			spinvektor[0][1][x][y]=spinvektor[0][0][x][y]


	spinvektor[0][1][0][0]=-spinvektor[0][0][0][0]

	H1=Hamiltonian(spinvektor[0][0],b)
	H2=Hamiltonian(spinvektor[0][1],b)
	DifH=H2-H1
#	print(spinvektor)
	print(H1,H2,DifH,spinvektor[0][0],spinvektor[0][1])

	for x in range(b*b*b*b):
		for y in range(b):
			if j == SpinConf:
				break
			x= x%b
			y= y%b

			Paccept=min(np.exp(-DifH),1.)
			#print(x,y,Paccept,j)
			H1=Hamiltonian(spinvektor[j][0],b)
			i = random.randint(0, 100)/100.
			print(i,Paccept,spinvektor[j][0],spinvektor[j][1])
			if i < Paccept:
				for x in range(b):
					for y in range(b):
						spinvektor[j][1][x][y]=spinvektor[j][0][x][y]

				spinvektor[j][1][x][y]=-spinvektor[j][0][x][y]
				H2=Hamiltonian(spinvektor[j][1],b)
				DifH=H2-H1
				j+=1
				print(j)
	#print(spinvektor)
	return spinvektor



metropolis(3,3)
#print(metropolis(3,15))
#plt.hist(metropolis(3,10))
#plt.title("Hits")
#plt.xlabel("Value")

#plt.show()
