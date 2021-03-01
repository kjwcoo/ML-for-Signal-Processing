import pandas as pd
import numpy as np
from glob import glob
import matplotlib.pyplot as plt

"""
Fetch data
"""
files = glob( 'Data\*.txt' )

for idx, file in enumerate( files ):
    if idx == 0:
        df = pd.read_csv( file, dtype=np.float32, skiprows=6, header=None, index_col=None, names=[ 'Time', 'Voltage', 'Trigger' ] )
    else:
        df.append( pd.read_csv( file, dtype=np.float32, skiprows=6, header=None, index_col=None ) )

"""
Parse data
"""
# First column: Time, Second column: Voltage, Thrid column: Trigger voltage
data = df.to_dict( 'list' )
maxData = np.max( data[ 'Trigger' ] )
minData = np.min( data[ 'Trigger' ] )
print( "Max: ", maxData, "Min: ", minData )

parsedData = []
newData = {}
trigMode = False
prevTrig = 0
minLen = 0
for idx, ( time, voltage, trigger ) in enumerate( zip( data[ 'Time' ], data[ 'Voltage' ], data[ 'Trigger' ] ) ):
    if trigger == maxData and trigMode is False:
        start = idx
        trigMode = True
    elif prevTrig == minData and trigger != minData and trigMode is True:
        end = idx
        trigMode = False
        if minLen == 0 or end - start < minLen:
            minLen = end - start
        newData[ 'Time' ] = [ x - data[ 'Time' ][ start ] for x in data[ 'Time' ][ start:end ] ] # Reset initial time to 0
        newData[ 'Voltage' ] = data[ 'Voltage' ][ start:end ]
        newData[ 'Trigger' ] = data[ 'Trigger' ][ start:end ]
        parsedData.append( newData )
        newData = {}
        
    prevTrig = trigger

"""
Check if correctly parsed
"""
for plotData in parsedData:
    plt.plot( plotData[ 'Time' ], plotData[ 'Voltage' ] )
plt.show()

"""
Write parsed data in the ParsedData foler
"""
for idx, writeData in enumerate( parsedData ):
    name = "ParsedData\data_" + str( idx ) + ".csv"
    pd.DataFrame( zip( writeData[ 'Time' ][ : minLen ], writeData[ 'Voltage' ][ : minLen ] ), columns=[ 'Time', 'Voltage' ] ).to_csv( name, index=False )
