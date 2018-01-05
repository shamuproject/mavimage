import picamera

'''
Camera class. Capture image
Attributes: width, height, gps:GPS
'''

class Camera:

    def __init__(self, width, height, gps):
        # gps:GPS
        self.camera = picamera.PiCamera()
        self.width = width
        self.height = height
        self.gps = gps

    def take_picture(self):
        # capture image
        camera = self.camera
        image = camera.capture('image.jpg')
        # image:Image
        return image
