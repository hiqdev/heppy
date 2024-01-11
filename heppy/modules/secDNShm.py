from secDNS import secDNS

class secDNShm(secDNS):
### RESPONSE parsing
    def parse_dsData(self, response, tag):
        secData = {
            'keyTag':       response.find_text(tag, 'secDNShm:keyTag'),
            'digestAlg':    response.find_text(tag, 'secDNShm:alg'),
            'digestType':   response.find_text(tag, 'secDNShm:digestType'),
            'digest':       response.find_text(tag, 'secDNShm:digest'),
        }
        for child in tag :
            if child.tag == '{' + self.xmlns + '}keyData' :
                secData['keyData'] = {
                    'keyFlags':     response.find_text(child, 'secDNShm:flags'),
                    'keyProtocol':  response.find_text(child, 'secDNShm:protocol'),
                    'keyAlg':       response.find_text(child, 'secDNShm:alg'),
                    'pubKey':       response.find_text(child, 'secDNShm:pubKey'),
                }
        response.put_to_list('secDNS', secData)

    def parse_keyData(self, response, tag):
        response.put_to_list('keyData', {
            'keyTag':       response.find_text(tag, 'secDNShm:keyTag'),
            'keyFlags':     response.find_text(tag, 'secDNShm:flags'),
            'keyProtocol':  response.find_text(tag, 'secDNShm:protocol'),
            'keyAlg':       response.find_text(tag, 'secDNShm:alg'),
            'pubKey':       response.find_text(tag, 'secDNShm:pubKey'),
        })


