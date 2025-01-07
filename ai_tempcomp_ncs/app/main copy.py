'''
===================[Processing]===================
STEP1.c# select template ROI
STEP2.c# capture Panoramic_image
STEP3.c# select model
STEP4.c# argument input :python .py --model_path  model --template_path template
STEP5.python recieve Panoramic_image
STEP6.python return result to c# [combination patch images,image name, NG/OK] 
====================================================
'''
try:
    from openvino.inference_engine import IENetwork, ExecutableNetwork, IECore
    import openvino.inference_engine.ie_api
except:
    print(RED + '\nPlease make sure your OpenVINO environment variables are set by sourcing the' + YELLOW + ' setupvars.sh ' + RED + 'script found in <your OpenVINO install location>/bin/ folder.\n' + NOCOLOR)
    exit(1)
# import keyboard
import numpy
import time
import sys
import threading
import os
from sys import argv
import datetime
import queue
from queue import *
import time
import skimage.io as io
import skimage.transform as trans
import os
import sys
import logging as log
import numpy as np
import h5py
import time 
#import tensorflow as tf
from inferenceToolkit import Network
import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
from skimage import morphology 
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
params = {'axes.titlesize':32, 'xtick.labelsize':24, 'ytick.labelsize':24, 'axes.labelsize': 32, 'axes.titlesize': 32}
matplotlib.rcParams.update(params)

import matplotlib.pyplot as plt
import logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
log = logging.getLogger()
import random
import time
import numpy as np
from eii.exc import ReceiveTimeout
import json
import time
import random
from immcEiiUtils import EiiConfigMgr, EiiClient, EiiPublisher
import base64


'''
mylib
'''
from argumentToolkit import argument
from config import NCS_setting
from socketToolkit import socket_class
# import torch.nn as nn

from tqdm.auto import tqdm
'''
=======
Global variable
========
'''
args = argument().build_argparser().parse_args()
# MYRIAD_name=args.MYRIAD_name

_NCS_setting=NCS_setting()
_socket=socket_class()
number_of_inferences = 500
quit_flag = False
reset_flag = False
type_dict={"NG":0,"OK":1}

sep = os.path.sep
Panoramic_image_dir= "." + sep + "test_dataset"



def image_to_base64(image_path):
    """
    将图片转换为 Base64 编码字符串
    :param image_path: 图片文件的路径
    :return: Base64 编码的字符串
    """
    try:
        # 以二进制模式读取图片
        with open(image_path, "rb") as image_file:
            # 使用 base64 编码
            base64_string = base64.b64encode(image_file.read()).decode("utf-8")
        return base64_string
    except Exception as e:
        print(f"Error converting image to Base64: {e}")
        return None 
    
    

def infer_async_thread_proc(input_blob,out_blob,exec_net: ExecutableNetwork, first_request_index: int,
                            labels_list: list,test_data_inputs_list:list,
                            first_image_index:int, last_image_index:int,
                            num_total_inferences: int, result_list: list, result_index:int,
                            start_barrier: threading.Barrier, end_barrier: threading.Barrier,
                            simultaneous_infer_per_thread:int, infer_result_queue:queue.Queue):

    while (True):
        # sync with the main start barrier
        #usually we'll wait on simultaneous_infer_per_thread but the last time it could be less.
        images_to_wait_on = simultaneous_infer_per_thread
        start_barrier.wait()

        handle_list = [None]*simultaneous_infer_per_thread

        image_index = first_image_index

        while (image_index <= last_image_index) :
            # Start the simultaneous async inferences
            for start_index in range(0, simultaneous_infer_per_thread):    
                
                handle_list[start_index] = exec_net.start_async(request_id=first_request_index+start_index, 
                                                                inputs={input_blob: test_data_inputs_list[image_index]}), \
                                            labels_list[image_index], \
                                            image_index
                image_index += 1
                if (image_index > last_image_index):
                    images_to_wait_on = start_index + 1
                    break # done with all our images.

                
            # Wait for the simultaneous async inferences to finish.

            for wait_index in range(0, images_to_wait_on):
                res = None
                infer_stat = handle_list[wait_index][0].wait()
                # output0
                res = handle_list[wait_index][0].outputs[out_blob]
                

                #output1
                image_label = handle_list[wait_index][1]
                index = handle_list[wait_index][2]

                # put a tuple on the output queue with
                infer_result_queue.put((index,res,image_label), True)
                handle_list[wait_index] = None

            if (quit_flag == True):
                # the quit flag was set from main so break out of loop
                break


        # save the time spent on inferences within this inference thread and associated reader thread

        print("thread " + str(result_index) + " end barrier reached")

        # wait for all inference threads to finish
        end_barrier.wait()

        if (not reset_flag):
            break
        print("thread " + str(result_index) + " looping back")


