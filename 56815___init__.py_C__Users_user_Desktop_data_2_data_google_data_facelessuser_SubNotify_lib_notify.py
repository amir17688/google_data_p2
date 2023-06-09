"""
Notify.

Copyright (c) 2013 - 2015 Isaac Muse <isaacmuse@gmail.com>
License: MIT
"""
from __future__ import unicode_literals
from __future__ import absolute_import
import sys
from .notify_growl import get_growl, enable_growl, growl_enabled, setup_growl, has_growl, growl_destroy

PY3 = (3, 0) <= sys.version_info < (4, 0)

if PY3:
    binary_type = bytes  # noqa
else:
    binary_type = str

if sys.platform.startswith('win'):
    _PLATFORM = "windows"
elif sys.platform == "darwin":
    _PLATFORM = "osx"
else:
    _PLATFORM = "linux"

if _PLATFORM == "windows":
    from .notify_windows import get_notify, alert, setup, windows_icons, destroy
elif _PLATFORM == "osx":
    from .notify_osx import get_notify, alert, setup, destroy
elif _PLATFORM == "linux":
    from .notify_linux import get_notify, alert, setup, destroy

__all__ = ("info", "warning", "error", "setup_notifications", "enable_growl", "has_growl", "destroy_notifications")


###################################
# Fallback Notifications
###################################
class NotifyFallback(object):
    """Fallback class."""

    def __init__(self, *args, **kwargs):
        """Init class."""

        self.sound = kwargs.get("sound", False)

    def Show(self):
        """Fallback just plays an alert."""

        if self.sound:
            alert()


DEFAULT_NOTIFY = NotifyFallback


###################################
# Notification Calls
###################################
def info(title, message, sound=False):
    """Info notification."""

    send_notify(title, message, sound, "Info")


def error(title, message, sound=False):
    """Error notification."""
    send_notify(title, message, sound, "Error")


def warning(title, message, sound=False):
    """Warning notification."""

    send_notify(title, message, sound, "Warning")


def send_notify(title, message, sound, level):
    """Send notification."""

    if title is not None and isinstance(title, binary_type):
        title = title.decode('utf-8')

    if message is not None and isinstance(message, binary_type):
        message = message.decode('utf-8')

    if level is not None and isinstance(level, binary_type):
        level = level.decode('utf-8')

    def default_notify(title, message, sound):
        """Default fallback notify."""

        DEFAULT_NOTIFY(title, message, sound=sound).Show()

    notify = get_notify()
    growl = get_growl()
    if growl_enabled():
        growl(level, title, message, sound, default_notify)
    elif _PLATFORM in ["osx", "linux"]:
        notify(title, message, sound, default_notify)
    elif _PLATFORM == "windows":
        notify(title, message, sound, windows_icons[level], default_notify)
    else:
        default_notify(title, message, sound)


###################################
# Setup Notifications
###################################
def setup_notifications(app_name, png=None, icon=None, term_notify=(None, None)):
    """Setup notifications for all platforms."""

    if icon is not None and isinstance(icon, binary_type):
        icon = icon.decode('utf-8')

    if isinstance(app_name, binary_type):
        app_name = app_name.decode('utf-8')

    setup_growl(app_name, png, alert)
    setup(
        app_name,
        icon if _PLATFORM == "windows" else png,
        term_notify if _PLATFORM == "osx" else None
    )


def destroy_notifications():
    """Destory notifications if possible."""

    growl_destroy()
    destroy()
