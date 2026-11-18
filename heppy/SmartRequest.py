# -*- coding: utf-8 -*-

import json
import logging
from enum import Enum
from heppy.Request import Request
from heppy.Response import Response

ERROR_KIND_KEY = '_error_kind'
CONNECTION_ERROR = 'connection'


class SmartRequest():

    def __init__(self, input):
        self.input      = input
        self.query      = None
        self.type       = None

    def get_query(self):
        if self.query is None:
            self.query = self.prepare_query()
        return self.query

    def prepare_query(self):
        if self.is_json():
            return self.query_from_dict(json.loads(self.input))
        elif self.is_dict():
            return self.query_from_dict(self.input)
        elif self.is_xml():
            return self.input
        else:
            raise Exception('it was expected to be impossible')

    def is_xml(self):
        return self.get_type() == Type.XML

    def is_json(self):
        return self.get_type() == Type.JSON

    def is_dict(self):
        return self.get_type() == Type.DICT

    def get_type(self):
        if self.type is None:
            self.type = self.detect_type()
        return self.type

    def detect_type(self):
        if isinstance(self.input, dict):
            return Type.DICT
        self.input = str(self.input)
        if self.input.startswith('{'):
            return Type.JSON
        self.query = self.input
        return Type.XML

    def query_from_dict(self, data):
        return str(Request.build(data))

    def perform(self, request, relogin = None):
        try:
            query = self.get_query()

            reply = request(query)
            if relogin is None:
                return self.prepare_response(reply)

            response = Response.parsexml(reply)
            self.log_authorization_error(query, reply, response)
            if self.needs_relogin(response):
                response = None
                relogin()
                reply = request(query)
            return self.prepare_response(reply, response)
        except Exception as e:
            return self.prepare_error(e)

    @staticmethod
    def log_authorization_error(query, reply, response):
        """Log a 2201 with the request (passwords masked) and the raw reply.

        A registry may answer 2201 for reasons that are not about the object
        (e.g. a session or account restriction), and the reason is often only
        in the reply's extValue. Callers get just result_code and msg, so the
        raw reply (with svTRID, to quote to the registry) is kept here.
        """
        if response.data.get('result_code') != '2201':
            return
        logging.warning(
            'EPP 2201 %s: %s\nrequest:\n%s\nreply:\n%s',
            response.data.get('svTRID', '-'),
            ' / '.join(str(response.data.get(key)) for key in ('result_msg', 'result_reason') if response.data.get(key)),
            Request.mask_passwords(query if isinstance(query, str) else query.decode('utf-8')),
            reply if isinstance(reply, str) else reply.decode('utf-8'),
        )

    def needs_relogin(self, response):
        if (response.data.get('result_code', '0') in ['2002', '2200', '2500', '2501', '2502']) :
            return True
        return False

    def prepare_error(self, error):
        message = str(error)
        if self.is_xml():
            return message
        data = {'_error': message}
        if isinstance(error, OSError):
            data[ERROR_KIND_KEY] = CONNECTION_ERROR
        if self.is_dict():
            return data
        if self.is_json():
            return json.dumps(data)

    def prepare_response(self, xml, response = None):
        if self.is_xml():
            return xml
        if response is None:
            response = Response.parsexml(xml)
        if self.is_dict():
            return response.data
        if self.is_json():
            return json.dumps(response.data)

    def parse_response(self, xml, response):
        return response.data

class Type(Enum):
    XML = 1
    JSON = 2
    DICT = 3
