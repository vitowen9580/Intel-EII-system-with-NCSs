# Packages for running AI inference
import numpy as np
from exe import config_reader as CR
from models import nn_lite_model as NN_Lite

# Packages for running EII message bus
from eii.exc import ReceiveTimeout
import json
import time

from immcEiiUtils import EiiConfigMgr, EiiClient, EiiPublisher

class ThirdPartyApp:
    def __init__(self, **kwargs):
        ''' Initialize the third party application '''
        try:
            # Initialize the AI model
            config_record_p = "./99_model_record/69-NN_TEE-TF-2-9-1-ZS-F-RELU/config_record.config" # Config record saved while model training
            last_end_ckpt = 10000 # The steps of saved file to be reuse
            delegate_p = "" # External delegate library path
            user_config = CR.config_reader("JP_NN_proto", config_record_p)["JP_NN_proto"].nn_hd_info
            if delegate_p == "":
                self.JP_NN_LITE = NN_Lite.NN_TFLITE(user_config, last_end_ckpt, None)
            else:
                self.JP_NN_LITE = NN_Lite.NN_TFLITE(user_config, last_end_ckpt, None, delegate_p)

            # Initialize ThirdPartApp runtime parameters
            self.TC_module_name = kwargs['ECB_SlotTitle']
            assert self.TC_module_name, "ECB_SlotTitle in build/eii_config.json cannot be empty."

            self.inference_channel_names = kwargs['ECB_ChTitle_inference']
            assert len(self.inference_channel_names) > 0, "ECB_ChTitle_inference in build/eii_config.json cannot be empty."

            self.env_temp_channel_name = kwargs['ECB_ChTitle_env_temp']
            assert self.env_temp_channel_name, "ECB_ChTitle_env_temp in build/eii_config.json cannot be empty."

            self.num_channels = len(self.inference_channel_names) + 1
            self.lastest_data_timestamp = 0

            self.all_channel_names = [f"Ch{i+1}" for i in range(7)]
        except Exception as e:
            print(f"[Error] Third party app init error:\n{e}")
            raise


    def get_query_data(self, meta_str):
        ''' Validates the query result string and return its dictionary if the query is valid.
            Otherwise, return None '''
        # Check the string
        if meta_str == "":
            return None, "[INFO] Empty query result."
        elif "null" in meta_str:
            # Some fields in the query result is empty, so the query is invalid
            return None, "[INFO] Null values in query result."
        
        # Check the dictionary
        meta_dict_lst = json.loads(meta_str)
        for i in range(self.num_channels - 1):
            if meta_dict_lst[i]['time'] != meta_dict_lst[i+1]['time']:
                return None, "[INFO] Not the latest query result."
        if meta_dict_lst[0]['time'] == self.lastest_data_timestamp:
            return None, "[INFO] Repeated timestamp."
        
        # Transform the received data from Msg bus to the input of 3rd party app
        app_input = {point['channel']:point['data']/3 for point in meta_dict_lst}
        for i in range(self.num_channels + 1, 8):
            app_input[f"Ch{i}"] = app_input[self.inference_channel_names[0]] + (i - self.num_channels)*0.05
        app_input["time"] = meta_dict_lst[0]['time']
        return app_input, None


    def run(self, input):
        ''' Executes the third party application with the input '''
        batch_f = np.float32([[np.float32(input[key]) - np.float32(input[self.env_temp_channel_name]) for key in self.all_channel_names]])
        inf_result = self.JP_NN_LITE.model_inference(batch_f)
        print(inf_result)

        output_dict = {
            'comp1': inf_result[0][0].item(),
            'comp2': inf_result[0][1].item(),
            'comp3': inf_result[0][2].item(),
            'comp4': inf_result[0][3].item(),
            'Siemens_comp': sum([inf_result[0][i] for i in range(4)])/4
        }
        print(output_dict)

        self.lastest_data_timestamp = input['time'] # Update the latest timestamp if the application runs successfully
        return output_dict


def main():
    client_name = "temp_data_reader"
    client_topic = "ecb_daq"
    publisher_name = "temp_compensation_writer"
    publisher_topic = "temp_compensation_data"

    msgbus_query_cmd = {
        "command": "read",
        "payload":{
            "topic": client_topic,
            "query": f"select * from (select last(data) as data from {client_topic} where module = 'TC module' group by channel)"
        }
    }

    data_reader = None
    data_writer = None

    try:
        # Intialize the message buxs context with config manager
        cfg_mgr = EiiConfigMgr()

        # Intialize the client to read temperature data
        data_reader = EiiClient(cfg_mgr, client_name)

        # Initialize the publisher to write temperature compensation data
        data_writer = EiiPublisher(cfg_mgr, publisher_name, publisher_topic)

        # Initialize the 3rd party application
        app_config = cfg_mgr.get_config_dict()
        third_party_app = ThirdPartyApp(**app_config)
        
        while True:
            try:
                data_reader.request(msgbus_query_cmd)
                response, _  = data_reader.recv(timeout=500)

                if response['response']['metadata'] is None:
                    print(f'[INFO] The query result is empty')
                elif response['statuscode'] != 0:
                    print(f'[INFO] Error: Status code is not 0. {response}')
                else:
                    input_data, mesg = third_party_app.get_query_data(response['response']['metadata'])

                    if input_data is None:
                        print(mesg)
                    else:
                        print(f"Received data:\n{input_data}")

                        # Apply some data transform to verify the data flow
                        output_data = third_party_app.run(input_data)
                        data_writer.publish(output_data)
            except ReceiveTimeout:
                print(f'[INFO] Client reception timeout.')
            time.sleep(0.4)

    except KeyboardInterrupt:
        print('[INFO] Quitting...')
    finally:
        if data_reader is not None:
            data_reader.close()

        if data_writer is not None:
            data_writer.close()

if __name__ == "__main__":
    main()