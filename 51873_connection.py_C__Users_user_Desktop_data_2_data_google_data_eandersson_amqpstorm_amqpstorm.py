"""AMQP-Storm Connection."""

import logging
import time
from time import sleep

from pamqp import exceptions as pamqp_exception
from pamqp import frame as pamqp_frame
from pamqp import header as pamqp_header
from pamqp import specification as pamqp_spec

from amqpstorm import compatibility
from amqpstorm.base import IDLE_WAIT
from amqpstorm.base import Stateful
from amqpstorm.channel import Channel
from amqpstorm.channel0 import Channel0
from amqpstorm.exception import AMQPConnectionError
from amqpstorm.exception import AMQPInvalidArgument
from amqpstorm.heartbeat import Heartbeat
from amqpstorm.io import EMPTY_BUFFER
from amqpstorm.io import IO

LOGGER = logging.getLogger(__name__)


class Connection(Stateful):
    """AMQP Connection"""

    def __init__(self, hostname, username, password, port=5672, **kwargs):
        """
        :param str hostname: Hostname
        :param str username: Username
        :param str password: Password
        :param int port: Server port
        :param str virtual_host: Virtualhost
        :param int heartbeat: RabbitMQ Heartbeat interval
        :param int|float timeout: Socket timeout
        :param bool ssl: Enable SSL
        :param dict ssl_options: SSL kwargs (from ssl.wrap_socket)
        :param bool lazy: Lazy initialize the connection
        :return:
        """
        super(Connection, self).__init__()
        self.parameters = {
            'hostname': hostname,
            'username': username,
            'password': password,
            'port': port,
            'virtual_host': kwargs.get('virtual_host', '/'),
            'heartbeat': kwargs.get('heartbeat', 60),
            'timeout': kwargs.get('timeout', 30),
            'ssl': kwargs.get('ssl', False),
            'ssl_options': kwargs.get('ssl_options', {})
        }
        self._validate_parameters()
        self.heartbeat = Heartbeat(self.parameters['heartbeat'])
        self._io = IO(self.parameters, on_read=self._read_buffer)
        self._channel0 = Channel0(self)
        self._channels = {}
        if not kwargs.get('lazy', False):
            self.open()

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, _):
        if exception_value:
            message = 'Closing connection due to an unhandled exception: %s'
            LOGGER.warning(message, exception_type)
        self.close()

    @property
    def is_blocked(self):
        """Is the connection currently being blocked from publishing by
        the remote server.

        :rtype: bool
        """
        return self._channel0.is_blocked

    @property
    def server_properties(self):
        """Returns the RabbitMQ Server properties.

        :rtype: dict
        """
        return self._channel0.server_properties

    @property
    def socket(self):
        """Returns an instance of the socket.

        :rtype: socket
        """
        return self._io.socket

    @property
    def fileno(self):
        """Socket Fileno.

        :return:
        """
        if not self._io.socket:
            return None
        return self._io.socket.fileno()

    def open(self):
        """Open Connection.

        :raises AMQPConnectionError: Raises if a Connection cannot be
                                     established.
        """
        LOGGER.debug('Connection Opening')
        self.set_state(self.OPENING)
        self._exceptions = []
        self._io.open(self._exceptions)
        self._send_handshake()
        self._wait_for_connection_to_open()
        self.heartbeat.start(self._exceptions)
        LOGGER.debug('Connection Opened')

    def close(self):
        """Close connection."""
        LOGGER.debug('Connection Closing')
        self.heartbeat.stop()
        if not self.is_closed and self._io.socket:
            self._close_channels()
            self.set_state(self.CLOSING)
            self._channel0.send_close_connection_frame()
        self._io.close()
        self.set_state(self.CLOSED)
        LOGGER.debug('Connection Closed')

    def channel(self, rpc_timeout=120):
        """Open Channel.

        :param int rpc_timeout: Timeout before we give up waiting for an RPC
                                response from the server.

        :raises AMQPInvalidArgument: Raises on invalid arguments.
        :raises AMQPChannelError: Raises if the channel cannot be opened
                                  before the rpc_timeout is reached.
        :raises AMQPConnectionError: Raises if the Connection is closed.
        """
        LOGGER.debug('Opening a new Channel')
        if not compatibility.is_integer(rpc_timeout):
            raise AMQPInvalidArgument('rpc_timeout should be an integer')
        elif self.is_closed:
            raise AMQPConnectionError('socket/connection closed')

        with self.lock:
            channel_id = len(self._channels) + 1
            channel = Channel(channel_id, self, rpc_timeout)
            self._channels[channel_id] = channel
            channel.open()
        LOGGER.debug('Channel #%d Opened', channel_id)
        return self._channels[channel_id]

    def check_for_errors(self):
        """Check connection for errors.

        :raises AMQPConnectionError: Raises if the connection
                                     encountered an error.
        :return:
        """
        if not self.exceptions:
            return
        self.set_state(self.CLOSED)
        self.close()
        raise self.exceptions[0]

    def write_frame(self, channel_id, frame_out):
        """Marshal and write an outgoing pamqp frame to the socket.

        :param int channel_id:
        :param pamqp_spec.Frame frame_out: Amqp frame.
        :return:
        """
        frame_data = pamqp_frame.marshal(frame_out, channel_id)
        self._io.write_to_socket(frame_data)

    def write_frames(self, channel_id, multiple_frames):
        """Marshal and write multiple outgoing pamqp frames to the socket.

        :param int channel_id:
        :param list multiple_frames: Amqp frames.
        :return:
        """
        frame_data = EMPTY_BUFFER
        for single_frame in multiple_frames:
            frame_data += pamqp_frame.marshal(single_frame, channel_id)
        self._io.write_to_socket(frame_data)

    def _validate_parameters(self):
        """Validate Connection Parameters.

        :return:
        """
        if not compatibility.is_string(self.parameters['hostname']):
            raise AMQPInvalidArgument('hostname should be a string')
        elif not compatibility.is_integer(self.parameters['port']):
            raise AMQPInvalidArgument('port should be an integer')
        elif not compatibility.is_string(self.parameters['username']):
            raise AMQPInvalidArgument('username should be a string')
        elif not compatibility.is_string(self.parameters['password']):
            raise AMQPInvalidArgument('password should be a string')
        elif not compatibility.is_string(self.parameters['virtual_host']):
            raise AMQPInvalidArgument('virtual_host should be a string')
        elif not isinstance(self.parameters['timeout'], (int, float)):
            raise AMQPInvalidArgument('timeout should be an integer or float')
        elif not compatibility.is_integer(self.parameters['heartbeat']):
            raise AMQPInvalidArgument('heartbeat should be an integer')

    def _send_handshake(self):
        """Send RabbitMQ Handshake.

        :return:
        """
        self._io.write_to_socket(pamqp_header.ProtocolHeader().marshal())

    def _wait_for_connection_to_open(self):
        """Wait for the connection to fully open.

        :return:
        """
        start_time = time.time()
        timeout = (self.parameters['timeout'] or 10) + 0.25
        while not self.is_open:
            self.check_for_errors()
            if time.time() - start_time > timeout:
                raise AMQPConnectionError('Connection timed out')
            sleep(IDLE_WAIT)

    def _read_buffer(self, buffer):
        """Process the socket buffer, and direct the data to the correct
        channel.

        :return:
        """
        while buffer:
            buffer, channel_id, frame_in = \
                self._handle_amqp_frame(buffer)

            if frame_in is None:
                break

            self.heartbeat.register_beat()
            if channel_id == 0:
                self._channel0.on_frame(frame_in)
            else:
                self._channels[channel_id].on_frame(frame_in)

        return buffer

    @staticmethod
    def _handle_amqp_frame(data_in):
        """Unmarshal any incoming RabbitMQ frames and return the result.

        :param data_in: socket data
        :return: buffer, channel_id, frame
        """
        if not data_in:
            return data_in, None, None
        try:
            byte_count, channel_id, frame_in = pamqp_frame.unmarshal(data_in)
            return data_in[byte_count:], channel_id, frame_in
        except pamqp_exception.UnmarshalingException:
            return data_in, None, None
        except pamqp_spec.AMQPFrameError as why:
            LOGGER.error('AMQPFrameError: %r', why, exc_info=True)
            return data_in, None, None

    def _close_channels(self):
        """Close any open channels.

        :return:
        """
        for channel_id in self._channels:
            if not self._channels[channel_id].is_open:
                continue
            self._channels[channel_id].close()
