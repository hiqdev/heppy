#!/usr/bin/env python

import pika
import uuid
from pprint import pprint

from pika.connection import Parameters
from pika.connection import ConnectionParameters


class RPCServer:
    def __init__(self, config):
        self.config = config
        self.queue = config.get('queue')
        self.connection = pika.BlockingConnection(connection_parameters(config))

        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_qos(prefetch_count=1)

    def basic_consume(self, response):
        self.response = response
        self.channel.basic_consume(self.on_request, self.queue)
        self.channel.start_consuming()

    def consume(self, response, recheck, check_timeout):
        self.response = response
        for method, props, body in self.channel.consume(self.queue, inactivity_timeout=check_timeout):
            if method is not None:
                self.on_request(self.channel, method, props, body)
            recheck()

    def on_request(self, ch, method, props, body) -> None:
        reply = self.response(body.decode('utf-8') if isinstance(body, bytes) else body)
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to if props.reply_to is not None else method.routing_key,
            properties=pika.BasicProperties(
                correlation_id = props.correlation_id,
            ),
            body=str(reply.decode('utf-8') if isinstance(reply, bytes) else reply),
        )
        ch.basic_ack(delivery_tag = method.delivery_tag)

class RPCClient:
    def __init__(self, config):
        self.config = config
        self.queue = config.get('queue')
        self.connection = pika.BlockingConnection(connection_parameters(config))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.reply_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.reply_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

    def on_response(self, ch, method, props, body: bytes) -> None:
        if self.corr_id == props.correlation_id:
            self.reply = body

    def request(self, query) -> str:
        self.reply = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
            routing_key=self.queue,
            properties=pika.BasicProperties(
                reply_to = self.reply_queue,
                correlation_id = self.corr_id,
            ),
            body=(query.decode('utf-8') if isinstance(query, bytes) else query)
        )
        while self.reply is None:
            self.connection.process_data_events()
        return self.reply if isinstance(self.reply, str) else (self.reply).decode('utf-8')

def connection_parameters(config):
    args = {
        'host': config.get('host', ConnectionParameters._DEFAULT),
        'port': config.get('port', ConnectionParameters._DEFAULT),
        'virtual_host': config.get('virtual_host', ConnectionParameters._DEFAULT),
    }
    if 'username' in config:
        args['credentials'] = pika.PlainCredentials(
            config.get('username', Parameters.DEFAULT_USERNAME),
            config.get('password', Parameters.DEFAULT_PASSWORD)
        )
    return ConnectionParameters(**args)
