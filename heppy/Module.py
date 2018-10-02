
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

    def parse_add_list(self, response, tag):
        response.add_list(tag.tag.split('}')[1] + 's', tag.text)

    def parse_addpair(self, response, tag):
        response.addpair(tag.tag.split('}')[1] + 's', tag.text)

    def parse_descend(self, response, tag):
        for child in tag:
            response.parse(child)

    def parse_status(self, response, tag):
        response.addto('statuses', {tag.attrib['s']: tag.text})

    def parse_cd_tag(self, response, tag):
        name = tag[0]
        response.addto('avails', {name.text.lower(): name.attrib['avail']})
        if len(tag)>1:
            response.addto('reasons', {name.text.lower(): tag[1].text})

### REQUEST rendering

    def render_epp(self, request):
        if request.epp is None:
            request.epp = request.add_tag('epp', {'xmlns': request.get_module('epp').xmlns})
        return request.epp

    def render_clTRID(self, request):
        clTRID = request.get('clTRID', 'AA-00')
        if clTRID != 'NONE' and request.command is not None:
            request.add_subtag(request.command, 'clTRID', {}, clTRID)

    def render_root_command(self, request, command, attrs={}):
        if request.command is None:
            epp = self.render_epp(request)
            request.command = request.add_subtag(epp, 'command')
        return request.add_subtag(request.command, command, attrs)

    def render_header(self, request, source, action):
        return request.add_subtag(source, self.name + ':' + action, {'xmlns:' + self.name: self.xmlns})

    def render_command(self, request, action, attrs={}):
        command = self.render_root_command(request, action, attrs)
        return self.render_header(request, command, action)

    def render_command_fields(self, request, command, fields={'name': {}}, attrs={}):
        command = self.render_command(request, command, attrs)
        request.add_subtags(command, fields)
        return command

    def render_check_command(self, request, mod, field):
        command = self.render_command(request, 'check')
        for name in request.get(field + 's'):
            request.add_subtag(command, mod + ':' + field, text=name)
        return command

    def render_auth_info(self, request, parent, pw=None, attrs={}):
        if pw is None:
            pw = request.get('pw', '')
        authInfo = request.add_subtag(parent, self.name + ':authInfo')
        request.add_subtag(authInfo, self.name + ':pw', attrs, pw)

    def render_statuses(self, request, parent, status_data):
        for status, description in status_data.iteritems():
            request.add_subtag(parent, self.name + ':status', {'s': status}, description)

    def render_root_extension(self, request):
        if request.extension is None:
            request.extension = request.add_subtag(request.command, 'extension')
        return request.extension

    def render_extension(self, request, action):
        extension = self.render_root_extension(request)
        return self.render_header(request, extension, action)

    def render_extension_fields(self, request, action, fields):
        extension = self.render_extension(request, action)
        request.add_subtags(extension, fields)
        return extension
