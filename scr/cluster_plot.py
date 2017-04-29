from __future__ import division
import re
import sys
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

SIZE = 14
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc('font', size=SIZE)                # controls default text sizes
plt.rc('axes', titlesize=SIZE)           # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SIZE)          # fontsize of the tick labels
plt.rc('ytick', labelsize=SIZE)          # fontsize of the tick labels
plt.rc('legend', fontsize=SIZE)          # legend fontsize
#plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

class rssvstime:

    def __init__(self, data1, fileName ):
       
        print fileName
        graphDir = "../analysis/"
        atomics = fileName.split('/')[-3]
        placement = fileName.split('/')[-2]
        testNum = fileName.split('/')[-1].split('.')[0]
        #print atomics, placement,testNum
        
        y1 = []
        y2 = []
        x1 = [] 
        threadsLst = []
        medianLst = []
        for s in data1.split('\n'):
            if s.startswith("Num Threads: "):
                threadsLst.append( int(s.split(' ')[2]) )
            if s.startswith("Medians: "):
                thread = threadsLst[ -1 ]
                tempLst = [] 
                tempLst.append( thread )
                for med in s.split(' ')[1:-1]:
                    tempLst.append ( float ( med ) )
                medianLst.append( tempLst )

        # Sort the list coz file doesn't have threads sorted
        medianLst = sorted ( medianLst )        
        
        # Y2 - max latency
        # Y1 - min latency
        # X1 - thread IDs 
        for median in medianLst:
            y1.append( min( median[1:] ) )
            #y2.append( math.log( max( median[1:] ), 2 ) ) 
            y2.append( max( median[1:] ) ) 
            x1.append( median[0] ) 
        
        x1 = sorted ( x1 )
        
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        ax1.set_xlabel(' Cores ')
        ax1.set_ylabel(' Latency ( unit ) ')
       
        # Define colors
        colOff = (254/255,232/255,200/255)
        colRed = (227/255,74/255,51/255)
        colWhite = ( 1, 1, 1 )
        colBlack = ( 0, 0, 0 )
       
        # Plot line
        ax1.plot(x1, y1, color= colBlack,  marker='o' )
        ax1.plot(x1, y2, color= colBlack, marker='x', ms = 10,  mew = 2 )
        ax1.grid(True)

        # Fill Color
        ax1.fill_between( x1, 0, y2, facecolor = colRed )
        ax1.fill_between( x1, 0, y1, facecolor = colWhite )
       
        # Set X,Y limits
        ax1.set_xlim( [0, 1.1 * x1[-1] ] )
        ax1.set_ylim( [0, 1.2 * max(y2) ] )
        
        patch1 = mpatches.Patch( color = colRed, label='Base Pages')
        plt.legend([ patch1 ], ["Latency variation" ], loc='upper left')
        #plt.show()
        plt.scatter( , marker='o', color='y', label='Threads')
        plt.savefig( graphDir + atomics + '/' + placement + '/' + testNum + '_place.png')

if __name__ == '__main__':
    fileName = sys.argv[1]
    with open(sys.argv[1], 'rb') as f1:
        data1 = f1.read()
        rssvstime( data1,fileName )
