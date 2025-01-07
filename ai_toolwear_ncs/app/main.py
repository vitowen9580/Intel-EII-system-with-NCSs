try:
    from openvino.inference_engine import IENetwork, ExecutableNetwork, IECore
    import openvino.inference_engine.ie_api
except:
    print(RED + '\nPlease make sure your OpenVINO environment variables are set by sourcing the' + YELLOW + ' setupvars.sh ' + RED + 'script found in <your OpenVINO install location>/bin/ folder.\n' + NOCOLOR)
    exit(1)
import keyboard
import cv2
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
import cv2
from PIL import Image
import matplotlib.pyplot as plt
from Metrics import _metrics
import logging
logging.basicConfig(format="[ %(levelname)s ] %(message)s", level=logging.INFO, stream=sys.stdout)
log = logging.getLogger()
import warnings
from datetime import datetime

warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")
from immcEiiUtils import EiiConfigMgr, EiiClient, EiiPublisher
from ImageProcessingToolkit import Imageprocess
from argumentToolkit import argument
from config import NCS_setting

'''
=======
Global variable
========
'''
_Imageprocess=Imageprocess()
args = argument().build_argparser().parse_args()
_NCS_setting=NCS_setting()
metrics=_metrics()
number_of_inferences = 500
quit_flag = False
reset_flag = False
stop_threads = False

sep = os.path.sep
image_dir= "."+sep
stop_event = threading.Event()

def preprocess(frame):
    prepimg = frame[:, :].copy()
    prepimg = Image.fromarray(prepimg)
    prepimg = prepimg.resize((256, 256), Image.ANTIALIAS)
    prepimg = np.asarray(prepimg) / 255.0
    prepimg=prepimg.reshape((1, 256, 256, 3))
    prepimg = prepimg.transpose((0, 3, 1, 2))
    return prepimg

def infer_async_thread_proc(input_blob,out_blob,exec_net: ExecutableNetwork, first_request_index: int,
                            input_image_list: list,img_name_list:list,
                            first_image_index:int, last_image_index:int,
                            num_total_inferences: int, result_list: list, thread_index:int,
                            start_barrier: threading.Barrier, end_barrier: threading.Barrier,
                            simultaneous_infer_per_thread:int, infer_result_queue:queue.Queue,MYRIAD_name:int):

    while   not stop_threads:
        # sync with the main start barrier
        #usually we'll wait on simultaneous_infer_per_thread but the last time it could be less.
        images_to_wait_on = simultaneous_infer_per_thread
        start_barrier.wait()
        start_time = time.time()
        end_time = start_time

        handle_list = [None]*simultaneous_infer_per_thread

        image_index = first_image_index
        while (image_index <= last_image_index) :

            # Start the simultaneous async inferences
            for start_index in range(0, simultaneous_infer_per_thread):
                handle_list[start_index] = exec_net.start_async(request_id=first_request_index+start_index, 
                                                                inputs={input_blob: input_image_list[image_index]}), \
                                            img_name_list[image_index], \
                                            input_image_list[image_index], \
                                            thread_index,\
                                            MYRIAD_name,\
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
                outputs = res.transpose((2, 3, 1, 0)).reshape((256, 256))
                outputs = np.reshape(outputs, (256, 256))*255.0
                outputs = Image.fromarray(np.uint8(outputs), mode="P")
                outputs = np.asarray(outputs)

                #output1
                image_filename = handle_list[wait_index][1]

                #input
                inputs = handle_list[wait_index][2]
                inputs = inputs.transpose((2, 3, 1, 0)).reshape((256, 256,3))
                inputs = np.asarray(inputs)

                #thread_index
                res_thread_index=handle_list[wait_index][3]

                #MYRIAD_name
                res_MYRIAD_name=handle_list[wait_index][4]
                # put a tuple on the output queue with
                infer_result_queue.put((image_filename, outputs,inputs,res_thread_index,res_MYRIAD_name), True)
                handle_list[wait_index] = None

            if (quit_flag == True):
                
                # the quit flag was set from main so break out of loop
                break


        # save the time spent on inferences within this inference thread and associated reader thread
        end_time = time.time()
        total_inference_time = end_time - start_time
        result_list[thread_index] = total_inference_time

        # wait for all inference threads to finish
        end_barrier.wait()

        # if (not reset_flag):
        #     break
        break
        


