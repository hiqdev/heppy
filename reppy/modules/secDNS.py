from collections import OrderedDict

from ..Module import Module

class secDNS(Module):
    opmap = {
    }

### RESPONSE parsing

### REQUEST rendering

    def render_create(self, request):
        ext = self.render_extension(request, 'create')
        if request.get('maxSigLife'):
            request.sub(ext, 'secDNS:maxSigLife', {}, request.get('maxSigLife'))
        data = request.sub(ext, 'secDNS:dsData')
        request.subfields(data, OrderedDict([
            ('keyTag', {}),
            ('alg', {}),
            ('digestType', {}),
            ('digest', {}),
        ]))

