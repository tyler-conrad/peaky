# Copyright (c) Tyler Conrad.
# See LICENSE for details.

'''
Usage: peaky.py [options]
Options:
  -f, --fast     Act quickly
      --version  Display Twisted version and exit.
      --help     Display this help and exit.
'''

from sys import argv
from os import environ

from twisted.python.usage import Options
from twisted.python.usage import UsageError
from twisted.internet.protocol import ProcessProtocol
from twisted.internet import reactor

class Options(Options):
    optFlags = [
        ["fast", "f", "Act quickly"]]

opts = Options()
try:
    opts.parseOptions(argv[1:])
except UsageError as ue:
    print '%s: %s' % (argv[0], ue)
    print '%s: Try --help for usage details.' % (argv[0])
    exit(1)

if opts['fast']:
    print "fast",

class Top(ProcessProtocol):
    def __init__(self):
        self.data = ""

    def connectionMade(self):
#         self.transport.write(top)
        self.transport.closeStdin() # tell them we're done

    def outReceived(self, data):
        print "outReceived! with %d bytes!" % len(data)
        self.data = self.data + data

    def errReceived(self, data):
        print "errReceived! with %d bytes!" % len(data)
        print data

    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"

    def outConnectionLost(self):
        print "outConnectionLost! The child closed their stdout!"
        print self.data

    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."

    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)

    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"
        reactor.stop()

reactor.spawnProcess(
    processProtocol=Top(),
    executable="top",
    args=["top"],
    env={'TERM': environ['TERM']},
    usePTY=1)
reactor.run()
