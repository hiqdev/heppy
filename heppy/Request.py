import xml.dom.minidom
import xml.etree.ElementTree as ET

from Doc import Doc

class Request(Doc):
    def __init__(self, data):
        self.data       = data
        self.raw        = None
        self.epp        = None
        self.command    = None
        self.extension  = None

    def __str__(self, encoding='UTF-8', method='xml'):
        if self.raw is None:
            return ET.tostring(self.epp, encoding, method)
        else:
            return self.raw

    def element(self, tag, attrs = {}, text = None):
        res = ET.Element(tag, attrs)
        if text is not None:
            res.text = str(text)
        return res

    def sub(self, parent, tag, attrs = {}, text = None):
        res = ET.SubElement(parent, tag, attrs)
        if text is not None:
            res.text = str(text)
        return res

    def subfields(self, parent, fields, values = None):
        name = parent.tag.split(':')[0]
        for field, attrs in fields.iteritems():
            value = self.get(field) if values is None else values.get(field)
            if value:
                self.sub(parent, name + ':' + field, attrs, value)
        return parent

    @staticmethod
    def build(command, data, extensions = {}):
        request = Request(data)
        request.render(command)
        for ext in extensions.itervalues():
            request.render(ext)
        request.render('epp:clTRID')
        return request

    @staticmethod
    def buildFromArgs(args):
        extensions = args.get('extensions') or {}
        if extensions == {} and 'extension' in args:
            extensions = {'0': args.get('extension')}
        return Request.build(args.get('command'), args, extensions)

    def render(self, command):
        ns = command.split(':')[0]
        name = command.split(':')[1]
        module = self.get_module(ns)
        method = 'render_' + name
        if not hasattr(module, method):
            raise Exception('unknown command', ns + ':' + name)
        getattr(module, method)(self)

    @staticmethod
    def prettifyxml(request):
        string = str(request)
        if string[0] != '<':
            return string
        dom = xml.dom.minidom.parseString(string)
        return dom.toprettyxml(indent='    ')

