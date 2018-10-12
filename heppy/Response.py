import xml.etree.ElementTree as ET
from Doc import Doc


class Response(Doc):
    def __init__(self, root):
        self.data = {}
        self.root = root
        self.parse(self.root[0])

    def find(self, tag, name):
        return tag.find(name, namespaces=self.nsmap)

    def findall(self, tag, name):
        return tag.findall(name, self.nsmap)

    def find_text(self, parent, name):
        tag = self.find(parent, name)
        if tag is not None:
            return tag.text.strip()

    def _put_attr(self, data, tag, attr):
        attr_value = tag.attrib.get(attr)
        if attr_value:
            data[attr] = attr_value

    def put_tag_data(self, dest, root, tag_name, attrs=[]):
        if '@' in tag_name:
            tag_name, key = tag_name.split('@')
        elif ':' in tag_name:
            key = tag_name.split(':')[1]
        else:
            key = tag_name
        tag = self.find(root, tag_name)
        if tag is None:
            return
        dest[key] = tag.text.strip()
        for attr in attrs:
            self._put_attr(dest, tag, attr)

    def put_extension_block(self, response, command, root_tag, tags_data):
        data = dict()
        data['command'] = command
        module_name = command.split(':')[0]
        for tag_name, attrs in tags_data.iteritems():
            response.put_tag_data(data, root_tag, module_name + ':' + tag_name, attrs)
        response.put_to_list('extensions', data)

    def put_to_dict(self, name, values):
        if name not in self.data:
            self.data[name] = {}
        for k, v in values.iteritems():
            self.data[name][k] = v

    def put_to_list(self, name, value=[]):
        if name not in self.data:
            self.data[name] = []
        if type(value) in [list, tuple]:
            self.data[name].extend(value)
        else:
            self.data[name].append(value)

    def parse(self, tag):
        ns = tag.tag.split('}')[0][1:]
        name = tag.tag.split('}')[1]
        module = self.get_module(ns)
        if name in module.opmap:
            name = module.opmap[name]
        method = 'parse_' + name
        if not hasattr(module, method):
            raise Exception('unknown tag', ns + ':' + name)
        getattr(module, method)(self, tag)

    @staticmethod
    def parsexml(xml):
        root = ET.fromstring(xml)
        return Response(root)

    @staticmethod
    def build(name, start):
        type = globals()[name]
        return type(start)

