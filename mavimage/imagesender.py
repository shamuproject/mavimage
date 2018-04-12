from threading import Lock
'''
ImageSender class
Attributes:
    mavlink:MavLinkConnection
    image:ChunkedBytes
    acknowledged_chunks: bool
'''

class ImageSender:

    def __init__(self):
        """Initialize image receiver class. Add a wait time for the timer and initialize the
        image class and received chunks to empty
        """
        self._received_chunks = []
        self._mutex = Lock()

    def send(self, mavlink, image):
        # mavlink:MavLinkConnection, image:ChunkedBytes
        self.packets = len(image)
        self.size = len(image.flat())
        self._image = image
        self.register_handlers(mavlink)

    def register_handlers(self, mavlink):
        pass
        # mavlink:MavLinkConnection
        with self._mutex:
            mavlink.push_handler('DATA_TRANSMISSION_HANDSHAKE',
                                 self.data_transmission_handshake_handler)
            mavlink.push_handler('DATA_REQUEST',
                                 self.data_request_handler)

    def data_transmission_handshake_handler(self, mavlink, message):
        # mavlink:MavLinkConnection, message:MavLink_data_transmission_handshake_message
        mavlink.data_transmission_handshake_send(type="MAVLINK_DATA_STREAM_IMG_JPEG",
                                                 size=self.size, width=message.width, height=message.height,
                                                 packets=self.packets,
                                                 payload=253, jpg_quality=100, force_mavlink1=False)

    def data_request_handler(self, mavlink, message):
        #mavlink:MAVLinkConnection, message:MAVLink_data_ack_message
        missing = message.missing
        self._send_packets(mavlink, missing)

    def _send_packets(self, mavlink, missing):
        for i in missing:
            mavlink.encapsulated_data_send(i, self._image[i])

