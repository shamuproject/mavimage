import webp
'''
ImageReceiver class
Attributes:
    mavlink: MAVLinkConnection
    image: ChunkedBytes
    received_chunks: int
'''

class ImageReceiver:

    def __init__(self, _mavlink, _image, _received_chunks):
        # mavlink: MavLinkConnection, image: ChunkedBytes, received_chunks: int

    def receive(self, mavlink, image):
        # mavlink: MavLinkConnection, image:Image

    def register_handlers(self, mavlink):
        # mavlink: MavLinkConnection

    def data_transmission_handshake_handler(self, mavlink, message):
        # mavlink: MavLinkConnection, message: MAVLink_data_transmission_handshake_massge
        value = True
        # value: bool
        return value

    def encapsulated_data_handler(self, mavlink, message):
        # mavlink: MAVLinkConnection, message: MAVLink_encapsulated_data_message
        value = True
        # value: bool
        return value