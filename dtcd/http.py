import socket
import struct
import bottle
from wsgiref.simple_server import WSGIRequestHandler
from wsgiref.simple_server import WSGIServer


class SWSGI(WSGIServer):

    def __init__(self, family, address, handler):
        self.address_family = family
        if family == socket.AF_UNIX:
            self.csize = struct.calcsize('3i')
            self.get_request = self.get_unix_request
        WSGIServer.__init__(self, address, handler)

    def get_unix_request(self):
        sock, _ = WSGIServer.get_request(self)
        cred = sock.getsockopt(socket.SOL_SOCKET,
                               socket.SO_PEERCRED,
                               self.csize)
        cred = struct.unpack('3i', cred)
        ret = [sock, ['pid: %i, uid: %i, gid: %i' % cred, 0]]
        return ret


class HTTPHandler(WSGIRequestHandler):

    def log_request(*argv, **kwarg):
        return WSGIRequestHandler.log_request(*argv, **kwarg)


class Server(bottle.ServerAdapter):
    quiet = False

    def __init__(self, family=socket.AF_INET, host='127.0.0.1', port=7623):
        self.options = {}
        self.host = host
        self.port = port
        self.address_family = family
        if family == socket.AF_UNIX:
            self.server_address = self.host
        elif family == socket.AF_INET:
            self.server_address = (self.host, self.port)
        else:
            raise ValueError()

    def run(self, app):
        srv = SWSGI(self.address_family, self.server_address, HTTPHandler)
        srv.set_app(app)
        srv.serve_forever()
