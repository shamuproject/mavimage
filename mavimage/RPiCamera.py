import picamera
import GPS
'''
Class RPI Camera to be inherited by class Camera
Attributes: width
height
gps:GPS
piCamera:PiCamera
'''

class RPiCamera:

    def __init__(self, width, height, gps, picamera):
        # width, height, gps:GPS, picamera:PiCamera
        self.width = width
        self.height = height
    
