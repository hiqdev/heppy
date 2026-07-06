# -*- coding: utf-8 -*-

from .fee11 import fee11

class fee12(fee11):
    def parse_cd(self, response, tag):
        data = {}
        domain_xmlns = 'urn:ietf:params:xml:ns:domain-1.0'
        for child in tag:
            tagname = child.tag.replace('{' + self.xmlns + '}', '')
            if tagname == 'object':
                name_el = child.find('{%s}name' % domain_xmlns)
                if name_el is not None and name_el.text:
                    data['name'] = name_el.text.strip()
            elif tagname == 'command':
                if 'name' in child.attrib:
                    data['command'] = child.attrib['name']
                for cmd_child in child:
                    cmd_tagname = cmd_child.tag.replace('{' + self.xmlns + '}', '')
                    if cmd_child.text is not None:
                        data[cmd_tagname] = cmd_child.text.strip()
                    for attr_name, attr_value in cmd_child.attrib.items():
                        if attr_value is not None:
                            data[attr_name.lower()] = attr_value.lower()
            elif child.text is not None:
                data[tagname] = child.text.strip()
                for attr_name, attr_value in child.attrib.items():
                    if attr_value is not None:
                        data[attr_name.lower()] = attr_value.lower()
            else:
                for attr_name, attr_value in child.attrib.items():
                    if attr_value is not None:
                        data[attr_name.lower()] = attr_value.lower()
        if 'avail' in tag.attrib:
            data['avail'] = tag.attrib['avail'].lower()
        if 'name' in data:
            response.put_to_dict(self.name, {data['name']: data})

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency', {}, data.get('currency', 'USD'))
        command = request.add_subtag(ext, 'fee:command', {'name': data.get('action', 'create')})
        request.add_subtag(command, 'fee:period', {'unit': data.get('unit', 'y')}, data.get('period', 1))
