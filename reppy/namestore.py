from Module import Module

class namestore(Module):
    opmap = {
        'nsExtErrData': 'descend',
    }

    def parse_msg(self, tag):
        if 'code' in tag.attrib:
            self.set('nsExtErr.code', tag.attrib['code'])
        self.set('nsExtErr.msg', tag.text)

