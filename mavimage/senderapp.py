
'''
SenderAPP class. Inherited by App class
Attributes:
    mavlink:MAVLinkConnection
    photographer:Photographer
    logger:Logger=None
'''

class SenderApp:

    def __init__(self, mavlink, photographer, logger=None):
        self.logger = logger
