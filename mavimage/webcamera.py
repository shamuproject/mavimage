from SimpleCV import Camera
"""
WebCamera class to be inherited by Camera class

"""

class WebCamera(Camera):

    def __init__(self, webcamera, gps):
        # width, height, gps:GPS, webcamera:VideoCapture.device
        super().__init__(gps)
        self._webcamera = Camera()

    def take_picture(self):
        img = self._webcamera.getImage()
        return img