def main():


    
    # global quit_flag, pause_flag, reset_flag, total_paused_time, number_of_inferences
    global stop_threads,quit_flag, reset_flag, total_paused_time, number_of_inferences,image_dir


    model_xml_fullpath = args.xml_path
    model_bin_fullpath = args.bin_path
    image_dir= fr'{image_dir}/test_dataset/{args.TestData}'
    MYRIAD_name=args.MYRIAD_name

    print('args model_xml_fullpath:',model_xml_fullpath)
    print('args model_bin_fullpath:',model_bin_fullpath)


    # adjust number of inferences to evenly work out for number of images
    inferences_per_thread = int(number_of_inferences / ((NCS_setting.threads_per_dev * NCS_setting.num_ncs_devs)))
    inferences_per_thread = int(inferences_per_thread / NCS_setting.simultaneous_infer_per_thread) * NCS_setting.simultaneous_infer_per_thread
    total_number_threads = _NCS_setting.num_ncs_devs * NCS_setting.threads_per_dev


    MYRIADs=list()
    ie = IECore()
    for device_name in ie.available_devices:
        if(device_name.find('MYRIAD')>-1):
            MYRIADs.append(device_name)
    net = IENetwork(model=model_xml_fullpath, weights=model_bin_fullpath)
    input_blob = next(iter(net.inputs))
    out_blob = next(iter(net.outputs))
    n, c, h, w = net.inputs[input_blob].shape

    exec_net_list = [None] * _NCS_setting.num_ncs_devs
    for dev_index in range(0, _NCS_setting.num_ncs_devs):
        exec_net_list[dev_index] = ie.load_network(network=net, num_requests=NCS_setting.threads_per_dev*NCS_setting.simultaneous_infer_per_thread, device_name = MYRIAD_name)
    


    total_Panoramic_image_filename_list = os.listdir(image_dir)

    image_filename_list = [image_dir + sep + i for i in total_Panoramic_image_filename_list if (i.endswith('.jpg') or i.endswith(".png"))]
    print("Found " + str(len(image_filename_list)) + " images.")
    print(image_filename_list)


    patch_image_list=list()
    img_name_list=list()
    for name in image_filename_list:
        img_name_list.append(name.split('\\')[-1])
        patch_image_list.append(cv2.imread(name))
 
    start=time.time()
    total_image_count = len(patch_image_list)
    print("total_path_image_count is: " + str(total_image_count))



    infer_result_queue = queue.Queue(_NCS_setting.INFER_RES_QUEUE_SIZE)

    result_times_list = [None] * (_NCS_setting.num_ncs_devs * NCS_setting.threads_per_dev)
    thread_list = [None] * (_NCS_setting.num_ncs_devs * NCS_setting.threads_per_dev)
    start_barrier = threading.Barrier(_NCS_setting.num_ncs_devs*NCS_setting.threads_per_dev+1)
    end_barrier = threading.Barrier(_NCS_setting.num_ncs_devs*NCS_setting.threads_per_dev+1)


    
    '''
    =================
    images pre-process
    =================
    '''
    preprocessed_image_list = [None]*len(patch_image_list)
    for index,one_patch_image in enumerate(patch_image_list):
        one_preprocessed_image = _Imageprocess.preprocess_image(one_patch_image)
        preprocessed_image_list[index] = one_preprocessed_image



    base_images_per_thread = int(len(preprocessed_image_list) / total_number_threads)
    # extra_images = len(preprocessed_image_list) % base_images_per_thread
    
    '''
    =================
    distribute patch images to each device and thread
    =================
    '''
    # exec_net_list = [None] * _NCS_setting.num_ncs_devs
    last_image_index = -1
    for dev_index in range(0, _NCS_setting.num_ncs_devs):
        for dev_thread_index in range(0,NCS_setting.threads_per_dev):
            total_thread_index = dev_thread_index + (NCS_setting.threads_per_dev*dev_index)
            first_image_index = last_image_index + 1 
            last_image_index = int(first_image_index + base_images_per_thread - 1)

            if (NCS_setting.run_async):
                thread_list[total_thread_index] = threading.Thread(target=infer_async_thread_proc,
                                                                            args=[input_blob,out_blob,exec_net_list[dev_index], dev_thread_index*NCS_setting.simultaneous_infer_per_thread,
                                                                                    preprocessed_image_list, img_name_list,
                                                                                    first_image_index, last_image_index,
                                                                                    inferences_per_thread,
                                                                                    result_times_list, total_thread_index,
                                                                                    start_barrier, end_barrier, NCS_setting.simultaneous_infer_per_thread,
                                                                                    infer_result_queue,MYRIAD_name])
            else:
                pass
    # del net

    '''
    =================
    start thread
    =================
    '''
    
    for one_thread in thread_list:
        
        one_thread.start()


    '''
    =================
    wait for next Panoramic_image 
    key a:continue
    key q:quit
    =================
    '''


    for result_time_index in range(0, len(result_times_list)):
        result_times_list[result_time_index] = 0.0

    reset_flag = False
    quit_flag = False
    start_barrier.wait()
    # resetting the start barrier in case we are resetting rather than quiting
    start_barrier.reset()

        


    
    result_counter = 0
    output_list=list()
    while (result_counter < total_image_count):
        infer_res = infer_result_queue.get(True, NCS_setting.QUEUE_WAIT_SECONDS)
        infer_res_filename = infer_res[0]
        outputs = infer_res[1]
        inputs= infer_res[2]
        thread_index=infer_res[3]
        MYRIAD_name=infer_res[4]
        output_list.append([infer_res_filename,outputs,inputs,thread_index,MYRIAD_name])
        
        
        result_counter += 1
        infer_result_queue.task_done()



    end_barrier.wait()
    if (not quit_flag):
        reset_flag=True
        cv2.waitKey(-1)

    end_barrier.reset()

    if (not reset_flag):
        print("main not resetting, breaking")


    stop_threads=True
    '''
    clear
    '''
    for one_thread in thread_list:
        if one_thread != threading.current_thread():  # Skip the main thread
            one_thread.join()



    # clean up
    for one_exec_net in exec_net_list:
        del one_exec_net



    '''
    儲存result
    '''
    # for filename,predictions,input,_,_ in output_list:
    #     filename=filename.split('/')[-1]

    #     superimpose_images=_Imageprocess.superimpose_images_numpy_arrays(input*255,predictions)
    #     cv2.imwrite(f"result/{filename}", predictions)
    #     cv2.imwrite(f"result/superimpose_{filename}", superimpose_images)



    publisher_name = "test2"
    publisher_topic = "measurement_test2"
    try:
        # Intialize the message buxs context with config manager
        cfg_mgr = EiiConfigMgr()
        # Initialize the publisher to write temperature compensation data
        data_writer = EiiPublisher(cfg_mgr, publisher_name, publisher_topic)

        for index,(filename,predictions,input_img,_,_) in enumerate(output_list):
            superimpose_images=_Imageprocess.superimpose_images_numpy_arrays(input_img*255,predictions)
            
            
            superimpose_base64_string=_Imageprocess.image_to_base64(superimpose_images)
            input_img_base64_string=_Imageprocess.image_to_base64(input_img*255)
            predictions_base64_string=_Imageprocess.image_to_base64(predictions)
            white_pixels = str(int(np.sum(predictions == 255)))
            now = datetime.now()
            date_time_short = now.strftime("%Y-%m-%d %H:%M")
            output_dict = {
                f'filename_{index}': f'Image name:{filename}',
                f'toolwear_{index}': f'Amount of wear:{white_pixels}',
                f'model_{index}': f'{MYRIAD_name},model:{args.bin_path}',
                f'predictions_base64_string_{index}':predictions_base64_string,
                f'input_img_base64_string_{index}':input_img_base64_string,
                f'superimpose_base64_string_{index}':superimpose_base64_string
            }
            cv2.imwrite(f"result/{filename.split('/')[-1]}", superimpose_images)
            print('=======results===========')        

            print(output_dict[f'filename_{index}'],\
                output_dict[f'toolwear_{index}'],\
                output_dict[f'model_{index}'])
            # print(f"{filename} , Amount of wear:{white_pixels}")
            # cv2.waitKey(0)
            data_writer.publish(output_dict)

    except Exception as e:
        print(f"[ERROR]: {e}")
    finally:
        if data_writer is not None:
            data_writer.close()
    
    
    print('=======done===========')        


if __name__ == "__main__":
    sys.exit(main())
