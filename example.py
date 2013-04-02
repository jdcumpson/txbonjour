"""
    Example to show how to use the discovery feature.
    If you are using twisted services (tap) then you will want to use:
    
    txbonjour.discovery.make_broadcast_service
    
    and
    
    txbonjour.discovery.make_discover_service
    
"""
import sys

from twisted.internet import reactor, task, defer
from twisted.python import log

from txbonjour import discovery

class BProtocol(discovery.BroadcastProtocol):
    
    def registerReceived(self, *args):
        log.msg('now broadcasting')


class DProtocol(discovery.DiscoverProtocol):
    
    def addService(self, *args):
        log.msg('add service: %r' % (args,))
        
    def removeService(self, *args):
        log.msg('remove service: %r' % (args,))
        
    def browseError(self, *args):
        log.msg('browseError: %r' % (args,))
        
    def resolveError(self, err, *args):
        log.msg('resolveError: %r' % (args,))


if __name__ == "__main__":
    log.startLogging(sys.stdout)
    defer.setDebugging(1)
    
    # test cases without services
#    reader = discovery.discover(DProtocol(), '_nodes._udp', True)
#    reader.startReading()
#    breader = discovery.broadcast(BProtocol(), '_nodes._udp', 9994, 'Example')
#    breader.startReading()
#    d = task.deferLater(reactor, 5, breader.loseConnection)
    
    # testing with services
    dservice = discovery.make_discover_service(DProtocol(), '_nodes._udp',
                                                 True)
    bservice = discovery.make_broadcast_service(BProtocol(), '_nodes._udp',
                                                9994, 'Example')
    reactor.callWhenRunning(dservice.startService)
    reactor.callWhenRunning(bservice.startService)
    d = task.deferLater(reactor, 5, bservice.stopService)
    
    reactor.run()
    
