# -*- coding: utf-8 -*-

from ..Module import Module
from ..TagData import TagData
from pprint import pprint
from fee09 import fee09


class fee10(fee09):

    opmap = {
        'chkData':      'descend',
        'currency':     'set',
        'period':       'set',
        'fee':          'set',
    }

    def parse_cd(self, response, tag):
        data = {}
        for child in tag :
            tagname = child.tag.replace('{' + self.xmlns + '}', '')
            if child.text is not None:
                data.update({tagname: child.text.lower()})
            for name, value in child.attrib.items():
                if value is not None:
                    data.update({name.lower() : value.lower()})
            if tagname == 'command':
                for cchild in child:
                    if cchild.text is not None:
                        ctagname = cchild.tag.replace('{' + self.xmlns + '}', '')
                        data.update({ctagname: cchild.text.lower()})

        return response.put_to_dict(self.name, {
             data['objID'] : data
         })

    def render_check(self, request, data):
        ext = self.render_extension(request, 'check')
        request.add_subtag(ext, 'fee:currency',  {}, data.get('currency', 'USD'))
        create_command = request.add_subtag(ext, 'fee:command', {'name': data.get('action', 'create')})
        request.add_subtag(create_command, 'fee:period', {'unit': 'y'}, 1)

