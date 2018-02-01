from datetime import datetime
# import MavLinkConnection
# import pymavlink
'''
GPS class. Responsible for retrieving GPS data given connection and returning GPS data including lat, long, and time
January 2, 2018
Attributes: mav_connection:MAVLinkConnection
'''
class GPS:

    def __init__(self, mavlink):
        # mavlink:MAVLinkConnection
        self.register_handlers(mavlink)

    def register_handlers(self, mavlink):
        mavlink.push_handler('GLOBAL_POSITION_INT', self.global_position_int_handler)

    def global_position_int_handler(self, mavlink, message):
        self.lat = float(message.lat)
        self.lon = float(message.lon)
        self.alt = float(message.alt)
        # find absolute time
        self.time = datetime.now()
        self.record()

    def record(self):
        time = self.time
        latitude = self.lat
        longitude = self.lon
        altitude = self.alt
        return time, latitude, longitude, altitude



