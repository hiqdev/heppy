# -*- coding: utf-8 -*-

import json
import re
from enum import Enum
from heppy.Request import Request
from heppy.Response import Response


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
            if self.needs_relogin(response):
                response = None
                relogin()
                reply = request(query)
            return self.prepare_response(reply, response)
        except Exception as e:
            return self.prepare_error(e)

    RELOGIN_CODES = ['2002', '2200', '2500', '2501', '2502']

    def needs_relogin(self, response):
        code = response.data.get('result_code', '0')
        if code in self.RELOGIN_CODES:
            return True
        return code == '2201' and self.is_tld_authorization_error(response.data)

    @staticmethod
    def is_tld_authorization_error(data):
        """2201 that blames the TLD, not the object.

        A registry may drop a TLD from a live session's authorization
        (seen after maintenance: "Authorization error" / "Unauthorized TLD"
        for a TLD the account has served for years) while hello keeps
        working, so the session stays broken until the daemon restarts.
        A fresh login gets the TLD back. Any other 2201 (e.g. an object
        sponsored by another registrar) is a real answer and is returned
        as is. The rejected command was not executed, so it is safe to
        send it again once.
        """
        text = ' '.join(str(data.get(key) or '') for key in ('result_msg', 'result_reason'))
        return re.search(r'\btlds?\b', text, re.IGNORECASE) is not None

    def prepare_error(self, error):
        error = str(error)
        if self.is_xml():
            return error
        data = {'_error': error}
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
