txbonjour
=========

Bonjour!

A python package that is a Twisted plugin for using the Avahi/Bonjour service for network discovery.

```
easy_install txbonjour
```

Requires pybonjour:
https://code.google.com/p/pybonjour/
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





Copyright (c) 2013 JD Cumpson.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
