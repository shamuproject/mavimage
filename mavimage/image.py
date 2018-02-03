import Pillow
import piexif
import io
"""
Image class.
Attributes:
    image:PIL.Image
    gps:GPSRecord
"""

class Image:

    def __init__(self, image=None, gps=None):
        """image: PIL.Image, gps:GPSRecord"""
        self.gps = gps
        self.image = image

    def from_bytes(self, bytes, format=None):
        """constuct image from bytes into format. bytes string"""
        gps = exif_to_gps(bytes)
        stream = io.BytesIO(bytes)
        image = Pillow.Image.open(stream)
        webp = Pillow.Image.frombytes(image)
        piexif.insert(gps, image)

    def to_bytes(self, format=None):
        """constuct image to bytes from format (webp, jpeg). bytes string"""
        dict = gps_to_exif(self.gps)
        bytes_image = io.BytesIO()
        self.image.save(bytes_image, format=format)
        piexif.insert(dict, bytes_image, bytes)
        return bytes

    def save(self, fp, format=None):
        """save to fp pointer(name or open file object)"""

def gps_to_exif(self, gps_record):
    """gps_record: GPSRecord. Turn GPS record to exif"""
    dict = piexif.dump(gps_record)
    return dict

def exif_to_gps(self, exif):
    """"exif: dict. Turn exif to GPS record"""
    GPSRecord = piexif.load(exif)
    return GPSRecord