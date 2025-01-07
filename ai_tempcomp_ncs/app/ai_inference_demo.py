# Packages for running AI inference
import numpy as np
from eii.exc import ReceiveTimeout
import json
import time
import random
from immcEiiUtils import EiiConfigMgr, EiiClient, EiiPublisher

class ThirdPartyApp:
    def __init__(self):
        pass


    def run(self):
        ''' Executes the third party application and the input is input_dict '''  
        output_dict = {
            'comp1': 7,
            'comp2': 2,
            'comp3': 3,
            'comp4': 4,
            'condi': 5,
            'machine': 'test',
        }
        print(output_dict)
        return output_dict

def main():

    publisher_name = "test"
    publisher_topic = "measurement_test"
    try:
        # Intialize the message buxs context with config manager
        cfg_mgr = EiiConfigMgr()
        # Initialize the publisher to write temperature compensation data
        data_writer = EiiPublisher(cfg_mgr, publisher_name, publisher_topic)
        # Initialize the 3rd party application
        third_party_app = ThirdPartyApp()
        
        while True:
            output_data_dict=third_party_app.run()
            data_writer.publish(output_data_dict)
            time.sleep(1)
  
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")

    finally:
        if data_writer is not None:
            data_writer.close()

if __name__ == "__main__":
    main()