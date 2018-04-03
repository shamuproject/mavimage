"""Image Receiving protocol:
Call receive function.
Send Data Transmission handshake to UAV
Wait for response data transmission handshake with packets and size
Receive Encapsulated Data packets
Wait desired time and send a data request for the missing packets
"""

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
        """Initialize image receiver class. Add a wait time for the timer and initialize the
        image class and received chunks to empty
        Args:
            wait_time: seconds
        """
        self._received_chunks = []
        self._mutex = Lock()
        self._image = ChunkedBytes(None, 253)
        self._wait_time = wait_time

    def receive(self, mavlink):
        """receive image packets from mavConn. send data transmission handshake
        Args:
            mavlink: MavLinkConnection
            image: Image
        """
        self.register_handlers(mavlink)
        mavlink.data_transmission_handshake_send(type="MAVLINK_DATA_STREAM_IMG_JPEG",
                                                 size=0, width=0, height=0, packets=0,
                                                 payload=0, jpg_quality=0, force_mavlink1=False)

    def register_handlers(self, mavlink):
        """Push handlers with a lock so that they're received
        Args:
            mavlink: MavLinkConnection
        """
        with self._mutex:
            mavlink.push_handler('DATA_TRANSMISSION_HANDSHAKE',
                                 self.data_transmission_handshake_handler)
            mavlink.push_handler('ENCAPSULATED_DATA', self.encapsulated_data_handler)

    def data_transmission_handshake_handler(self, mavlink, message):
        """Receive info about the size of the message and number of expected packets
        Args:
            mavlink: MavLinkConnection, message: MAVLink_data_transmission_handshake_message
        """
        self.total_size = message.size
        self.payload = message.payload
        self.packets = message.packets

    def encapsulated_data_handler(self, mavlink, message):
        """handle receiving encapsulated data bytes, put into chunkedbytes
        timer for few seconds -- then send request for packets don't have
        recursively erase received packets
        Args:
            mavlink: MAVLinkConnection,
            message: MAVLink_encapsulated_data_message
        """
        self._received_chunks.append(message.seqnr)
        if self._image.flat() is None:
            self._image._bytes_item = message.data
        else:
            self._image + message.data
        mavlink.add_timer(self._wait_time, self._data_request)

    def _data_request(self, mavlink):
        """Request missing packets by checking received packets
        Args:
            mavlink: MAVLinkConnection,
        """
        missing = []
        for i in range(0, self.packets):
            missing.append(i)
        for i in range(0, self.packets):
            if i in self._received_chunks:
                missing.remove(i)
        if missing:
            mavlink.data_request_send(len(missing), missing)

