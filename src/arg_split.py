# Copyright (c) Tyler Conrad.
# See LICENSE for details.

"""

"""

from sys import argv
from log import Loggable

class ArgSplitterBase(object):
    def args_before_sep(self, _list):
        return _list[:_list.index('--')]

    def args_after_sep(self, _list):
        return _list[_list.index('--') + 1:]

    def kivy_args(self):
        return self.args_before_sep(argv)

    def non_kivy_args(self):
        return self.args_after_sep(argv)

    def top_args(self):
        nko = self.non_kivy_args()
        return self.args_before_sep(nko)

    def peaky_args(self):
        nko = self.non_kivy_args()
        pa = [argv[0]]
        pa.extend(self.args_after_sep(nko))
        return pa

class ArgSplitterErr(Loggable, ArgSplitterBase):
    def kivy_args(self):
        try:
            ko = super(ArgSplitterErr, self).kivy_args()
        except ValueError:
            self.debug('No kivy/non-kivy argument separator.')
            return argv
        return ko

    def non_kivy_args(self):
        try:
            nko = super(ArgSplitterErr, self).non_kivy_args()
        except ValueError:
            self.debug("Only kivy argument passed.")
            return []
        return nko

    def top_args(self):
        try:
            to = super(ArgSplitterErr, self).top_args()
        except ValueError:
            self.debug('No top/peaky argument separator.')
            return self.non_kivy_args()
        return to

    def peaky_args(self):
        try:
            po = super(ArgSplitterErr, self).peaky_args()
        except ValueError:
            self.debug('No peaky arguments.')
            return []
        return po

class ArgSplitterLog(ArgSplitterErr):
    def kivy_args(self):
        ko = super(ArgSplitterLog, self).kivy_args()
        self.info('Kivy options: {}', ' '.join(ko))
        return ko

    def top_args(self):
        to = super(ArgSplitterLog, self).top_args()
        self.info('Top options: {}', ' '.join(to))
        return to

    def peaky_args(self):
        po = super(ArgSplitterLog, self).peaky_args()
        self.info(' Peaky options: {}', ' '.join(po))
        return po

class ArgSplitter(ArgSplitterLog):
    pass
