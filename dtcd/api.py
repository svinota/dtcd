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

    def __init__(self, config):
        sn = netaddr.IPNetwork(config['supernet'])
        sn6 = netaddr.IPNetwork(config['supernet6'])

        self.networks = {'ipv4': list(sn.subnet(config['subnet_mask'])),
                         'ipv6': list(sn6.subnet(config['subnet_mask6']))}
        self.allocations = {'ipv4': {},
                            'ipv6': {}}

        self.lock = threading.Lock()
        self.locks = {}

    @route('GET', '/network/')
    def list_network(self):
        allocations = {z: {str(x): y for (x, y) in self.allocations[z].items()}
                       for z in self.allocations}
        return bottle.template('{{!ret}}', ret=json.dumps(allocations))

    @route('POST', '/network/<ipv:re:(%s|%s)>/' % ('ipv4', 'ipv6'))
    def allocate_network(self, ipv):
        uuid = bottle.request.body.getvalue().decode('utf-8')
        network = self.networks[ipv].pop()
        self.allocations[ipv][network] = uuid
        return bottle.template('{{!ret}}', ret=str(network))

    @route('DELETE', '/network/<ipv:re:(%s|%s)>/' % ('ipv4', 'ipv6'))
    def free_network(self, ipv):
        network = (netaddr
                   .IPNetwork(bottle
                              .request
                              .body
                              .getvalue()
                              .decode('utf-8')))
        (self
         .allocations[ipv]
         .pop(network))
        (self
         .networks[ipv]
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
