txbonjour
=========

Bonjour!

A python package that is a Twisted plugin for using the Avahi/Bonjour service for network discovery.

Requires pybonjour:
https://code.google.com/p/pybonjour/

OR
```
easy_install pybonjour
```

To use simply,

broadcasting:
============
```
from txbonjour import discovery
breader = discovery.broadcast(protocol_instance, service_string, port, service_name)
```
ie.
```
from txbonjour import discovery
proto = discovery.BroadcastProtocol()
breader = discovery.broadcast(proto, '_examples._tcp', 9999, 'Example')
```

or
```
from txbonjour import discovery
proto = disocovery.BroadcastProtocol()
s = discovery.make_broadcast_service(proto, '_examples._tcp', 9999, 'Example')
```

discovering:
===========

```
from txbonjour import discovery
dreader = discovery.discover(protocol_instance, service_string)
```

ie.
```
from txbonjour import discovery
proto = discovery.DiscoverProtocol()
dreader = discovery.discover(proto, '_examples._tcp')
```

or

```
from txbonjour import discovery
proto = disocovery.DiscoverProtocol()
s = discovery.make_discover_service(proto, '_examples._tcp')
```

Adieu!

