from Module import Module

class rgp(Module):
    opmap = {
        'infData':      'descend',
    }

    def parse_rgpStatus(self, tag):
        status = tag.attrib['s']
        self.set(status, tag.text)

