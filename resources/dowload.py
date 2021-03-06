# -*- coding: utf-8 -*- 

import os
import shutil
import requests
from config import Config

""" This class functions for get images and write in path uploads """
class ControllerDownload(object):
    def __init__(self, *args):
        self.url = "https://images8.alphacoders.com/768/768202.jpg"

    def get_download_img(self, *args):
        try:
            response = requests.get(self.url, stream=True)
            if response.status_code == 200:
                with open(os.path.join(Config.UPLOAD_FOLDER + 'file.png'), 'wb') as out_file:
                    out_file.write(response.content)
                    
        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}
    
    def scrapy_dir_uploads(self):
        images = []
        for root, dirs, files in os.walk(Config.UPLOAD_FOLDER):
            [images.append(row) for row in files]
        return images