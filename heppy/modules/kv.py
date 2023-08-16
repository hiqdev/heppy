from ..Module import Module
from ..TagData import TagData


class kv(Module):
    opmap = {
        'infData':  'descend',
    }

    def __init__(self, xmlns):
        Module.__init__(self, xmlns)
        self.name = 'kv'

### RESPONSE parsing
    def parse_kvlist(self, response, tag):
        data = {}
        for child in tag:
            for name, value in child.attrib.items():
                data.update({value.lower(): child.text.lower()})
        response.put_to_dict(self.name, data)

### REQUEST rendering

