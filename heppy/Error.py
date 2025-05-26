# -*- coding: utf-8 -*-

import logging


class Error(Exception):
    def __init__(self, message, data = {}):
        self.message = message
        self.data = data

    def __str__(self):
        return self.message + ": " + repr(self.data)

    @staticmethod
    def die(code, error, message = None):
        if isinstance(error, Exception):
            e = error
            error = '{0}.{1}'.format(type(e).__module__, type(e).__name__)
            message = str(e)
        print('Error: ' + error)
        if message:
            print(message)
        #logging.exception(message)
        exit(code)

