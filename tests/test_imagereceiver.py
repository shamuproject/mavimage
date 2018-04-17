"""Test image receiver by having messages sent, not sent, and seeing how data request reacts
"""
from mavimage.imagereceiver import ImageReceiver
import pytest
from pytest_mock import mocker
from unittest.mock import call
from mavimage.gps import GPSRecord
from mavimage.image import Image
import PIL
from datetime import datetime
from mavimage.chunkedbytes import ChunkedBytes
import math
import threading
import time

class Message_DataTrans:
    """Define a test data transmission handshake
    """
    def __init__(self):
        self.size = 253
        self.payload = 253
        self.packets = 23

class Message_DataTrans2:
    """Define a test data transmission handshake that we will send messages with
    """
    def __init__(self):
        self.size = 253
        self.payload = 253
        self.packets = 3

class Message_ImageTrans:
    """Define a test data transmission handshake that we will send messages with
    """
    def __init__(self):
        self.size = 253
        self.payload = 253
        self.packets = 2

im = PIL.Image.new('L', (4, 4))
date = datetime(2018, 2, 9, 13, 21, 30)
gps = GPSRecord(date, -40, 100, -100)
new_image = Image(im, gps)
image_bytes = new_image.to_bytes('webp')
chunk = ChunkedBytes(image_bytes, math.ceil(len(image_bytes)/2))


class Message_Image1:
    """Make an image by setting chunk size to half of the image and sending the image in two pieces
    """
    def __init__(self):
        self.seqnr = 0
        self.data = chunk[0]

class Message_Image2:
    def __init__(self):
        self.seqnr = 1
        self.data = chunk[1]

class Message_EncapData:
    """Test message1
    """
    def __init__(self):
        self.seqnr = 0
        self.data = b'abc'

class Message_EncapData2:
    """Test message2
    """
    def __init__(self):
        self.seqnr = 1
        self.data = b'abc'

class Message_EncapData3:
    """Test message3
    """
    def __init__(self):
        self.seqnr = 2
        self.data = b'abb'

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
        self.push_handler("DATA_ACK", self.data_ack_send)

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

    def add_timer(self, period, function):
        """Add a fake timer using threading so the code continues running but calls
        with the timer in the background
        """
        thread = threading.Thread(target=self.timer_helper, args=(period, function))
        thread.daemon = True
        thread.start()

    def timer_helper(self, period, function):
        """the actual timer
        """
        time.sleep(period)
        function(self)

def test_init():
    """Test initialization
    """
    test_receiver = ImageReceiver()
    assert test_receiver._received_chunks == []
    assert test_receiver._image._chunk_size == 253

def test_receive(mocker):
    """Test receive. Make sure handlers get pushed
    """
    mocker.patch.object(MockMav, 'push_handler')
    test_receiver = ImageReceiver()
    mav = MockMav()
    test_receiver.receive(mav)
    calls = [call('DATA_TRANSMISSION_HANDSHAKE', test_receiver.data_transmission_handshake_handler), call('ENCAPSULATED_DATA', test_receiver.encapsulated_data_handler)]
    MockMav.push_handler.assert_has_calls(calls, any_order=True)

def test_data_transmission_handshake_handler():
    """Test receiving packet numbers from data transmission handshake
    """
    mav = MockMav()
    receiver = ImageReceiver()
    message = Message_DataTrans()
    receiver.data_transmission_handshake_handler(mav, message)
    assert receiver.total_size == 253
    assert receiver.payload == 253
    assert receiver.packets == 23

def test_encapsulated_data_handler(mocker):
    """Test receiving all packets and make sure data_request is not called
    """
    mav = MockMav()
    mocker.patch.object(MockMav, 'data_request_send')
    receiver = ImageReceiver()
    messageinfo = Message_DataTrans2()
    receiver.data_transmission_handshake_handler(mav, messageinfo)
    message1 = Message_EncapData()
    message2 = Message_EncapData2()
    message3 = Message_EncapData3()
    receiver.encapsulated_data_handler(mav, message1)
    receiver.encapsulated_data_handler(mav, message2)
    receiver.encapsulated_data_handler(mav, message3)
    assert receiver._image.flat() == b'abcabcabb'
    assert 0 in receiver._received_chunks
    assert 1 in receiver._received_chunks
    assert 2 in receiver._received_chunks
    assert not MockMav.data_request_send.called, 'data_request_ send should not be called'

def test_data_request(mocker):
    """Testing receiving only one out of three packets. Has to wait 5 seconds to allow timer to catch up and
    request the packets
    """
    mav = MockMav()
    mocker.patch.object(MockMav, 'data_request_send')
    receiver = ImageReceiver()
    messageinfo = Message_DataTrans2()
    receiver.data_transmission_handshake_handler(mav, messageinfo)
    message1 = Message_EncapData()
    receiver.encapsulated_data_handler(mav, message1)
    time.sleep(5)
    assert receiver._image.flat() == b'abc'
    assert 0 in receiver._received_chunks

def test_data_request_respond(mocker):
    """Test sending two packets. Make sure the program requests the final packet
    Send the final packet then make sure data_request is not called again
    Make sure all packets received and placed in Image object
    """
    mav = MockMav()
    mocker.patch.object(MockMav, 'data_request_send')
    receiver = ImageReceiver()
    messageinfo = Message_DataTrans2()
    receiver.data_transmission_handshake_handler(mav, messageinfo)
    message1 = Message_EncapData()
    message2 = Message_EncapData2()
    message3 = Message_EncapData3()
    receiver.encapsulated_data_handler(mav, message1)
    receiver.encapsulated_data_handler(mav, message2)
    time.sleep(5)
    assert receiver.packets == 3
    assert receiver._image.flat() == b'abcabc'
    assert 0 in receiver._received_chunks
    assert 1 in receiver._received_chunks
    receiver.encapsulated_data_handler(mav, message3)
    assert receiver._image.flat() == b'abcabcabb'

def test_send_image():
    """Assert that can send an image. Check that the image sent in two chunks creates the full image
    """
    mav = MockMav()
    receiver = ImageReceiver()
    messageinfo = Message_ImageTrans()
    message1 = Message_Image1()
    message2 = Message_Image2()
    receiver.data_transmission_handshake_handler(mav, messageinfo)
    receiver.encapsulated_data_handler(mav, message1)
    receiver.encapsulated_data_handler(mav, message2)
    time.sleep(5)
    assert receiver.packets == 2
    assert receiver._image.flat() == image_bytes

