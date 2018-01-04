
from dronekit import connect
import datetime as d
'''
GPS class. Responsible for retrieving GPS data given connection and returning GPS data including lat, long, and time
January 2, 2018
'''
class GPS:

    def __init__(self, mav_connection):
        # establish connection attribute
        self.connection = mav_connection

    def register_handlers(self):
        # return connection
        return self.connection

    def global_position_int_handler(self, mav_connection):
        # find gps location and time of UAV
        connection_string = mav_connection
        vehicle = connect(connection_string, wait_ready=True)
        vehicle.wait_ready('autopilot_version')
        # returns the latitude and longitude of the UAV
        message = vehicle.location.global_frame
        time = d.datetime
        # need a way to find timestamp
        #####
        return message, time

    def record(self):
        # return the gps record
        link = self.register_handlers()
        gps, time = self.global_position_int_handler(link)
        return gps


