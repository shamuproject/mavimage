#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 16:06:24 2017

@author: laurenmcintire
"""
import pymavlink as pm
import pillow as pil
import webp as wp
# assumptions: either arrive or not. No buffer overflows
data = pm.mavutil.mavlink_connection('udp:localhost:14551', planner_format=False, 
                                     notimestamps=False, robust_parsing=True)
while True:
    msg = data.recv_match()
    if msg is not None:
        if msg.get_type() is "HEARTBEAT":
            print(msg)
        elif msg.get_type() is "NAV_CONTROLLER_OUTPUT":
            print(msg)

MAVLINK_DATA_STREAM_IMG_WEBP #enum

#DATA_TRANSMISSION_HANDSHAKE
# read in target, state (0) for request, id, type (MAVLINK_DATA_STREAM_TYPES), freq (frames/sec)
# send back message with # of packets, size of each packet, and image size (bytes), state=1
# wait for image from camera
#encode (wepb)
#ENCAPSULATED_IMAGE
#send meta data
#split into chunks
#send chunks
#chunks consist of sequence number and ID of image stream
# each new image has new DATA_TRANSMISSION_HANDSHAKE. Sequence number for each starts with 0
# wait for stop in DATA_TRANSMISSION_HANDSHAKE with frequency set to 0
# send back ACK packet with same data
# (sent)
# CAMERA_IMAGE_CAPTURED
# CAMERA_INFORMATION
# ENCAPSULATED_DATA
# (received)
# GLOBAL_POSITION_INT
# ALTITUDE
