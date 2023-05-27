import logging
from thespian.actors import ActorSystemMessage, ActorSystemFailure
try:
    from logging.config import dictConfig
except ImportError:
    # Old python that doesn't contain this...
    from thespian.system.dictconfig import dictConfig
from datetime import timedelta, datetime
import multiprocessing
import traceback
from thespian.system.utilis import setProcName, thesplog_control
from thespian.system.messages.multiproc import *
from thespian.system.transport import TransmitIntent


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Special Logging pseudo-Actor
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

MAX_LOGGING_STARTUP_DELAY = timedelta(seconds=3)
MAX_LOGGING_EXCEPTIONS_PER_SECOND = 20

# This is the process that handles logging output for all the Actors
# in this ActorSystem (and possibly forwarded logs from other
# ActorSystems).  This is similar to an Actor, and responds to
# messages like an Actor, but the startup of this is slightly
# different in that it starts without knowledge of the Admin and by
# special initialization.  It will process messages like other Actors,
# but will never talk back to the Admin (which it doesn't know about).
# It will ignore normal ActorExitRequest messages as well (in case it
# gets a spurious one) and only exit on receiving a LoggerExitRequest,
# which should only be generated by the local Admin.

class LoggerExitRequest(ActorSystemMessage): pass
class LoggerFileDup(ActorSystemMessage): pass


def startupASLogger(addrOfStarter, logEndpoint, logDefs,
                    transportClass, aggregatorAddress):
    # Dirty trick here to completely re-initialize logging in this
    # process... something the standard Python logging interface does
    # not allow via the API.  We also do not want to run
    # logging.shutdown() because (a) that does not do enough to reset,
    # and (b) it shuts down handlers, but we want to leave the
    # parent's handlers alone.  Dirty trick here to completely
    # re-initialize logging in this process... something the standard
    # Python logging interface does not allow via the API.
    logging.root = logging.RootLogger(logging.WARNING)
    logging.Logger.root = logging.root
    logging.Logger.manager = logging.Manager(logging.Logger.root)
    if logDefs:
        dictConfig(logDefs)
    else:
        logging.basicConfig()
    # Disable thesplog from within the logging process (by setting the
    # logfile size to zero) to try to avoid recursive logging loops.
    thesplog_control(logging.WARNING, False, 0)
    #logging.info('ActorSystem Logging Initialized')
    transport = transportClass(logEndpoint)
    setProcName('logger', transport.myAddress)
    transport.scheduleTransmit(None, TransmitIntent(addrOfStarter, LoggerConnected()))
    fdup = None
    last_exception = None
    last_exception_time = None
    exception_count = 0
    while True:
        try:
            r = transport.run(None)
            logrecord = r.message
            if isinstance(logrecord, LoggerExitRequest):
                logging.info('ActorSystem Logging Shutdown')
                return
            elif isinstance(logrecord, LoggerFileDup):
                fdup = getattr(logrecord, 'fname', None)
            elif isinstance(logrecord, logging.LogRecord):
                logging.getLogger(logrecord.name).handle(logrecord)
                if fdup:
                    with open(fdup, 'a') as ldf: ldf.write('%s\n'%str(logrecord))
                if aggregatorAddress and \
                   logrecord.levelno >= logging.WARNING:
                    transport.scheduleTransmit(None, TransmitIntent(aggregatorAddress,
                                                                    logrecord))
            else:
                logging.warn('Unknown message rcvd by logger: %s'%str(logrecord))
        except Exception:
            logging.error('Thespian Logger aborting (#%d) with error', exception_count, exc_info=True)
            if last_exception is None or datetime.now() - last_exception_time > timedelta(seconds=1):
                last_exception_time = datetime.now()
                exception_count = 0
            else:
                exception_count += 1
                if exception_count >= MAX_LOGGING_EXCEPTIONS_PER_SECOND:
                    logging.error('Too many Thespian Logger exceptions (#%d in %s); exiting!',
                                  exception_count, datetime.now() - last_exception_time)
                    return

class ThespianLogForwardHandler(logging.Handler):
    def __init__(self, toAddr, transport):
        logging.Handler.__init__(self, 1)  # forward EVERYTHING
        self._name = 'ThespianLogForwardHandler'
        self._fwdAddr = toAddr
        if not self._fwdAddr:
            raise NotImplemented('Cannot forward logs to a NULL target address')
        self._transport = transport
    def handle(self, record):
        # Can't pickle traceback objects, so pre-format them.  Sorry,
        # more logging internals here.
        if record.exc_info:
            if not record.exc_text:
                excinfo = traceback.format_exception(record.exc_info[0],
                                                     record.exc_info[1],
                                                     record.exc_info[2])
                record.exc_text = '\n'.join(excinfo)
            record.exc_info = None
        record.__dict__['actorAddress'] = str(self._transport.myAddress)
        msg = record.getMessage()
        record.msg = msg
        record.args = None
        self._transport.scheduleTransmit(None, TransmitIntent(self._fwdAddr, record))


class ThespianLogForwarder(logging.Logger):
    def __init__(self, toAddr, transport):
        # N.B.  In Python2.6, Logger and Handler don't derive from
        # object, so super() cannot be used here.
        logging.Logger.__init__(self, 'root', 1)  # forward EVERYTHING
        logging.Logger.addHandler(self, ThespianLogForwardHandler(toAddr, transport))
    def addHandler(self, hdlr):
        raise NotImplementedError('Cannot add logging handlers for Thespian Actors')
    def removeHandler(self, hdlr):
        raise NotImplementedError('Cannot add logging handlers for Thespian Actors')

