# Copyright (c) Tyler Conrad.
# See LICENSE for details.

'''
Usage: peaky.py [options]
Options:
  -i, --interactive  Launch in interactive mode.
  -l, --lines=   Max number of lines output from top. [default: 1024]
      --version  Display Twisted version and exit.
      --help     Display this help and exit.
'''
from sys import argv
from arg_split import ArgSplitter
ArgSplitter.argv = argv[:]

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
    def parse_opts(self, opt_parser, splitter):
        opt_parser.parseOptions(splitter.peaky_args()[1:])

    def peaky_opts(self, splitter):
        opt_parser = Options()
        self.parse_opts(opt_parser, splitter)
        return QueryDict(opt_parser)

    def term(self):
        return environ['TERM']

    def spawn_top(self, peaky_opts, top_args):
        from twisted.internet import reactor
        top_args = ['top']
        top_args.extend(top_args)
        
        reactor.spawnProcess(
            processProtocol=TopProc(),
            executable='top',
            args=top_args,
            env={
                'TERM': self.term(),
                'COLUMNS': '512',
                'LINES': str(peaky_opts.lines)},
            usePTY=1)

    def run_interactive(self, app):
        InteractiveLauncher(app).run()

    def load(self):
        splitter = ArgSplitter()
        splitter.kivy_args()
        po = self.peaky_opts(splitter)
        
        app = Peaky(kv_file='peaky.kv')
        if po.interactive:
            self.run_interactive(app)
        else:
            app.run()
        self.spawn_top(po, splitter.top_args())

class LoaderErr(LoaderBase):
    def parse_opts(self, opt_parser, splitter):
        try:
            opt = super(LoaderErr, self).parse_opts(opt_parser, splitter)
        except UsageError as ue:
            script_name = splitter.peaky_args()[0]
            print '%s: %s' % (script_name, ue)
            print '%s: Try --help for usage details.' % (script_name)
            exit(1)
        return opt

    def term(self):
        try:
            term = super(LoaderErr, self).term()
        except KeyError:
            print 'TERM environment variable not set.'
        return term

class LoaderLog(LoaderErr):
    def run_interactive(self, app):
        self.info('Starting app in interactive mode.')
        super(LoaderLog, self).run_interactive(app)

    def spawn_top(self, peaky_opts, top_args):
        self.debug('Spawning top subprocess.')
        super(LoaderLog, self).spawn_top(peaky_opts, top_args)

class Loader(LoaderLog):
    pass

Loader().load()
