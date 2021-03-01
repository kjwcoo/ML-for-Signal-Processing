import pandas as pd
import numpy as np
from glob import glob

files = glob( 'LabeledData/*.csv' )

saveData = []
saveTarget = []

for idx, file in enumerate( files ):
    df = pd.read_csv( file, dtype=np.float32, index_col=None )
    data = df.to_dict( 'list' )

    dataNow = data[ 'Voltage' ][ 1: ]
    dataLag = data[ 'Voltage' ][ :-1 ]

    prepData = {}
    prepData[ 'Time' ] = [ x - data[ 'Time' ][ 0 ] for x in data[ 'Time' ][ 1: ] ]
    prepData[ 'Voltage' ] = [ x1 - x2 for ( x1, x2 ) in zip( dataNow, dataLag) ]
    prepData[ 'Readout' ] = data[ 'Readout' ]

    # Save in npz file
    saveData.append( prepData[ 'Voltage' ] )
    saveTarget.append( [ prepData[ 'Readout' ][ 0 ] ] )
    
    # Save in csv file
    name = "PreparedData\data_" + str( idx ) + ".csv"
    pd.DataFrame( zip( prepData[ 'Time' ], prepData[ 'Voltage' ], prepData[ 'Readout' ] ), columns=[ 'Time', 'Voltage', 'Readout' ] ).to_csv( name, index=False )

data = np.stack( saveData, axis=0 )
target = np.stack( saveTarget, axis=0 )
np.savez( "ProcessedDataset.npz", data=saveData, label=saveTarget )
    
