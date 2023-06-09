import os
import sys
import tempfile

from twisted.trial import unittest
from twisted.python import util

from comet.icomet import IHandler
from comet.handler import SpawnCommand

SHELL = '/bin/sh'

class DummyEvent(object):
    def __init__(self, text=None):
        self.text = text or u""

class SpawnCommandProtocolTestCase(unittest.TestCase):
    def test_interface(self):
        self.assertTrue(IHandler.implementedBy(SpawnCommand))

    def test_good_process(self):
        spawn = SpawnCommand(sys.executable)
        d = spawn(DummyEvent())
        d.addCallback(self.assertEqual, True)
        return d

    def test_bad_process(self):
        spawn = SpawnCommand("/not/a/real/executable")
        return self.assertFailure(spawn(DummyEvent()), Exception)

    def test_write_data(self):
        if not os.access(SHELL, os.X_OK):
            raise unittest.SkipTest("Shell not available")
        TEXT = u"Test spawn process"
        output_file = tempfile.NamedTemporaryFile()
        def read_data(result):
            try:
                # NamedTemporaryFile is opened in binary mode, so we need to
                # encode the read for comparison.
                self.assertEqual(output_file.read().decode('utf-8'), TEXT)
            finally:
                output_file.close()
        spawn = SpawnCommand('/bin/sh', util.sibpath(__file__, "test_spawn.sh"), output_file.name)
        d = spawn(DummyEvent(TEXT))
        d.addCallback(read_data)
        return d
