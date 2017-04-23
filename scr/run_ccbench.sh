#!/bin/bash

testname=$1
cpus=$2
threads=$3
runType=$4
atomic=$5
iterations=100000
cd ..

result_dir=results/$atomic/$runType/$testname/
mkdir -p $result_dir
echo "./ccbench -t $testname -c $cpus -x $threads $runType $atomic"

./ccbench -t $testname -c $cpus -x $threads -e 8 -s 0 -r $iterations -f -u > $result_dir/$cpus"_"$threads.txt 2>&1
