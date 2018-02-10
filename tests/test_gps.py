from mavimage.gps import GPS
import pytest
from pytest_mock import mocker


class MockMessage:
    def __init__(self):
        self.lat = 10000000.0
        self.lon = 10000000.0
        self.alt = 1.0

class MockMav:
    def push_handler(self, message, function):
        pass


def test_init(mocker):
    mocker.patch.object(MockMav, 'push_handler')
    mav = MockMav()
    gps = GPS(mav)
    MockMav.push_handler.assert_called_with('GLOBAL_POSITION_INT', gps.global_position_int_handler)

def test_record():
    """ensure message is retrieved and attributes are stored"""
    mav = MockMav()
    gps = GPS(mav)
    message = MockMessage()
    gps.global_position_int_handler(mav, message)
    assert(gps.alt == 1.0)
    assert(gps.lat == 1.0)
    assert(gps.lon == 1.0)
    #assert(lat == 1.0)
    #assert(long == 1.0)
    #assert(alt == 1.0)
    #assert(time == 1.0)





