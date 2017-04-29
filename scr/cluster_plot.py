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
        
        # Y1 - min latency
        # X1 - thread IDs 
        for median in medianLst:
            for elt in median[1:]:
                y1.append(elt)
            for cnt in range(median[0]):
                x1.append( median[0])
        
        fig1 = plt.figure()
        plt.xticks(list(set(x1)), fontsize=12)
        plt.ylim( [-0.1 * max(y1), 1.1 * max(y1)]  )
        plt.xlabel('No. of threads', fontsize=12)
        plt.ylabel('Latency (cycles)', fontsize=12)
        plt.title(atomics.upper() + ' on Shared', fontsize = 14)
        plt.scatter( x1, y1, marker='x', color='b', label='Threads')
        plt.grid()
        plt.show()
        plt.savefig( graphDir + atomics + '/' + placement + '/' + testNum + '_place.png')

if __name__ == '__main__':
    fileName = sys.argv[1]
    with open(sys.argv[1], 'rb') as f1:
        data1 = f1.read()
        rssvstime( data1,fileName )
