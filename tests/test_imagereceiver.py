from mavimage.imagereceiver import ImageReceiver
import pytest
from pytest_mock import mocker
from unittest.mock import call

class Message_DataTrans:
    def __init__(self):
        self.size = 253
        self.payload = 253
        self.packets = 1

class Message_EncapData:
    def __init__(self):
        self.seqnr = 0
        self.data = b'abc'

class Message_EncapData2:
    def __init__(self):
        self.seqnr = 127
        self.data = b'abc'

class MockMav:
    def __init__(self):
        self.handlers = {}

    def push_handler(self, message, function):
        self.handlers[message] = function

    def data_ack_send(self, packets, received):
        pass

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
    message = Message_EncapData()
    receiver.encapsulated_data_handler(mav, message)
    assert receiver._image.flat() == b'abc'
    assert receiver._received_chunks == [0]

    mav = MockMav()
    message = Message_EncapData2()
    receiver = ImageReceiver()
    receiver.encapsulated_data_handler(mav, message)
    assert receiver._image.flat() == b'abc'
    assert receiver._received_chunks == [127]

    mav = MockMav()
    message = Message_EncapData3()
    receiver = ImageReceiver()
    receiver.encapsulated_data_handler(mav, message)
    mav.handlers["DATA_TRANSMISSION_HANDSHAKE"](mav, message)
    assert receiver._image.flat() == b'abc'
    assert receiver._received_chunks == [0,1]
