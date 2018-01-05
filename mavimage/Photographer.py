from pymavlink import mavutil
'''
Photographer class. 
Attributes: camera:Camera, image_sender:ImageSender, image_writer:ImageWriter
'''

class Photographer:

    def __init__(self, camera, image_sender, image_writer=None):
        # camera: PiCamera, image_sender:ImageSender, image_writer:ImageWriter
        self.image_sender = image_sender
        self.camera = camera

    def register_handlers(self, mavlink):
        #what is this supposed to do?
        # mavlink: MAVLinkConnection
        return mavlink

    def data_transmission_handshake_handler(self, mavlink, message):
        # mavlink:MavLinkConnection, message:str
        # return a bool, True if heartbeat message?
        msg_type = message.get_type()
        if msg_type == "HEARTBEAT":
            return True
        else:
            return False


