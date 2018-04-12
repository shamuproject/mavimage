"""
Photographer class. 
Attributes: camera:Camera, image_sender:ImageSender, image_writer:ImageWriter
"""

class Photographer:

    def __init__(self, camera, image_sender, image_writer=None):
        """camera: PiCamera, image_sender:ImageSender, image_writer:ImageWriter"""
        self.sender = image_sender
        self.camera = camera
        self.writer = image_writer

    def register_handlers(self, mavlink):
        """Pass mavlink: MAVLinkConnection to call push_handler function"""
        mavlink.push_handler('DATA_TRANSMISSION_HANDSHAKE', self.data_transmission_handshake_handler)

    def data_transmission_handshake_handler(self, mavlink, message):
        """mavlink:MavLinkConnection, message:str"""
        image = self.camera.take_picture()
        self.sender.send(mavlink, image)
        if self.writer:
            self.writer.write(image)






