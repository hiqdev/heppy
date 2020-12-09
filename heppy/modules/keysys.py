from ..Module import Module
from ..TagData import TagData


class keysys(Module):
    opmap = {
        'resData':      'descend',
        'infData':      'descend',
        'renDate':      'set',
        'punDate':      'set',
        'domain-roid':  'set',
        'renewalmode':  'set',
        'transfermode': 'set',
        'transferlock': 'set',
        'contactInfData':'descend',
        'validated':    'set',
        'verification-requested': 'set',
        'verified': 'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'keysys'

### RESPONSE parsing

    def parse_poll(self, response, tag):
        pass

### REQUEST rendering

    def render_renew(self, request, data):
        ext = self.render_extension(request, 'update')
        domain = request.add_subtag(ext, 'keysys:domain')
        request.add_subtag(domain, 'keysys:renewalmode', {}, data.get('renewalmode'))
        request.add_subtag(domain, 'keysys:transfermode', {}, data.get('transfermode', 'DEFAULT'))

    def render_create(self, request, data):
        pass

    def render_update(self, request, data):
        pass




