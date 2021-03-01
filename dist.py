import pandas as pd
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
import scipy.stats as stat

"""
Fetch data
"""
files = glob( 'ParsedData/*.csv' )

for idx, file in enumerate( files ):
    datum = pd.read_csv( file, dtype=np.float32, header=None, index_col=None )
    datum = np.array( datum, dtype=np.float32 )
    
    # Majority voting to calculate sampling rate
    ts_1 = datum[ 1, 0 ] - datum[ 0, 0 ]
    ts_2 = datum[ 2, 0 ] - datum[ 1, 0 ]
    ts_3 = datum[ 3, 0 ] - datum[ 2, 0 ]
    if ts_1 == ts_2:
        ts = ts_1
    elif ts_1 == ts_3:
        ts = ts_1
    else:
        ts = ts_2

    # Data
    data = datum[ :, 1 ]
    dataSize = data.size
    hDataSize = np.floor( dataSize / 2.0 ).astype( np.int32 )

    # Box-Cox Transform
    if idx == 0:
        dataTrans, lbda = stat.boxcox( data )  # lambda fitting
    else:
        dataTrans = stat.boxcox( data, lbda )
    transSize = dataTrans.size
    hTransSize = np.floor( transSize / 2.0 ).astype( np.int32 )
    
    # Trend differencing
    dataNow = dataTrans[ 1: ]
    dataLag = dataTrans[ :-1 ]
    dataDiff = dataNow - dataLag
    diffSize = dataDiff.size
    hDiffSize = np.floor( diffSize / 2.0 ).astype( np.int32 )


    # Plot
    print( 1 / ts / 10 ** 6, " MHz "  )
    plt.clf()
    plt.figure( 1 )
    charName = 'CharData/name_' + str( idx ) + '.png' 
    freqData = np.fft.fftfreq( n=dataSize, d=ts )
    distData = np.fft.fft( data ) / dataSize
    plt.subplot( 121 )
    plt.plot( ts * np.arange( dataSize ), data )
    plt.subplot( 122 )
    plt.plot( freqData[ : hDataSize ], abs( distData[ : hDataSize ] ) )
    plt.tight_layout()
    plt.savefig( charName )

    plt.clf()
    plt.figure( 2 )
    diffName = 'DiffData/name_' + str( idx ) + '.png' 
    freqDiff = np.fft.fftfreq( n=diffSize, d=ts )
    distDiff = np.fft.fft( dataDiff ) / diffSize
    plt.subplot( 121 )
    plt.plot( ts * np.arange( diffSize ), dataDiff )
    plt.subplot( 122 )
    plt.plot( freqDiff[ : hDiffSize ], abs( distDiff[ : hDiffSize ] ) )
    plt.savefig( diffName )

    plt.clf()
    plt.figure( 3 )
    transName = 'TransData/name_' + str( idx ) + '.png' 
    freqTrans = np.fft.fftfreq( n=transSize, d=ts )
    distTrans = np.fft.fft( dataTrans ) / transSize
    plt.subplot( 121 )
    plt.plot( ts * np.arange( transSize ), dataTrans )
    plt.subplot( 122 )
    plt.plot( freqTrans[ : hTransSize ], abs( distTrans[ : hTransSize ] ) )
    plt.savefig( transName )
