"""
ImageWriter class
Attributes:
    path_format: str
"""


class ImageWriter:

    def __init__(self, path_format):
        self.path = path_format

    def write(self, image):
        image.save(self.path, given_format="jpeg")