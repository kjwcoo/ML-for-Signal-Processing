import pandas as pd
import numpy as np
from glob import glob
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Functions for curve fitting
def normal( x, mu, sigma, A ):
    return A * np.exp( -( x - mu ) ** 2 / ( 2 * sigma ** 2 ) )

def bimodal( x, mu1, sigma1, A1, mu2, sigma2, A2 ):
    return normal( x, mu1, sigma1, A1 ) + normal( x, mu2, sigma2, A2 )

# Extracting minimum voltage values
files = glob( 'ParsedData/*.csv' )
minVoltage = np.zeros( len( files ) )

for idx, file in enumerate( files ):
    df = pd.read_csv( file, dtype=np.float32, index_col=None )
    data = df.to_dict( 'list' )

    minVoltage[ idx ] = min( data[ 'Voltage' ] )

# Curve fitting
y, x, _ = plt.hist( minVoltage, 150 )
x = ( x[ 1: ] + x[ :-1 ] ) / 2  # Use central value
params, cov = curve_fit( bimodal, x, y )
plt.plot( x, bimodal( x, *params ), color='red' )
plt.show()

# Calculate threshold
thres = ( params[ 0 ] + params[ 3 ] ) / 2

# Labeling
"""
voltage > thres: singlet( 0 )
voltage < thres: triplet( 1 )
"""

for idx, file in enumerate( files ):
    df = pd.read_csv( file, dtype=np.float32, index_col=None )
    data = df.to_dict( 'list' )

    if all( x > thres for x in data[ 'Voltage' ] ):
        data[ 'Readout' ] = np.zeros( len( data[ 'Voltage' ] ) )
    else:
        data[ 'Readout' ] = np.ones( len( data[ 'Voltage' ] ) )

    plt.plot( data[ 'Voltage' ] )
    plt.show()
    print( data[ 'Readout' ][ 0 ] )]
    name = "LabeledData\data_" + str( idx ) + ".csv"
    pd.DataFrame( zip( data[ 'Time' ], data[ 'Voltage' ], data[ 'Readout' ] ), columns=[ 'Time', 'Voltage', 'Readout' ] ).to_csv( name, index=False )
