# -*- coding:utf-8 -*-

import json
from .stream import CallbackHandler, CallbackMessage

class GraphMessage(object):
    TOPIC = '/v1.0/graph/api/invoke'

class RequestLine(object):
    def __init__(self):
        self.method = 'GET'
        self.uri = '/'
        self.extensions = {}

    @classmethod
    def from_dict(cls, d):
        msg = RequestLine()
        for name, value in d.items():
            if name == 'method':
                msg.method = value
            elif name == 'uri':
                msg.uri = value
            else:
                msg.extensions[name] = value
        return msg

    def to_dict(self):
        result = self.extensions.copy()
        if self.method is not None:
            result['method'] = self.method
        if self.uri is not None:
            result['uri'] = self.uri
        return result

class StatusLine(object):
    def __init__(self):
        self.code = 200
        self.reason_phrase = 'OK'
        self.extensions = {}

    @classmethod
    def from_dict(cls, d):
        msg = RequestLine()
        for name, value in d.items():
            if name == 'code':
                msg.code = value
            elif name == 'reasonPhrase':
                msg.reason_phrase = value
            else:
                msg.extensions[name] = value
        return msg

    def to_dict(self):
        result = self.extensions.copy()
        if self.code is not None:
            result['code'] = self.code
        if self.reason_phrase is not None:
            result['reasonPhrase'] = self.reason_phrase
        return result

class GraphRequest(object):
    def __init__(self):
        self.body = None
        self.request_line = RequestLine()
        self.headers = {}
        self.extensions = {}

    @classmethod
    def from_dict(cls, d):
        msg = GraphRequest()
        for name, value in d.items():
            if name == 'body':
                msg.body = value
            elif name == 'headers':
                msg.headers = value
            elif name == 'requestLine':
                msg.request_line = RequestLine.from_dict(value)
            else:
                msg.extensions[name] = value
        return msg

    def to_dict(self):
        result = self.extensions.copy()
        if self.body is not None:
            result['body'] = self.body
        if self.headers is not None:
            result['headers'] = self.headers
        if self.request_line is not None:
            result['requestLine'] = self.request_line.to_dict()
        return result

class GraphResponse(object):
    def __init__(self):
        self.body = None
        self.headers = {}
        self.status_line = StatusLine()
        self.extensions = {}

    @classmethod
    def from_dict(cls, d):
        msg = GraphResponse()
        for name, value in d.items():
            if name == 'body':
                msg.body = value
            elif name == 'headers':
                msg.headers = value
            elif name == 'statusLine':
                msg.status_line = StatusLine.from_dict(value)
            else:
                msg.extensions[name] = value
        return msg

    def to_dict(self):
        result = self.extensions.copy()
        if self.body is not None:
            result['body'] = self.body
        if self.headers is not None:
            result['headers'] = self.headers
        if self.status_line is not None:
            result['statusLine'] = self.status_line.to_dict()
        return result


class GraphHandler(CallbackHandler):

    def __init__(self):
        super(GraphHandler, self).__init__()


