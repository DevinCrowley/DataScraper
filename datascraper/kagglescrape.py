import requests
import zipfile
import numpy as np
import sys

from .abcscrape import ABCScraper
from pathlib import Path
import os
import re
import sys


class KaggleScraper(ABCScraper):
    def __init__(self):
        super().__init__()
        self._data_source = "kaggle"

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
                zip_ref.extractall(path=str(p))  # TODO: broken

        # remove zip file
        os.remove(Path(self.data_dir) / (datasetName + ".zip"))

    def get_data(self, url):

        datasetName = self.download_to_zip(url)

        self.extract_zip(datasetName)

        # lowest_dir directly holds the data files.
        lowest_dir = Path(self.data_dir) / datasetName

        # output will be a list that get_data() returns of the form [(data1, columns1), (data2, columns2), ...]
        output = []

        # loop over all of the files in the directory we just made,
        # and append a tuple of (data, columns) to output on each loop.
        for file in lowest_dir.iterdir():
            if not file.is_file():
                continue

            suffix = file.suffix

            if suffix == ".csv":
                data = np.loadtxt(file, delimiter=",", skiprows=1)
                with file.open() as openFile:
                    columns = openFile.readline().split(",")
                output.append((data, columns))
            else:
                raise NotImplementedError(f"File type {suffix} not yet implemented.")
        # output list populated

        # output is the list [(data1, columns1), (data2, columns2), ...]
        return output

        # $ kg dataset -u <username> -p <password> -o <owner> -d <dataset>
        # https://www.kaggle.com/mohansacharya/graduate-admissions
        # kaggle datasets download -d mohansacharya/graduate-admissions
        # checking kaggle cli documentation


def main():
    url = sys.argv[1]
    k = KaggleScraper()
    output = k.get_data(url)

    print(output[0][1])
    for i in range(10):
        print(output[0][0][i])


if __name__ == "__main__":
    main()
