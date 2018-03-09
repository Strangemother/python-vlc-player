"""Overlay content on top of the main video
"""
from PyQt5.QtWidgets import (
        QApplication, QWidget, QFrame, QHBoxLayout,
        QVBoxLayout, QLabel, QTextEdit, QMainWindow,
        QPushButton, QMenu, QAction, QLabel

    )
from PyQt5.QtCore import Qt, QTimer, QSize
from player.flags import FlagsMixin
from player.action import MouseActionQWidget

class Overlay(QMainWindow, MouseActionQWidget, FlagsMixin):
    '''An overlay is a standard (or standalone) window positon over
    the VideoFrame for presenting player information. Using a seperate layer
    bypasses issues with an external hooked hwnd frame, allowing fully
    transparent text and graphics with the OS handling antialiasing

    + transparent
    + always on top
    + no OS buttons
    '''
    flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(self.flags)
        self.set_flags()
        self.setMouseTracking(True)
        self.setWindowTitle('Video Player Overlay')

        self.text = ''
        self.label = QLabel(self.text, self)
        self.setStyleSheet("background-color: rgba(80,10,10, 90); color: white")
        self.resize(800, 500)
        self.label.setStyleSheet("color: white")

        self.show()
        # self.pycwnd = win32ui.CreateWindowFromHandle(whndl)

    # install an event filter for Windows' messages. Forward messages to
    # the other HWND
    def winEvent(self,MSG):

        # forward Left button down message to the other window.  Not sure
        # what you want to do exactly, so I'm only showing a left button click.  You could
        if MSG.message == win32con.WM_LBUTTONDOWN or \
           MSG.message == win32con.WM_LBUTTONUP:

            print("left click in front window")
            self.pycwnd.SendMessage(MSG.message, MSG.wParam, MSG.lParam)
            return True, 0 # tells Qt to ignore the message

        return super(Front,self).winEvent(MSG)

    def mouse_move(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        if self.dragging:

            x = self._mouse_down.x()
            y = self._mouse_down.y()

            self.parent.move(event.globalX() - x,  event.globalY() - y)
