# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData

class fee(Module):
    opmap = {
        'domain':       'set',
        'currency':     'set',
        'action':       'set',
        'period':       'set',
        'fee':          'set',
        # Per draft-brown-epp-fees (fee-0.5 through at least fee-0.12), a
        # <fee:chkData> response MUST contain one <fee:cd> per checked
        # object, mirroring domain:chkData/domain:cd — never fields directly
        # under chkData. Descend into each <fee:cd> and dispatch to parse_cd
        # instead of trying (and failing) to read fields off chkData itself.
        'chkData':      'descend',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'fee'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag_extension(response, tag)

    def parse_cd_nested_command(self, response, tag, object_id=False,
                                 command_text_fallback=False, lowercase=False,
                                 always_store=False):
        """Shared parser for the <fee:cd> shape where price fields nest
        inside <fee:command name="..."> (fee10-fee12, fee21/fee23) — each
        draft revision differs only in how the checked object is identified
        and whether attribute values get lowercased.

        object_id: True for a plain-text <fee:objID> (fee10, fee21); False
            for <fee:object><domain:name>...</domain:name></fee:object>
            (fee11, fee12).
        command_text_fallback: also accept <fee:command>name-as-text</fee:command>
            with no "name" attribute — confirmed against a real registry for
            fee-0.11's response; other versions only ever send the
            name-attribute form.
        lowercase: lowercase captured attribute values (fee10, fee12).
        always_store: always call put_to_dict, defaulting the key to
            'domain' if no identifier was found (fee10's historical
            behaviour); other versions skip storing when the identifier is
            missing.
        """
        data = {}
        domain_xmlns = 'urn:ietf:params:xml:ns:domain-1.0'

        def norm(value):
            return value.lower() if lowercase else value

        key_field = 'objID' if object_id else 'name'
        for child in tag:
            tagname = child.tag.replace('{' + self.xmlns + '}', '')
            if not object_id and tagname == 'object':
                name_el = child.find('{%s}name' % domain_xmlns)
                if name_el is not None and name_el.text:
                    data['name'] = name_el.text.strip()
            elif tagname == 'command':
                if 'name' in child.attrib:
                    data['command'] = child.attrib['name']
                elif command_text_fallback and child.text is not None and child.text.strip():
                    data['command'] = child.text.strip()
                for cmd_child in child:
                    cmd_tagname = cmd_child.tag.replace('{' + self.xmlns + '}', '')
                    if cmd_child.text is not None:
                        data[cmd_tagname] = cmd_child.text.strip()
                    for attr_name, attr_value in cmd_child.attrib.items():
                        if attr_value is not None:
                            data[attr_name.lower()] = norm(attr_value)
            elif child.text is not None:
                data[tagname] = child.text.strip()
                for attr_name, attr_value in child.attrib.items():
                    if attr_value is not None:
                        data[attr_name.lower()] = norm(attr_value)
            else:
                for attr_name, attr_value in child.attrib.items():
                    if attr_value is not None:
                        data[attr_name.lower()] = norm(attr_value)
        if 'avail' in tag.attrib:
            data['avail'] = tag.attrib['avail'].lower()
        if always_store:
            response.put_to_dict(self.name, {data.get(key_field, 'domain'): data})
        elif key_field in data:
            response.put_to_dict(self.name, {data[key_field]: data})

    def parse_infData(self, response, tag):
        self.parse_extension_block(response, 'fee:info', tag, {
            'currency': ['currency'],
            'fee':      ['fee'],
            'action':   ['action'],
            'period':   ['period'],
        })

    def parse_delData(self, response, tag):
        self.parse_extension_block(response, 'fee:delete', tag, {
            'currency': ['currency'],
            'credit':   ['credit'],
        })

    def parse_trnData(self, response, tag):
        self.parse_typical_tag(response, tag, 'fee:transfer')

    def parse_creData(self, response, tag):
        self.parse_typical_tag(response, tag, 'fee:create')

    def parse_renData(self, response, tag):
        self.parse_typical_tag(response, tag, 'fee:renew')

    def parse_updData(self, response, tag):
        self.parse_typical_tag(response, tag, 'fee:update')

    def parse_typical_tag(self, response, tag, command):
        self.parse_extension_block(response, command, tag, {
            'currency': ['currency'],
            'fee':      ['fee'],
        })

    def parse_extension_block(self, response, command, tag, fields):
        data = {'command': command}
        for key, tag_names in fields.items():
            for tag_name in tag_names:
                child = tag.find('{%s}%s' % (self.xmlns, tag_name))
                if child is None:
                    continue
                data[key] = child.text.strip() if child.text is not None else None
                for attr_name, attr_value in child.attrib.items():
                    if attr_name in data:
                        data.setdefault('attributes', {})[attr_name] = attr_value
                    else:
                        data[attr_name] = attr_value
                break
        response.put_to_list('extensions', data)

### REQUEST rendering

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        domain = request.add_subtag(ext, 'fee:domain')
        request.add_subtag(domain, 'fee:name',      {}, data.get('name'))
        request.add_subtag(domain, 'fee:currency',  {}, data.get('currency', 'USD'))
        commandprop = {}
        if (data.get('phase', None) != None) :
            commandprop.update({"phase" : data.get('phase')})
        if (data.get('subphase', None) != None) :
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

    def render_create(self, request, data):
        self.render_extension_with_fields(request, 'create', [
            TagData('currency', data.get('currency')),
            TagData('fee', data.get('fee'))
        ])

    def render_renew(self, request, data):
        self.render_extension_with_fields(request, 'renew', [
            TagData('currency', data.get('currency')),
            TagData('fee', data.get('fee')),
        ])

    def render_transfer(self, request, data):
        self.render_extension_with_fields(request, 'transfer', [
            TagData('currency', data.get('currency', 'USD')),
            TagData('fee', data.get('fee')),
        ])
