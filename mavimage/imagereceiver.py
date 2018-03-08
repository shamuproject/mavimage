from multiprocessing import Lock
from .chunkedbytes import ChunkedBytes
from pymavlink import mavutil


class ImageReceiver:
    """ImageReceiver class
    Attributes:
        mavlink: MAVLinkConnection
        image: ChunkedBytes
        received_chunks: int
    """
    def __init__(self):
         self._received_chunks = []
         self._mutex = Lock()
         self._image = ChunkedBytes(None, 253)

    def receive(self, mavlink):
        # mavlink: MavLinkConnection, image:Image
        self.register_handlers(mavlink)

    def register_handlers(self, mavlink):
        # mavlink: MavLinkConnection
        with self._mutex:
            mavlink.push_handler('DATA_TRANSMISSION_HANDSHAKE', self.data_transmission_handshake_handler)
            mavlink.push_handler('ENCAPSULATED_DATA', self.encapsulated_data_handler)

    def data_transmission_handshake_handler(self, mavlink, message):
        # mavlink: MavLinkConnection, message: MAVLink_data_transmission_handshake_message
        self.total_size = message.size
        # may be unnecessary
        self.payload = message.payload
        self.packets = message.packets

    def encapsulated_data_handler(self, mavlink, message):
        # mavlink: MAVLinkConnection, message: MAVLink_encapsulated_data_message
        # handle receiving encapsulated data bytes, put into chunkedbytes
        self._received_chunks.append(message.seqnr)
        if self._image.flat() == None:
            self._image._bytes_item = message.data
        else:
            self._image = self._image + message.data
            if message.seqnr % 127 == 0:
                self._data_ack_register(mavlink, self._received_chunks)

    def _data_ack_register(self, mavlink, received):
        mavlink.mav.data_ack_send(127, received)


