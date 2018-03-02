import webp
'''
ImageSender class
Attributes:
    mavlink:MavLinkConnection
    image:ChunkedBytes
    acknowledged_chunks: bool
'''

class ImageSender:

    def send(self, mavlink, image):
        pass
        # mavlink:MavLinkConnection, image:Image

    def register_handlers(self, mavlink):
        pass
        # mavlink:MavLinkConnection

    def data_transmission_handshake_handler(self, mavlink, message):
        # mavlink:MavLinkConnection, message:MavLink_data_transmission_handshake_message
        value = True
        # value: bool
        return value

    def data_ack_handler(self, mavlink, message):
        #mavlink:MAVLinkConnection, message:MAVLink_data_ack_message
        value = True
        # value: bool
        return value
