#!/bin/bash

declare -a atomics=('cas' 'tas' 'fai')
declare -a configs=('1sHT' '1sNoHT' '2sHT' '2sNoHT')

for atomic in "${atomics[@]}"
do
    for config in "${configs[@]}"
    do
        file=/home/spai2/ccbench/analysis/"$atomic"/"$config"/*.txt
        python graph_ccbench.py $file&
        echo $file
    done
done
