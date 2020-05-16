# encoding=utf-8
# ---------------------------------------
#   语言：Python2.7
#   日期：2017-07-10
#   作者：code pande
#   功能：DNS解析换成缓存
# ---------------------------------------


from gevent import socket

_dnscache = {}


def _setDNSCache():
    """ DNS缓存 """

    def _getaddrinfo(*args, **kwargs):
        if args in _dnscache:
            # print str(args) + " in cache"
            return _dnscache[args]
        else:
            # print str(args) + " not in cache"
            _dnscache[args] = socket._getaddrinfo(*args, **kwargs)
            return _dnscache[args]

    if not hasattr(socket, '_getaddrinfo'):
        socket._getaddrinfo = socket.getaddrinfo
        socket.getaddrinfo = _getaddrinfo
