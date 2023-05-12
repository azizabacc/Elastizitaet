#! /usr/bin/env python
''' test linear regression with kafe, 
    consider errors in x and y and correlated 
    absolute and relative uncertainties
..  author:: Guenter Quast <g.quast@kit.edu>
'''

import numpy as np, matplotlib.pyplot as plt


# -- define test configuration 
# Masse der Gewichte
m1=0.1
m2=0.2
m3=0.5
m4=1

# Kraft abhaengigkeit mit Messuhr
def F(m,s):
    return (m-3.6*s)*9.81

# def Mittelwert
N=3 #da drei werte pro Messung
def mean(a):
  return np.sum(a)/N

def variance(a):
    v=np.sum((a-mean(a))**2)/(N-1)
    return v

def sigma(a):
    s= np.sqrt(variance(a))
    return s

def sigmamean(a):
    return sigma(a)/np.sqrt(N)
'''
PVC=[(0.32, 0.35, 0.34),(0.8,0.7,0.7),(1.82, 1.83, 1.82),(3.71,3.63,3.59)]
#PVC02=(0.8,0.7,0.7)
#PVC05=(1.82, 1.83, 1.82) 
#PVC1 =(3.71,3.63,3.59)
i=0
while i<5:
    print mean(PVC[i])
    i=i+1
'''
PVC=[(0.32, 0.35, 0.34),(0.8,0.7,0.7),(1.82, 1.83, 1.82),(3.71,3.63,3.59)]
MES=[(0.03,0.03,0.03),(0.07,0.07,0.06),(0.17,0.17,0.16),(0.41,0.39,0.39)]
CU =[(0.02,0.01,0.02),(0.05,0.05,0.06),(0.16,0.16,0.15),(0.33,0.33,0.32)]
ALU=[(0.07,0.07,0.06),(0.13,0.13,0.14),(0.32,0.32,0.33),(0.63,0.63,0.63)]
FE =[(0.015,0.0125,0.012),(0.04,0.04,0.04),(0.10,0.10,0.10),(0.22,0.21,0.21)]

i=0

meanPVC=np.zeros(4)
meanMES=np.zeros(4)
meanCU =np.zeros(4)
meanALU=np.zeros(4)
meanFE =np.zeros(4)
sigmamPVC=np.zeros(4)
sigmamMES=np.zeros(4)
sigmamCU =np.zeros(4)
sigmamALU=np.zeros(4)
sigmamFE =np.zeros(4)
while i<4:
    meanPVC[i]=mean(PVC[i])
    meanMES[i]=mean(MES[i])
    meanCU [i]=mean(CU [i])
    meanALU[i]=mean(ALU[i])
    meanFE [i]=mean(FE [i])
    sigmamPVC[i]=sigmamean(PVC[i])
    sigmamMES[i]=sigmamean(MES[i])
    sigmamCU [i]=sigmamean(CU[i])
    sigmamALU[i]=sigmamean(ALU[i])
    sigmamFE [i]=sigmamean(FE[i])
    i=i+1

m=(0.1,0.2,0.5,1)
# Kraft abhaengigkeit mit Messuhr   /1000 wegen g zu kg
def F(masse,s):
    return (m-3.6*s/1000)*9.81


xdataPVC=F(m,meanPVC)
xdataMES=F(m,meanMES)
xdataCU =F(m,meanCU )
xdataALU=F(m,meanALU)
xdataFE =F(m,meanFE )

ydataPVC=meanPVC
ydataMES=meanMES
ydataCU =meanCU 
ydataALU=meanALU
ydataFE =meanFE

def generate_dataset(output_file_path,xdata,ydata,sigmax,sigmay):
    import kafe
    my_dataset = kafe.Dataset(data=(xdata, ydata))
    my_dataset.add_error_source('x', 'simple', sigmax)
    my_dataset.add_error_source('y', 'simple', sigmay)
    
    my_dataset.write_formatted(output_file_path)


#generate_dataset('datasetPVC.dat',xdataPVC,ydataPVC,sigmamPVC/10.,sigmamPVC)
generate_dataset('datasetMES2.dat',xdataMES,ydataMES,sigmamMES/10.,sigmamMES)
#generate_dataset('datasetCU_.dat',xdataCU ,ydataCU ,sigmamCU /10.,sigmamCU )
#generate_dataset('datasetALU.dat',xdataALU,ydataALU,sigmamALU/10.,sigmamALU)
#generate_dataset('datasetFE_.dat',xdataFE ,ydataFE ,sigmamFE /10.,sigmamFE )