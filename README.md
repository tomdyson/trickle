Trickle
=======

A future activity streaming app, starting with two Tornado-based experiments in websockets: one using plain websockets from the Tornado library and Redis for message persistence; the other using SocketTornad.IO, a Python implementation of Socket.IO, which falls back to Flash sockets and long polling for non-websocket-capable browsers.

## Dependencies

* Python 2.6
* Tornado 1.1

## Plain websocket dependencies

* [Redis 1.2.6+](http://code.google.com/p/redis/)
* [redis-py](http://github.com/andymccurdy/redis-py)

## SocketTornad.IO dependencies

* [SocketTornad.IO](https://github.com/SocketTornadIO/SocketTornad.IO)