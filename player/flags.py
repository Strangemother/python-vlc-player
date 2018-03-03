import operator
from PyQt5.QtCore import Qt


INVISIBLE = [
    Qt.FramelessWindowHint,
    Qt.Tool,
    Qt.WindowCloseButtonHint,
    Qt.WindowStaysOnTopHint
    ]

FRAMELESS = [Qt.FramelessWindowHint]

class FlagsMixin(object):

    # flags = [Qt.FramelessWindowHint, Qt.Tool, Qt.WindowCloseButtonHint, Qt.WindowStaysOnTopHint]
    flags = None

    def remove_flag(self, flag):
        if flag in self.flags:
            self.flags.remove(flag)

    def add_flag(self, flag):
        if (flag in self.flags) is False:
            self.flags = list(self.flags).append(flag)

    def build_flags(self, flags=None):
        flags = flags or self.flags

        res = 0
        for f in self.flags:
            res = operator.__or__(res, f)
        return res

    def set_flags(self, flags=None):
        flags = flags or self.flags
        flag_object = self.build_flags(flags)
        self.setWindowFlags(flag_object)
