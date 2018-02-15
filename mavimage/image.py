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
        """construct image from bytes into format. bytes string. return Image
        Turn into BytesIO
        open the stream
        Extract GPS data image_bytes and convert it to GPSRecord
        Transform into image of format with exif data"""
        stream = io.BytesIO(image_bytes)
        image = PIL.Image.open(stream)
        gps = exif_to_gps(image_bytes)
        return Image(image, gps)

    def to_bytes(self, given_format):
        """construct image to bytes from self.image (PIL.Image). bytes string. Save as BytesIO object
        Create exif from given GPS record
        open image and convert into bytesIO"""
        output = io.BytesIO()
        self.save(output, given_format)
        output.seek(0)
        return output.read()

    def save(self, fp, given_format):
        """open file object(BytesIO))"""
        gps_dict = gps_to_exif(self._gps)
        dict_whole = {"0th": {}, "Exif": {}, "GPS": gps_dict,
                      "Interop": {}, "thumbnail": None}
        exif_bytes = piexif.dump(dict_whole)
        self._image.save(fp, format=given_format, exif=exif_bytes)

def gps_to_exif(gps_record):
    """gps_record: GPSRecord. Turn GPS record to exif"""
    gps_dict = {}
    gps_dict[piexif.GPSIFD.GPSLongitudeRef] = b'E' if gps_record.longitude >= 0 else b'W'
    gps_dict[piexif.GPSIFD.GPSLongitude] = (
        tuple([float(x).as_integer_ratio() for x in deg2dms(abs(gps_record.longitude))]))
    gps_dict[piexif.GPSIFD.GPSLatitudeRef] = b'N' if gps_record.latitude >= 0 else b'S'
    gps_dict[piexif.GPSIFD.GPSLatitude] = (
        tuple([float(x).as_integer_ratio() for x in deg2dms(abs(gps_record.latitude))]))
    gps_dict[piexif.GPSIFD.GPSAltitudeRef] = 0 if gps_record.altitude >= 0 else 1
    gps_dict[piexif.GPSIFD.GPSAltitude] = float(abs(gps_record.altitude)).as_integer_ratio()
    gps_dict[piexif.GPSIFD.GPSMapDatum] = b'WGS-84'
    gps_dict[piexif.GPSIFD.GPSTimeStamp] = (
        tuple(float(x).as_integer_ratio() for x in (
            [gps_record.time.hour, gps_record.time.minute, gps_record.time.second])))
    gps_dict[piexif.GPSIFD.GPSDateStamp] = gps_record.time.strftime('%Y:%m:%d')
    return gps_dict


def exif_to_gps(exif):
    """"exif: dict. Turn exif to GPS record"""
    gps_exif = piexif.load(exif)
    gps_exif = gps_exif["GPS"]
    time = datetime.strptime(gps_exif[piexif.GPSIFD.GPSDateStamp].decode("utf-8"), '%Y:%m:%d')
    time = time.replace(hour=gps_exif[piexif.GPSIFD.GPSTimeStamp][0][0], minute=(
        gps_exif[piexif.GPSIFD.GPSTimeStamp][1][0]), second=gps_exif[piexif.GPSIFD.GPSTimeStamp][2][0])
    sign_lat = -1 if gps_exif[piexif.GPSIFD.GPSLatitudeRef] == b'S' else 1
    latitude = sign_lat * dms2deg(gps_exif[piexif.GPSIFD.GPSLatitude][0][0]/gps_exif[piexif.GPSIFD.GPSLatitude][0][1],
                                  gps_exif[piexif.GPSIFD.GPSLatitude][1][0]/gps_exif[piexif.GPSIFD.GPSLatitude][1][1],
                                  gps_exif[piexif.GPSIFD.GPSLatitude][2][0]/gps_exif[piexif.GPSIFD.GPSLatitude][2][1])
    sign_long = -1 if gps_exif[piexif.GPSIFD.GPSLongitudeRef] == b'W' else 1
    longitude = sign_long * dms2deg(gps_exif[piexif.GPSIFD.GPSLongitude][0][0]/gps_exif[piexif.GPSIFD.GPSLongitude][0][1],
                                    gps_exif[piexif.GPSIFD.GPSLongitude][1][0]/gps_exif[piexif.GPSIFD.GPSLongitude][1][1],
                                    gps_exif[piexif.GPSIFD.GPSLongitude][2][0]/gps_exif[piexif.GPSIFD.GPSLongitude][2][1])
    sign_alt = 1 if gps_exif[piexif.GPSIFD.GPSAltitudeRef] == 0 else -1
    altitude = sign_alt * gps_exif[piexif.GPSIFD.GPSAltitude][0]/gps_exif[piexif.GPSIFD.GPSAltitude][1]
    gps_record = GPSRecord(time, latitude, longitude, altitude)
    return gps_record


def deg2dms(degrees):
    deg = int(degrees)
    minutes = int((degrees-deg)*60)
    sec = round(((((degrees - deg)*60)-minutes)*60), 4)
    return deg, minutes, sec


def dms2deg(d, m, s):
    degree = round((s/60+m)/60+d, 8)
    return degree
