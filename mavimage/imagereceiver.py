from multiprocessing import Lock
from .chunkedbytes import ChunkedBytes

class ImageReceiver:
    """ImageReceiver class
    Attributes:
        mavlink: MAVLinkConnection
        image: ChunkedBytes
        received_chunks: int
    """
    def __init__(self, wait_time=5):
         self._received_chunks = []
         self._mutex = Lock()
         self._image = ChunkedBytes(None, 253)
         self._wait_time = wait_time

    def receive(self, mavlink):
        """Args:
            mavlink: MavLinkConnection
            image: Image
        """
        self.register_handlers(mavlink)
        mavlink.data_transmission_handshake_send(type="MAVLINK_DATA_STREAM_IMG_JPEG", size=0, width=0, height=0, packets=0, payload=0, jpg_quality=0, force_mavlink1=False)

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

        # timer for few seconds -- then send request for packets don't have
        # recursively erase received packets
        mavlink.add_timer(5, self._data_ack)
        self._received_chunks.append(message.seqnr)
        if self._image.flat() == None:
            self._image._bytes_item = message.data
        else:
            self._image + message.data

    def _data_ack(self, mavlink, received):
        sorted_received = sorted(received)
        missing = []
        j = 0
        for i in range(1,self.packets):
            if sorted_received[i-1] != j:
                missing.append(received[i-1])
            else:
                j = j+1
        mavlink.data_ack_send(len(missing), missing)

