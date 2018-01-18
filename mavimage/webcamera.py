from SimpleCV import Camera
"""
WebCamera class to be inherited by Camera class

"""

class WebCamera:

    def __init__(self, width, height, gps, webcamera):
        # width, height, gps:GPS, webcamera:VideoCapture.device
        super().__init__(gps)
        self._webcamera = Camera()

    def take_picture(self):
        img = self._webcamera.getImage()

