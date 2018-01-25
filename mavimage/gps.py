
from dronekit import connect
import datetime as d
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
        # establish connection attribute
        self.connection = mavlink

    def register_handlers(self):
        mavconnection = MavLinkConnection
        message = pymavlink.MAVLinkMessage
        mavconnection.push_handler(self.global_position_int_handler(mavconnection, message))

    def global_position_int_handler(self, mavlink, message):
        data = (message.raw_items())
        return data

    def record(self):
        # return the gps record
        data = self.global_position_int_handler(self.connection)
        return data


