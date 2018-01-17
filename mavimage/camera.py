from abc import ABCMeta
from abc import abstractmethod

'''
Camera class. Capture image
Attributes: width, height, gps:GPS
'''

class Camera(object, metaclass=ABCMeta):

    def __init__(self, gps):
        # gps:GPS
        self._gps = gps

    @abstractmethod
    def take_picture(self):
        # capture image
        pass

