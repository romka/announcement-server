__author__ = 'Roman Arkharov'

from optparse import OptionParser

from serverfactory import AnnouncementServerFactory

from twisted.application import internet, service
from twisted.python import log

# Rename example_secret.py to secret.py and fill it with your own values between 1 and 255
secret = [line.strip() for line in open('secret.py')]
log.msg(secret)

secret2 = []
for s in secret:
    secret2.append(int(s))

host = 'kece.ru'
port = 10190
max_clients = 10000

db_host = '10.20.2.105'
db_port = 27017
db_name = 'announcement_server'

top_service = service.MultiService()

announcement_service = service.Service()
announcement_service.setServiceParent(top_service)

log.msg('before init AnnouncementServerFactory')
factory = AnnouncementServerFactory(max_clients, announcement_service, db_name, db_host, db_port, secret2)
log.msg('after init AnnouncementServerFactory')

tcp_service = internet.TCPServer(port, factory, interface=host)
tcp_service.setServiceParent(top_service)

application = service.Application("main")

# this hooks the collection we made to the application
top_service.setServiceParent(application)
