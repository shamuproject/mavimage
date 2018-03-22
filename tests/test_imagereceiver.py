from mavimage.imagereceiver import ImageReceiver
import pytest
from pytest_mock import mocker
from unittest.mock import call
import time

class Message_DataTrans:
    def __init__(self):
        self.size = 253
        self.payload = 253
        self.packets = 1

class Message_DataTrans2:
    def __init__(self):
        self.size = 253
        self.payload = 253
        self.packets = 3

class Message_EncapData:
    def __init__(self):
        self.seqnr = 0
        self.data = b'abc'

class Message_EncapData2:
    def __init__(self):
        self.seqnr = 1
        self.data = b'abc'

class Message_EncapData3:
    def __init__(self):
        self.seqnr = 2
        self.data = b'abc'

class MockMav:
    def __init__(self):
        self.handlers = {}

    def push_handler(self, message, function):
        self.handlers[message] = function

    def data_ack_send(self, packets, received):
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
        time.sleep(period)
        function(self)

def test_init():
    test_receiver = ImageReceiver()
    assert test_receiver._received_chunks == []
    assert test_receiver._image._chunk_size == 253

def test_receive(mocker):
    mocker.patch.object(MockMav, 'push_handler')
    test_receiver = ImageReceiver()
    mav = MockMav()
    test_receiver.receive(mav)
    calls = [call('DATA_TRANSMISSION_HANDSHAKE', test_receiver.data_transmission_handshake_handler), call('ENCAPSULATED_DATA', test_receiver.encapsulated_data_handler)]
    MockMav.push_handler.assert_has_calls(calls, any_order=True)

def test_data_transmission_handshake_handler():
    mav = MockMav()
    receiver = ImageReceiver()
    message = Message_DataTrans()
    receiver.data_transmission_handshake_handler(mav, message)
    assert receiver.total_size == 253
    assert receiver.payload == 253
    assert receiver.packets == 1

def test_encapsulated_data_handler():
    mav = MockMav()
    receiver = ImageReceiver()
    messageinfo = Message_DataTrans2()
    receiver.data_transmission_handshake_handler(mav, messageinfo)
    message1 = Message_EncapData()
    message2 = Message_EncapData2()
    message3 = Message_EncapData3()
    receiver.encapsulated_data_handler(mav, message1)
    receiver.encapsulated_data_handler(mav, message2)
    receiver.encapsulated_data_handler(mav, message3)
    assert receiver._image.flat() == b'abcabcabc'
    assert 0 in receiver._received_chunks
    assert 1 in receiver._received_chunks
    assert 2 in receiver._received_chunks

def test_data_ack(mocker):
    mav = MockMav()
    mocker.patch.object(MockMav, 'data_ack_send')
    receiver = ImageReceiver()
    messageinfo = Message_DataTrans2()
    receiver.data_transmission_handshake_handler(mav, messageinfo)
    message1 = Message_EncapData()
    receiver.encapsulated_data_handler(mav, message1)
    assert receiver._image.flat() == b'abc'
    assert 0 in receiver._received_chunks
    MockMav.data_ack_send.assert_called_with(2, [1,2])

    mav = MockMav()
    mocker.patch.object(MockMav, 'data_ack_send')
    receiver = ImageReceiver()
    messageinfo = Message_DataTrans2()
    receiver.data_transmission_handshake_handler(mav, messageinfo)
    message1 = Message_EncapData()
    message2 = Message_EncapData2()
    receiver.encapsulated_data_handler(mav, message1)
    receiver.encapsulated_data_handler(mav, message2)
    assert receiver.packets == 3
    assert receiver._image.flat() == b'abcabc'
    assert 0 in receiver._received_chunks
    assert 1 in receiver._received_chunks
    MockMav.data_ack_send.assert_has_calls([call(1, [2]), call(2, [1,2])], any_order=True)
