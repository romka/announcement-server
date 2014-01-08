__author__ = 'Roman Aarkharov'

import simplejson as json
import time
from twisted.python import log

from db import Db
from crypt import Crypt

class Announcement:
    def __init__(self, max_clients, db_name, db_host, db_port, secret):
        self.sequence = secret
        self.base64_alt = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

        self.db = Db(self, db_name, db_host, db_port)
        self.announces = self.db.load_announces()
        self.announces_time = int(time.time())

        log.msg(self.announces)

        self.crypt = Crypt(self.sequence)

    def get_announce(self, protocol, game_name):
        result = self.announces.get(game_name, {'result': '0'})

        j = json.dumps(result)
        c = self.crypt.crypt(j)

        log.msg('Send data to client')
        protocol.writeData(c)
        protocol.transport.loseConnection()

        # refresh announces
        if int(time.time()) - self.announces_time > 15:
            self.announces = self.db.load_announces()
            log.msg('Announces updated')
            self.announces_time = int(time.time())

