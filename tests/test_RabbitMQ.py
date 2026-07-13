# -*- coding: utf-8 -*-

import unittest
from unittest.mock import MagicMock, patch
from heppy.RabbitMQ import RPCServer


class TestRPCServerOnRequest(unittest.TestCase):
    def setUp(self):
        self.server = RPCServer.__new__(RPCServer)
        self.server.message_ttl = '5000'

    def make_props(self, reply_to='reply-queue', correlation_id='corr-1'):
        props = MagicMock()
        props.reply_to = reply_to
        props.correlation_id = correlation_id
        return props

    def make_method(self, routing_key='routing-queue', delivery_tag=1):
        method = MagicMock()
        method.routing_key = routing_key
        method.delivery_tag = delivery_tag
        return method

    def test_publishes_response_result(self):
        self.server.response = lambda body: 'ok: ' + body
        ch = MagicMock()
        props = self.make_props()
        method = self.make_method()

        self.server.on_request(ch, method, props, 'ping')

        ch.basic_publish.assert_called_once()
        kwargs = ch.basic_publish.call_args.kwargs
        self.assertEqual(kwargs['routing_key'], props.reply_to)
        self.assertEqual(kwargs['properties'].correlation_id, props.correlation_id)
        self.assertEqual(kwargs['body'], 'ok: ping')
        ch.basic_ack.assert_called_once_with(delivery_tag=method.delivery_tag)

    def test_decodes_bytes_body_before_passing_to_response(self):
        received = {}

        def response(body):
            received['body'] = body
            return 'ok'

        self.server.response = response
        ch = MagicMock()

        self.server.on_request(ch, self.make_method(), self.make_props(), b'ping')

        self.assertEqual(received['body'], 'ping')

    def test_encodes_bytes_reply_before_publishing(self):
        self.server.response = lambda body: b'binary-reply'
        ch = MagicMock()

        self.server.on_request(ch, self.make_method(), self.make_props(), 'ping')

        self.assertEqual(ch.basic_publish.call_args.kwargs['body'], 'binary-reply')

    def test_falls_back_to_routing_key_when_reply_to_is_missing(self):
        self.server.response = lambda body: 'ok'
        ch = MagicMock()
        method = self.make_method(routing_key='fallback-queue')
        props = self.make_props(reply_to=None)

        self.server.on_request(ch, method, props, 'ping')

        self.assertEqual(ch.basic_publish.call_args.kwargs['routing_key'], 'fallback-queue')

    def test_exception_from_response_is_returned_as_reply_body(self):
        def response(body):
            raise ValueError('boom')

        self.server.response = response
        ch = MagicMock()

        with patch('heppy.RabbitMQ.logging.exception') as mock_log:
            self.server.on_request(ch, self.make_method(), self.make_props(), 'ping')

        self.assertEqual(ch.basic_publish.call_args.kwargs['body'], 'boom')
        ch.basic_ack.assert_called_once()
        mock_log.assert_called_once()

    def test_exception_still_acks_the_message(self):
        def response(body):
            raise ValueError('boom')

        self.server.response = response
        ch = MagicMock()
        method = self.make_method(delivery_tag=42)

        with patch('heppy.RabbitMQ.logging.exception'):
            self.server.on_request(ch, method, self.make_props(), 'ping')

        ch.basic_ack.assert_called_once_with(delivery_tag=42)


if __name__ == '__main__':
    unittest.main()
