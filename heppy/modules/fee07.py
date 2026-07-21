# -*- coding: utf-8 -*-

from ..TagData import TagData
from .fee import fee

class fee07(fee):
    # Pre-RFC-8748 draft behaviour (draft-brown-epp-fees, roughly fee-0.5
    # through fee-0.9): <fee:check> wraps the queried object in a single
    # <fee:domain>, keyed by <fee:name> — not fee's <fee:objID>/nested
    # <fee:command>. These drafts also still extended <info> (dropped by the
    # time of fee10/fee11/fee12 — confirmed rejected by a real registry:
    # "no declaration ... for element 'fee:info'"). fee05, fee06, fee08 and
    # fee09 (which further overrides parse_cd/render_check for its own
    # object/objID shape) inherit from here rather than from fee directly so
    # they keep this <info> support.
    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag)

    def parse_infData(self, response, tag):
        self.parse_extension_block(response, 'fee:info', tag, {
            'currency': ['currency'],
            'fee':      ['fee'],
            'action':   ['action'],
            'period':   ['period'],
        })

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        domain = request.add_subtag(ext, 'fee:domain')
        request.add_subtag(domain, 'fee:name',      {}, data.get('name'))
        request.add_subtag(domain, 'fee:currency',  {}, data.get('currency', 'USD'))
        commandprop = {}
        if data.get('phase', None) is not None:
            commandprop.update({"phase" : data.get('phase')})
        if data.get('subphase', None) is not None:
            commandprop.update({"subphase" : data.get('subphase')})
        request.add_subtag(domain, 'fee:command',   commandprop, data.get('action', 'create'))
        request.add_subtag(domain, 'fee:period',    {'unit': data.get('unit', 'y')}, data.get('period', '1'))

    def render_info(self, request, data):
        self.render_extension_with_fields(request, 'info', [
            TagData('currency', data.get('currency')),
            TagData('command', data.get('action', 'create'), {
                'phase': data.get('phase'),
                'subphase': data.get('subphase'),
            }),
            TagData('period', data.get('period', 1), {
               'unit': data.get('unit', 'y')
            }),
        ])
