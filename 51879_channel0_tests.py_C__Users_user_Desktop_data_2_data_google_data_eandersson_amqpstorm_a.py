import logging
import time
import platform

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import amqpstorm

from pamqp.specification import Connection
from pamqp.heartbeat import Heartbeat

from amqpstorm.channel0 import Channel0
from amqpstorm import AMQPConnectionError

from amqpstorm.tests.utility import FakeConnection
from amqpstorm.tests.utility import FakeFrame
from amqpstorm.tests.utility import MockLoggingHandler

logging.basicConfig(level=logging.DEBUG)


class Channel0Tests(unittest.TestCase):
    def test_channel0_client_properties(self):
        channel = Channel0(FakeConnection())
        result = channel._client_properties()

        information = 'See https://github.com/eandersson/amqpstorm'
        python_version = 'Python %s' % platform.python_version()

        self.assertIsInstance(result, dict)
        self.assertTrue(result['capabilities']['authentication_failure_close'])
        self.assertTrue(result['capabilities']['consumer_cancel_notify'])
        self.assertTrue(result['capabilities']['publisher_confirms'])
        self.assertTrue(result['capabilities']['connection.blocked'])
        self.assertTrue(result['capabilities']['basic.nack'])
        self.assertEqual(result['information'], information)
        self.assertEqual(result['platform'], python_version)

    def test_channel0_credentials(self):
        connection = FakeConnection()
        connection.parameters['username'] = 'guest'
        connection.parameters['password'] = 'password'
        channel = Channel0(connection)
        credentials = channel._plain_credentials()

        self.assertEqual(credentials, '\0guest\0password')

    def test_channel0_close_connection(self):
        connection = FakeConnection()
        connection.set_state(connection.OPEN)
        channel = Channel0(connection)

        self.assertTrue(connection.is_open)
        channel._close_connection(
            Connection.Close(reply_text=b'',
                             reply_code=200)
        )
        self.assertEqual(connection.exceptions, [])
        self.assertTrue(connection.is_closed)

    def test_channel0_forcefully_closed_connection(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        connection.set_state(connection.OPEN)
        channel = Channel0(connection)
        channel._close_connection(
            Connection.Close(reply_text=b'',
                             reply_code=500)
        )
        self.assertTrue(connection.is_closed)
        self.assertRaises(AMQPConnectionError, connection.check_for_errors)

    def test_channel0_send_start_ok_frame(self):
        connection = FakeConnection()
        connection.parameters['username'] = 'guest'
        connection.parameters['password'] = 'password'
        channel = Channel0(connection)
        channel._send_start_ok_frame(Connection.Start(mechanisms=b'PLAIN'))

        self.assertNotEqual(connection.frames_out, [])
        channel_id, frame_out = connection.frames_out.pop()
        self.assertEqual(channel_id, 0)
        self.assertIsInstance(frame_out, Connection.StartOk)
        self.assertNotEqual(frame_out.locale, '')
        self.assertIsNotNone(frame_out.locale)

    def test_channel0_send_tune_ok_frame(self):
        connection = FakeConnection()
        channel = Channel0(connection)
        channel._send_tune_ok_frame()

        self.assertNotEqual(connection.frames_out, [])
        channel_id, frame_out = connection.frames_out.pop()
        self.assertEqual(channel_id, 0)
        self.assertIsInstance(frame_out, Connection.TuneOk)

    def test_channel0_send_close_connection_frame(self):
        connection = FakeConnection()
        channel = Channel0(connection)
        channel.send_close_connection_frame()

        self.assertNotEqual(connection.frames_out, [])
        channel_id, frame_out = connection.frames_out.pop()
        self.assertEqual(channel_id, 0)
        self.assertIsInstance(frame_out, Connection.Close)

    def test_channel0_invalid_authentication_mechanism(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel0(connection)
        channel._send_start_ok_frame(
            Connection.Start(mechanisms='CRAM-MD5 SCRAM-SHA-1 SCRAM-SHA-256'))
        self.assertRaises(AMQPConnectionError, connection.check_for_errors)


class Channel0FrameTests(unittest.TestCase):
    def setUp(self):
        self.logging_handler = MockLoggingHandler()
        logging.root.addHandler(self.logging_handler)

    def test_channel0_open_ok_frame(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel0(connection)

        self.assertFalse(connection.is_open)

        channel.on_frame(Connection.OpenOk())

        self.assertTrue(connection.is_open)

    def test_channel0_on_close_frame(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        connection.set_state(connection.OPEN)
        channel = Channel0(connection)

        self.assertFalse(connection.exceptions)

        channel.on_frame(Connection.Close())

        self.assertTrue(connection.exceptions)
        self.assertTrue(connection.is_closed)

        self.assertRaisesRegexp(AMQPConnectionError,
                                'Connection was closed by remote server: ',
                                connection.check_for_errors)

    def test_channel0_is_blocked(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel0(connection)

        self.assertFalse(channel.is_blocked)

        channel.on_frame(Connection.Blocked('unit-test'))

        self.assertTrue(channel.is_blocked)
        self.assertEqual(self.logging_handler.messages['warning'][0],
                         'Connection is blocked by remote server: unit-test')

    def test_channel0_unblocked(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel0(connection)

        channel.on_frame(Connection.Blocked())

        self.assertTrue(channel.is_blocked)

        channel.on_frame(Connection.Unblocked())

        self.assertFalse(channel.is_blocked)
        self.assertEqual(self.logging_handler.messages['info'][0],
                         'Connection is no longer blocked by remote server')

    def test_channel0_on_hearbeat_registers_heartbeat(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        last_heartbeat = connection.heartbeat._last_heartbeat
        start_time = time.time()
        channel = Channel0(connection)

        time.sleep(0.1)

        def fake(*_):
            pass

        # Don't try to write to socket during test.
        channel._write_frame = fake

        # As the heartbeat timer was never started, it should be 0.
        self.assertEqual(connection.heartbeat._last_heartbeat, 0.0)

        channel.on_frame(Heartbeat())

        self.assertNotEqual(connection.heartbeat._last_heartbeat,
                            last_heartbeat)
        self.assertGreater(connection.heartbeat._last_heartbeat, start_time)

    def test_channel0_unhandled_frame(self):
        connection = amqpstorm.Connection('localhost', 'guest', 'guest',
                                          lazy=True)
        channel = Channel0(connection)

        channel.on_frame(FakeFrame())

        self.assertEqual(self.logging_handler.messages['error'][0],
                         "[Channel0] Unhandled Frame: FakeFrame")
