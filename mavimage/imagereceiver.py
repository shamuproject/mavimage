from multiprocessing import Lock
from .chunkedbytes import ChunkedBytes

class ImageReceiver:
    """ImageReceiver class
    Attributes:
        mavlink: MAVLinkConnection
        image: ChunkedBytes
        received_chunks: int
    """
    def __init__(self, _image, _received_chunks):
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
        # mavlink: MavLinkConnection, message: MAVLink_data_transmission_handshake_massge
        self.total_size = message.size
        # may be unnecessary
        self.payload = message.payload
        self.packets = message.packets

    def encapsulated_data_handler(self, mavlink, message):
        # mavlink: MAVLinkConnection, message: MAVLink_encapsulated_data_message
        # handle receiving encapsulated data bytes, put into chunkedbytes
        self._received_chunks.append(message.seqnr)
        self._image = self._image + message.data

