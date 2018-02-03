from datetime import datetime
# import MavLinkConnection
# import pymavlink
'''
GPS class. Responsible for retrieving GPS data given connection and returning GPS data including lat, long, and time
Attributes: mav_connection:MAVLinkConnection
'''
class GPS:

    def __init__(self, mavlink):
        ''' mavlink:MAVLinkConnection '''
        self.register_handlers(mavlink)

    def register_handlers(self, mavlink):
        '''Call push handler in mavlink with request for GLOBAL_POSITION_INT message'''
        mavlink.push_handler('GLOBAL_POSITION_INT', self.global_position_int_handler)

    def global_position_int_handler(self, mavlink, message):
        '''store message attributes'''
        '''mavlink:MAVLinkConnection, message:GLOBAL_POSITION_INT'''
        self.lat = float(message.lat)/10000000
        self.lon = float(message.lon)/10000000
        self.alt = float(message.alt)
        # find absolute time
        self.time = datetime.now()
        self.record()

    def record(self):
        '''return time, latitude, longitude, and altitude'''
        time = self.time
        latitude = self.lat
        longitude = self.lon
        altitude = self.alt
        return GPSRecord(time, latitude, longitude, altitude)


class GPSRecord:
    def __init__(self, time, latitude, longitude, altitude):
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude



