import json
import bottle
import netaddr
import threading


def route(method, path):
    def decorator(f):
        f.http_route = path
        f.http_method = method
        return f
    return decorator


class APIv1(object):

    prefix = '/v1'

    def __init__(self, supernet, subnet_mask):
        sn = netaddr.IPNetwork(supernet)
        self.networks = list(sn.subnet(subnet_mask))
        self.allocations = {}
        self.lock = threading.Lock()
        self.locks = {}

    @route('GET', '/network/')
    def list_network(self):
        allocations = {str(x): y for (x, y) in self.allocations.items()}
        return bottle.template('{{!ret}}', ret=json.dumps(allocations))

    @route('POST', '/network/')
    def allocate_network(self):
        uuid = bottle.request.body.getvalue().decode('utf-8')
        network = self.networks.pop()
        self.allocations[network] = uuid
        return bottle.template('{{!ret}}', ret=str(network))

    @route('DELETE', '/network/')
    def free_network(self):
        network = (netaddr
                   .IPNetwork(bottle
                              .request
                              .body
                              .getvalue()
                              .decode('utf-8')))
        (self
         .allocations
         .pop(network))
        (self
         .networks
         .append(network))

    @route('GET', '/lock/')
    def list_lock(self):
        return bottle.template('{{!ret}}', ret=json.dumps(self.locks))

    @route('POST', '/lock/')
    def allocate_lock(self):
        lock_id = bottle.request.body.getvalue().decode('utf-8')
        with self.lock:
            if lock_id in self.locks:
                return bottle.template('{{!ret}}', ret='')
            else:
                self.locks[lock_id] = True
                return bottle.template('{{!ret}}', ret=lock_id)

    @route('DELETE', '/lock/')
    def free_lock(self):
        lock_id = bottle.request.body.getvalue().decode('utf-8')
        with self.lock:
            if lock_id in self.locks:
                self.locks.pop(lock_id)
                return bottle.template('{{!ret}}', ret=lock_id)
            else:
                return bottle.template('{{!ret}}', ret='')
