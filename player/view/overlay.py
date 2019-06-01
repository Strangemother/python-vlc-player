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
from input.mouse import MouseActionQWidget
#from player.action import MouseActionQWidget


class OverlayMixin(object):

    def overlay_above_all(self):
        self.overlay.above_all()

    def init_overlay(self):
        self.overlay = Overlay(self)
        self.resized.connect(self.overlay_above_all)
        self.moved.connect(self.overlay_above_all)
        self.play_event.connect(self.overlay_above_all)


class Overlay(QMainWindow, MouseActionQWidget, FlagsMixin):
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

        self.draw_layers = (Draw(), Drawable(), HoverFrame())
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
        for layer in self.draw_layers:
            layer.size = psize
            layer.frame(qp, step, e)


def place(x,y, w, h=None):
    return (x, y, x + w, y + (h or w))

def box(qp, coords, color):
    qp.setBrush(QColor(*color))
    qp.drawRect(*coords)


def ellipse(qp, coords, color):
    qp.setBrush(QColor(*color))
    qp.drawEllipse(*coords)



def  circle(qp, coords, color):
    coords += (coords[-1], )


class Draw(object):

    def frame(self, qp, step, e):
        col = QColor(0, 0, 0)
        #col.setNamedColor('#d4d4d4')
        #qp.setPen(col)

        qp.setPen(Qt.NoPen)
        #qp.setPen(QColor(255, 0, 0))
        qp.setFont(QFont('Open Sans', 20))
        qp.drawText(e.rect(), Qt.AlignCenter, 'apples')
        #box(qp,(10, 10 + step, 60, 15 + step),(200, 0, 0, 44),)
        #box(qp, (130, 15, 90, 60), (255, 80, 0, 160))
        center = (250, 15, 90, 60)
        marked = place(100, 100, 50)
        ellipse(qp, marked, (255, 14, 0, 50))


class Drawable(Draw):

    color = (0,0,0,100)
    function = staticmethod(box)
    xy = (150, 100, )
    wh = (50, )

    def draw(self, qp, step):
        marked = place(*self.xy, *self.wh)
        method = self.function
        col = self.color
        method(qp, marked,  col)

    def frame(self, qp, step, e):
        self.draw(qp, step)


class HoverFrame(Drawable):
    """A unit over the player to show meta data and input actions
    such as a play button.
    """
    color = (0,0,0, 100)
    function = staticmethod(box)
    xy = (0, 0)
    wh = (200, 50)
