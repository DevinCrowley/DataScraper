import requests
import numpy as np
from abcscrape import ABCScraper
from pathlib import Path
import os
import re

class KaggleScraper(ABCScraper):
    def __init__(self):
        if Path(''):
            pass  # TODO: Check if data_dir/kaggle exists. Need to make ABCSCraper.data_dir property first in `abcscrape.py`.

    def check_credentials():
        """
        check if credentials exist in the home directory.
        """
        if (Path.home() / ".kaggle/kaggle.json").exists()
            return True
        else:
            return False

    def get_data(self, url):
        
        # Check credentials
        if check_credentials():
            print("Credentials check passed: ~/.kaggle/kaggle.json file exists.")
        else:
            raise Exception("Credentials not set up for kaggle. For instructions see \nhttps://github.com/Kaggle/kaggle-api")
        
        # Get data
        basesite = "kaggle.com/"
        datasetUrlIndex = url.find(basesite) + len(basesite)
        dataset = url[datasetUrlIndex:]

        kaggleCommand = f"kaggle datasets download -p {where put} {dataset}"



        # $ kg dataset -u <username> -p <password> -o <owner> -d <dataset>
        # https://www.kaggle.com/mohansacharya/graduate-admissions
        # kaggle datasets download -d mohansacharya/graduate-admissions
        # checking kaggle cli documentation