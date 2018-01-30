#import picamera

from .camera import Camera
import io
import time
from PIL import Image
'''
Class RPI Camera to be inherited by class Camera
Attributes: width
height
gps:GPS
piCamera:PiCamera
'''

class RPiCamera(Camera):

    def __init__(self, picamera, gps):
        # width, height, gps:GPS, picamera:PiCamera
        #super().__init__(gps)
        #self._picamera = picamera.PiCamera()
        pass

    def take_picture(self):
        #stream = io.BytesIO()
        #with self._picamera as camera:
         #   camera.start_preview()
          #  time.sleep(2)
           # camera.capture(stream, format='jpeg')
        #stream.seek(0)
        #image = Image.open(stream)
        #return image
        pass
