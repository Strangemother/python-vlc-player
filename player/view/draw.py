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


def place(x,y, w, h=None):
    return (x, y,  w, h or w)


def box(qp, coords, color):
    qp.setBrush(QColor(*color))
    qp.drawRect(*coords)


def ellipse(qp, coords, color):
    qp.setBrush(QColor(*color))
    qp.drawEllipse(*coords)


def text(qp, coords, **params):
    qp.setPen(QColor(*params['color']))
    qp.setFont(QFont(params.get('font'), params.get('font_size')))
    qp.drawText(params.get('bound', None), coords, params.get('text'))


def  circle(qp, coords, color):
    coords += (coords[-1], )


class Draw(object):

    def frame(self, qp, step, e):
        col = QColor(0, 0, 0)
        #col.setNamedColor('#d4d4d4')
        #qp.setPen(col)
        qp.setPen(QColor(255, 255, 255))
        qp.setFont(QFont('Open Sans', 20))
        qp.drawText(e.rect(), Qt.AlignCenter, 'apples')
        #box(qp,(10, 10 + step, 60, 15 + step),(200, 0, 0, 44),)
        #box(qp, (130, 15, 90, 60), (255, 80, 0, 160))
        qp.setPen(Qt.NoPen)
        marked = self.position(qp)
        ellipse(qp, marked, (255, 14, 0, 50))

    def position(self, qp):
        return place(100, 100, 50)


class Drawable(Draw):

    color = (0,0,0, 200)
    function = staticmethod(box)
    xy = (150, 100, )
    wh = (50, )
    clear = True
    antialiasing = False


    def __init__(self, function=None, **kw):
        if function is not None:
            self.function = function
            staticmethod(self.function)

        if kw.get('pos', None) is not None:
            self.xy=None

        self.__dict__.update(kw)

    def frame(self, qp, step, e):
        if self.clear:
            qp.setPen(Qt.NoPen)

        qp.setRenderHint(QPainter.Antialiasing, on=self.antialiasing)

        self.draw(qp, step, e)

    def draw(self, qp, step, e):

        marked = self.position(qp)
        method = self.function
        return method(qp, marked,  self.color)

    def position(self, qp):
        if hasattr(self, 'pos'):
            return self.pos
        return place(*self.xy, *self.wh)


class Text(Drawable):
    function = staticmethod(text)
    font = 'Open Sans'
    font_size = 20
    text = 'placeholder'

    def draw(self, qp, step, e):
        position = self.position(qp)
        method = self.function
        return method(qp, position,
            font=self.font,
            bound=e.rect(),
            font_size=self.font_size,
            text=self.text,
            color=self.color
            )

    def position(self, qp):
        return Qt.AlignCenter


class HoverFrame(Drawable):
    """A unit over the player to show meta data and input actions
    such as a play button.
    """
    color = (0,0,0, 150)
    function = staticmethod(box)
    xy = (0, 0)
    wh = (200, 50)
