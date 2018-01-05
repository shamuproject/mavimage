from pymavlink import mavutil

'''
MAVLinkConnection class
Attributes: mavfile
'''

class MAVLinkConnection:

    def __init__(self, mav):
        # mav:MAVFile
        self.mav = mav

    def push_handler(self, message, handler):
        # message:str, handler:function(mav, message)
        self.mav.push(handler(message))

    def pop_handler(self, message):
        # message:Str
        handler = self.mav.pop(message)
        # handler: function(mav, message)
        return handler

    def clear_handler(self, message):
        # message:str

    def add_timer(self, period, handler):
        # period:int, handler:function(mav)

