# -*- coding: utf-8 -*-

from .fee import fee

class fee21(fee):
    # Per draft-ietf-regext-epp-fees, <fee:cd> identifies the checked object
    # with a plain-text <fee:objID> (not fee11/12's <fee:object><domain:name>,
    # nor a bare <fee:name>) and nests price fields inside <fee:command
    # name="...">, not as siblings of it. fee.parse_cd (parse_cd_tag_extension)
    # only reads direct children of <cd> and keys the result on 'name', so it
    # neither finds objID under 'name' nor descends into <command> — it must
    # not be inherited unchanged here.
    def parse_cd(self, response, tag):
        data = {}
        for child in tag:
            tagname = child.tag.replace('{' + self.xmlns + '}', '')
            if tagname == 'command':
                if 'name' in child.attrib:
                    data['command'] = child.attrib['name']
                for cmd_child in child:
                    cmd_tagname = cmd_child.tag.replace('{' + self.xmlns + '}', '')
                    if cmd_child.text is not None:
                        data[cmd_tagname] = cmd_child.text.strip()
                    for attr_name, attr_value in cmd_child.attrib.items():
                        if attr_value is not None:
                            data[attr_name.lower()] = attr_value
            elif child.text is not None:
                data[tagname] = child.text.strip()
                for attr_name, attr_value in child.attrib.items():
                    if attr_value is not None:
                        data[attr_name.lower()] = attr_value
            else:
                for attr_name, attr_value in child.attrib.items():
                    if attr_value is not None:
                        data[attr_name.lower()] = attr_value
        if 'avail' in tag.attrib:
            data['avail'] = tag.attrib['avail'].lower()
        if 'objID' in data:
            response.put_to_dict(self.name, {data['objID']: data})

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency',  {}, data.get('currency', 'USD'))
        request.add_subtag(ext, 'fee:command', {'name': data.get('action', 'create')})
