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

def printLstStats(lst, thread):
    print "Thr: " , thread
    print "Med: " , median(lst)
    print "Min: ", min(lst)
    print "Max: ", max(lst)
    print "Avg: ", sum(lst)/len(lst)
    print 

mypath="results_/"

f = []
for (dirpath, dirnames, filenames) in walk(mypath):
    f.extend(filenames)
    print f

for fs in f:
    fil=open(mypath + fs, 'r')
    bw=[]

    print fs
    totThrd=fs.split('_')
    print totThrd[0]
    threads=totThrd[1].split('.')[0].split(',')
    print threads

    
    lst = []
    for thread in threads:
        for line in fil:
            if int(thread) < 10 and line.startswith('[  ' + str(thread) + ':'):
                num = int(line.split(':')[2].split(']')[0])
                lst.append( num )
                #print num,
        printLstStats(lst,thread)
