"""Overlay content on top of the main video
"""
from PyQt5.QtWidgets import (
        QApplication, QWidget, QFrame, QHBoxLayout,
        QVBoxLayout, QLabel, QTextEdit, QMainWindow,
        QPushButton, QMenu, QAction, QLabel

    )
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QSize
from flags import FlagsMixin
from input.mouse import MouseActionQWidgetBus
#from player.action import MouseActionQWidget
from player.view import draw

class OverlayMixin(object):

    def overlay_above_all(self):
        self.overlay.above_all()

    def init_overlay(self):
        self.overlay = Overlay(self)
        self.resized.connect(self.overlay_above_all)
        self.moved.connect(self.overlay_above_all)
        self.play_event.connect(self.overlay_above_all)


class Overlay(QMainWindow, MouseActionQWidgetBus, FlagsMixin):
    '''An overlay is a standard (or standalone) window positon over
    the VideoFrame for presenting player information. Using a seperate layer
    bypasses issues with an external hooked hwnd frame, allowing fully
    transparent text and graphics with the OS handling antialiasing

    + transparent
    + always on top
    + no OS buttons
    '''
    flags = (Qt.FramelessWindowHint
            | Qt.WindowCloseButtonHint
            | Qt.Tool
            #| Qt.SplashScreen
            #| Qt.WindowStaysOnTopHint
            )

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(self.flags)
        self.set_flags()
        self.setMouseTracking(True)
        self.setWindowTitle('Video Player Overlay')
        self._step = 0
        self.text = ''
        self.label = QLabel(self.text, self)
        self.setStyleSheet("background-color: rgba(80,10,10, 90); color: white")
        self.resize(800, 800)
        self.label.setStyleSheet("color: white")

        parent.resized.connect(self._resize)
        parent.moved.connect(self._move)
        parent.play_event.connect(self._seat)

        greenish = (0, 255, 10, 100)
        self.draw_layers = (
            #Draw(),
            #Drawable(),
            draw.HoverFrame(),
            draw.Text(text='playing', color=greenish),
            draw.Drawable(draw.ellipse,
                #pos=Qt.AlignCenter,
                xy=(50,50),
                wh=(30, ),
                color=greenish,
                antialiasing=False,
            ),
            draw.Drawable(draw.ellipse,
                #pos=Qt.AlignCenter,
                xy=(200,50),
                wh=(30, ),
                color=greenish,
                antialiasing=True,
            ),
            draw.Drawable(draw.ellipse,
                #pos=Qt.AlignCenter,
                xy=(300,50),
                wh=(30, ),
                color=greenish,
                antialiasing=False,
            ),
        )

        self.show()
        # self.pycwnd = win32ui.CreateWindowFromHandle(whndl)

    def _resize(self):
        parent = self.parent
        psize = parent.size()
        offset = parent.settings.get('bezel', 0)
        # container.setStyleSheet("background-color: #4499EE;")
        self.resize(psize)

    def _move(self):
        self.move(self.parent.pos())

    def above_all(self):
        self.activateWindow()

    def _seat(self):
        self._resize()
        self._move()
        self.above_all()

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
        if self.dragging is True and self._mouse_down is not None:
            x = self._mouse_down.x()
            y = self._mouse_down.y()

            self.parent.move(event.globalX() - x,  event.globalY() - y)

    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self._step += 1
        self.draw_frame(qp, e)
        qp.end()

    def draw_frame(self, qp, e):
        step = self._step
        psize = self.parent.size()
        qp.setPen(Qt.NoPen)

        for layer in self.draw_layers:
            layer.size = psize
            layer.frame(qp, step, e)
