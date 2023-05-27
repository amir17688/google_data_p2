import logging
import sys

import rasterio
from rasterio._drivers import driver_count
from rasterio.env import Env


def test_drivers():
    with Env() as m:
        assert driver_count() > 0
        assert type(m) == Env
    assert driver_count() > 0


def test_drivers_bwd_compat():
    with rasterio.drivers() as m:
        assert driver_count() > 0
        assert type(m) == Env
    assert driver_count() > 0


def test_cpl_debug_true(tmpdir):
    """Setting CPL_DEBUG=True results in GDAL debug messages."""
    log = logging.getLogger('rasterio._gdal')
    log.setLevel(logging.DEBUG)
    logfile = str(tmpdir.join('test.log'))
    fh = logging.FileHandler(logfile)
    log.addHandler(fh)

    with Env(CPL_DEBUG=True):
        with rasterio.open("tests/data/RGB.byte.tif"):
            pass

    log = open(logfile).read()
    assert "GDAL: GDALOpen(tests/data/RGB.byte.tif" in log


def test_cpl_debug_false(tmpdir):
    """Setting CPL_DEBUG=False results in no GDAL debug messages."""
    log = logging.getLogger('rasterio._gdal')
    log.setLevel(logging.DEBUG)
    logfile = str(tmpdir.join('test.log'))
    fh = logging.FileHandler(logfile)
    log.addHandler(fh)

    with Env(CPL_DEBUG=False):
        with rasterio.open("tests/data/RGB.byte.tif"):
            pass

    # Expect no debug messages from GDAL.
    log = open(logfile).read()
    assert "GDAL: GDALOpen(tests/data/RGB.byte.tif" not in log
