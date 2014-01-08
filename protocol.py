__author__ = 'Roman Arkharov'

from twisted.internet.protocol import Protocol
import time
import simplejson as json
from twisted.python import log

class AnnouncementProtocol(Protocol):
    return_codes = {}
    return_codes['wrong_request'] = '1'
    return_codes['wrong_arguments'] = '2'
    return_codes['server_not_ready'] = '3'
    return_codes['unhandled_situation'] = '4'

    def connectionLost(self, reason):
        pass
        log.msg('AnnouncementProtocol.connectionLost. Connection lost for client')
        # self.factory.Announcement_service.connectionClosedByClient(self.client_id)

    def connectionMade(self):
        """
            When user connected
        """
        log.msg('AnnouncementProtocol.connectionMade. New connection')

    def dataReceived(self, raw_data):
        game_name = raw_data

        self.factory.announcement_service.get_announce(self, game_name)

    def writeData(self, data):
        #self.transport.write(data + '\x00')
        log.msg('data for user ' + data)
        self.transport.write(data)
