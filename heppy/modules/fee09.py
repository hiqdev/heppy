from fee import fee

class fee09(fee):
    def parse_cd_tag(self, response, tag):
        feedata = {}
        for child in tag :
            tagname = child.tag.replace('{' + self.xmlns + '}', '')
            feedata.update({tagname: child.text.lower()})

        response.put_to_dict('fee', {
            feedata['objID']: feedata
        })

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        domain = request.add_subtag(ext, 'fee:object', {'objURI': data.get('objURI', 'urn:ietf:params:xml:ns:domain-1.0')})
        request.add_subtag(domain, 'fee:objID',     {'element':'name'}, data.get('name'))
        request.add_subtag(domain, 'fee:currency',  {},                 data.get('currency'))
        request.add_subtag(domain, 'fee:command',   {
            #'phase': data.get('phase', 'claims'),
            #'subphase': data.get('subphase', 'landrush' if data.get('phase', 'claims') == 'claims' else ''),
        }, data.get('action'))
        request.add_subtag(domain, 'fee:period',    {'unit':'y'},       data.get('period'))
