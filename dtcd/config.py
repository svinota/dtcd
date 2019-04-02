import os
import json


class Config(dict):

    version = 1

    def __init__(self, path='/etc/dtcd/dtcd.conf'):
        self.path = os.environ.get('DTCD_CONFIG', path)

    def load(self):
        with open(self.path, 'r') as f:
            self.update(json.load(f))
        if int(self['version']) > self.version:
            raise RuntimeError('config version mismatch: %s; must be <= %s'
                               % (self['version'], self.version))
        return self

    def dump(self, path=None):
        path = path or self.path
        with open(path, 'w') as f:
            json.dump(dict(self), f, indent=3)
        return self
