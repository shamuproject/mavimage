import picamera

'''
Camera class. Capture image
'''

class Camera:
    def __init__(self, width, height, gps):
        self.camera = picamera.PiCamera()
        self.width = width
        self.height = height
        self.gps = gps

    def take_picture(self):
        camera = self.camera
        image = camera.capture('image.jpg')
        return image
