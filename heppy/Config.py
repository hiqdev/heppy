#!/usr/bin/env python

import os
import sys
import json
import fcntl
import collections

# http://stackoverflow.com/questions/10703858
def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2.  If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    """
    for k,v2 in d2.items():
        v1 = d1.get(k) # returns None if v1 has no value for this key
        if (isinstance(v1, collections.Mapping)
        and isinstance(v2, collections.Mapping)):
            merge_dict(v1, v2)
        else:
            d1[k] = v2

class Config(dict):
    def __init__(self, filename, mustExist = True):
        self.abs_path = os.path.abspath(filename)
        self.bin_path = os.path.abspath(sys.argv[0])
        self.path = self.find_path(filename)
        self.file = None
        self.load(mustExist)

    def load(self, mustExist = True):
        try:
            with open(self.path) as file:
                jstr = file.read()
                #print self.path + ' ' + jstr
                if jstr:
                    self.merge(json.loads(jstr))
        except Exception as e:
            if mustExist:
                raise e

    def lock(self):
        self._open()
        try:
            fcntl.lockf(self.file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            pass
        except:
            return False
        return True

    def _open(self):
        if not self.file:
            self.file = open(self.path, 'w', 0)
        return self.file

    def exists(self):
        return os.path.isfile(self.path)

    def save(self):
        self.lock()
        self.file.write(json.dumps(self, indent=4))
        fcntl.lockf(self.file, fcntl.LOCK_UN)
        self._close()

    def _close(self):
        self.file.close()
        self.file = None

    def merge(self, data):
        merge_dict(self, data)

    def get_path(self, name):
        filename = self.get(name, '')
        return self.find_path(filename)

    def find_path(self, filename):
        if os.path.isfile(filename):
            return filename

        if '/' != filename[0]:
            filename = os.path.join(os.path.dirname(self.abs_path), filename)

        ext = os.path.splitext(filename)[1]

        if ext != '.json':
            return self.find_path(filename + '.json')

        return filename
