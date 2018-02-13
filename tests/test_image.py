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

def test_to_bytes():
    im = PIL.Image.new('L', (3, 3))
    time = datetime(1, 1, 1, 1, 1, 1)
    gps = GPSRecord(time, 1, 1, 1)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('WebP')
    assert (type(image_bytes) == bytes)


def test_from_bytes():
    im = PIL.Image.new('L', (3, 3))
    time = datetime(1, 1, 1, 1, 1, 1)
    gps = GPSRecord(time, 1, 1, 1)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('WebP')
    image = new_image.from_bytes(image_bytes)



