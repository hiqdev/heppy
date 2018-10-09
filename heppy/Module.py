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

    def render_clTRID(self, request, data):
        clTRID = data.get('clTRID', 'AA-00')
        if clTRID != 'NONE' and request.command is not None:
            request.add_subtag(request.command, 'clTRID', text=clTRID)

    def render_root_command(self, request, command, attrs={}):
        if request.command is None:
            epp = self.render_epp(request)
            request.command = request.add_subtag(epp, 'command')
        return request.add_subtag(request.command, command, attrs)

    def render_header(self, request, parent, command, attrs={}):
        header_attrs = {'xmlns:' + self.name: self.xmlns}
        if attrs:
            header_attrs.update(attrs)
        return request.add_subtag(parent, self.name + ':' + command, header_attrs)

    def render_command(self, request, command, attrs={}):
        command_tag = self.render_root_command(request, command, attrs)
        return self.render_header(request, command_tag, command)

    def render_command_with_fields(self, request, command, fields, attrs={}):
        command = self.render_command(request, command, attrs)
        request.add_subtags(command, fields)
        return command

    def render_check_command(self, request, data, field):
        command = self.render_command(request, 'check')
        for name in data.get(field + 's'):
            request.add_subtag(command, self.name + ':' + field, text=name)
        return command

    def render_auth_info(self, request, parent, pw='', attrs={}):
        authInfo = request.add_subtag(parent, self.name + ':authInfo')
        request.add_subtag(authInfo, self.name + ':pw', attrs, pw)

    def render_statuses(self, request, parent, status_data):
        for status, description in status_data.iteritems():
            request.add_subtag(parent, self.name + ':status', {'s': status}, description)

    def render_root_extension(self, request):
        if request.extension is None:
            request.extension = request.add_subtag(request.command, 'extension')
        return request.extension

    def render_extension(self, request, action, attrs={}):
        extension = self.render_root_extension(request)
        return self.render_header(request, extension, action, attrs)

    def render_extension_with_fields(self, request, command, fields, attrs={}):
        extension = self.render_extension(request, command, attrs)
        request.add_subtags(extension, fields)
        return extension
