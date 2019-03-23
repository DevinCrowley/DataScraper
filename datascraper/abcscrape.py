""" Abstract base class file. All other classes should derive from Scraper, and must have all methods defined in it. """

# TODO : Put TODOs at the top of files in this format
# TODO : method describing where data goes once it's got?
# TODO : what other methods do we need in the top-level class?

from abc import ABC
import numpy as np


class ABCScraper(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_data(self, url):
        """Abstract method ~ 
        Return a numpy.ndarray object populated from 
        a known website pointed to by url."""
        pass
