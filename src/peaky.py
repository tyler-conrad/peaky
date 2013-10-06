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

from twisted.python.usage import Options
from twisted.python.usage import UsageError

from twisted.python.log import PythonLoggingObserver
PythonLoggingObserver(loggerName='kivy').start()

from kivy.app import App
from kivy.support import install_twisted_reactor
from kivy.utils import QueryDict
from kivy.interactive import InteractiveLauncher

from top import TopProc
from log import Loggable

class Options(Options):
    optFlags = [
        ['interactive', 'i', 'Launch in interactive mode.']]

    optParameters = [
        ['lines', 'l', 1024, 'Max number of lines output from top.', int]]

class Peaky(App):
    def __init__(self, **kw):
        super(Peaky, self).__init__(**kw)
        install_twisted_reactor()

class LoaderBase(Loggable):
    def parse_opts(self, opt_parser):
        opt_parser.parseOptions(argv[argv.index('--') + 1:])

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
                'TERM': self.term(),
                'COLUMNS': '512',
                'LINES': str(opt.lines)},
            usePTY=1)

    def load(self):
        app = Peaky(kv_file='peaky.kv')
        opt = self.get_opt()
        print opt.interactive
        if opt.interactive:
            InteractiveLauncher(app).run()
        else:
            app.run()
        self.spawn_top(opt)

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
            term = super(LoaderErr, self).term()
        except KeyError:
            print 'TERM environment variable not set.'
        return term

class Loader(LoaderErr):
    pass

Loader().load()
