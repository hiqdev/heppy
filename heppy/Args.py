import re
import sys

class Args(dict):
    def __init__(self):
        if len(sys.argv)<3:
            print('usage: {0} path command -o1=v1 ..'.format(sys.argv[0]))
            exit(1)

        args = sys.argv
        self['zcmd']    = args.pop(0)
        self['path']    = args.pop(0)
        self['command'] = args.pop(0)
        self['zdir'], self['zbin'] = self['zcmd'].rsplit('/', 1)

        for raw in args:
            m = re.match(r'^-(\S+)=(.*)$', raw)
            if m:
                name = m.group(1)
                if name.find('.')>0:
                    f, s = name.split('.', 1)
                    if not f in self:
                        self[f] = {}
                    self[f][s] = m.group(2)
                else:
                    self[name] = m.group(2)

