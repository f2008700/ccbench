#!/bin/bash

x=1
testcase=$1
numcpu=$2
cpu0=$3
cpu1=$4
cpu2=$5
offset=$6
grepp=$7
while [ $x -lt 11 ];
do
	#echo Hello $testcase $cpu0 $cpu1 $cpu2
	if [ $numcpu -eq 2 ]
		then
			echo "Running on two cpus"
			./ccbench -t $testcase -c 2 -x $cpu0 -y $cpu1 -e 8 -s 0 -r 50000 -f -u | grep med | grep "$grepp" | tee -a "$testcase"_"$cpu0"_"$cpu1".txt
	elif [ $numcpu -eq 3 ]
		then
			echo "Running on three cpus"
			./ccbench -t $testcase -c 3 -x $cpu0 -y $cpu1 -z $cpu2 -e 8 -s 0 -r 50000 -f -u | grep med | grep "$grepp" | tee -a "$testcase"_"$cpu0"_"$cpu1"_"$cpu2".txt
	elif [ $numcpu -eq 1 ]
		then
			echo "Running on one cpu"
			./ccbench -t $testcase -c 1 -x $cpu0 -e 8 -s 0 -r 50000 -f -u | grep med | grep "$grepp" | tee -a "$testcase"_"$cpu0".txt
	else 
		./ccbench -t $testcase -c $numcpu -x $cpu0 -y $cpu1 -z $cpu2 -o $offset -e 8 -s 0 -r 50000 -f -u | grep med | grep "$grepp" | tee -a "$testcase"_"$cpu0"_"$cpu1"_"$cpu2"_o"$offset".txt
		#echo "Incorrect argument for num cpus"
	fi
	#./ccbench -t $testcase -c 3 -x $cpu0 -y $cpu1 -z $cpu2 -e 8 -s 0 -r 50000
	#echo Bye $testcase $cpu0 $cpu1 $cpu2
	x=$(( $x + 1 ))
done