from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import time

# Prepare the dataset
############################################################################################
# Load the iris dataset
import numpy as np
import pandas as pd

print('Loading data...')

data_root = './data/'
train_data_1 = pd.read_csv(data_root + 'EXP_20200720.csv', dtype=int)
train_data_2 = pd.read_csv(data_root + 'EXP_20200616.csv', dtype=int)
test_data = pd.read_csv(data_root + 'EXP_20200817.csv', dtype=int)

train_data_labels_1 = train_data_1['Disp']
train_data_labels_2 = train_data_2['Disp']
test_data_labels = test_data['Disp']

train_data_time = train_data_1['Time'].to_numpy()
test_data_time = test_data['Time'].to_numpy()

train_data_1 = train_data_1.drop(['Time', 'Disp', 'Speed'], axis=1)
train_data_2 = train_data_2.drop(['Time', 'Disp', 'Speed'], axis=1)
test_data = test_data.drop(['Time', 'Disp', 'Speed'], axis=1)

train_data_1.head()

train_data_1 = train_data_1.to_numpy()
train_data_2 = train_data_2.to_numpy()
train_data_labels_1 = train_data_labels_1.to_numpy()
train_data_labels_2 = train_data_labels_2.to_numpy()

train_data = np.concatenate((train_data_1, train_data_2[:800, :]), axis=0)
valid_data = train_data_2[800:, :]
test_data = test_data.to_numpy()

train_data_labels = np.concatenate((train_data_labels_1, train_data_labels_2[:800]), axis=0)
valid_data_labels = train_data_labels_2[800:]
test_data_labels = test_data_labels.to_numpy()

mean = train_data.mean(axis=0)
std = train_data.std(axis=0)
train_data = (train_data - mean) / std
valid_data = (valid_data - mean) / std
test_data = (test_data - mean) / std

train_data

train_data = train_data.reshape(train_data.shape[0], 1 , train_data.shape[1])
valid_data = valid_data.reshape(valid_data.shape[0],1 ,valid_data.shape[1] )
test_data = test_data.reshape(test_data.shape[0], 1,test_data.shape[1])

train_data_copy = train_data.copy()

print('Size of training data: {}'.format(train_data.shape))
print('Size of validation data: {}'.format(valid_data.shape))
print('Size of testing data: {}'.format(test_data.shape))
import torch
from torch.utils.data import Dataset

class TCDataset(Dataset):
    def __init__(self, X, y=None):
        self.data = torch.from_numpy(X).float()
        
        if y is not None:
            y = y.astype(np.float64)
            self.label = torch.FloatTensor(y)
        else:
            self.label = None

    def __getitem__(self, idx):
        if self.label is not None:
            return self.data[idx], self.label[idx]
        else:
            return self.data[idx]

    def __len__(self):
        return len(self.data)

BATCH_SIZE = 64

from torch.utils.data import DataLoader

train_set = TCDataset(train_data, train_data_labels)
val_set = TCDataset(valid_data, valid_data_labels)
train_loader = DataLoader(train_set, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_set, batch_size=BATCH_SIZE, shuffle=False)

from tqdm.auto import tqdm

# create testing dataset
test_set = TCDataset(test_data, test_data_labels)
test_loader = DataLoader(test_set, batch_size=1, shuffle=False)

def get_device():
    #return 'cuda' if torch.cuda.is_available() else 'cpu'
    return _NCS_setting.inference_device
