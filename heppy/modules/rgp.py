from ..Module import Module
from ..TagData import TagData


class rgp(Module):
    opmap = {
        'infData':      'descend',
    }

    def parse_rgpStatus(self, response, tag):
        status = tag.attrib['s']
        response.set(status, tag.text)

    def render_default(self, request, data):
        ext = self.render_extension(request, 'update')
        request.add_subtag(ext, 'rgp:restore', { 'op': 'request'})

    def render_request(self, request, data):
        return self.render_default(request, data)

    def render_report(self, request, data):
        ext = self.render_extension(request, 'update')
        restore = request.add_subtag(ext, 'rgp:restore', { 'op': 'report'})
        report = request.add_subtag(restore, 'rgp:report')
        request.add_subtag(report, 'rgp:preData', {}, data.get('preData'))
        request.add_subtag(report, 'rgp:postData', {}, data.get('postData'))
        request.add_subtag(report, 'rgp:delTime', {}, data.get('delTime'))
        request.add_subtag(report, 'rgp:resTime', {}, data.get('resTime'))
        request.add_subtag(report, 'rgp:resReason', {}, data.get('resReason', 'Registrant error'))
        request.add_subtag(report, 'rgp:statement', {}, data.get('statement', 'This registrar has not restored the Registered Name in order to assume the rights to use or sell the Registered Name for itself or for any third party'))
        request.add_subtag(report, 'rgp:statement', {}, data.get('statement', 'The information in this report is true to best of this registrar\'s knowledge, and this registrar acknowledges that intentionally supplying false information in this report shall constitute an incurable material breach of the Registry-Registrar Agreement'))

