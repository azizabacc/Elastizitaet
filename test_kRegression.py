#! /usr/bin/env python
''' test linear regression with kafe, 
    consider errors in x and y and correlated 
    absolute and relative uncertainties
..  author:: Guenter Quast <g.quast@kit.edu>
'''

import numpy as np, matplotlib.pyplot as plt
from PhyPraKit import generateXYdata, kRegression

# -- define test configuration 
xmin =  1.
xmax =  10.
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

xdata=np.arange(xmin, xmax+1. ,1.)
nd=len(xdata)
# generate pseudo data
xt, yt, ydata = generateXYdata(xdata, model,
        sigx_abs, 0., srely=sigy_rel, xrelcor=sxrelcor, yabscor=syabscor)
ey=sigy_rel* yt * np.ones(nd) # set array of relative y errors

# (numerical) linear regression
a, b, ea, eb, cor, chi2 = kRegression(
    xdata, ydata,
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


