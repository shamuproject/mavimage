from mavimage.image import Image
from mavimage.gps import GPS, GPSRecord
import pytest
from pytest_mock import mocker
import PIL.Image
from datetime import datetime


def test_init():
    im = PIL.Image.new('L', (3, 3))
    gps = GPSRecord(1, 1, 1, 1)
    new_image = Image(im, gps)
    assert (new_image._image == im)
    assert (new_image._gps == gps)

"""def test_to_bytes():
    im = PIL.Image.new('L', (3, 3))
    time = datetime(1, 1, 1, 1, 1, 1)
    gps = GPSRecord(time, 1, 1, 100)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('WebP')
    assert (type(image_bytes) == bytes)
"""

def test_from_bytes():
    im = PIL.Image.new('L', (4, 4))
    time = datetime(1, 1, 1, 1, 1, 1)
    gps = GPSRecord(time, 1000, 1000, 1000)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('jpeg')
    image_from_byte = new_image.from_bytes(image_bytes)
    image_compare = image_from_byte.to_bytes('jpeg')
    assert(image_bytes == image_compare)
    assert(image_from_byte._gps.altitude == new_image._gps.altitude)
    assert (image_from_byte._gps.longitude == new_image._gps.longitude)
    assert (image_from_byte._gps.latitude == new_image._gps.latitude)
    assert (image_from_byte._gps.time == new_image._gps.time)


