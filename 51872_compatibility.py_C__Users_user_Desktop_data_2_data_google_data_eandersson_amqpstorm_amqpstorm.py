"""Python 2/3 Compatibility layer."""

import sys

try:
    import ssl
except ImportError:
    ssl = None

PYTHON3 = sys.version_info >= (3, 0, 0)

if PYTHON3:
    RANGE = range
else:
    RANGE = xrange

SSL_CERT_MAP = {}
SSL_VERSIONS = {}
DEFAULT_SSL_VERSION = None
SSL_SUPPORTED = True if ssl else False
SSL_OPTIONS = [
    'keyfile',
    'certfile',
    'cert_reqs',
    'ssl_version',
    'ca_certs'
]

if SSL_SUPPORTED:
    if hasattr(ssl, 'PROTOCOL_TLSv1_2'):
        DEFAULT_SSL_VERSION = ssl.PROTOCOL_TLSv1_2
    elif hasattr(ssl, 'PROTOCOL_TLSv1_1'):
        DEFAULT_SSL_VERSION = ssl.PROTOCOL_TLSv1_1
    elif hasattr(ssl, 'PROTOCOL_TLSv1'):
        DEFAULT_SSL_VERSION = ssl.PROTOCOL_TLSv1
    else:
        SSL_SUPPORTED = False

    if hasattr(ssl, 'PROTOCOL_TLSv1_2'):
        SSL_VERSIONS['protocol_tlsv1_2'] = ssl.PROTOCOL_TLSv1_2
    if hasattr(ssl, 'PROTOCOL_TLSv1_1'):
        SSL_VERSIONS['protocol_tlsv1_1'] = ssl.PROTOCOL_TLSv1_1
    if hasattr(ssl, 'PROTOCOL_TLSv1'):
        SSL_VERSIONS['protocol_tlsv1'] = ssl.PROTOCOL_TLSv1

    SSL_CERT_MAP = {
        'cert_none': ssl.CERT_NONE,
        'cert_optional': ssl.CERT_OPTIONAL,
        'cert_required': ssl.CERT_REQUIRED
    }


def is_string(obj):
    """Is this a string.

    :param object obj:
    :rtype: bool
    """
    if PYTHON3:
        str_type = (bytes, str)
    else:
        str_type = (bytes, str, unicode)
    return isinstance(obj, str_type)


def is_integer(obj):
    """Is this an integer.

    :param object obj:
    :return:
    """
    if PYTHON3:
        return isinstance(obj, int)
    return isinstance(obj, (int, long))


def is_unicode(obj):
    """Is this a unicode string.

        This always returns False if running on Python 3.

    :param object obj:
    :rtype: bool
    """
    if PYTHON3:
        return False
    return isinstance(obj, unicode)


def try_utf8_decode(value):
    """Try to decode an object.

    :param value:
    :return:
    """
    if not is_string(value):
        return value
    elif PYTHON3 and not isinstance(value, bytes):
        return value
    elif not PYTHON3 and not isinstance(value, unicode):
        return value

    try:
        return value.decode('utf-8')
    except (UnicodeEncodeError, AttributeError):
        pass

    return value


def patch_uri(uri):
    """If a custom uri schema is used with python 2.6 (e.g. amqps),
    it will ignore some of the parsing logic.

        As a work-around for this we change the amqp/amqps schema
        internally to use http/https.

    :param str uri: AMQP Connection string
    :rtype: str
    """
    index = uri.find(':')
    if uri[:index] == 'amqps':
        uri = uri.replace('amqps', 'https', 1)
    elif uri[:index] == 'amqp':
        uri = uri.replace('amqp', 'http', 1)
    return uri
