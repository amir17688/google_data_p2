from . import nanomsg, ffi
import sys

NN_MSG = int(ffi.cast("size_t", -1))

ustr = str if sys.version_info[0] > 2 else unicode

class Socket(object):
    
    def __init__(self, domain, protocol):
        self.sock = nanomsg.nn_socket(domain, protocol)
    
    def close(self):
        nanomsg.nn_close(self.sock)
    
    def getsockopt(self, level, option):
        buf = ffi.new('int*')
        size = ffi.new('size_t*')
        size[0] = 4
        rc = nanomsg.nn_getsockopt(self.sock, level, option, buf, size)
        assert rc >= 0, rc
        return buf[0]
    
    def setsockopt(self, level, option, value):
        if isinstance(value, int):
            buf = ffi.new('int*')
            buf[0] = value
            vlen = 4
        elif isinstance(value, ustr):
            buf = ffi.new('char[%s]' % len(value), value.encode())
            vlen = len(value)
        elif isinstance(value, bytes):
            buf = ffi.new('char[%s]' % len(value), value)
            vlen = len(value)
        else:
            raise TypeError("value must be a int, str or bytes")
        rc = nanomsg.nn_setsockopt(self.sock, level, option, buf, vlen)
        assert rc >= 0, rc
    
    def bind(self, addr):
        addr = addr.encode() if isinstance(addr, ustr) else addr
        buf = ffi.new('char[]', addr)
        rc = nanomsg.nn_bind(self.sock, buf)
        assert rc > 0, rc
    
    def connect(self, addr):
        addr = addr.encode() if isinstance(addr, ustr) else addr
        buf = ffi.new('char[]', addr)
        rc = nanomsg.nn_connect(self.sock, buf)
        assert rc > 0, rc
    
    def send(self, data, flags=0):
        if isinstance(data, memoryview):
            buf = ffi.from_buffer(data)
        else:
            data = data.encode() if isinstance(data, ustr) else data
            buf = ffi.new('char[%i]' % len(data), data)
        rc = nanomsg.nn_send(self.sock, buf, len(data), flags)
        assert rc > 0, rc
    
    def recv(self, flags=0):
        buf = ffi.new('char**')
        rc = nanomsg.nn_recv(self.sock, buf, NN_MSG, flags)
        assert rc > 0, rc
        s = ffi.buffer(buf[0], rc)[:]
        nanomsg.nn_freemsg(buf[0])
        return s
