from ..Module import Module

class rgp(Module):
    opmap = {
        'infData':      'descend',
    }

    def parse_rgpStatus(self, response, tag):
        status = tag.attrib['s']
        response.set(status, tag.text)

