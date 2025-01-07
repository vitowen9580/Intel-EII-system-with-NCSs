#!/bin/bash
while true
do
    for dir in test1 test2 test3    
    do
        # python3 main.py -d "$dir" -x model/Unet_.xml -b model/Unet_.bin -m MYRIAD.1.8.1-ma2480
            python3 main.py -d "$dir" -x model/AttUnet_.xml -b model/AttUnet_.bin -m CPU
        sleep 5
    done
done