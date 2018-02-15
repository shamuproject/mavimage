from mavimage.image import Image, gps_to_exif, exif_to_gps, deg2dms, dms2deg
from mavimage.gps import GPS, GPSRecord
import pytest
from pytest_mock import mocker
import PIL.Image
from datetime import datetime
import piexif


def test_init():
    im = PIL.Image.new('L', (3, 3))
    gps = GPSRecord(1, 1, 1, 1)
    new_image = Image(im, gps)
    assert (new_image._image == im)
    assert (new_image._gps == gps)

def test_from_bytes():
    im = PIL.Image.new('L', (4, 4))
    time = datetime(2000, 9, 18, 20, 17, 30)
    gps = GPSRecord(time, 40.15, -105.201, 4000)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('jpeg')
    image_from_byte = new_image.from_bytes(image_bytes)
    image_compare = image_from_byte.to_bytes('jpeg')
    assert(image_bytes == image_compare)
    assert(image_from_byte._gps.altitude == new_image._gps.altitude)
    assert (image_from_byte._gps.longitude == new_image._gps.longitude)
    assert (image_from_byte._gps.latitude == new_image._gps.latitude)
    assert (image_from_byte._gps.time == new_image._gps.time)

    im = PIL.Image.new('L', (16, 16))
    time = datetime(2018, 2, 9, 13, 21, 30)
    gps = GPSRecord(time, -40, 100, -100)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('jpeg')
    image_from_byte = new_image.from_bytes(image_bytes)
    image_compare = image_from_byte.to_bytes('jpeg')
    assert(image_bytes == image_compare)
    assert(image_from_byte._gps.altitude == new_image._gps.altitude)
    assert (image_from_byte._gps.longitude == new_image._gps.longitude)
    assert (image_from_byte._gps.latitude == new_image._gps.latitude)
    assert (image_from_byte._gps.time == new_image._gps.time)

    im = PIL.Image.new('L', (16, 16))
    time = datetime(2018, 2, 9, 13, 21, 30)
    gps = GPSRecord(time, -40.15, 100.2, -100)
    new_image = Image(im, gps)
    image_bytes = new_image.to_bytes('webp')
    image_from_byte = new_image.from_bytes(image_bytes)
    image_compare = image_from_byte.to_bytes('webp')
    assert(image_bytes == image_compare)
    assert(image_from_byte._gps.altitude == new_image._gps.altitude)
    assert (image_from_byte._gps.longitude == new_image._gps.longitude)
    assert (image_from_byte._gps.latitude == new_image._gps.latitude)
    assert (image_from_byte._gps.time == new_image._gps.time)

def test_exif_to_gps():
    time = datetime(2000, 9, 18, 20, 17, 30)
    gps = GPSRecord(time, 40.15, -105.201, 4000)
    dictionary = gps_to_exif(gps)
    dictionary = piexif.dump(dictionary)
    gps_compare = exif_to_gps(dictionary)
    assert(gps.longitude == gps_compare.longitude)
    assert (gps.latitude == gps_compare.latitude)
    assert (gps.altitude == gps_compare.altitude)
    assert (gps.time == gps_compare.time)

def test_dms2deg():
    degree1 = 100
    degree2 = -3.1415
    degree3 = -900
    d1, m1, s1 = deg2dms(degree1)
    degree1_compare = dms2deg(d1, m1, s1)
    assert (degree1_compare == degree1)
    d2, m2, s2 = deg2dms(degree2)
    degree2_compare = dms2deg(d2, m2, s2)
    assert (degree2_compare == degree2)
    d3, m3, s3 = deg2dms(degree3)
    degree3_compare = dms2deg(d3, m3, s3)
    assert (degree3_compare == degree3)