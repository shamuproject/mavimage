"""Handle Image class and helper functions
Lauren McIntire"""

from fractions import Fraction
from datetime import datetime
import io
import PIL.Image
import piexif
from .gps import GPSRecord


class Image:
    """
    Image class.
    Attributes:
    image:PIL.Image
    gps:GPSRecord
    Manage combining images with GPS coordinates
    can handle JPEG and WebP formats"""

    def __init__(self, image=None, gps=None):
        """image: PIL.Image, gps:GPSRecord"""
        self._image = image
        self._gps = gps

    @classmethod
    def from_bytes(cls, image_bytes):
        """ Input: image_bytes: bytes object
        Output: Image: Image class
        construct image from bytes into format. bytes string. return Image
        Turn into BytesIO
        open the stream
        Extract GPS data image_bytes and convert it to GPSRecord
        Transform into image of format with exif data"""
        stream = io.BytesIO(image_bytes)
        image = PIL.Image.open(stream)
        gps = exif_to_gps(image.info.get('exif'))
        return Image(image, gps)

    def to_bytes(self, given_format):
        """ Input: given_format: string
        Output: bytes
        construct image to bytes from self.image (PIL.Image). bytes string. Save as BytesIO object
        Create exif from given GPS record
        open image and convert into bytesIO"""
        output = io.BytesIO()
        self.save(output, given_format)
        output.seek(0)
        return output.read()

    def save(self, fp, given_format):
        """Input: fp: BytesIO object, given_format: string
        open file object(BytesIO)), insert exif bytes, and save to file pointer"""
        gps_dict = gps_to_exif(self._gps)
        exif_bytes = piexif.dump(gps_dict)
        self._image.save(fp, format=given_format, exif=exif_bytes)

def gps_to_exif(gps_record):
    """Input: gps_record: GPSRecord.
    Output: dict_whole: dictionary with exif data
    Turn GPS record to exif"""
    gps_dict = {}
    gps_dict[piexif.GPSIFD.GPSLongitudeRef] = b'E' if gps_record.longitude >= 0 else b'W'
    long_deg, long_min, long_sec = deg2dms(abs(gps_record.longitude))
    gps_dict[piexif.GPSIFD.GPSLongitude] = ((Fraction(long_deg).limit_denominator().numerator,
                                             Fraction(long_deg).limit_denominator().denominator),
                                            (Fraction(long_min).limit_denominator().numerator,
                                             Fraction(long_min).limit_denominator().denominator),
                                            (Fraction(long_sec).limit_denominator().numerator,
                                             Fraction(long_sec).limit_denominator().denominator))
    gps_dict[piexif.GPSIFD.GPSLatitudeRef] = b'N' if gps_record.latitude >= 0 else b'S'
    lat_deg, lat_min, lat_sec = deg2dms(abs(gps_record.latitude))
    gps_dict[piexif.GPSIFD.GPSLatitude] = ((Fraction(lat_deg).limit_denominator().numerator,
                                            Fraction(lat_deg).limit_denominator().denominator),
                                           (Fraction(lat_min).limit_denominator().numerator,
                                            Fraction(lat_min).limit_denominator().denominator),
                                           (Fraction(lat_sec).limit_denominator().numerator,
                                            Fraction(lat_sec).limit_denominator().denominator))
    gps_dict[piexif.GPSIFD.GPSAltitudeRef] = 0 if gps_record.altitude >= 0 else 1
    gps_dict[piexif.GPSIFD.GPSAltitude] = (int(abs(gps_record.altitude)), 1)
    gps_dict[piexif.GPSIFD.GPSMapDatum] = b'WGS-84'
    gps_dict[piexif.GPSIFD.GPSTimeStamp] = ((gps_record.time.hour, 1), (gps_record.time.minute, 1),
                                            (Fraction(gps_record.time.second).limit_denominator().numerator,
                                             Fraction(gps_record.time.second).limit_denominator().denominator))
    gps_dict[piexif.GPSIFD.GPSDateStamp] = gps_record.time.strftime('%Y:%m:%d')
    dict_whole = {"0th": {}, "Exif": {}, "GPS": gps_dict,
                  "Interop": {}, "thumbnail": None}
    return dict_whole


def exif_to_gps(exif):
    """"Turn exif to GPS record
    Input: exif: dict
    Output: gps_record: GPSRecord"""
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
    longitude = sign_long * dms2deg(gps_exif[piexif.GPSIFD.GPSLongitude][0][0] /
                                    gps_exif[piexif.GPSIFD.GPSLongitude][0][1],
                                    gps_exif[piexif.GPSIFD.GPSLongitude][1][0] /
                                    gps_exif[piexif.GPSIFD.GPSLongitude][1][1],
                                    gps_exif[piexif.GPSIFD.GPSLongitude][2][0] /
                                    gps_exif[piexif.GPSIFD.GPSLongitude][2][1])
    sign_alt = 1 if gps_exif[piexif.GPSIFD.GPSAltitudeRef] == 0 else -1
    altitude = sign_alt * gps_exif[piexif.GPSIFD.GPSAltitude][0]/gps_exif[piexif.GPSIFD.GPSAltitude][1]
    gps_record = GPSRecord(time, latitude, longitude, altitude)
    return gps_record


def deg2dms(degrees):
    """Convert degrees to Degrees, Minutes, Seconds
    Input: degrees
    Output: deg(degrees), mins(degrees minutes), sec(degrees sec)"""
    deg = int(degrees)
    minutes = int((degrees-deg)*60)
    sec = round(((((degrees - deg)*60)-minutes)*60), 8)
    return deg, minutes, sec


def dms2deg(deg, mins, sec):
    """Convert Degrees, Minutes, Seconds to degrees up to 8 decimal places
    Input: deg(degrees), mins(degrees minutes), sec(degrees sec)
    Output: degrees"""
    degree = round((sec/60+mins)/60+deg, 8)
    return degree
