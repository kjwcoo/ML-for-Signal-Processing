import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import os, sys, argparse
from glob import glob

def respond( event ):
    global eventVal
    if event.key in [ '0', '1', '2' ]:
        eventVal = int( event.key )
        plt.close( event.canvas.figure )
        
eventVal = 0

parser = argparse.ArgumentParser( description='Visually label voltage plots' )
parser.add_argument( '--dst', required=True, help='Output directory' )
parser.add_argument( '--src', required=True, nargs='+', help='Input directories' ) 

args = parser.parse_args()
outDir = args.dst
try:
    os.mkdir( outDir )
except OSError:
    print( "You are using an existing directory! PROHIBITED ACTION" )
    sys.exit()
        
for i in range( len( args.src ) ):
    title = str( args.src[ i ] ) + "\*.csv"
    files = glob( title )

    for idx, file in enumerate( files ):
        df = pd.read_csv( file, dtype=np.float32, index_col=None )
        data = df.to_dict( 'list' )
        plt.cla()
        plt.gcf().canvas.mpl_connect( 'key_press_event', respond )
        plt.plot( data[ 'Time' ], data[ 'Voltage' ] )
        plt.show()

        label = pd.DataFrame( { 'Label' : [ eventVal ] } )
        new = pd.concat( [ df, label ], axis=1 )
        name = outDir + "/" + os.path.basename( file )
        new.to_csv( name, index=False )
    
        
        
    

