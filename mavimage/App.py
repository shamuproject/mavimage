import SenderApp
import ReceiverApp
'''
App class. Inherits SenderApp and ReceiverApp classes
Attributes:
    mavlink:MavLinkConnection
    logger:Logger
'''

class App(SenderApp, ReceiverApp):

    def __init__(self, mavlink, logger=None):
        # mavlink:MavlinkConnection, logger:Logger
