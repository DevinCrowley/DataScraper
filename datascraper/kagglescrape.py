import requests
import zipfile
import numpy as np
from datascraper.abcscrape import ABCScraper
from pathlib import Path
import os
import re


class KaggleScraper(ABCScraper):
    def __init__(self):
        super().__init__()
        self._data_source = "kaggle"
        print("end of kaggle_init")

    def check_credentials(self):
        """
        check if credentials exist in the home directory.
        """
        if (Path.home() / ".kaggle/kaggle.json").exists():
            return True
        else:
            return False

    def download_to_zip(self, url):

        # Check credentials
        if self.check_credentials():
            print("Credentials check passed: ~/.kaggle/kaggle.json file exists.")
        else:
            raise Exception(
                "Credentials not set up for kaggle. For instructions see \nhttps://github.com/Kaggle/kaggle-api"
            )

        # Get data
        # Assumes url is of the form .*kaggle.com/author/datasetName
        basesite = "kaggle.com/"
        datasetUrlIndex = url.find(basesite) + len(basesite)
        dataset_identifier = url[datasetUrlIndex:]
        slashIndex = dataset_identifier.find("/")
        datasetName = dataset_identifier[slashIndex + 1 :]

        kaggleCommand = (
            f"kaggle datasets download -p {self.data_dir} {dataset_identifier}"
        )
        print(f"saving data into {self._data_dir}")
        os.system(kaggleCommand)

        return datasetName

    def extract_zip(self, datasetName):

        # make output directory if it doesn't exist.
        p = Path(self.data_dir) / datasetName
        p.mkdir(exist_ok=True)

        # check if directory is empty. If it is,
        # unzip the file into output directory.
        if (
            list(p.glob("*")) == []
        ):  # TODO: make sure that on one-file downloads it deals with no zipping
            with zipfile.ZipFile(str(p) + ".zip") as zip_ref:
                zip_ref.extractall(datasetName + ".zip", path=str(p))  # TODO: broken

        # remove zip file
        os.remove(Path(self.data_dir) / (datasetName + ".zip"))

    def get_data(self, url):

        datasetName = self.download_to_zip(url)

        self.extract_zip(datasetName)

        # data = gimme.now(plz) # thanks

        # return data

        # $ kg dataset -u <username> -p <password> -o <owner> -d <dataset>
        # https://www.kaggle.com/mohansacharya/graduate-admissions
        # kaggle datasets download -d mohansacharya/graduate-admissions
        # checking kaggle cli documentation
