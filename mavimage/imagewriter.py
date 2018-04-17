from abc import ABCMeta
from abc import abstractmethod
"""
ImageWriter class
Attributes:
    path_format: str
"""


class ImageWriter(object, metaclass=ABCMeta):

    def __init__(self, path_format):
        self.path = path_format

    @abstractmethod
    def write(self, image):
        pass
