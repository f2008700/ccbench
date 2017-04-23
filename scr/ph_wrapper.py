import subprocess as sp
import time

atomics={"cas":{}, "tas":{}, "fai":{}, "swap":{}}
#socHT={"1sNoHT":[],"1sHT":[],"2sNoHT":[],"2sHT":[]}
socHT={"1sNoHT":[]}
threads=[ { 1:{},2:{},4:{} } ]
states={"cas":[16,41,20,12,46], 
        "tas":[18,43,22,14,47],
        "fai":[17,42,21,13,48] } 

def thr_populate():
    for runType in socHT:
        if runType == '1sNoHT':
            for threads in socHT[runType]:
                socHT[runType][threads] = [range(threads)]

def main(): 
    """
    Main starting function of the code
    """
    for atomic in atomics:
        atomics[ atomic ] = socHT
        i=0
        for x in range(len(socHT)):
            atomics[ atomic ][ socHT.keys()[x] ] = threads[i]
            i=i+1
        
    thr_populate()
   
    print 'len is',len(atomics)
    for atomic in atomics:
        #print atomic
        start = time.time()
        for state in states: 
            for testNum in states[state]: 
                if atomic == state:
                    for runType in atomics[atomic]:
                        #print runType
                        for numThreads in atomics[atomic][runType]:
                            #print numThreads
                            #print atomics[atomic][runType][numThreads]
                            for j in range(len(atomics[atomic][runType][numThreads])):
                                #print ">>", atomics[atomic][runType][numThreads][j]
                                threadlist = ""
                                cpus = len(atomics[atomic][runType][numThreads][j])
                                #print atomics[atomic][runType][numThreads][j]
                                for k in range(cpus):
                                    threadlist = threadlist + str(atomics[atomic][runType][numThreads][j][k])
                                    if k < cpus - 1:
                                        threadlist = threadlist + ","
                                    
                                #print threadlist
                                arg = []
                                arg = arg + ["./run_ccbench.sh"]
                                arg = arg + [str(testNum)]
                                arg = arg + [str(cpus)]
                                arg = arg + [threadlist]
                                arg = arg + [str(runType)]
                                arg = arg + [str(atomic)]
                                sp.check_call(args=arg)
                
        end = time.time()
        print  atomic, "Time: ", end - start, " (s)"
    
if __name__ == '__main__':
    main()
