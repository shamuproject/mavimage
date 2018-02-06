from PIL import Image, ExifTags
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
        self.image = image
        self.gps = gps

    @classmethod
    def from_bytes(image_bytes):
        """construct image from bytes into format. bytes string. return Image"""
        """Turn into BytesIO"""
        stream = io.BytesIO(image_bytes)
        """open the stream """
        image = Image.open(stream)
        """Extract GPS data image_bytes and convert it to GPSRecord"""
        gps_bytes = piexif.load(image.info["exif"])
        gps = exif_to_gps(gps_bytes)
        """Transform into image of format with exif data"""
        # webp = Image.Image.frombytes(image)
        wepb = image.save(file, "WEBP", exif=gps)

    def to_bytes(self):
        """construct image to bytes from format (webp, jpeg). bytes string"""
        """Create exif from given GPS record"""
        gps_record = gps_to_exif(self.gps)
        """open image and convert into bytes"""
        with open(self.image) as image_stream:
            f = image_stream.read()
            b = bytearray(f)
        """Attach exif data"""
        piexif.insert(gps_record, b)
        return b

    def save(self, fp):
        """save to fp pointer(name(string) or open file object(BytesIO))"""
        Image.Image.save(fp, format='WEBP', paramters=self.gps)

def gps_to_exif(self, gps_record):
    """gps_record: GPSRecord. Turn GPS record to exif"""
    dict_record = piexif.dump(gps_record)
    return dict_record

def exif_to_gps(self, exif):
    """"exif: dict. Turn exif to GPS record"""
    gps_record = piexif.load(exif)
    return gps_record
