from mavimage.image import Image
from mavimage.gps import GPS, GPSRecord
import pytest
from pytest_mock import mocker
import PIL.Image


def test_init():
    im = PIL.Image.new('L', (3, 3))
    gps = GPSRecord(1, 1, 1, 1)
    new_image = Image(im, gps)
    assert (new_image._image == im)
    assert (new_image._gps == gps)

    