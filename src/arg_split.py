# Copyright (c) Tyler Conrad.
# See LICENSE for details.

"""

"""

import sys
from log import Loggable

class ArgSplitterBase(object):
    def args_before_sep(self, _list):
        return _list[:_list.index('--')]

    def args_after_sep(self, _list):
        return _list[_list.index('--') + 1:]

    def kivy_args(self):
        return self.args_before_sep(sys.argv)

    def non_kivy_args(self):
        return self.args_after_sep(sys.argv)

    def top_args(self):
        nko = self.non_kivy_args()
        return self.args_before_sep(nko)

    def append_peaky_args(self, arg_list, non_kivy_args):
        arg_list.extend(self.args_after_sep(non_kivy_args))
        return arg_list

    def peaky_args(self):
        return self.append_peaky_args(
            [sys.argv[0]],
            self.non_kivy_args())

class ArgSplitterErr(Loggable, ArgSplitterBase):
    def append_peaky_args(self, arg_list, non_kivy_args):
        try:
            arg_list = super(ArgSplitterErr, self).append_peaky_args(
                arg_list,
                non_kivy_args)
        except ValueError:
            self.debug('No peaky arguments.')
        return arg_list

    def kivy_args(self):
        try:
            ko = super(ArgSplitterErr, self).kivy_args()
        except ValueError:
            self.debug('No kivy/non-kivy argument separator.')
            return sys.argv
        return ko

    def non_kivy_args(self):
        try:
            nko = super(ArgSplitterErr, self).non_kivy_args()
        except ValueError:
            self.debug("Only kivy arguments passed.")
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
        po = super(ArgSplitterErr, self).peaky_args()
        if len(po) == 1:
            self.debug('No peaky arguments.')
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
        self.info('Peaky options: {}', ' '.join(po))
        return po

class ArgSplitter(ArgSplitterLog):
    pass
