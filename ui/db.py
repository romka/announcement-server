__author__ = 'Roman Arkharov'

from pymongo import MongoClient
from flask import flash

class Db:
    """
        Database communication class.
    """
    def __init__(self):
        """
            Initialize variables.
        """
        from flask import current_app

        self.db_name = current_app.config['MONGODB_DATABASE']
        self.db_host = current_app.config['MONGODB_HOST']
        self.db_port = current_app.config['MONGODB_PORT']

    def delete_announce(self, game):
        sync_mongo = MongoClient(self.db_host, self.db_port)

        sync_db = sync_mongo[self.db_name]
        sync_records = sync_db.announces

        return sync_records.remove({"game":game})

    def update_announce(self, data):
        sync_mongo = MongoClient(self.db_host, self.db_port)

        sync_db = sync_mongo[self.db_name]
        sync_records = sync_db.announces

        return sync_records.update({"game": data['game']}, {"game": data['game'], "announces": data['announces'], "links": data['links']}, True)


    def load_announces(self):
        # Sync mongo connection
        sync_mongo = MongoClient(self.db_host, self.db_port)

        sync_db = sync_mongo[self.db_name]
        sync_records = sync_db.announces

        data = sync_records.find()

        result = {}

        for item in data:
            if item.has_key('links') and item.has_key('announces'):
                #flash(item['game'])
                result[item['game']] = {
                    'result': '1',
                    'links': item['links'],
                    'announces': item['announces'],
                    }

        return result
