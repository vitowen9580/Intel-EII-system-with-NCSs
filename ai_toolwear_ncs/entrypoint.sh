#!/bin/bash

# cd /app/code
# python3 ai_inference_demo.py &
# python3 ai_inference_ecb.py &

# # Keep it running and watch the processes
# while [ true ]
# do
#     demo_stat=$(ps ax | grep 'python3 ai_inference_demo.py' | grep -v 'grep')
#     ecb_stat=$(ps ax | grep 'python3 ai_inference_ecb.py' | grep -v 'grep')

#     if [ -z "$demo_stat" ] || [ -z "$ecb_stat" ] ; then
#         echo "Restarting TempComp..."
#         exit
#     fi 

#     sleep 3
# done

sleep infinity