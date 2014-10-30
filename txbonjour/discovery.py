'''
Created on 2013-02-09

@author: jdcumpson
@author: Noobie
@copyright: (c) JD Cumpson 2013.
'''

import pybonjour
from twisted.python import log
from twisted.internet import reactor, defer
from zope import interface

from txbonjour.service import (BonjourService, BonjourReader,
                               IBroadcastProtocol, IDiscoverProtocol)


class BroadcastProtocol(object):
    
    def registerReceived(self, *args):
        """Override in sub-classes."""
        
    def connectionMade(self):
        """Override in sub-classes."""
        
    def connectionLost(self, reason=None):
        """Override in sub-classes."""


class DiscoverProtocol(object):
    
    interface.implements(IDiscoverProtocol)
    
    def browseError(self, error_code, *args):
        """
        Override in sub-classes.
        """
        
    def resolveError(self, error, *args):
        """
        Override in sub-classes.
        """
    
    def addService(self, service_name, host, port, interface_index, flags):
        """
        Override in sub-classes.
        """
        
    def removeService(self, service_name, host, port, interface_index, flags):
        """
        Override in sub-classes.
        """
    
    def connectionMade(self):
        """
        Override in sub-classes.
        """
        
    def connectionLost(self, reason=None):
        """
        Override in sub-classes.
        """


def _resolve(protocol, resolve_ip=True, *args):
    """
    Resolve browsed services then return them.
    """
    d = defer.Deferred()
    
    
    if resolve_ip:
        def _cb(ip, args):
            args[5] = ip
            return args
        
        def _resolve_ip(args):
            fqdm = args[5]
            args = list(args)
            d = reactor.resolve(fqdm)
            d.addCallback(_cb, args)
            return d
        d.addCallback(_resolve_ip)
    
    def cb(*args):
        reader.loseConnection()
        error_code = args[3]
            
        if error_code != pybonjour.kDNSServiceErr_NoError:
            d.errback(args)
        d.callback(args)
    
    args = list(args)
    args.append(cb)
        
    sdref = pybonjour.DNSServiceResolve(*args)
    reader = BonjourReader(DiscoverProtocol(), sdref)
    reader.startReading()
    return d


def _dispatch(protocol, resolving=False, resolve_ip=True, *args):
    """
    Dispatches callbacks from the pybonjour module interface to our protocol.
    """
    # cheaply identify if it's a broadcast or discovery
    if len(args) == 6:
        sdref, flags, interface_index, service_name, registry_type, \
            reply_domain = args
        error_code = pybonjour.kDNSServiceErr_NoError
        return reactor.callLater(0, protocol.registerReceived, *args)
    
    else:
        sdref, flags, interface_index, error_code, service_name, registry_type, \
            reply_domain = args
    
    def _call(*args):
        error_code = args[3]
        if error_code != pybonjour.kDNSServiceErr_NoError:
            args = list(args)
            error_code = args.pop(3)
            reactor.callLater(0, protocol.browseError, error_code, *args)
        elif not flags & pybonjour.kDNSServiceFlagsAdd:
            reactor.callLater(0, protocol.removeService,
                                args[4], args[5], args[6], args[2], args[1],
                                )
        elif flags & pybonjour.kDNSServiceFlagsAdd:
            reactor.callLater(0, protocol.addService, 
                              args[4], args[5], args[6], args[2], args[1],
                              )
            
    if not resolving:
        return _call(*args)
    
    temp = list(args)
    temp.pop(3)
    resolve_args = temp[2:]
    resolve_args.insert(0, 0)
    d = defer.maybeDeferred(_resolve, protocol, resolve_ip, *resolve_args)
    d.addCallback(lambda res:_call(*res))
    d.addErrback(lambda res:log.err(res))
    d.addErrback(lambda res: reactor.callLater(0, protocol.resolveError, 
                                                    res, *resolve_args))


def broadcast(protocol, regtype, port, name, record=None, _do_start=True):
    """
    Make a BonjourReader instance. A bonjour reader is just like a file 
    descriptor for read-only. It implements the twisted interface 
    'twisted.internet.interfaces.IReadDescriptor'. This service will
    watch the Bonjour output that corresponds to this service.
    
    XXX: this should probably actually disconnect readers in more of a one-off
         broadcast type message. ie. reader.stopReading() after finished. To
         be consistent with the behaviour of the discover method, it does not.

    @param protocol: A protocol implementing IBroadcastProtocl
    @param regtype: A string for the mDNS registry via pybonjour
    @param name: The name of your service
    @param port: The port that your service is listening on
    @param record: A pybonjour.TXTRecord instance (mDNS record)
    @param _do_start: if True, starts immediately.
    @return: a BonjourReader instance
    @rtype: txbonjour.service.BonjourReader
    
    @see: https://code.google.com/p/pybonjour/
    @see: http://http://twistedmatrix.com/documents/current/api/
            twisted.internet.interfaces.IReactorFDSet.html
    """
    if record is None:
        record = pybonjour.TXTRecord({})
    def cb(*args):
        _dispatch(protocol, False, False, *args)
#    cb = lambda *res:_dispatch(protocol, False, *res)
    sdref = pybonjour.DNSServiceRegister(regtype=regtype,
                                         port=port,
                                         callBack=cb,
                                         txtRecord=record,
                                         name=name,
                                         )
    reader = BonjourReader(protocol, sdref)
    if _do_start:
        reader.startReading()
    return reader


def discover(protocol, regtype, resolve=True, resolve_ip=True, _do_start=True):
    """
    Make a BonjourReader instance. This instance will monitor the Bonjour
    daemon and call the appropriate method on the protocol object when it is
    read from the service.
    
    @param protocol: A protocol implementing IDiscoverProtocol
    @param regtype: A string for the mDNS registry via pybonjour
    @param resolve: Perform a resolve on the service address before exposing it
    @param resolve_ip: If resolve, and if True, get IP from FQDM
    @param _do_start: if True, starts immediately
    @returns: A BonjourReader instance
    @rtype: txbonjour.service.BonjourReader
    """
    cb = lambda *res:_dispatch(protocol, resolve, resolve_ip, *res)
    sdref = pybonjour.DNSServiceBrowse(regtype=regtype, callBack=cb)
    reader = BonjourReader(protocol, sdref)
    return reader


def connectBonjour(*args, **kwargs):
    """ 
    Creates a broadcast service via broadcast.
    
    @note: this is a shortcut if you are not using twisted.application.service.
            See tap.py.
    @see: txbonjour.tap
    @param args: All the same args as broadcast 
    @return: a BonjourService instance.
    @rtype: txbonjour.service.BonjourService
    
    @see: http://twistedmatrix.com/documents/12.2.0/core/howto/application.html 
    """
    reader = broadcast(*args, _do_start=False, **kwargs)
    return BonjourService(reader)


def listenBonjour(*args, **kwargs):
    """ 
    Creates a discover service via discover.
    
    @note: this is a shortcut if you are not using twisted.application.service.
            See tap.py.
    @see: txbonjour.tap
    @return: a BonjourService instance.
    @rtype: txbonjour.service.BonjourService
    
    @see: http://twistedmatrix.com/documents/12.2.0/core/howto/application.html 
    """
    reader = discover(*args, _do_start=False, **kwargs)
    return BonjourService(reader)


# backwards compat
make_broadcast_service = connectBonjour
make_discover_service = listenBonjour
