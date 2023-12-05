#!/bin/bash

clear
need_help (){
    echo Usage : ./main.sh /Path/to/data
    echo This script will find all the vcf files présent in the subdirectories of the path given in argument and will count the number of variants all the files.
    echo You can add the following options after the path to improve the script :
    echo -h : Display this help
    echo -v : Display the version of the script
    echo -g int : Change the gap between the variants \(default = 0\)
    echo -t int : Change the threshold of the variants \(default = 0.75\)

}

version=1.0

if [ "$1" == "" ]
then 
    need_help
    exit 1
else 
    param_array=( "$@")
    length=${#param_array[@]}
    for (( i=0; i<$length; i++ ))
    do
        
        if [ ${param_array[$i]} == "-h" ]
        then

            need_help
            exit 1
        fi
    
        if [ ${param_array[$i]} == "-v" ]
        then
            echo $version
            exit 0
        fi

        if [ ${param_array[$i]} == "-g" ]
        then
            gap=${param_array[i+1]}
        fi
        if [ ${param_array[$i]} == "-t" ]
        then
            threshold=${param_array[i+1]}
        fi
    done
        python3 parcourir.py "$1" "$gap" "$threshold"
        exit 0
fi


