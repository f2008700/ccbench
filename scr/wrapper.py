import subprocess as sp
import time

atomics={"cas":{}, "tas":{}, "fai":{}, "swap":{}}
socHT={"1sNoHT":[],"1sHT":[],"2sNoHT":[],"2sHT":[]}
threads=[ {2:{},4:{},8:{},16:{},28:{}},
    {4:{},8:{},16:{},32:{},56:{}},
    {2:{},4:{},8:{},16:{},28:{}},
    {1:{},2:{},4:{},8:{},14:{}}]
states={"cas":[16,41,20,12], 
        "tas":[18,43,22,14],
        "fai":[17,42,21,13],
        "swap":[19,44,23,15] }

def thr_populate():
    for runType in socHT:
        if runType == '1sNoHT':
            for threads in socHT[runType]:
                socHT[runType][threads] = [range(threads)]
        elif runType == '1sHT':
            for threads in socHT[runType]:

                if threads == 2:
                    socHT[runType][threads] = [[0,28]]
                elif threads == 4:
                    socHT[runType][threads] = [[0,1,28,29]]
                elif threads == 8:
                    socHT[runType][threads] = [range(4) + range(28,32)]
                elif threads == 16:
                    socHT[runType][threads] = [range(8) + range(28,36)] 
                elif threads == 28:
                    socHT[runType][threads] = [range(14) + range(28,42)] 
                else:
                    print "1Wrong threads num. Breaking!" , threads
                    return
        elif runType == '2sNoHT':
            for threads in socHT[runType]:
                if threads == 2:
                    socHT[runType][threads] = [[ 0, 14 ]] 
                elif threads == 4:
                    socHT[runType][threads] = [ range(2) + range(14,16), range(1) + range(14,17) ] 
                elif threads == 8:
                    socHT[runType][threads] = [ range(1) + range(14,21), 
                                                range(2) + range(14,20),
                                                range(3) + range(14,19),
                                                range(4) + range(14,18) ]

                elif threads == 16:
                    socHT[runType][threads] = [ range(2) + range(14,28),
                                                range(3) + range(14,27),
                                                range(4) + range(14,26),
                                                range(5) + range(14,25),
                                                range(6) + range(14,24),
                                                range(7) + range(14,23),
                                                range(8) + range(14,22) ]
                                
                elif threads == 28:
                    socHT[runType][threads] = [ range(28) ]
                else:
                    print "2Wrong threads num. Breaking!" , threads
                    return
        elif runType == '2sHT':
            for threads in socHT[runType]:
                if threads == 4:
                    socHT[runType][threads] = [[ 0,14,28,42 ]]
                elif threads == 8:
                    socHT[runType][threads] = [ range(2) + range(14,16) + range(28,30) + range(42,44),
                                                range(1) + range(14,17) + range(28,29) + range(42,45) ] 
                elif threads == 16:
                    socHT[runType][threads] = [ range(1) + range(14,21) + range(28,29) + range(42,49),
                                                range(2) + range(14,20) + range(28,30) + range(42,48),
                                                range(3) + range(14,19) + range(28,31) + range(42,47),
                                                range(4) + range(14,18) + range(28,32) + range(42,46) ]
                elif threads == 32 :
                    socHT[runType][threads] = [ range(2) + range(14,28) + range(28,30) + range(42,56),
                        range(3) + range(14,27) + range(28,31) + range(42,55),
                        range(4) + range(14,26) + range(28,32) + range(42,54),
                        range(5) + range(14,25) + range(28,33) + range(42,53),
                        range(6) + range(14,24) + range(28,34) + range(42,52),
                        range(7) + range(14,23) + range(28,35) + range(42,51),
                        range(8) + range(14,22) + range(28,36) + range(42,50) ]
                elif threads == 56:
                    socHT[runType][threads] = [range(56)] 
                else:
                    print "3Wrong threads num. Breaking!" , threads
                    return

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
        if atomic == "swap":
            continue
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
