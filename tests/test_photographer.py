from mavimage.photographer import Photographer
from mavimage.imagesender import ImageSender
from mavimage.jpegwriter import JPEGWriter
from mavimage.rpicamera import RPiCamera
from mavimage.gps import GPS
import os
import pytest
import pytest_mock

class Mock_Mav():
    def push_handler(self, message, function):
        pass

    def data_transmission_handshake(self):
        pass

def test_init():
    mav = Mock_Mav()
    cam = None
    gps = GPS(mav)
    camera = RPiCamera(cam, gps)
    writer = JPEGWriter('{}'.format(os.getcwd()))
    sender = ImageSender()
    photo = Photographer(mav, camera, sender, writer)
    assert photo.sender == sender
    assert photo.camera == camera
    assert photo.writer == writer

def test_register(mocker):
    mav = Mock_Mav
    mocker.patch.object(Mock_Mav, 'push_handler')
    mav = Mock_Mav()
    gps = GPS(mav)
    cam = RPiCamera(None, gps)
    camera = RPiCamera(cam, gps)
    writer = JPEGWriter('{}'.format(os.getcwd()))
    sender = ImageSender()
    photo = Photographer(mav, camera, sender, writer)
    Mock_Mav.push_handler.assert_called_with('DATA_TRANSMISSION_HANDSHAKE', photo.data_transmission_handshake_handler)

def test_data_transmission():
    mav = Mock_Mav
    mav = Mock_Mav()
    gps = GPS(mav)
    camera = RPiCamera(None, gps)
    writer = JPEGWriter('{}'.format(os.getcwd()))
    sender = ImageSender()
    photo = Photographer(mav, camera, sender, writer)
    message = None
    photo.data_transmission_handshake_handler(mav, message)
    assert camera.take_picture.called
    assert sender.send.called
    assert writer.writer.called
