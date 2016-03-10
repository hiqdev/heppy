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
            self.render_dsData(request, parent, request)
        else:
            self.render_keyData(request, parent, request)

    def render_dsData(self, request, parent, values):
        data = request.sub(parent, 'secDNS:dsData')
        request.sub(data, 'secDNS:keyTag',      {}, values.get('keyTag'))
        request.sub(data, 'secDNS:alg',         {}, values.get('digestAlg'))
        request.sub(data, 'secDNS:digestType',  {}, values.get('digestType'))
        request.sub(data, 'secDNS:digest',      {}, values.get('digest'))
        self.render_keyData(request, data, values)

    def render_keyData(self, request, parent, values):
        if not request.get('pubKey'):
            return
        data = request.sub(parent, 'secDNS:keyData')
        request.sub(data, 'secDNS:flags',       {}, values.get('flags'))
        request.sub(data, 'secDNS:protocol',    {}, values.get('protocol'))
        request.sub(data, 'secDNS:alg',         {}, values.get('keyAlg'))
        request.sub(data, 'secDNS:pubKey',      {}, values.get('pubKey'))

