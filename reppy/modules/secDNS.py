from collections import OrderedDict

from ..Module import Module

class secDNS(Module):
    opmap = {
    }

### RESPONSE parsing

### REQUEST rendering

    def render_create(self, request):
        ext = self.render_extension(request, 'create')
        self.render_allData(request, ext)

    def render_allData(self, request, parent):
        if request.get('maxSigLife'):
            request.sub(parent, 'secDNS:maxSigLife', {}, request.get('maxSigLife'))
        if request.get('digest'):
            self.render_dsData(request, parent)
        else:
            self.render_keyData(request, parent)

    def render_dsData(self, request, parent):
        data = request.sub(parent, 'secDNS:dsData')
        request.subfields(data, OrderedDict([
            ('keyTag', {}),
            ('alg', 'digestAlg'),
            ('digestType', {}),
            ('digest', {}),
        ]))
        self.render_keyData(request, data)

    def render_keyData(self, request, parent):
        if not request.get('pubKey'):
            return
        data = request.sub(parent, 'secDNS:keyData')
        request.subfields(data, OrderedDict([
            ('flags', {}),
            ('protocol', {}),
            ('alg', 'keyAlg'),
            ('pubKey', {}),
        ]))

