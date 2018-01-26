from mavimage.gps import GPS
import pytest

mavlink = 1.0


class Message:
    def __init__(self):
        self.lat = 1.0
        self.lon = 1.0
        self.alt = 1.0
        self.time_boot_ms = 1.0

def test_init():
    instance = GPS(mavlink)
    assert(instance.connection == 1.0)

def test_record():
    instance = GPS(mavlink)
    message = Message
    instance.global_position_int_handler(mavlink, message)
    time, lat, lon, alt = instance.record()
    assert(message.alt == 1.0)
    assert(message.lat == 1.0)
    assert (message.lon == 1.0)
    assert (message.time_boot_ms == 1.0)
    assert (lat == 1.0)
    assert (long == 1.0)
    assert (alt == 1.0)
    assert (time == 1.0)





