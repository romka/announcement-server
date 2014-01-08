__author__ = 'Roman Arkharov'

from twisted.internet.protocol import ServerFactory

from protocol import AnnouncementProtocol
from announcement import Announcement

from twisted.python import log

log.msg('AnnouncementServerFactory')

class AnnouncementServerFactory(ServerFactory):

    protocol = AnnouncementProtocol

    def startFactory(self):
        self.announcement_service = Announcement(self.max_clients, self.db_name, self.db_host, self.db_port, self.secret)

    def __init__(self, max_clients, service, db_name, db_host, db_port, secret):
        """
          Server factory constructor
        """

        self.service = service
        self.max_clients = max_clients
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port
        self.secret = secret

        log.msg('Announcement server initialized')

    def buildProtocol(self, addr):
        """
          This method calls when new client connected
        """
        p = self.protocol()
        p.factory = self
        return p
