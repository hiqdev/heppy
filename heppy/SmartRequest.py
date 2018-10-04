#!/usr/bin/env python

import json
import sys
from enum import Enum
from pprint import pprint
from Request import Request
from Response import Response


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
        return str(Request.buildFromDict(data))

    def perform(self, request, relogin = None):
        try:
            query = self.get_query()
            reply = request(query)
            if relogin is None:
                return self.prepare_response(reply)

            ### TODO: FIXME relogin is buggy because of 2002 can happen on different occasions
            response = Response.parsexml(reply)
            if response.data.get('result_code', '0') == '2002':
                response = None
                relogin()
                reply = request(query)
            return self.prepare_response(reply, response)
        except Exception as e:
            return self.prepare_error(e)

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
            response = Response.parsexml(reply)
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
