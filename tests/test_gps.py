from mavimage.gps import GPS

mavlink = 1.0


class Message:
    Message.lat = 1.0
    Message.lon = 1.0
    Message.alt = 1.0
    Message.time_boot_ms = 1.0


def test_global_position_int_handler():
    message = Message
    link = GPS.global_position_int_handler(mavlink, message)
    assert (link.latitude == 1.0)
    assert (link.longitude == 1.0)
    assert (link.altitude == 1.0)
    assert (link.time_boot_ms == 1.0)





