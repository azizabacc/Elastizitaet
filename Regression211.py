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



PVC=(0.049, 0.1193, 0.2403)
MES=(0.005,0.013,0.027)
CU =(0.0035,0.0105,0.0225)
ALU=(0.008,0.02,0.041)
FE =(0.003,0.0071,0.015)


F=(0.2*9.81,0.5*9.81,1.*9.81)


L=0.429
Lf=0.0005
R=2.00
Rf=0.04
vf=0.0005
# von Auslenkung zu Winkel
def alpha(s):
    i=0
    al=np.zeros(3)
    while i<3:
        al[i]=s[i]/(2.0*L+4.0*(L+R))
        i=i+1
    return al

xdataPVC=F
xdataMES=F
xdataCU =F
xdataALU=F
xdataFE =F
ydataPVC=alpha(PVC)
ydataMES=alpha(MES)
ydataCU =alpha(CU )
ydataALU=alpha(ALU)
ydataFE =alpha(FE )

#Ausrechnen Fehler y
def y(v):
    i=0
    yer=np.zeros(3)
    while i<3:
        yer[i]=np.sqrt((1/(2.*L+4.*(L+R)))**2*(vf**2)+(6.*v[i]/(2.*L+4.*(L+R))**2)**2*(Lf**2)+(4.*v[i]/(2.*L+4.*(L+R))**2)**2*(Rf**2))
        i=i+1
    return yer
yerPVC=y(PVC)
yerMES=y(MES)
yerCU =y(CU )
yerALU=y(ALU)
yerFE =y(FE )



def generate_datasets(output_file_path1, output_file_path2, output_file_path3, output_file_path4, output_file_path5):
    '''The following block generates the Datasets and writes a file for
    each of them.'''

    import numpy as np  # need some functions from numpy

    my_datasets = []


    my_datasets.append(kafe.Dataset(data=(xdataPVC, ydataPVC)))
    my_datasets[-1].add_error_source('y', 'simple', yerPVC)


    my_datasets.append(kafe.Dataset(data=(xdataMES, ydataMES)))
    my_datasets[-1].add_error_source('y', 'simple', yerMES)
    
    my_datasets.append(kafe.Dataset(data=(xdataCU , ydataCU )))
    my_datasets[-1].add_error_source('y', 'simple', yerCU )
    
    my_datasets.append(kafe.Dataset(data=(xdataALU, ydataALU)))
    my_datasets[-1].add_error_source('y', 'simple', yerALU)
    
    my_datasets.append(kafe.Dataset(data=(xdataFE , ydataFE )))
    my_datasets[-1].add_error_source('y', 'simple', yerFE )

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
generate_datasets('211PVC.dat',  
                  '211MES.dat',
                  '211CU_.dat',
                  '211ALU.dat',
                  '211FE_.dat')
'''
# Initialize the Datasets
my_datasets = [kafe.Dataset(title="PVC"),
               kafe.Dataset(title="Messing"),
               kafe.Dataset(title="Kupfer"),
               kafe.Dataset(title="Aluminium"),
               kafe.Dataset(title="Eisen")]

# Load the Datasets from files
my_datasets[0].read_from_file(input_file='211PVC.dat')
my_datasets[1].read_from_file(input_file='211MES.dat')
my_datasets[2].read_from_file(input_file='211CU_.dat')
my_datasets[3].read_from_file(input_file='211ALU.dat')
my_datasets[4].read_from_file(input_file='211FE_.dat')
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

# daten auslesen
mnPVC  = my_fits[0].get_parameter_values(rounding=False)
mnfPVC = my_fits[0].get_parameter_errors(rounding=False)
mnMES  = my_fits[1].get_parameter_values(rounding=False)
mnfMES = my_fits[1].get_parameter_errors(rounding=False)
mnCU   = my_fits[2].get_parameter_values(rounding=False)
mnfCU  = my_fits[2].get_parameter_errors(rounding=False)
mnALU  = my_fits[3].get_parameter_values(rounding=True)
mnfALU = my_fits[3].get_parameter_errors(rounding=False)
mnFE   = my_fits[4].get_parameter_values(rounding=False)
mnfFE = my_fits[4].get_parameter_errors(rounding=False)

#E Modul bestimmen
L=0.429
Lf=0.0005
b=25.0
bf=0.000025
d=0.0060
df=0.000025


def E(m):
    E=3.*(L**2)*0.001/(4.*b*(d**3)*m)
    return E   

mnPVC=np.around(mnPVC[0], decimals=8)
mnMES=np.around(mnMES[0], decimals=8)
mnCU =np.around(mnCU [0], decimals=8)
mnALU=np.around(mnALU[0], decimals=8)
mnFE =np.around(mnFE [0], decimals=8)

# Fehler auf E berechnen
def Ef(m,mf):
    Ef=np.sqrt((3.*L/(2.*b*(d**3)*m))**2*(Lf**2)
               +(3.*L**2/(4.*(m**2)*(d**3)*b))**2*(mf**2)
               +(3.*L**2/(4.*m*(d**3)*(b**2)))**2*(bf**2)
               +(9.*L**2/(4*b*(d**4)*m))**2*(df**2))
    return Ef*0.001

mnfPVC=np.around(mnfPVC[0],decimals=6)    
mnfMES=np.around(mnfMES[0],decimals=7)   
mnfCU =np.around(mnfCU [0],decimals=7)   
mnfALU=np.around(mnfALU[0],decimals=6)   
mnfFE =np.around(mnfFE [0],decimals=7)  


my_plot.axes.annotate(r'$ m_{PVC} = $' + str(2.3e-03), xy=(3.48, 0.023), size=10, ha='right')
my_plot.axes.annotate(r'$ m_{Mes} = $' + str(2.7e-04), xy=(3.6, 0.022), size=10, ha='right')
my_plot.axes.annotate(r'$ m_{Cu} = $'  + str(2.3e-04), xy=(3.6, 0.021), size=10, ha='right')
my_plot.axes.annotate(r'$ m_{Al} = $'  + str(4.0e-04), xy=(3.48, 0.020), size=10, ha='right')
my_plot.axes.annotate(r'$ m_{Fe} = $'  + str(1.5e-04), xy=(3.6, 0.019), size=10, ha='right')


my_plot.axes.annotate(r'$\pm $' + str(mnfPVC), xy=(3.62, 0.02319), size=10, ha='left')
my_plot.axes.annotate(r'$\pm $' + str(mnfMES), xy=(3.62, 0.02219), size=10, ha='left')
my_plot.axes.annotate(r'$\pm $' + str(mnfCU ), xy=(3.62, 0.02119), size=10, ha='left')
my_plot.axes.annotate(r'$\pm $' + str(mnfALU), xy=(3.62, 0.02019), size=10, ha='left')
my_plot.axes.annotate(r'$\pm $' + str(mnfFE ), xy=(3.62, 0.01919), size=10, ha='left')
# Verschoenern
my_plot.axis_labels = ['$F \ in \ N$', r'$ Biegewinkel    \alpha      $']


# Draw the plots
my_plot.plot_all(show_info_for=None, show_data_for='all', show_function_for='all', show_band_for='meaningful')


###############
# Plot output #
###############

# Save the plots
my_plot.save('Aufgabe1_2ueb.pdf')

# Show the plots
#my_plot.show()
