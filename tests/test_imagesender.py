from mavimage.imagesender import ImageSender
import pytest
from pytest_mock import mocker
from unittest.mock import call
from mavimage.gps import GPSRecord
from mavimage.image import Image
import PIL
from datetime import datetime
from mavimage.chunkedbytes import ChunkedBytes
import math

class MockMav:
    """Mock the mav class to mock pushing handlers and calling a timer
    for data requests
    """
    def __init__(self):
        self.handlers = {}

    def push_handler(self, message, function):
        self.handlers[message] = function

    def data_request_send(self, packets, received):
        """Fake data_request_send
        """
        self.push_handler("DATA_REQUEST", self.data_request_send)

    def data_transmission_handshake_send(self, type, size, width, height, packets, payload, jpg_quality,
                                         force_mavlink1=False):
        """


        type                      : type of requested/acknowledged data (as defined in ENUM DATA_TYPES in mavlink/include/mavlink_types.h) (uint8_t)
        size                      : total data size in bytes (set on ACK only) (uint32_t)
        width                     : Width of a matrix or image (uint16_t)
        height                    : Height of a matrix or image (uint16_t)
        packets                   : number of packets beeing sent (set on ACK only) (uint16_t)
        payload                   : payload size per packet (normally 253 byte, see DATA field size in message ENCAPSULATED_DATA) (set on ACK only) (uint8_t)
        jpg_quality               : JPEG quality out of [1,100] (uint8_t)

        """
        pass

    def encapsulated_data_send(self, seqnr, data, force_mavlink1=False):
        """


        seqnr                     : sequence number (starting with 0 on every transmission) (uint16_t)
        data                      : image data bytes (uint8_t)

        """
        pass


def test_send():
    im = PIL.Image.new('L', (4, 4))
    date = datetime(2018, 2, 9, 13, 21, 30)
    gps = GPSRecord(date, -40, 100, -100)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('webp')
    chunk = ChunkedBytes(image_bytes, math.ceil(len(image_bytes) / 4))
    image_sender = ImageSender()
    mav = MockMav()
    image_sender.send(mav, chunk)