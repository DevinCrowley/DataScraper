import requests
import numpy as np
from .abcscrape import ABCScraper
from pathlib import Path
import os
import re

class KaggleScraper(ABCScraper):
    def __init__(self):
        super().__init__()
        self._data_source = "kaggle"
        print('end of kaggle_init')

    def check_credentials(self):
        """
        check if credentials exist in the home directory.
        """
        if (Path.home() / ".kaggle/kaggle.json").exists():
            return True
        else:
            return False

    def get_data(self, url):
        
        # Check credentials
        if self.check_credentials():
            print("Credentials check passed: ~/.kaggle/kaggle.json file exists.")
        else:
            raise Exception("Credentials not set up for kaggle. For instructions see \nhttps://github.com/Kaggle/kaggle-api")
        
        # Get data
        # Assumes url is of the form .*kaggle.com/author/datasetName
        basesite = "kaggle.com/"
        datasetUrlIndex = url.find(basesite) + len(basesite)
        dataset_identifier = url[datasetUrlIndex:]

        kaggleCommand = f"kaggle datasets download -p {self.data_dir} {dataset_identifier}"

        os.system(kaggleCommand)



        # $ kg dataset -u <username> -p <password> -o <owner> -d <dataset>
        # https://www.kaggle.com/mohansacharya/graduate-admissions
        # kaggle datasets download -d mohansacharya/graduate-admissions
        # checking kaggle cli documentation