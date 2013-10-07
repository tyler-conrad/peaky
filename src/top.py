# Copyright (c) Tyler Conrad.
# See LICENSE for details.

"""

"""
from twisted.conch.ui.ansi import AnsiParser
from twisted.conch.ui.ansi import ColorText
from twisted.internet.protocol import ProcessProtocol

from kivy.base import stopTouchApp

def stop_peaky(exit_code=0):
    stopTouchApp()
    try:
        exit(exit_code)
    except:
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
        if 'top:' in data:
            stop_peaky(1)

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
        print reason.getErrorMessage()

    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"
        print reason.getErrorMessage()
