try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local


_thread_locals = local()


def request_is_secure():
    return getattr(_thread_locals, 'cb_request_is_secure', None)


class ThreadLocals(object):
    def process_request(self, request):
        _thread_locals.cb_request_is_secure = request.is_secure()
