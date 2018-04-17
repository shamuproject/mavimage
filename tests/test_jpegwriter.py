import pytest
import unittest
from mavimage.jpegwriter import JPEGWriter
from mavimage.imagewriter import ImageWriter
from mavimage.image import Image
import PIL
from datetime import datetime
from mavimage.gps import GPSRecord
import os

def test_writer():
    cwd = os.getcwd()
    writer = JPEGWriter(cwd)
    im = PIL.Image.new('L', (16, 16))
    time = datetime(2018, 2, 9, 13, 21, 30)
    gps = GPSRecord(time, -40.15, 100.2, -100)
    image = Image(im, gps)
    writer.write(image)
    assert PIL.Image.open('{}/02-09-2018-13-21-30.jpeg'.format(cwd))


