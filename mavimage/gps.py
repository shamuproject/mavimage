from datetime import datetime

"""GPS class. Responsible for retrieving GPS data given connection and returning GPS data including lat, long, and time
Attributes: mav_connection:MAVLinkConnection
"""
class GPS:

    def __init__(self, mavlink):
        """ Initialize GPS class
        Args:
            mavlink:MAVLinkConnection
        """
        self.register_handlers(mavlink)

    def register_handlers(self, mavlink):
        """Call push handler in mavlink with request for GLOBAL_POSITION_INT message
        Args:
              mavlink: MavlinkConnection
        """
        mavlink.push_handler('GLOBAL_POSITION_INT', self.global_position_int_handler)

    def global_position_int_handler(self, mavlink, message):
        """store message attributes
        Args:
               mavlink:MAVLinkConnection,
               message:GLOBAL_POSITION_INT
        """
        self.lat = float(message.lat)/10000000
        self.lon = float(message.lon)/10000000
        self.alt = float(message.alt)
        # find absolute time
        self.time = datetime.now()
        self.record()

    def record(self):
        """Set Record
        Returns:
               GPSRecord(time, lat, lon, alt): GPSRecord
        """
        time = self.time
        latitude = self.lat
        longitude = self.lon
        altitude = self.alt
        return GPSRecord(time, latitude, longitude, altitude)


class GPSRecord:
    """GPSRecord class. Helper function for GPS class to return a GPS Record
    Attributes:
        time: datetime
        latitude (float)
        longitude (float)
        altitude (int)
    """
    def __init__(self, time, latitude, longitude, altitude):
        """Initialize GPSRecord class
        Args:
             time
             latitude
             longitude
             altitude
        """
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude

    def __eq__(self, other):
        return self.time == other.time and \
               self.latitude == other.latitude and \
               self.longitude == other.longitude and \
               self.altitude == other.altitude

    def __ne__(self, other):
        return not self == other
