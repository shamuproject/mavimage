from datetime import datetime, timedelta
import MavLinkConnection
import pymavlink
'''
GPS class. Responsible for retrieving GPS data given connection and returning GPS data including lat, long, and time
January 2, 2018
Attributes: mav_connection:MAVLinkConnection
'''
class GPS:

    def __init__(self, mavlink):
        # mavlink:MAVLinkConnection
        pass

    def register_handlers(self, mavlink):
        mavlink.push_handler('GLOBAL_POSITION_INT', self.global_position_int_handler)

    def global_position_int_handler(self, mavlink, message):
        self.latitude = float(message.lat)
        self.longitude = float(message.lon)
        self.altitude = float(message.alt)
        # find absolute time
        self.time = datetime(message.time_boot_ms) + timedelta(message.time_boot_ms)

    def record(self):
        # return the gps record
        pass



