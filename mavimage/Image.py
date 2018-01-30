from PIL import Image
'''
Image class.
Attributes:
    image:PIL.Image
    gps:GPSRecord
'''

class Image:

    def __init__(self, image=None, gps=None):
        # image: PIL.Image, gps:GPSRecord

    def from_bytes(self, bytes, format=None):

    def to_bytes(self, format=None):
        return bytes

    def save(self, fp, format=None):

    def gps_to_exif(self, gps_record):
        # gps_record: GPSRecord
        return dict

    def exif_to_gps(self, exif):
        # exif: dict
        return GPSRecord