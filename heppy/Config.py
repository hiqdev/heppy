#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import fcntl
from collections.abc import Mapping  # Updated for Python 3 compatibility

# http://stackoverflow.com/questions/10703858
def merge_dict(d1, d2):
    """
    Modifies d1 in-place to contain values from d2. If any value
    in d1 is a dictionary (or dict-like), *and* the corresponding
    value in d2 is also a dictionary, then merge them in-place.
    """
    for k, v2 in d2.items():
        v1 = d1.get(k)  # Returns None if v1 has no value for this key
        if isinstance(v1, Mapping) and isinstance(v2, Mapping):
            merge_dict(v1, v2)
        else:
            d1[k] = v2


class Config(dict):
    def __init__(self, filename, mustExist=True):
        self.abs_path = os.path.abspath(filename)
        self.bin_path = os.path.abspath(sys.argv[0])
        self.path = self.find_path(filename)
        self.file = None
        self.load(mustExist)

    def load(self, mustExist=True):
        try:
            with open(self.path, encoding="utf-8") as file:  # Explicit encoding
                jstr = file.read()
                if jstr:
                    self.merge(json.loads(jstr))
        except Exception as e:
            if mustExist:
                raise e

    def lock(self):
        self._open()
        try:
            fcntl.lockf(self.file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:  # Catch specific exception for non-blocking lock
            return False
        return True

    def _open(self):
        if not self.file:
            self.file = open(self.path, 'w', encoding="utf-8")  # Explicit encoding
        return self.file

    def exists(self):
        return os.path.isfile(self.path)

    def save(self):
        if self.lock():
            self.file.write(json.dumps(self, indent=4, ensure_ascii=False))  # Ensure UTF-8 compatibility
            fcntl.lockf(self.file, fcntl.LOCK_UN)
            self._close()

    def _close(self):
        if self.file:
            self.file.close()
        self.file = None

    def merge(self, data):
        merge_dict(self, data)

    def get_dir(self):
        return os.path.dirname(self.path)

    def get_path(self, name):
        filename = self.get(name, '')
        return self.find_path(filename)

    def find_path(self, filename):
        if os.path.isfile(filename):
            return filename

        if filename and not filename.startswith('/'):
            filename = os.path.join(os.path.dirname(self.abs_path), filename)

        ext = os.path.splitext(filename)[1]

        if ext != '.json':
            return self.find_path(filename + '.json')

        return filename
    