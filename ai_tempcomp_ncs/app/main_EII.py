import random
import time
import numpy as np
from eii.exc import ReceiveTimeout
import json
import time
import random
from immcEiiUtils import EiiConfigMgr, EiiClient, EiiPublisher
import base64

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
    
    
class ThirdPartyApp:
    def __init__(self):
        self.count=0
        pass

    def run(self):
        self.image_urls = [
            "0.png",
            "result.png",
        ]

        image_url=self.image_urls[self.count%2]
        # base64_string=image_to_base64(f'/home/edge_insights_industrial/images/{image_url}')
        base64_string=image_to_base64(f'tempimage/{image_url}')

        
        output_dict = {
            'comp11': random.random(),
            'comp22': 2,
            'comp33': 3,
            'comp44': 4,
            'condii': 5,
            # 'image_url': f"https://192.168.50.33:3000/public/images/{image_url}"
            'image_url':image_url,
            'base64_string':base64_string
        }
        print(output_dict)  # 打印输出，检查是否正常
        self.count=self.count+1

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
            output_data_dict = third_party_app.run()
            print(output_data_dict)  # 打印输出，检查是否正常
            data_writer.publish(output_data_dict)

            time.sleep(1)

    except Exception as e:
        print(f"[ERROR] 发生错误: {e}")
    finally:
        if data_writer is not None:
            data_writer.close()

if __name__ == "__main__":
    main()
