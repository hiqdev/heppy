
from pprint import pprint

class Module:
    opmap = {}

    def __init__(self, xmlns):
        self.name   = self.__class__.__name__
        self.xmlns  = xmlns

### RESPONSE parsing

    def parse_nothing(self, response, tag):
        pass

    def parse_set(self, response, tag):
        response.set(tag.tag.split('}')[1], tag.text)

    def parse_addpair(self, response, tag):
        response.addpair(tag.tag.split('}')[1] + 's', tag.text)

    def parse_descend(self, response, tag):
        for child in tag:
            response.parse(child)

    def parse_status(self, response, tag):
        response.addpair('statuses', tag.attrib['s'])

    def parse_cd_tag(self, response, tag):
        name = tag[0]
        response.addto('avails', {name.text.lower(): name.attrib['avail']})
        if len(tag)>1:
            response.addto('reasons', {name.text.lower(): tag[1].text})

### REQUEST rendering

    def render_epp(self, request):
        if request.epp is None:
            request.epp = request.element('epp', {'xmlns': request.get_module('epp').xmlns})
        return request.epp

    def render_clTRID(self, request):
        clTRID = request.get('clTRID', 'AA-00')
        if clTRID != 'NONE' and request.command is not None:
            request.sub(request.command, 'clTRID', {}, clTRID)

    def render_root_command(self, request, command, attrs={}):
        if request.command is None:
            epp = self.render_epp(request)
            request.command = request.sub(epp, 'command')
        return request.sub(request.command, command, attrs)

    def render_header(self, request, source, action):
        return request.sub(source, self.name + ':' + action, {'xmlns:' + self.name: self.xmlns})

    def render_command(self, request, action, attrs={}):
        command = self.render_root_command(request, action, attrs)
        return self.render_header(request, command, action)

    def render_command_fields(self, request, command, fields={'name': {}}, attrs={}):
        command = self.render_command(request, command, attrs)
        request.subfields(command, fields)
        return command

    def render_check_command(self, request, mod, field):
        command = self.render_command(request, 'check')
        for name in request.get(field + 's').itervalues():
            request.sub(command, mod+':'+field, {}, name)
        return command

    def render_root_extension(self, request):
        if request.extension is None:
            request.extension = request.sub(request.command, 'extension')
        return request.extension

    def render_extension(self, request, action):
        extension = self.render_root_extension(request)
        return self.render_header(request, extension, action)

    def render_extension_fields(self, request, action, fields):
        extension = self.render_extension(request, action)
        request.subfields(extension, fields)
        return extension

