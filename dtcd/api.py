import json
import bottle
import netaddr


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

    @route('GET', '/network/')
    def list_network(self):
        allocations = {x: str(y) for (x, y) in self.allocations.items()}
        return bottle.template('{{!ret}}', ret=json.dumps(allocations))

    @route('POST', '/network/')
    def allocate_network(self):
        uuid = bottle.request.body.getvalue().decode('utf-8')
        if uuid in self.allocations:
            network = self.allocations[uuid]
        else:
            network = self.networks.pop()
            self.allocations[uuid] = network
        return bottle.template('{{!ret}}', ret=str(network))

    @route('DELETE', '/network/')
    def free_network(self):
        uuid = bottle.request.body.getvalue().decode('utf-8')
        (self
         .networks
         .append(self
                 .allocations
                 .pop(uuid)))
