import logging

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from pamqp import specification
from pamqp.body import ContentBody
from pamqp.header import ContentHeader

import amqpstorm
from amqpstorm import exception
from amqpstorm import Message
from amqpstorm import Channel
from amqpstorm.basic import Basic
from amqpstorm.exchange import Exchange
from amqpstorm.queue import Queue
from amqpstorm.exception import *

from amqpstorm.tests.utility import FakeConnection
from amqpstorm.tests.utility import FakeFrame
from amqpstorm.tests.utility import MockLoggingHandler

logging.basicConfig(level=logging.DEBUG)


class ChannelTests(unittest.TestCase):
    def test_channel_id(self):
        channel = Channel(0, None, 360)
        self.assertEqual(int(channel), 0)

        channel = Channel(1557, None, 360)
        self.assertEqual(int(channel), 1557)

    def test_channel_close(self):
        channel = Channel(0, None, 360)

        # Set up Fake Channel.
        channel._inbound = [1, 2, 3]
        channel.set_state(channel.OPEN)
        channel._consumer_tags = [1, 2, 3]

        # Close Channel.
        channel._close_channel(specification.Channel.Close(reply_text=''))

        self.assertEqual(channel._inbound, [])
        self.assertEqual(channel._consumer_tags, [])
        self.assertEqual(channel._state, channel.CLOSED)

    def test_channel_basic_handler(self):
        channel = Channel(0, None, 360)

        self.assertIsNone(channel._basic)
        self.assertIsInstance(channel.basic, Basic)
        self.assertIsNotNone(channel._basic)

    def test_channel_exchange_handler(self):
        channel = Channel(0, None, 360)

        self.assertIsNone(channel._exchange)
        self.assertIsInstance(channel.exchange, Exchange)
        self.assertIsNotNone(channel._exchange)

    def test_channel_queue_handler(self):
        channel = Channel(0, None, 360)

        self.assertIsNone(channel._queue)
        self.assertIsInstance(channel.queue, Queue)
        self.assertIsNotNone(channel._queue)


