#! /usr/bin/env python
''' test linear regression with kafe, 
    consider errors in x and y and correlated 
    absolute and relative uncertainties
..  author:: Guenter Quast <g.quast@kit.edu>
'''

import numpy as np, matplotlib.pyplot as plt
from PhyPraKit import generateXYdata, kRegression

# -- define test configuration 
# Masse der Gewichte
m1=0.1
m2=0.2
m3=0.5
m4=1
m=(0.1,0.2,0.5,1)


# def Mittelwert
N=3 #da drei werte pro Messung
def mean(a):
  return np.sum(a)/N

def variance(a):
    v=np.sum((a-mean(a))**2)/N-1
    return v

def sigma(a):
    s= np.sqrt(variance(a))
    return s

def sigmamean(a):
    return sigma(a)/np.sqrt(N)



'''
# generate pseudo data
xt, yt, ydata = generateXYdata(xdata, model,
        sigx_abs, 0., srely=sigy_rel, xrelcor=sxrelcor, yabscor=syabscor)
ey=sigy_rel* yt * np.ones(nd) # set array of relative y errors
'''
# Messdaten

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

xmin =  m[0]*9.81
xmax =  m[3]*9.81
#  the model y(x) 
a_true = 0.3
b_true = 1.0
def model(x):
   return a_true*x + b_true

# set some uncertainties
sigx_abs = 0.2 # absolute error on x 
sigy_rel = 0.1 # relative error on y
#       errors of this kind only supported by kafe
sxrelcor=0.05 #  a relative, correlated error on x 
syabscor=0.1  #  an absolute, correlated error on y


# x Werte ausrechnen
# Kraft abhaengigkeit mit Messuhr /1000 wegen g zu kg
def F(masse,s):
    return (m-3.6*s/1000)*9.81
 
xdataPVC=F(m,meanPVC)
'''print xdataMES=F(m,meanMES)
print xdataCU =F(m,meanCU )
print xdataALU=F(m,meanALU)
print xdataFE =F(m,meanFE )

#y Werte

print ydataPVC=meanPVC
print ydataMES=meanMES
print ydataCU =meanCU 
print ydataALU=meanALU
print ydataFE =meanFE

nd=len(xdataPVC)



# (numerical) linear regression
a, b, ea, eb, cor, chi2 = kRegression(
    xdataPVC, ydataPVC,
    sigx_abs, ey, xrelcor=sxrelcor, yabscor=syabscor,
    plot=True)

print '*==* first data set'
print '  x = ', xdata
print '  sx = ', sigx_abs
print '  y = ', xdata
print '  sy = ', ey
print 'fit result:'
print '  a=%.2f+-%.2f, b=%.2f+-%.2f, corr=%.2f, chi2/df=%.2f\n'\
      % (a, ea, b, eb, cor, chi2/(nd-2.))


