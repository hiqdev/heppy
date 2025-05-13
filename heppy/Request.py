import xml.dom.minidom
import xml.etree.ElementTree as ET

from pprint import pprint
from heppy.Doc import Doc


class Request(Doc):

    def __init__(self):
        self.raw        = None
        self.epp        = None
        self.command    = None
        self.extension  = None

    def __str__(self, encoding='UTF-8', method='xml'):
        if self.raw is None:
            return self.toxml(encoding, method)
        else:
            return self.raw

    def toxml(self, encoding='UTF-8', method='xml'):
        return ET.tostring(self.epp, encoding, method)

    def add_tag(self, tag, attrs={}, text=None):
        res = ET.Element(tag, attrs)
        if text is not None:
            res.text = str(text)
        return res

    def add_subtag(self, parent, tag, attrs={}, text=None):
        res = ET.SubElement(parent, tag, attrs)
        if text is not None:
            res.text = str(text)
        return res

    def add_subtags(self, parent, tags):
        ns = parent.tag.split(':')[0]
        for tag in tags:
            if tag.value:
                self.add_subtag(parent, ns + ':' + tag.name, tag.attrs, tag.value)
        return parent

    @staticmethod
    def build(data):
        request = Request()
        request.render(data['command'], data)
        for extension in data.get('extensions', {}):
            request.render(extension['command'], extension)
        request.render('epp:clTRID', data)
        return request

    def render(self, command, data):
        if ':' in command:
            module_name, command_name = command.split(':')
        else:
            module_name = command
            command_name = 'default'
        module = self.get_module(module_name)
        method = 'render_' + command_name
        if not hasattr(module, method):
            raise Exception('unknown command',  command)
        getattr(module, method)(self, data)

    @staticmethod
    def prettifyxml(request):
        string = str(request)
        if string[0] != '<':
            return string
        dom = xml.dom.minidom.parseString(string)
        return dom.toprettyxml(indent='    ')
