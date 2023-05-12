'''
A Tale of Two Fits
------------------

    This simple example demonstrates the fitting of a linear function to
    two Datasets and plots both Fits into the same Plot.
'''

###########
# Imports #
###########

# import everything we need from kafe
import kafe

# additionally, import the model function we
# want to fit:
from kafe.function_library import linear_2par
import numpy as np

####################
# Helper functions #
####################


# def Mittelwert
N=6 #da sechs werte pro Messung
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

m=0.837
L=0.80 
Lf=0.0005

dStab=0.00395 
dStabf=0.000001

dGewicht=0.07 
dGewichtf=0.000025

aDrehachse=0.110


#Periodendauer
Gnull=(0.563, 0.567, 0.567, 0.561, 0.556, 0.569)
Gzwei=(1.109, 1.109, 1.110, 1.090, 1.085, 1.112)
Gvier=(1.457, 1.459, 1.464, 1.443, 1.437, 1.437)

i=0

meanGnull=mean(Gnull)
meanGzwei=mean(Gzwei)
meanGvier=mean(Gvier)

sigmamGnull=sigmamean(Gnull)
sigmamGzwei=sigmamean(Gzwei)
sigmamGvier=sigmamean(Gvier)

#Berechne Fehler auf G
L=0.80
Lf=0.0005
R=0.07
Rf=0.000025
I=2.*0.106
dT=(meanGvier-meanGzwei)
Gf=np.sqrt((8.*np.pi*L*I/((R**4)*(dT**2)))**2*(Lf**2)
           +(32.*np.pi*L*I/((R**5)*(dT**2)))**2*(Rf**2)
           +(16.*np.pi*L*I/((R**4)*(dT**3)))**2*(sigmamGzwei**2)
           +(16.*np.pi*L*I/((R**4)*(dT**3)))**2*(sigmamGvier**2)) 
Gf=Gf/(10**9)
print Gf

#Ausgabe
print  'Mittel G0  ', meanGnull
print  'Mittel G2  ', meanGzwei
print  'Mittel G4  ', meanGvier

print  'Fehler G0  ', sigmamGnull
print  'Fehler G2  ', sigmamGzwei
print  'Fehler G4  ', sigmamGvier





