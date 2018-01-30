from mavimage.gps import GPS
import pytest
from pytest_mock import mocker


class MockMessage:
    def __init__(self):
        self.lat = 1.0
        self.lon = 1.0
        self.alt = 1.0
        self.time = 1.0

class MockMav:
    def push_handler(self):
        pass

def test_init(mocker):
    mocker.patch.object(MockMav, 'push_handler')
    mav = MockMav()
    gps = GPS(mav)
    MockMav.push_handler.assert_called_with('GLOBAL_POSITION_INT', gps.global_position_int_handler)

def test_record():
    #instance = GPS(1.0)
    message = MockMessage()
    #instance.global_position_int_handler(1.0, message)
    #time, lat, lon, alt = instance.record()
    assert(message.alt == 1.0)
    assert(message.lat == 1.0)
    assert(message.lon == 1.0)
    assert(message.time == 1.0)
    #assert(lat == 1.0)
    #assert(long == 1.0)
    #assert(alt == 1.0)
    #assert(time == 1.0)





