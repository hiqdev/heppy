from ..Module import Module


class secDNS(Module):
    opmap = {
        'infData':      'descend',
        'maxSigLife':   'set',
    }

### RESPONSE parsing
    def parse_dsData(self, response, tag):
        secData = {
            'keyTag':       response.find_text(tag, 'secDNS:keyTag'),
            'digestAlg':    response.find_text(tag, 'secDNS:alg'),
            'digestType':   response.find_text(tag, 'secDNS:digestType'),
            'digest':       response.find_text(tag, 'secDNS:digest'),
        }
        for child in tag :
            if child.tag == '{' + self.xmlns + '}keyData' :
                secData['keyData'] = {
                    'keyFlags':     response.find_text(child, 'secDNS:flags'),
                    'keyProtocol':  response.find_text(child, 'secDNS:protocol'),
                    'keyAlg':       response.find_text(child, 'secDNS:alg'),
                    'pubKey':       response.find_text(child, 'secDNS:pubKey'),
                }
        response.put_to_list('secDNS', secData)

    def parse_keyData(self, response, tag):
        response.put_to_list('keyData', {
            'keyTag':       response.find_text(tag, 'secDNS:keyTag'),
            'keyFlags':     response.find_text(tag, 'secDNS:flags'),
            'keyProtocol':  response.find_text(tag, 'secDNS:protocol'),
            'keyAlg':       response.find_text(tag, 'secDNS:alg'),
            'pubKey':       response.find_text(tag, 'secDNS:pubKey'),
        })

### REQUEST rendering

    def render_create(self, request):
        ext = self.render_extension(request, 'create')
        self.render_allData(request, ext, request)

    def render_update(self, request, data):
        ext = self.render_extension(request, 'update')
        for k in ('add', 'rem', 'chg'):
            if data.get(k):
                command = request.add_subtag(ext, 'secDNS:' + k)
                self.render_allData(request, command, data.get(k))

    def render_allData(self, request, parent, values):
        if values.get('all')=='true':
            request.add_subtag(parent, 'secDNS:all', {}, 'true')
            return
        if values.get('maxSigLife'):
            request.add_subtag(parent, 'secDNS:maxSigLife', {}, values.get('maxSigLife'))
        if values.get('digest'):
            self.render_dsData(request, parent, values)
        else:
            self.render_keyData(request, parent, values)

    def render_dsData(self, request, parent, values):
        data = request.add_subtag(parent, 'secDNS:dsData')
        request.add_subtag(data, 'secDNS:keyTag',      {}, values.get('keyTag'))
        request.add_subtag(data, 'secDNS:alg',         {}, values.get('digestAlg'))
        request.add_subtag(data, 'secDNS:digestType',  {}, values.get('digestType'))
        request.add_subtag(data, 'secDNS:digest',      {}, values.get('digest'))
        self.render_keyData(request, data, values)

    def render_keyData(self, request, parent, values):
        if not values.get('pubKey'):
            return
        data = request.add_subtag(parent, 'secDNS:keyData')
        request.add_subtag(data, 'secDNS:flags',       {}, values.get('flags', '257'))
        request.add_subtag(data, 'secDNS:protocol',    {}, values.get('protocol', '3'))
        request.add_subtag(data, 'secDNS:alg',         {}, values.get('keyAlg'))
        request.add_subtag(data, 'secDNS:pubKey',      {}, values.get('pubKey'))

