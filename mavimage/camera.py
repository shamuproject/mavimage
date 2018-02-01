from abc import ABCMeta
from abc import abstractmethod

"""
Camera class. Capture image
Attributes: gps:GPS
"""

class Camera(object, metaclass=ABCMeta):

    def __init__(self, gps):
        """store gps:GPS"""
        self._gps = gps
        super().__init__()

    @abstractmethod
    def take_picture(self):
        """abstract method to capture image"""
        pass

