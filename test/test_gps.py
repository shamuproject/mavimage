from .gps import GPS

mavlink = 1.0

def test_initialization():

    test_mav = GPS(mavlink)
    assert(test_mav.connection == 1.0)