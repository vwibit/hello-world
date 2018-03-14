import numpy as np
import sys
import math

########### loads cluster #####
a=np.loadtxt(open(sys.argv[1], "rb"), delimiter=",", skiprows=1)

######## maps the distance to the origin #######
distancemap=[[int(((n - len(a)//2)**2 + (m - len(a)//2)**2)**0.5) for n in range(len(a)+1)] for m in range(len(a)+1)]

########## correlation for one point in the cluster ##########
def correlation(ort,gitter,N,T):
	gitter_x=0
	gitter_y=0
	zaehler=0
	while gitter_x < N:
		while gitter_y < N:

			zaehler += gitter[gitter_x][gitter_y]*gitter[(gitter_x + int(ort[0]-N//2))%(N-1)][(gitter_y + int(ort[1]-N//2))%(N-1)]
			gitter_y+=1
		gitter_x+=1
		gitter_y=0
	return(zaehler/(N*N*T))


def average_correlation(radius,gitter,N,T):
	av_gitter_x =0
	av_gitter_y=0
	counter_1=0.0
	counter_2=0.0
	while av_gitter_x < N:
		while av_gitter_y < N:
			if distancemap[av_gitter_x][av_gitter_y] == radius:
				counter_1 += correlation([av_gitter_x,av_gitter_y],gitter,N,T)
				counter_2 = counter_2 + 1
			av_gitter_y+=1
		av_gitter_x+=1
		av_gitter_y=0
	return(counter_1/counter_2)

#################prints into file ln r to ln C(r)#####
list=[]
for i in range(30):
	print(i)
	list.append(str(math.log(i+1))+str(" ")+str(math.log(average_correlation(i+1,a,len(a),int(sys.argv[2])))))


file=open('correlation_'+ sys.argv[1] + '.txt','w')
for item in list:
    file.write("%s\n" % item)
file.close()
