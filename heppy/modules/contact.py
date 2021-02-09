from ..Module import Module
from ..TagData import TagData


class contact(Module):
    opmap = {
        'infData':      'descend',
        'chkData':      'descend',
        'creData':      'descend',
        'authInfo':     'descend',
        'addr':         'descend',
        'panData':      'descend',
        'paTRID':       'descend',
        'paDate':       'set',
        'id':           'set',
        'roid':         'set',
        'name':         'set',
        'org':          'set',
        'street':       'set',
        'city':         'set',
        'pc':           'set',
        'sp':           'set',
        'cc':           'set',
        'email':        'set',
        'voice':        'set',
        'fax':          'set',
        'clID':         'set',
        'crID':         'set',
        'upID':         'set',
        'crDate':       'set',
        'upDate':       'set',
        'trDate':       'set',
        'pw':           'set',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'contact'

### RESPONSE parsing

    def parse_cd(self, response, tag):
        return self.parse_cd_tag(response, tag)

    def parse_postalInfo(self, response, tag):
        type = tag.attrib['type']
        data = self.parse_descend_local(response, tag)
        response.put_to_dict(type, data)

    def parse_set_local(self, response, tag):
        return tag.text

    def parse_descend_local(self, response, tag):
        data = {}
        for child in tag:
            tagname = child.tag.replace('{' + self.xmlns + '}', '')
            if (self.opmap.get(tagname, None) != None):
                if (self.opmap.get(tagname) == 'descend') :
                    d = self.parse_descend_local(response, child)
                    data[tagname] = d
                else :
                    d = self.parse_descend_local(response, child)
                    data[tagname] =  self.parse_set_local(response, child)
        return data

    def parse_disclose(self, response, tag):
        flag = tag.attrib['flag']
        data = {'flag' : flag}
        for child in tag:
            tagname = child.tag.replace('{' + self.xmlns + '}', '')
            tagtype = child.get('type', None)
            if (tagtype is None):
                data[tagname] = flag
            else :
                if (data.get(tagtype, None) is None):
                    data[tagtype] = {}
                data[tagtype][tagname] = flag

        response.put_to_dict('disclose', data)


### REQUEST rendering

    def render_check(self, request, data):
        return self.render_check_command(request, data, 'id')

    def render_info(self, request, data):
        command = self.render_command_with_fields(request, 'info', [
            TagData('id', data.get('id'))
        ])
        if 'pw' in data:
            self.render_auth_info(request, command, data.get('pw'))

    def render_create(self, request, data):
        command = self.render_command_with_fields(request, 'create', [
            TagData('id', data.get('id'))
        ])

        self.render_postal_info(request, data, command)
        self.render_contact_info(request, data, command)

        if 'pw' in data:
            self.render_auth_info(request, command, data.get('pw'))

    def render_delete(self, request, data):
        self.render_command_with_fields(request, 'delete', [
            TagData('id', data.get('id'))
        ])

    def render_update(self, request, data):
        command = self.render_command_with_fields(request, 'update', [
            TagData('id', data.get('id'))
        ])

        if 'add' in data:
            self.render_update_section(request, data, command, 'add')
        if 'rem' in data:
            self.render_update_section(request, data, command, 'rem')
        if 'chg' in data:
            chg = request.add_subtag(command, 'contact:chg')
            chg_data = data.get('chg')
            self.render_postal_info(request, chg_data, chg)
            self.render_contact_info(request, chg_data, chg)
            if 'pw' in chg_data:
                self.render_auth_info(request, chg, chg_data['pw'])
            if 'disclose' in chg_data:
                self.render_disclose(request, chg_data['disclose'], chg)

    def render_update_section(self, request, data, command, operation):
        element = request.add_subtag(command, 'contact:' + operation)
        data = data.get(operation)
        if 'statuses' in data:
            self.render_statuses(request, element, data['statuses'])

    def render_postal_info(self, request, data, parent):
        attrs = {'type': data.get('type', 'int')}
        postal_info = request.add_subtag(parent, 'contact:postalInfo', attrs)
        if 'name' in data:
            request.add_subtag(postal_info, 'contact:name', text=data.get('name'))
        if 'org' in data:
            request.add_subtag(postal_info, 'contact:org', text=data.get('org'))
        self.render_addr(request, postal_info, data)

    def render_addr(self, request, parent, data):
        addr = request.add_subtag(parent, 'contact:addr')

        if 'street1' in data:
            request.add_subtag(addr, 'contact:street', text=data.get('street1'))
        if 'street2' in data:
            request.add_subtag(addr, 'contact:street', text=data.get('street2'))
        if 'street3' in data:
            request.add_subtag(addr, 'contact:street', text=data.get('street3'))

        if 'city' in data:
            request.add_subtag(addr, 'contact:city', text=data.get('city'))

        if 'sp' in data:
            request.add_subtag(addr, 'contact:sp', text=data.get('sp'))
        if 'pc' in data:
            request.add_subtag(addr, 'contact:pc', text=data.get('pc'))
        request.add_subtag(addr, 'contact:cc', text=data.get('cc'))

    def render_contact_info(self, request, data, parent):
        if 'voice' in data:
            request.add_subtag(parent, 'contact:voice', text=data.get('voice'))
        if 'fax' in data:
            request.add_subtag(parent, 'contact:fax', text=data.get('fax'))
        if 'email' in data:
            request.add_subtag(parent, 'contact:email', text=data.get('email'))

    def render_disclose(self, request, data, parent):
        disclose = request.add_subtag(parent, 'contact:disclose', {"flag": data})
        request.add_subtag(disclose, 'contact:name', {"type": "int"})
        request.add_subtag(disclose, 'contact:name', {"type": "loc"})
        request.add_subtag(disclose, 'contact:org', {"type": "int"})
        request.add_subtag(disclose, 'contact:org', {"type": "loc"})
        request.add_subtag(disclose, 'contact:addr', {"type": "int"})
        request.add_subtag(disclose, 'contact:addr', {"type": "loc"})
        request.add_subtag(disclose, 'contact:voice')
        request.add_subtag(disclose, 'contact:fax')
        request.add_subtag(disclose, 'contact:email')
        return request
#       self.render_command_with_fields(parent, 'disclose', [
#           TagData('name', attrs={"type":"int"}),
#           TagData('name', attrs={"type":"loc"}),
#           TagData('org', attrs={"type":"int"}),
#           TagData('org', attrs={"type":"loc"}),
#           TagData('addr', attrs={"type":"loc"}),
#           TagData('addr', attrs={"type":"int"}),
#           TagData('voice'),
#           TagData('fax'),
#       ], {"flag" : data})
