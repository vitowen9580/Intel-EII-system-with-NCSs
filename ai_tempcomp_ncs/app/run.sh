#!/bin/bash 
#EXP_20200817_1.csv EXP_20200817_2.csv EXP_20200817_3.csv
while true
do
  for dir in EXP_20200817.csv 
  do
      # python3 main.py -d "$dir" -x model/model_withpermute.xml -b model/model_withpermute.bin -m MYRIAD.1.8.2-ma2480
      python3 main.py -d "$dir" -x model/model_withpermute.xml -b model/model_withpermute.bin -m CPU

  done
  sleep 5
done
