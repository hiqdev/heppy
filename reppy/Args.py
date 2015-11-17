import re
import sys

def parse():
    if len(sys.argv)<3:
        print('usage: {0} path command -o1=v1 ..'.format(sys.argv[0]))
        exit(1)

    data = {}
    args = sys.argv
    data['zcmd']    = args.pop(0)
    data['path']    = args.pop(0)
    data['command'] = args.pop(0)

    for raw in args:
        m = re.match(r'^-(\S+)=(.*)$', raw)
        if m:
            name = m.group(1)
            if name.find('.')>0:
                f, s = name.split('.', 1)
                if not f in data:
                    data[f] = {}
                data[f][s] = m.group(2)
            else:
                data[name] = m.group(2)

    return data