class ChannelExceptionTests(unittest.TestCase):
    def test_chanel_invalid_close_parameter(self):
        channel = Channel(0, None, 360)
        self.assertRaisesRegexp(AMQPInvalidArgument,
                                'reply_code should be an integer',
                                channel.close, 'Hello', 'error')
        self.assertRaisesRegexp(AMQPInvalidArgument,
                                'reply_text should be a string',
                                channel.close, 200, 200)

    def test_chanel_callback_not_set(self):
        channel = Channel(0, None, 360)
        self.assertRaisesRegexp(AMQPChannelError,
                                'no consumer_callback defined',
                                channel.process_data_events)

    def test_channel_throw_exception_check_for_error(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(channel.OPEN)
        channel.exceptions.append(AMQPConnectionError('Test'))

        self.assertRaises(AMQPConnectionError, channel.check_for_errors)

    def test_channel_check_error_no_exception(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        channel.check_for_errors()

    def test_channel_check_error_when_closed(self):
        channel = Channel(0, FakeConnection(), 360)

        self.assertRaises(exception.AMQPChannelError, channel.check_for_errors)

    def test_channel_check_error_connection_closed(self):
        channel = Channel(0, FakeConnection(FakeConnection.CLOSED), 360)

        self.assertRaises(exception.AMQPConnectionError,
                          channel.check_for_errors)

    def test_channel_raises_when_closed(self):
        channel = Channel(0, FakeConnection(FakeConnection.OPEN), 360)
        channel.set_state(channel.CLOSED)

        self.assertFalse(channel.is_open)
        self.assertRaisesRegexp(exception.AMQPChannelError,
                                'channel was closed',
                                channel.check_for_errors)
        self.assertTrue(channel.is_closed)

    def test_channel_closed_after_connection_closed(self):
        channel = Channel(0, FakeConnection(FakeConnection.CLOSED), 360)
        channel.set_state(channel.OPEN)

        self.assertTrue(channel.is_open)
        self.assertRaisesRegexp(exception.AMQPConnectionError,
                                'connection was closed',
                                channel.check_for_errors)
        self.assertTrue(channel.is_closed)

    def test_channel_closed_after_connection_exception(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel(0, connection, 360)
        connection.exceptions.append(AMQPConnectionError('error'))
        channel.set_state(channel.OPEN)

        self.assertTrue(connection.is_closed)
        self.assertTrue(channel.is_open)
        self.assertRaisesRegexp(exception.AMQPConnectionError, 'error',
                                channel.check_for_errors)
        self.assertTrue(channel.is_closed)

    def test_channel_consume_exception_when_recoverable(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        connection.set_state(connection.OPEN)
        channel = Channel(0, connection, 360)
        channel.set_state(channel.OPEN)
        channel.exceptions.append(AMQPChannelError('no-route'))

        self.assertTrue(connection.is_open)
        self.assertTrue(channel.is_open)

        self.assertRaisesRegexp(exception.AMQPChannelError, 'no-route',
                                channel.check_for_errors)

        self.assertTrue(channel.is_open)

        channel.check_for_errors()


class ChannelBuildMessageTests(unittest.TestCase):
    def test_channel_build_message(self):
        channel = Channel(0, None, 360)

        message = b'Hello World!'
        message_len = len(message)

        deliver = specification.Basic.Deliver()
        header = ContentHeader(body_size=message_len)
        body = ContentBody(value=message)

        channel._inbound = [deliver, header, body]
        result = channel._build_message()

        self.assertEqual(result._body, message)

    def test_channel_build_out_of_order_message(self):
        channel = Channel(0, None, 360)

        message = b'Hello World!'
        message_len = len(message)

        deliver = specification.Basic.Deliver()
        header = ContentHeader(body_size=message_len)
        body = ContentBody(value=message)

        channel._inbound = [deliver, deliver, header, body]
        result = channel._build_message()

        self.assertEqual(result, None)

    def test_channel_build_message_body(self):
        channel = Channel(0, None, 360)

        message = b'Hello World!'
        message_len = len(message)

        body = ContentBody(value=message)
        channel._inbound = [body]
        result = channel._build_message_body(message_len)

        self.assertEqual(message, result)

    def test_channel_build_empty_inbound_messages(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)
        result = None
        for message in channel.build_inbound_messages(break_on_empty=True):
            result = message

        self.assertIsNone(result)

    def test_channel_build_inbound_messages(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)

        message = b'Hello World!'
        message_len = len(message)

        deliver = specification.Basic.Deliver()
        header = ContentHeader(body_size=message_len)
        body = ContentBody(value=message)

        channel._inbound = [deliver, header, body]

        for message in channel.build_inbound_messages(break_on_empty=True):
            self.assertIsInstance(message, Message)

    def test_channel_build_multiple_inbound_messages(self):
        channel = Channel(0, FakeConnection(), 360)
        channel.set_state(Channel.OPEN)

        message = b'Hello World!'
        message_len = len(message)

        deliver = specification.Basic.Deliver()
        header = ContentHeader(body_size=message_len)
        body = ContentBody(value=message)

        channel._inbound = [deliver, header, body, deliver, header, body,
                            deliver, header, body, deliver, header, body]

        index = 0
        for message in channel.build_inbound_messages(break_on_empty=True):
            self.assertIsInstance(message, Message)
            index += 1

        self.assertEqual(index, 4)


class ChannelFrameTests(unittest.TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler()
        logging.root.addHandler(self.logging_handler)

    def test_channel_consume_ok_frame(self):
        tag = 'hello-world'
        channel = Channel(0, None, rpc_timeout=360)

        channel.on_frame(specification.Basic.ConsumeOk(tag))

        self.assertEqual(channel.consumer_tags[0], tag)

    def test_channel_cancel_ok_frame(self):
        tag = 'hello-world'
        channel = Channel(0, None, rpc_timeout=360)
        channel.add_consumer_tag(tag)

        channel.on_frame(specification.Basic.CancelOk(tag))

        self.assertFalse(channel.consumer_tags)

    def test_channel_flow_frame(self):
        connection = FakeConnection()
        connection.set_state(connection.OPEN)
        channel = Channel(0, connection, rpc_timeout=360)
        channel.set_state(channel.OPEN)

        channel.on_frame(specification.Channel.Flow())

        self.assertIsInstance(connection.frames_out[0][1],
                              specification.Channel.FlowOk)

    def test_channel_basic_cancel_frame(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel(0, connection, rpc_timeout=360)

        channel.on_frame(specification.Basic.Cancel('unit-test'))

        self.assertEqual(self.logging_handler.messages['warning'][0],
                         'Received Basic.Cancel on consumer_tag: unit-test')

    def test_channel_basic_return_frame(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel(0, connection, rpc_timeout=360)

        channel.on_frame(specification.Basic.Return(reply_code=500,
                                                    reply_text='test',
                                                    exchange='exchange',
                                                    routing_key='routing_key'))

        self.assertEqual(str(channel.exceptions[0]),
                         "Message not delivered: test (500) to queue "
                         "'routing_key' from exchange 'exchange'")

    def test_channel_close_frame(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel(0, connection, rpc_timeout=360)

        channel.on_frame(specification.Channel.Close(reply_code=500,
                                                     reply_text='test'))

        self.assertEqual(str(channel.exceptions[0]),
                         'Channel 0 was closed by remote server: test')

    def test_channel_basic_return_raises_when_500(self):
        channel = Channel(0, None, 360)

        basic_return = specification.Basic.Return(reply_code=500,
                                                  reply_text='Error')
        channel._basic_return(basic_return)

        self.assertEqual(len(channel.exceptions), 1)
        why = channel.exceptions.pop(0)
        self.assertIsInstance(why, AMQPMessageError)
        self.assertEqual(str(why), "Message not delivered: Error (500) "
                                   "to queue '' from exchange ''")

    def test_channel_unhandled_frame(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel(0, connection, rpc_timeout=360)

        channel.on_frame(FakeFrame())

        self.assertEqual(self.logging_handler.messages['error'][0],
                         "[Channel0] Unhandled Frame: FakeFrame -- "
                         "{'data_1': 'hello world'}")
