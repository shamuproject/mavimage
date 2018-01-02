from pymavlink import mavutil
import sys
from optparse import OptionParser
from dronekit import connect, VehicleMode

class GPS:

    def __init__(self, connection):
        parser = OptionParser("readdata.py [options]")
        parser.add_option("--baudrate", dest="baudrate", type='int',
                          help="master port baud rate", default=115200)
        parser.add_option("--device", dest="device", default=None, help="serial device")
        parser.add_option("--rate", dest="rate", default=4, type='int', help="requested stream rate")
        parser.add_option("--source-system", dest='SOURCE_SYSTEM', type='int', default=255,
                          help='MAVLink source system')
        parser.add_option("--showmessages", dest="showmessages", action='store_true',
                          help="show incoming messages", default=False)
        (opts, args) = parser.parse_args()

        if opts.device is None:
            print("Please select a serial device")
            sys.exit(1)
        self.connection = mavutil.mavlink_connection(opts.device, baud=opts.baudrate)

    def register_handlers(self):
        return self.connection

    def global_position_int_handler(self, message):
        '''parser = OptionParser(
            description='Print out vehicle state information. Connects to SITL on local PC by default.')
        parser.add_option('--connect',
                            help="vehicle connection target string. If not specified, SITL automatically started and used.")
        args = parser.parse_args()

        connection_string = args.connect
        sitl = None

        # Start SITL if no connection string specified
        if not connection_string:
            import dronekit_sitl
            sitl = dronekit_sitl.start_default()
            connection_string = sitl.connection_string()'''
        connection_string = self.connection
        vehicle = connect(connection_string, wait_ready=True)
        vehicle.wait_ready('autopilot_version')
        message = vehicle.gps_0
        return message


