import xml.dom.minidom
import xml.etree.ElementTree as ET

from Doc import Doc

class Request(Doc):

    def __init__(self):
        # self.data           = data
        self.raw            = None
        self.epp            = None
        self.command        = None
        self.extension      = None
        # self.extension_data = None

    def __str__(self, encoding='UTF-8', method='xml'):
        if self.raw is None:
            return ET.tostring(self.epp, encoding, method)
        else:
            return self.raw

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

    def add_subtags(self, parent, fields, values=None):
        name = parent.tag.split(':')[0]
        for field, attrs in fields.iteritems():
            value = self.get(field) if values is None else values.get(field)
            if value:
                self.add_subtag(parent, name + ':' + field, attrs, value)
        return parent

    @staticmethod
    def build(data):
        request = Request()
        request.render(data['command'], data)
        for extension in data.get('extensions', {}):
            request.render(extension['command'], data['extension'])
        request.render('epp:clTRID', data)
        return request

    # @staticmethod
    # def buildFromDict(args):
    #     extensions = args.get('extensions') or {}
    #     if extensions == {} and 'extension' in args:
    #         extensions = {'0': args.get('extension')}
    #     return Request.build(args.get('command'), args, extensions)

    def render(self, command, data):
        module_name, command_name = command.split(':')
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
