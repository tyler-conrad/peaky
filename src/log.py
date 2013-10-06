# Copyright (c) Tyler Conrad.
# See LICENSE for details.

"""

"""

from logging import DEBUG
from logging import INFO
from logging import WARNING
from logging import ERROR
from logging import CRITICAL

from twisted.python import log

class Loggable(object):
    def log(self, msg, args, level):
        log.msg(self.__class__.__name__
            + ': '
            + msg.format(args),
            logLevel=level)

    def debug(self, msg, args=None):
        self.log(msg, args, DEBUG)

    def info(self, msg, args=None):
        self.log(msg, args, INFO)

    def warn(self, msg, args=None):
        self.log(msg, args, WARNING)

    def err(self, msg, args=None):
        self.log(msg, args, ERROR)

    def crit(self, msg, args=None):
        self.log(msg, args, CRITICAL)