import re
import sys
import copy

class Args(dict):
    def __init__(self):
        if len(sys.argv)<3:
            print('usage: {0} path command -o1=v1 ..'.format(sys.argv[0]))
            exit(1)

        args = copy.deepcopy(sys.argv)
        self['zcmd']    = args.pop(0)
        self['path']    = args.pop(0)
        self['command'] = args.pop(0)
        self['zdir'], self['zbin'] = self['zcmd'].rsplit('/', 1)

        no=0
        for raw in args:
            m = re.match(r'^-(\S+?)=(.*)$', raw)
            if m:
                name = m.group(1)
                if name.find('.')>0:
                    f, i, s = name.split('.', 2)
                    i = int(i)
                    if not f in self:
                        self[f] = []
                    if len(self[f]) < i+1:
                        self[f].append({})
                    self[f][i][s] = m.group(2)
                else:
                    self[name] = m.group(2)
            else:
                self[no] = raw
                no += 1


