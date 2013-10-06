# Copyright (c) Tyler Conrad.
# See LICENSE for details.

'''
Usage: peaky.py [options]
Options:
  -l, --lines=   Max number of lines output from top. [default: 1024]
      --version  Display Twisted version and exit.
      --help     Display this help and exit.
'''

from sys import argv
from os import environ

from twisted.internet import reactor
from twisted.internet.protocol import ProcessProtocol
from twisted.python.usage import Options
from twisted.python.usage import UsageError
from twisted.conch.ui.ansi import AnsiParser
from twisted.conch.ui.ansi import ColorText

class Options(Options):
#     optFlags = [
#         ["fast", "f", "Act quickly"]]

    optParameters = [
        ['lines', 'l', 1024, 'Max number of lines output from top.', int]]

opts = Options()
try:
    opts.parseOptions(argv[1:])
except UsageError as ue:
    print '%s: %s' % (argv[0], ue)
    print '%s: Try --help for usage details.' % (argv[0])
    exit(1)

class PeakyAnsiParser(AnsiParser, object):
    def __init__(
            self,
            defaultFG=ColorText.WHITE,
            defaultBG=ColorText.BLACK):
        super(PeakyAnsiParser, self).__init__(
            defaultFG,
            defaultBG)
        self.color_text_list = []

    def writeString(self, color_text):
        text = color_text.text = color_text.text.replace('\r\n', '')
        if not text or text == 'B':
            return

        self.color_text_list.append(color_text)

class Top(ProcessProtocol):
    def __init__(self):
        self.data = ''

    def connectionMade(self):
        pass

    def outReceived(self, data):
        if 'top -' in data:
            def color_text_list():
                pap = PeakyAnsiParser()
                pap.parseString(self.data)
                return pap.color_text_list

            self.data = data
        else:
            self.data += data

    def errReceived(self, data):
        print "errReceived! with %d bytes!" % len(data)
        print data

    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"

    def outConnectionLost(self):
        print "outConnectionLost! The child closed their stdout!"

    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."

    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)

    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"
        reactor.stop()

def env_term():
    try:
        return environ['TERM']
    except KeyError:
        print 'TERM environment variable not set.'
        return None
        

reactor.spawnProcess(
    processProtocol=Top(),
    executable='top',
    args=['top'],
    env={
        'TERM': environ['TERM'],
        'COLUMNS': '512',
        'LINES': str(opts['lines']),
    },
    usePTY=1)

reactor.run()
