#!/bin/bash

declare -a atomics=('cas' 'tas' 'fai')
declare -a configs=('1sHT' '1sNoHT' '2sHT' '2sNoHT')

for atomic in "${atomics[@]}"
do
    for config in "${configs[@]}"
    do
        for file in `ls ../analysis/"$atomic"/"$config"/*.txt`
        do
            #file=../analysis/"$atomic"/"$config"/$file
            python cluster_plot.py $file
            echo $file
        done
    done
done
