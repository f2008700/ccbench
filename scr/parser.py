import sys
from os import walk

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

def geoMed(lst):
    print len(lst)

def printLstStats(lst, sequence ):
    print "Seq: " , sequence
    print "Med: " , median(lst)
    """
    print "Min: ", min(lst)
    print "Max: ", max(lst)
    print "Avg: ", sum(lst)/len(lst)
    """
    print 

#mypath="/home/spai2/res/"
'''
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    print f
'''

def parse(f):
    for fs in f:
        #fil=open(mypath + fs, 'r')
        fil=open( fs, 'r')
        bw=[]

        print "File ", fs
        totThrd=fs.split('_')[0]
        threads = int( totThrd.split('/')[-1] )
        
        iterations = 100 * 1000 
        #threads = totThrd[1].split('.')[0].split(',')
        #print threads
        
        #c = range ( int(totThrd[0]) )
        #c = [None ] *  int(totThrd[0]) 
        #x = [ c for i in range(100 * 1000)]
        x = [ [ 0 ] * threads for _ in range( iterations ) ]

        flag = 0
        for thread in range(threads):
            for line in fil:
                stri = '[' + str(thread) + ':'
                if line.startswith(stri):
                    latency = int(line.split(':')[2].split(']')[0])
                    row = int(line.split(':')[1].split(']')[0])
                    col = int(line.split(':')[3].split(']')[0]) - 1
                    flag = 1         
                    x[row][col] = latency
                elif flag == 1:
                    flag = 0
                    break
            fil.close()
            fil = open ( fs, 'r' )
        '''                
        for i in range(11):
            for j in range(threads):
                print x[i][j], ' ',
            print 
        '''
        for i in range(threads):
            newx = [] 
            for j in range(len(x)):
                if ( x[j][i] == None ):
                    print j,i
                newx.append(x[j][i])
                #print x[i][j], ' ',
            printLstStats(newx, i)
         

def main():
    i = 0
    f = []
    for i in range ( 1,len ( sys.argv ) ):
        #print i,sys.argv[i]
        f.append( sys.argv[i] ) 
    parse(f)


if __name__ == '__main__':
    main()

