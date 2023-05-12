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
from kafe import ASCII, LaTeX, FitFunction
# additionally, import the model function we
# want to fit:
from kafe.function_library import linear_2par
import numpy as np

####################
# Helper functions #
####################

# -- define test configuration 


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



PVC=(1.147,2.096,3.226,4.198)
MES=(0.8398,1.679,2.524,3.365,4.206)
CU =(0.7958,1.589,2.384,3.179,3.976)
ALU=(0.5765,1.163,1.747,2.319,2.897)
FE =(0.6133,1.223,1.833,2.445,3.057)

xdataPVC=(2,4,6,8)
xdata=(2,4,6,8,10)


yer=0.00000001

def generate_datasets(output_file_path1, output_file_path2, output_file_path3, output_file_path4, output_file_path5):
    '''The following block generates the Datasets and writes a file for
    each of them.'''

    import numpy as np  # need some functions from numpy

    my_datasets = []


    my_datasets.append(kafe.Dataset(data=(xdataPVC, PVC)))
    my_datasets[-1].add_error_source('y', 'simple', yer)


    my_datasets.append(kafe.Dataset(data=(xdata, MES)))
    my_datasets[-1].add_error_source('y', 'simple', yer)
    
    my_datasets.append(kafe.Dataset(data=(xdata , CU )))
    my_datasets[-1].add_error_source('y', 'simple', yer)
    
    my_datasets.append(kafe.Dataset(data=(xdata, ALU)))
    my_datasets[-1].add_error_source('y', 'simple', yer)
    
    my_datasets.append(kafe.Dataset(data=(xdata , FE )))
    my_datasets[-1].add_error_source('y', 'simple', yer)

    my_datasets[0].write_formatted(output_file_path1)
    my_datasets[1].write_formatted(output_file_path2)
    my_datasets[2].write_formatted(output_file_path3)
    my_datasets[3].write_formatted(output_file_path4)
    my_datasets[4].write_formatted(output_file_path5)
    

############
# Workflow #
############

# Generate the Dataseta and store them in files
'''
generate_datasets('datasetPVCA3.dat',  
                  'datasetMESA3.dat',
                  'datasetCU_A3.dat',
                  'datasetALUA3.dat',
                  'datasetFE_A3.dat')
'''
# Initialize the Datasets
my_datasets = [kafe.Dataset(title="PVC"),
               kafe.Dataset(title="Messing"),
               kafe.Dataset(title="Kupfer"),
               kafe.Dataset(title="Aluminium"),
               kafe.Dataset(title="Eisen")]

# Load the Datasets from files
my_datasets[0].read_from_file(input_file='datasetPVCA3.dat')
my_datasets[1].read_from_file(input_file='datasetMESA3.dat')
my_datasets[2].read_from_file(input_file='datasetCU_A3.dat')
my_datasets[3].read_from_file(input_file='datasetALUA3.dat')
my_datasets[4].read_from_file(input_file='datasetFE_A3.dat')
# Create the Fits
my_fits = [kafe.Fit(dataset,
                    linear_2par,
                    fit_label="Linear regression " )
           for dataset in my_datasets]

# Do the Fits
for fit in my_fits:
    fit.do_fit()

# Create the plots
my_plot = kafe.Plot(my_fits[0],
                    my_fits[1],
                    my_fits[2],
                    my_fits[3],
                    my_fits[4])

mnPVC  = my_fits[0].get_parameter_values(rounding=False)
mnMES  = my_fits[1].get_parameter_values(rounding=False)
mnCU   = my_fits[2].get_parameter_values(rounding=False)
mnALU  = my_fits[3].get_parameter_values(rounding=True)
mnFE   = my_fits[4].get_parameter_values(rounding=False)

LPVC=1.456
LMES=1.459
LCU =1.447
LALU=1.461
LFE =1.461 
#Geschwindigkeit v berechnen
def v(m,L):
    return L/(m*0.001)

vPVC=np.around(v(mnPVC[0],LPVC), decimals=2)
vMES=np.around(v(mnMES[0],LMES), decimals=2)
vCU =np.around(v(mnCU [0],LCU ), decimals=2)
vALU=np.around(v(mnALU[0],LALU), decimals=2)
vFE =np.around(v(mnFE [0],LFE ), decimals=2)
pPVC=1.43
pMES=8.43
pCU =9.27
pALU=2.91
pFE =8.07


def E(v,p):
    return v**2*p*0.001

mnPVC=np.around(mnPVC[0], decimals=3)
mnMES=np.around(mnMES[0], decimals=3)
mnCU =np.around(mnCU [0], decimals=3)
mnALU=np.around(mnALU[0], decimals=4)
mnFE =np.around(mnFE [0], decimals=3)
print mnALU
# Fehler auf die E bzw auf die Dichte
mPVC=167
mMES=984
mCU =1032
mALU=327
mFE =926

dPVC=10.37*0.001
dMES=9.97*0.001
dCU =9.93*0.001
dALU=9.93*0.001
dFE =0.97*0.001

df= 0.00001
Lf=0.0005
def Ef(v,m,L,d):
    Vf=np.sqrt((0.25*np.pi*2.*d*L)**2*(df**2)+(0.25*(d**2)*np.pi)**2*(Lf)**2)
    V=0.24*np.pi*(d**2)*L
    Ef=(2.*(v**2)*(m*0.001)/(V**2))*Vf
    Ef=Ef/(10**6)
    return Ef


#cheat
#EfFE=EfFE/1000.

my_plot.axes.annotate(r'$ m_{PVC} = $' + str(mnPVC), xy=(3.1, 4.2), size=10, ha='right')
my_plot.axes.annotate(r'$ m_{Mes} = $' + str(mnMES), xy=(3.1, 4.0), size=10, ha='right')
my_plot.axes.annotate(r'$ m_{Cu} = $'  + str(mnCU ), xy=(3.1, 3.8), size=10, ha='right')
my_plot.axes.annotate(r'$ m_{Al} = $'  + str(0.289), xy=(3.1, 3.6), size=10, ha='right')
my_plot.axes.annotate(r'$ m_{Fe} = $'  + str(mnFE ), xy=(3.1, 3.4), size=10, ha='right')
'''
my_plot.axes.annotate(r'$\pm $' + str(mnfPVC), xy=(3.82, 4.229), size=10, ha='left')
my_plot.axes.annotate(r'$\pm $' + str(mnfMES), xy=(3.82, 4.029), size=10, ha='left')
my_plot.axes.annotate(r'$\pm $' + str(mnfCU ), xy=(3.82, 3.829), size=10, ha='left')
my_plot.axes.annotate(r'$\pm $' + str(mnfALU), xy=(3.82, 3.629), size=10, ha='left')
my_plot.axes.annotate(r'$\pm $' + str(mnfFE ), xy=(3.82, 3.429), size=10, ha='left')
#Verschoenern
my_plot.axis_labels = [r'$Anzahl  Durchl\"aufe$', '$t \ in \ ms$']
'''

# Draw the plots
my_plot.plot_all(show_info_for=None, show_data_for='all', show_function_for='all', show_band_for='meaningful')


###############
# Plot output #
###############

# Save the plots
my_plot.save('Aufgabe2_1ueb.pdf')




# Show the plots
#my_plot.show()
