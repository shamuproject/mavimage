from SimpleCV import Camera
"""
WebCamera class to be inherited by Camera class

"""

class WebCamera:

    def __init__(self, width, height, gps, webcamera):
        # width, height, gps:GPS, webcamera:VideoCapture.device
        self.width = width
        self.height = height
        self.gps = gps
        webcamera = Camera()
        self.webcamera = webcamera

