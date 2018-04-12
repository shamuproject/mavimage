from .imagewriter import ImageWriter
"""
JPEGWriter class
Attributes:
    path_format: str
"""


class JPEGWriter(ImageWriter):

    def __init__(self, path_format):
        """Initialize JPEG writer
        Args:
            path_format: str
        """
        super().__init__(path_format)

    def write(self, image):
        """write image to file with date
        Args:
            image:Image
        """
        date = image._gps.time.strftime('%m-%d-%Y-%H-%M-%S')
        name = '{}{}{}{}'.format(self.path, '/', date, '.jpeg')
        image.save(name, given_format='jpeg')
