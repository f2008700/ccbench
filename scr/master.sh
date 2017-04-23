#!/bin/bash +x

x=1
iterations=500000
testcase=$1
numcpu=$2
cpu0=$3
cpu1=$4
cpu2=$5
offset=$6
grepp=$7


run_test() {
    echo "Run Test"
    echo $tests $CPU $threads
    cd ..
    echo "./ccbench -t $tests -c $CPU -x $threads -e 8 -s 0 -r $iterations -f -u | grep med | grep \"$grepp\" | tee -a \"$tests\"_\"$CPU\"_\"$threads\".txt"
    #./ccbench -t $testcase -c $CPU -x $threads -e 8 -s 0 -r 50000 -f -u | grep med | tee -a "$tests"_"$CPU"_"$threads".txt
    ./ccbench -t $tests -c $CPU -x $threads -e 8 -s 0 -r $iterations -f -u | grep med | tee -a results/"$tests"_"$CPU"_"$threads".txt

}

run_threads() {
    for tests in "${testNums[@]}"
    do
        #echo $tests
    
        # Test Cases
        declare -a threadNums=( 1 2 4 8 14 )
        declare -a threadNums=( 2 )
        for threadNum in "${threadNums[@]}"
        do
            case $threadNum in
                "1") threads="6"
                    ;;
                "2") threads="0,6"
                    ;;
                "4") threads="1,2,4"
                    ;;
                "8") threads="1"
                    ;;
                "14") threads="2"
                    ;;
                *) echo "Unusual thread nums. Breaking!!"
                    ;;
            esac
            CPU=$threadNum
            #echo $tests $CPU $threads
            run_test $test $CPU $threads
            
            echo $threads         
        done
        
    done
}

# CAS - 1
# TAS - 2
# FAI - 3
# SWAP - 4

declare -a atomicsNums=( 1 2 3 4 )
declare -a atomicsNums=( 1 )
for atomics in "${atomicsNums[@]}"
do
    case $atomics in
        "1") echo "CAS"

            # TODO - Check the test nums with the enum sequence
            declare -a testNums=( 16 41 20 12 )
            declare -a testNums=( 20 )
            run_threads testNums
            ;;
        "2") echo "TAS"
            declare -a testNums=( 18 43 22 14 )
            run_threads

            ;;
        "3") echo "FAI"
            declare -a testNums=( 17 42 21 13 )
            run_threads

            ;;
        "4") echo "SWAP"
            declare -a testNums=( 19 44 23 15 )
            run_threads
            
            ;;
        *) echo "Default"
            exit
            ;;
    esac
done




