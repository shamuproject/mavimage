from mavimage.imagereceiver import ImageReceiver
import pytest
from pytest_mock import mocker

class Message_DataTrans:
    def __init__(self):
        self.size = 253
        self.payload = 253
        self.packets = 1

class Message_EncapData:
    def __init__(self):
        self.seqnr = 0
        self.data = []

class MockMav:
    def push_handler(self, message, function):
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
    MockMav.push_handler.assert_called_with('DATA_TRANSMISSION_HANDSHAKE', test_receiver.data_transmission_handshake_handler)
    MockMav.push_handler.assert_called_with('ENCAPSULATED_DATA', test_receiver.encapsulated_data_handler)


    
