# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData

class keysys(Module):
    opmap = {
        'resData':      'descend',
        'infData':      'descend',
        'creData':      'descend',
        'renDate':      'set',
        'punDate':      'set',
        'domain-roid':  'set',
        'renewalmode':  'set',
        'transfermode': 'set',
        'transferlock': 'set',
        'contactInfData':'descend',
        'validated':    'set',
        'ren': 'set',
        'verification-requested': 'set',
        'verified': 'set',
        'whois-privacy': 'set',
        'es-admin-identificacion': 'set',
        'de-accept-trustee-tac': 'set',
        'es-admin-legalform': 'set',
        'es-admin-tipo-identificacion': 'set',
        'es-billing-identificacion': 'set',
        'es-billing-tipo-identificacion': 'set',
        'es-billing-legalform': 'set',
        'es-tech-identificacion': 'set',
        'es-tech-tipo-identificacion': 'set',
        'es-tech-legalform': 'set',
        'es-owner-identificacion': 'set',
        'es-owner-tipo-identificacion': 'set',
        'es-owner-legalform': 'set',
        'travel-uin': 'set',
        'real-submit': 'set',
        'pro-authority': 'set',
        'pro-authority-website': 'set',
        'pro-license-number': 'set',
        'pro-av-license-authority-website': 'set',
        'pro-profession': 'set',
        'pro-av-license-holder-birthdate': 'set',
        'pro-av-license-iso-countrycode': 'set',
        'pro-av-license-issue-date': 'set',
        'pro-av-professiontype': 'set',
        'de-nsentry': 'set',
        'ownerchangestatus': 'set',
        'be-requestauthcode': 'set',
        'dnsbe-contact-type': 'set',
        'old-nameserver0': 'set',
        'old-nameserver1': 'set',
        'old-nameserver2': 'set',
        'old-nameserver3': 'set',
        'time-to-suspension': 'set',
        'eu-accept-trustee-tac': 'set',
        'eu-naturalperson': 'set',
        'cn-accept-trustee-tac': 'set',
        'cn-owner-id-number': 'set',
        'cn-owner-id-type': 'set',
        'cn-owner-type': 'set',
        'idn-language': 'set',
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
        ext = self.render_extension(request, 'create')
        domain = request.add_subtag(ext, 'keysys:domain')
        if (data.get('eu-accept-trustee-tac', None) != None):
            request.add_subtag(domain, 'keysys:eu-accept-trustee-tac', {}, data.get('eu-accept-trustee-tac'))

    def render_transfer(self, request, data):
        if (data.get('eu-accept-trustee-tac', None) != None):
            ext = self.render_extension(request, 'transfer')
            domain = request.add_subtag(ext, 'keysys:domain')
            request.add_subtag(domain, 'keysys:eu-accept-trustee-tac', {}, data.get('eu-accept-trustee-tac'))
            request.add_subtag(domain, 'keysys:ownercontact0', {}, data.get('registrant'))

    def render_update(self, request, data):
        ext = self.render_extension(request, 'update')
        domain = request.add_subtag(ext, 'keysys:domain')
#        request.add_subtag(domain, 'keysys:accept-trade', {}, '1')

    def render_delete(self, request, data):
        ext = self.render_extension(request, 'delete')
        domain = request.add_subtag(ext, 'keysys:domain')
        request.add_subtag(domain, 'keysys:action', {}, 'push')
        request.add_subtag(domain, 'keysys:target', {}, data.get('target', 'TRANSIT'))

    def render_whoisprotect(self, request, data):
        ext = self.render_extension(request, 'update')
        domain = request.add_subtag(ext, 'keysys:domain')
        request.add_subtag(domain, 'keysys:whois-privacy', {}, data.get('whois-privacy', u'0'))
