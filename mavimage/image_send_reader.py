#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 18:27:23 2017

@author: laurenmcintire
"""

# based on: https://gist.github.com/vo/9331349

# mavlink reader. Read in mavlink message on UAV
import sys, os
from optparse import OptionParser
# where is mavlink?
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../mavlink'))
from pymavlink import mavutil

def handle_heartbeat(msg):
    mode = mavutil.mode_string_v10(msg)
    is_armed = msg.base_mode & mavutil.mavlink.MAV_MODE_SAFETY_ARMED
    is_enabled = msg.base_mode & mavutil.mavlink.MAV_MODE_FLAG_GUIDED_ENABLED
    
def send_image(msg):
    # which channel?
    # from command line
    channel = channel_input
    return 
    
def read_loop(m):
    #grab message
    while(True):
        msg = m.rec_match(blocking=False)
        if not msg:
            return
    msg_type = msg.get_type()
    if msg_type == "HEARTBEAT":
        handle_heartbeat(msg)
    elif msg_type == "DATA_TRANSMISSION_HANDSHAKE":
        send_image(msg)
        
def main():
    #command line options
    parser = OptionParser("readdata.py [options]")
    parser.add_option("--baudrate", dest="baudrate",type='int',
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
        
    master = mavutil.mavlink_connection(opts.device, baud=opts.baudrate)
    
    #wait for heartbeat to get system ID
    master.wait_gps_fix()
    #send response
    master.mav.request_data_stream_send(master.target_system, master.target_component, 
                                        mavutil.mavlink.MAV_DATA_STREAM_ALL, opts.rate, 1)
    # begin read link
    read_loop(master)
    
if __name__ == '__main__':
    main()