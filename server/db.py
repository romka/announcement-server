__author__ = 'Roman Arkharov'

import txmongo
from pymongo import MongoClient
from twisted.internet import defer
from twisted.python import log
import base64

class Db:
    """
        Database communication class.
    """
    def __init__(self, parent, db_name, db_host, db_port):
        """
            Initialize variables.
        """
        self.db_status = 'not ready'

        self.parent = parent
        self.db_name = db_name
        self.db_host = db_host
        self.db_port = db_port

    def load_announces(self):
        # Sync mongo connection
        sync_mongo = MongoClient(self.db_host, self.db_port)

        sync_db = sync_mongo[self.db_name]
        sync_records = sync_db.announces

        data = sync_records.find()

        result = {}

        for item in data:
            if item.has_key('links') and item.has_key('announces'):
                a = item['announces']
                for k in a:
                    announce = item['announces'][k]
                    announce = announce.encode('utf-8-sig')
                    announce = base64.b64encode(announce)
                    announce = announce.replace('77u/', '')

                    item['announces'][k] = announce
                    log.msg('')
                    log.msg('ENC ANNOUNSE:' + announce)

                result[item['game']] = {
                    'result': '1',
                    'links': item['links'],
                    'announces': item['announces'],
                }

        return result