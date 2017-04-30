import sys
import os

def median(lst):
    lst = sorted(lst)
    if len(lst) < 1:
            return None
    if len(lst) %2 == 1:
            return lst[((len(lst)+1)/2)-1]
    else:
            return float(sum(lst[(len(lst)/2)-1:(len(lst)/2)+1]))/2.0

'''
def printLstStats(lst, sequence, outf):
    #outf.write('Turn: ' + str(sequence) + ' ')
    for i in lst:
        outf.write(str(i) + ' ')
    print "Seq: " , sequence
    print "Med: " , median(lst)
    print "Min: ", min(lst)
    print "Max: ", max(lst)
    print "Avg: ", sum(lst)/len(lst)
    print 

for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    print f
'''

def parse(f):
    for fs in f:
        #fil=open(mypath + fs, 'r')
        fil=open( fs, 'r')
        bw=[]

        valid_path = fs.split('/')[4]
        if valid_path != "results":
            sys.exit("Need to provide absolute path: /home/spai2/ccbench/results/")
        
        atomic = fs.split('/')[5]
        socketConfig = fs.split('/')[6]

        print "File ", fs
        totThrd=fs.split('_')[0]
        threads = int( totThrd.split('/')[-1] )
        test = totThrd.split('/')[-2]
        placement = fs.split('_')[1]
        placement = placement.split('.')[0]

        outfile = os.path.join(analysisDir, atomic, socketConfig, test + '.txt')

        outf = open(outfile, 'a+')
        outf.write('Num Threads: '+ str(threads) + '\n')
        places = ', '.join(placement.split(','))
        outf.write('Thread Placement: '+ places + '\n')
        outf.write('Medians: ')

        iterations = 100 * 1000 
        
        # Hols the result Matrix
        x = [ [ None ] * threads for _ in range( iterations ) ]
        rawX = [ [ None ] * threads for _ in range( iterations ) ]
        rawSpins = [ [ None ] * threads for _ in range( iterations ) ]
        flag = 0
        for thread in range(threads):
            for line in fil:
                spin = None
                stri = '[' + str(thread) + ':'
                if line.startswith(stri):
                    latency = int(line.split(':')[2].split(']')[0])
                    row = int(line.split(':')[1].split(']')[0])
                    col = int(line.split(':')[3].split(']')[0]) - 1
                    spin = int(line.split('{')[1].split('}')[0])

                    flag = 1         
                    x[row][col] = latency
                    rawX[row][thread] = latency
                    rawSpins[row][thread] = spin
                elif flag == 1:
                    flag = 0
                    break
            fil.close()
            fil = open ( fs, 'r' )
        """
        for i in range(iterations):
            for j in range(threads):
                #print x[i][j], ' ',
                if x[i][j] != None:
                    print 'i: ', i, 'j: ', j
            print 
        return
        """
        medianLst = []
        for i in range(threads):
            newx = [] 
            for j in range(len(x)):
                if ( x[j][i] == None ):
                    print j,i
                newx.append(x[j][i])
                #print x[i][j], ' ',
            if i == 0:
                '''
                for xii in newx:
                    print xii
                '''
            medianLst.append ( median( newx ) )
            #printLstStats(newx, i, outf)

        eucledianLst = []
        for i in range( len( rawX )):
            sumi = 0
            for j in range( len( rawX[i] )):
                sumi += ( rawX[i][j] - medianLst[j] ) ** 2
                if i == 0 and j == 0:
                    print medianLst[j], sumi, rawX[i][j]
            eucledianLst.append( sumi )  

        idx = eucledianLst.index( min( eucledianLst ) )
        print "Index: ", idx 
        repMedians = rawX[ idx ]
        #printLstStats(rawX)
        for i in repMedians:
            outf.write(str(i) + ' ')
        outf.write('\n' + 'Spin counts: ')
        repSpins = rawSpins[ idx ]
        #printLstStats(rawX)
        for i in repSpins:
            outf.write(str(i) + ' ')
        outf.write('\n' + 'Iter Num: '+ str(idx))

        outf.write('\n\n')
        outf.close()
         

analysisDir = "/home/spai2/ccbench/analysis"

def main():
    i = 0
    f = []
    for i in range ( 1,len ( sys.argv ) ):
        #print i,sys.argv[i]
        f.append( sys.argv[i] ) 
    parse(f)


if __name__ == '__main__':
    main()

