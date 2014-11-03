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

from txbonjour import discovery, tap

if __name__ == "__main__":
    log.startLogging(sys.stdout)
    proto = tap.LoggingProtocol()

    # testing with services
    dservice = discovery.listenBonjour(proto, '_nodes._udp',)
    bservice = discovery.connectBonjour(proto,
                                       regtype='_nodes._udp',
                                       port=9994,
                                       name='ExampleUDPService',
                                       )
    reactor.callWhenRunning(dservice.startService)
    reactor.callWhenRunning(bservice.startService)
    d = task.deferLater(reactor, 5, bservice.stopService)

    def exit(service):
        rm(service)
        log.msg('broadcast service stopped, exiting now')
        reactor.stop()
        
    rm = proto.removeService
    proto.removeService = exit

    reactor.run()

