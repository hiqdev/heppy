from Module import Module

class domain(Module):
    opmap = {
        'greeting':     'descend',
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
        'ns':           'descend',
        'authInfo':     'descend',
        'name':         'set',
        'roid':         'set',
        'clID':         'set',
        'crID':         'set',
        'upID':         'set',
        'crDate':       'set',
        'upDate':       'set',
        'exDate':       'set',
        'pw':           'set',
        'registrant':   'set',
    }

    def parse_cd(self, tag):
        avails  = self.response.get('avails', {})
        reasons = self.response.get('reasons', {})
        name    = self.find(tag, 'domain:name')
        reason  = self.find(tag, 'domain:reason')
        avails[name.text] = name.attrib['avail']
        if reason is not None:
            reasons[name.text] = reason.text
        self.set('avails',  avails)
        self.set('reasons', reasons)

    def parse_status(self, tag):
        status = tag.attrib['s']
        statuses = self.response.get('statuses', {})
        statuses[status] = status
        self.set('statuses', statuses)

    def parse_hostObj(self, tag):
        ns = tag.text.lower()
        nss = self.response.get('nss', {})
        nss[ns] = ns
        self.set('nss', nss)

    def parse_host(self, tag):
        host = tag.text.lower()
        hosts = self.response.get('hosts', {})
        hosts[host] = host
        self.set('hosts', hosts)

    def parse_contact(self, tag):
        self.set(tag.attrib['type'], tag.text)

