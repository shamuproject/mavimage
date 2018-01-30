from mavimage.camera import Camera
from mavimage.rpicamera import RPiCamera
import imghdr

def test_image():
    image = RPiCamera.take_picture()
    image_type = imghdr.what(image)
    assert (image_type == 'jpeg')