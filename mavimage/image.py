import PIL.Image
import piexif
import io
import math
from .gps import GPSRecord
from datetime import datetime

"""
Image class.
Attributes:
    image:PIL.Image
    gps:GPSRecord
"""


class Image:

    def __init__(self, image=None, gps=None):
        """image: PIL.Image, gps:GPSRecord"""
        self._image = image
        self._gps = gps

    @classmethod
    def from_bytes(cls, image_bytes):
        """construct image from bytes into format. bytes string. return Image"""
        """Turn into BytesIO"""
        #stream = io.BytesIO(image_bytes)
        """open the stream """
        image = PIL.Image.open(image_bytes)
        """Extract GPS data image_bytes and convert it to GPSRecord"""
        gps = exif_to_gps(image)
        """Transform into image of format with exif data"""
        return Image(image, gps)


    def to_bytes(self, given_format):
        """construct image to bytes from self.image (PIL.Image). bytes string. Save as BytesIO object"""
        """Create exif from given GPS record"""
        """open image and convert into bytesIO"""
        output = io.BytesIO()
        self.save(output, given_format)
        return output

    def save(self, fp, format):
        """open file object(BytesIO))"""
        gps_dict = gps_to_exif(self._gps)
        gps_bytes = piexif.dump(gps_dict)
        with io.BytesIO() as inputIO:
            self._image.save(inputIO, format)
            inputIO.seek(0)
            byte_image = inputIO.getvalue()
        piexif.insert(gps_bytes, byte_image, fp)

def gps_to_exif(gps_record):
    """gps_record: GPSRecord. Turn GPS record to exif"""
    gps_dict = {}
    gps_dict[piexif.GPSIFD.GPSLongitudeRef] = b'E' if gps_record.longitude >= 0 else b'W'
    gps_dict[piexif.GPSIFD.GPSLongitude] = (
        tuple([float(x).as_integer_ratio() for x in deg2dms(gps_record.longitude)]))
    gps_dict[piexif.GPSIFD.GPSLatitudeRef] = b'N' if gps_record.latitude >= 0 else b'S'
    gps_dict[piexif.GPSIFD.GPSLatitude] = (
        tuple([float(x).as_integer_ratio() for x in deg2dms(gps_record.latitude)]))
    gps_dict[piexif.GPSIFD.GPSAltitudeRef] = 0 if gps_record.altitude >= 0 else 1
    gps_dict[piexif.GPSIFD.GPSAltitude] = abs(gps_record.altitude)
    gps_dict[piexif.GPSIFD.GPSMapDatum] = b'WGS-84'
    gps_dict[piexif.GPSIFD.GPSTimeStamp] = (
        tuple(float(x).as_integer_ratio() for x in (
            [gps_record.time.hour, gps_record.time.minute, gps_record.time.second])))
    gps_dict[piexif.GPSIFD.GPSDateStamp] = gps_record.time.strftime('%Y:%m:%d')
    return gps_dict


def exif_to_gps(exif):
    """"exif: dict. Turn exif to GPS record"""
    all_exif = piexif.load(exif)
    gps_exif = all_exif["GPS"]
    time = datetime.strptime(gps_exif[piexif.GPSIFD.GPSDateStamp], '%Y:%m:%d')
    time.replace(hour=gps_exif[piexif.GPSIFD.GPSTimeStamp[0][0]], minute=(
        gps_exif[piexif.GPSIFD.GPSTimeStamp[1][0]]), second=gps_exif[piexif.GPSIFD.GPSTimeStamp[1][0]])
    sign_lat = -1 if gps_exif[piexif.GPSIFD.GPSLatitudeRef] == b'W' else 1
    latitude = sign_lat * dms2deg(gps_exif[piexif.GPSIFD.GPSLatitude][0][0]/gps_exif[piexif.GPSIFD.GPSLatitude][0][1],
                                  gps_exif[piexif.GPSIFD.GPSLatitude][1][0]/gps_exif[piexif.GPSIFD.GPSLatitude][1][1],
                                  gps_exif[piexif.GPSIFD.GPSLatitude][2][0]/gps_exif[piexif.GPSIFD.GPSLatitude][2][1])
    sign_long = -1 if gps_exif[piexif.GPSIFD.GPSLongitudeRef] == b'S' else 1
    longitude = sign_long * dms2deg(gps_exif[piexif.GPSIFD.GPSLatitude][0][0]/gps_exif[piexif.GPSIFD.GPSLatitude][0][1],
                                    gps_exif[piexif.GPSIFD.GPSLatitude][1][0]/gps_exif[piexif.GPSIFD.GPSLatitude][1][1],
                                    gps_exif[piexif.GPSIFD.GPSLatitude][2][0]/gps_exif[piexif.GPSIFD.GPSLatitude][2][1])
    sign_alt = 1 if gps_exif[piexif.GPSIFD.GPSAltitudeRef] == 0 else -1
    altitude = sign_alt * gps_exif[piexif.GPSIFD.GPSAltitude]
    gps_record = GPSRecord(time, latitude, longitude, altitude)
    return gps_record


def deg2dms(degrees):
    deg = int(abs(degrees))
    minutes = int((degrees-deg)*60)
    sec = math.floor((((degrees - deg)*60)-minutes)*60)
    return deg, minutes, sec


def dms2deg(d, m, s):
    degree = round((s/60+m)/60+d, 8)
    return degree
