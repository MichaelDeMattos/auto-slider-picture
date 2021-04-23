# -*- coding: utf-8 -*- 

import os
import shutil
import requests
from config import Config

""" This class functions for get images and write in path uploads """
class ControllerDownload(object):
    def __init__(self, *args):
        self.url = "url_image"

    def get_download_img(self, *args):
        try:
            response = requests.get(self.url, stream=True)
            if response.status_code == 200:
                with open(os.path.join(Config.UPLOAD_FOLDER + 'file.png'), 'wb') as out_file:
                    out_file.write(response.content)
            else:
                pass

        except Exception as error:
            print("Error: ", str(error))
            return {"status": 500, "error": str(error)}