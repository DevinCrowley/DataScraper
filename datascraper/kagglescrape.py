import requests
import numpy as np
from abcscrape import ABCScraper
from pathlib import Path


class KaggleScraper(ABCScraper):
    def check_credentials():
        if (Path.home() / ".kaggle").is_dir():
            return True
        else:
            return False

    def get_data(self, url):
        pass
