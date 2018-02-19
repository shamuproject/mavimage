""" test file for image class
"""
from mavimage.image import Image, gps_to_exif, exif_to_gps, deg2dms, dms2deg
from mavimage.gps import GPS, GPSRecord
import pytest
from pytest_mock import mocker
import PIL.Image
from datetime import datetime
import piexif


def test_init():
    """test initialization of Image class
    """
    im = PIL.Image.new('L', (3, 3))
    gps = GPSRecord(1, 1, 1, 1)
    new_image = Image(im, gps)
    assert new_image._image == im
    assert new_image._gps == gps

def test_exif_to_gps():
    """test converting between exif and gps
    """
    time = datetime(2000, 9, 18, 20, 17, 30)
    gps = GPSRecord(time, 40.15, -105.201, 4000)
    gps_compare = exif_to_gps(gps_to_exif(gps))
    assert gps == gps_compare

def test_dms2deg():
    """test converting between dms and degrees
    """
    deg, mins, sec = deg2dms(100.9)
    assert deg == 100 and mins == 54 and sec == 0
    assert dms2deg(70, 16, 18) == 70.27166667
    assert dms2deg(*deg2dms(100)) == 100
    assert dms2deg(*deg2dms(-3.1415)) == -3.1415
    assert dms2deg(*deg2dms(-900)) == -900

def test_from_bytes():
    """test the whole class
    """
    im = PIL.Image.new('L', (4, 4))
    time = datetime(2000, 9, 18, 20, 17, 30)
    gps = GPSRecord(time, 40.15, -105.201, 4000)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('jpeg')
    image_from_byte = new_image.from_bytes(image_bytes)
    image_compare = image_from_byte.to_bytes('jpeg')
    assert image_bytes == image_compare
    assert image_from_byte._gps == new_image._gps

    im = PIL.Image.new('L', (16, 16))
    time = datetime(2018, 2, 9, 13, 21, 30)
    gps = GPSRecord(time, -40, 100, -100)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('webp')
    image_from_byte = new_image.from_bytes(image_bytes)
    image_compare = image_from_byte.to_bytes('webp')
    assert image_bytes == image_compare
    assert image_from_byte._gps == new_image._gps

    im = PIL.Image.new('L', (16, 16))
    time = datetime(2018, 2, 9, 13, 21, 30)
    gps = GPSRecord(time, -40.15, 100.2, -100)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('webp')
    image_from_byte = new_image.from_bytes(image_bytes)
    image_compare = image_from_byte.to_bytes('webp')
    assert image_bytes == image_compare
    assert image_from_byte._gps == new_image._gps



