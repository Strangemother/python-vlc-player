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
        if self.flags is None:

            self.flags = [flag]
            return

        if (flag in self.flags) is False:
            if isinstance(self.flags, tuple):
                self.flags = list(self.flags)
            self.flags.append(flag)

    def build_flags(self, flags=None):
        flags = flags or self.flags
        return flags

    def set_flags(self, flags=None):
        flags = flags or self.flags
        flag_object = self.build_flags(flags)
        if isinstance(flag_object, Qt.WindowFlags):
            self.setWindowFlags(flag_object)
            return

        for f in flag_object:
            self.setWindowFlag(f, True)
