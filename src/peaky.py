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

from twisted.internet.protocol import ProcessProtocol
from twisted.python.usage import Options
from twisted.python.usage import UsageError
from twisted.conch.ui.ansi import AnsiParser
from twisted.conch.ui.ansi import ColorText

from kivy.app import App
from kivy.support import install_twisted_reactor
from kivy.utils import QueryDict
from kivy.interactive import InteractiveLauncher

class Options(Options):
    optFlags = [
        ['interactive', 'i', 'Launch in interactive mode.']]

    optParameters = [
        ['lines', 'l', 1024, 'Max number of lines output from top.', int]]

class LoaderBase(object):
    def parse_opts(self, opt_parser):
        opt_parser.parseOptions(argv[1:])

    def get_opt(self):
        opt_parser = Options()
        self.parse_opts(opt_parser)
        return QueryDict(opt_parser)

    def term(self):
        return environ['TERM']

    def spawn_top(self, opt):
        from twisted.internet import reactor
        reactor.spawnProcess(
            processProtocol=TopProc(),
            executable='top',
            args=['top'],
            env={
                'TERM': environ['TERM'],
                'COLUMNS': '512',
                'LINES': str(opt.lines)},
            usePTY=1)

    def load(self):
        app = Peaky(kv_file='peaky.kv')
        opt = self.get_opt()
        if opt.interactive:
            InteractiveLauncher(app).run()
        else:
            app.run()

class LoaderErr(LoaderBase):
    def parse_opts(self, opt_parser):
        try:
            opt = super(LoaderErr, self).parse_opts(opt_parser)
        except UsageError as ue:
            print '%s: %s' % (argv[0], ue)
            print '%s: Try --help for usage details.' % (argv[0])
            exit(1)
        return opt

    def term(self):
        try:
            term = super(LoaderErr, self).env_term()
        except KeyError:
            print 'TERM environment variable not set.'
        return term

class Loader(LoaderErr):
    pass

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

class TopProc(ProcessProtocol):
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

class Peaky(App):
    def __init__(self, **kw):
        super(Peaky, self).__init__(**kw)
        install_twisted_reactor()

Loader().load()