def main():

    # global quit_flag, pause_flag, reset_flag, total_paused_time, number_of_inferences
    global quit_flag, reset_flag, total_paused_time, number_of_inferences,Panoramic_image_dir

    model_xml_fullpath = args.xml_path
    model_bin_fullpath = args.bin_path
    heatmap_title=''

    print('args model_xml_fullpath:',model_xml_fullpath)
    print('args model_bin_fullpath:',model_bin_fullpath)


    # adjust number of inferences to evenly work out for number of images
    inferences_per_thread = int(number_of_inferences / ((NCS_setting.threads_per_dev * NCS_setting.num_ncs_devs)))
    inferences_per_thread = int(inferences_per_thread / NCS_setting.simultaneous_infer_per_thread) * NCS_setting.simultaneous_infer_per_thread
    total_number_threads = _NCS_setting.num_ncs_devs * NCS_setting.threads_per_dev

    '''
    =================
    NCS initialize
    =================
    '''
    ie = IECore()
    net = ie.read_network(model=model_xml_fullpath, weights=model_bin_fullpath)

    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))

    exec_net_list = [None] * _NCS_setting.num_ncs_devs
    for dev_index in range(0, _NCS_setting.num_ncs_devs):
        exec_net_list[dev_index] = ie.load_network(network=net, num_requests=NCS_setting.threads_per_dev*NCS_setting.simultaneous_infer_per_thread, device_name = 'MYRIAD')
    # MYRIAD_name
  


    # create testing dataset
    test_set = TCDataset(test_data, test_data_labels)
    test_loader = DataLoader(test_set, batch_size=1, shuffle=False)





    predict = []
    test_loss = 0.0
    device = get_device()
    print(f'=============DEVICE: {device}')
    labels_list=list()
    test_data_inputs_list=list()
    start = time.time()
    log.info("start_time{}".format(str(start)))

    with torch.no_grad():
        for i, data in enumerate(tqdm(test_loader)):
            test_data_inputs, labels = data
            test_data_inputs, labels = test_data_inputs.to('cpu'), labels.to('cpu')
            test_data_inputs=np.reshape(test_data_inputs,(1,8,1))
            labels_list.append(labels)
            test_data_inputs_list.append(test_data_inputs)


        total_image_count = len(test_data_inputs_list)
        infer_result_queue = queue.Queue(_NCS_setting.INFER_RES_QUEUE_SIZE)

        result_times_list = [None] * (_NCS_setting.num_ncs_devs * NCS_setting.threads_per_dev)
        thread_list = [None] * (_NCS_setting.num_ncs_devs * NCS_setting.threads_per_dev)
        start_barrier = threading.Barrier(_NCS_setting.num_ncs_devs*NCS_setting.threads_per_dev+1)
        end_barrier = threading.Barrier(_NCS_setting.num_ncs_devs*NCS_setting.threads_per_dev+1)




        base_images_per_thread = int(len(test_data_inputs_list)/ total_number_threads)
        print('base_images_per_thread:',base_images_per_thread)
        extra_images = len(test_data_inputs_list) % base_images_per_thread

        exec_net_list = [None] * _NCS_setting.num_ncs_devs

        last_image_index = -1

        for dev_index in range(0, _NCS_setting.num_ncs_devs):
            exec_net_list[dev_index] = ie.load_network(network=net, num_requests=NCS_setting.threads_per_dev*NCS_setting.simultaneous_infer_per_thread, device_name = device)

            for dev_thread_index in range(0,NCS_setting.threads_per_dev):
                total_thread_index = dev_thread_index + (NCS_setting.threads_per_dev*dev_index)
                first_image_index = last_image_index + 1 
                last_image_index = int(first_image_index + base_images_per_thread - 1)
                if (total_thread_index < extra_images):
                    last_image_index += 1
                # log.info("D"+str(dev_index)+"D:"+str(dev_index)+"S:"+str(first_image_index)+"~E:"+str(last_image_index))
                log.info("Device{}-Thread{}=S:{}~E:{}".format(str(dev_index),str(dev_thread_index),str(first_image_index),str(last_image_index)))
                # log.info("MYRIAD_name:{},Device{}-Thread{}=S:{}~E:{}".format(str(MYRIAD_name),str(dev_index),str(dev_thread_index),str(first_image_index),str(last_image_index)))

                if (NCS_setting.run_async):
                    thread_list[total_thread_index] = threading.Thread(target=infer_async_thread_proc,
                                                                                args=[input_blob,out_blob,exec_net_list[dev_index], dev_thread_index*NCS_setting.simultaneous_infer_per_thread,
                                                                                        labels_list, test_data_inputs_list,
                                                                                        first_image_index, last_image_index,
                                                                                        inferences_per_thread,
                                                                                        result_times_list, total_thread_index,
                                                                                        start_barrier, end_barrier, NCS_setting.simultaneous_infer_per_thread,
                                                                                        infer_result_queue])
                else:
                    pass
        del net



        '''
        =================
        start thread
        =================
        '''
        for one_thread in thread_list:
            one_thread.start()

        while (True):


            for result_time_index in range(0, len(result_times_list)):
                result_times_list[result_time_index] = 0.0

            reset_flag = False
            quit_flag = False
            start_barrier.wait()
            # resetting the start barrier in case we are resetting rather than quiting
            start_barrier.reset()

            total_paused_time = 0.0


            result_counter = 0
            output_list=list()
            while (result_counter < total_image_count):
                infer_res = infer_result_queue.get(True, NCS_setting.QUEUE_WAIT_SECONDS)
                index= infer_res[0]
                result = infer_res[1]
                label= infer_res[2]

                output_list.append([int(index),result[0][0],label[0].cpu().detach().numpy()])

                # if keyboard.is_pressed('q'):  
                # # if Stop_recieve:
                #     print('You Pressed A Key!')
                #     quit_flag=True
                #     # _socket.send_csharp('Stop')
                #     log.info("Python Stop")
                #     del net
                #     break 
                
                
                result_counter += 1
                infer_result_queue.task_done()

                    
            end_barrier.wait()

            end_barrier.reset()

            if (not reset_flag):
                print("main not resetting, breaking")
                break

            print("main thread looping back.")
    
        log.info("Inferences finished")

        '''
        clear
        '''
        for one_thread in thread_list:
            one_thread.join()
        # clean up
        for one_exec_net in exec_net_list:
            del one_exec_net

    spend_time =time.time()-start
    FPS=np.round(len(test_loader)/spend_time,5)

    log.info("spend_time:{}".format(str(spend_time)))
    log.info("FPS:{}".format(str(FPS)))



    output=np.array(output_list)
    output=output[output[:, 0].argsort()]
    with open('prediction_NCS.csv', 'w') as f:
        f.write('Time,Disp\n')
        for i, y in enumerate(output[:,1]):
            f.write('{},{}\n'.format(i + 1, y))




    plt.figure(figsize=(50, 30))
    plt.plot(test_data_time, output[:,2] * 0.1, color='black')
    plt.plot(test_data_time, output[:,1] * 0.1, color='red')
    plt.title('Prediction')
    plt.xlabel('Time (min)')
    plt.ylabel('Displacement (μm)')
    plt.grid(True)
    plt.savefig('result.png')
    # plt.show()
    RMSE=np.sqrt(((output[:,1] * 0.1 - output[:,2]  * 0.1) ** 2).mean())
    print('RMSE:',RMSE)



    publisher_name = "test"
    publisher_topic = "measurement_test"
    try:
        # Intialize the message buxs context with config manager
        cfg_mgr = EiiConfigMgr()
        # Initialize the publisher to write temperature compensation data
        data_writer = EiiPublisher(cfg_mgr, publisher_name, publisher_topic)
        # Initialize the 3rd party application

            
        base64_string=image_to_base64(f'result.png')
        output_dict = {
            'RMSE': RMSE,
            'base64_string':base64_string
        }
        data_writer.publish(output_dict)


    except Exception as e:
        print(f"[ERROR] 发生错误: {e}")
    finally:
        if data_writer is not None:
            data_writer.close()
    print('=======done===========')        



if __name__ == "__main__":
    sys.exit(main())
