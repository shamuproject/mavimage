from .imagewriter import ImageWriter
"""
JPEGWriter class
Attributes:
    path_format: str
"""


class JPEGWriter(ImageWriter):

    def __init__(self, path_format):
        super().__init__(path_format)

    def write(self, image):
        image.save(self.path, given_format="jpeg")
