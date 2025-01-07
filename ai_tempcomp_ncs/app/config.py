class system_config_setting:
    slice_pixel=256
    stride=16
    #True:On ,False:off
    #filter HEAD & noise

class NCS_setting:
    #"CPU","MYRIAD" 
    inference_device = "MYRIAD" 
    QUEUE_WAIT_SECONDS = 2

    threads_per_dev = 1 #4
    simultaneous_infer_per_thread = 12 #total 2993 data/(threads_per_dev*num_ncs_devs)
    num_ncs_devs = 1
    run_async = True
    INFER_RES_QUEUE_SIZE = simultaneous_infer_per_thread
    
    # threads_per_dev = 2 #4
    # simultaneous_infer_per_thread = 700
    # num_ncs_devs = 2
