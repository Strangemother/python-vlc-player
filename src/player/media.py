import os

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
        QApplication, QWidget, QFrame, QHBoxLayout,
        QVBoxLayout, QLabel, QTextEdit, QMainWindow,
        QPushButton, QMenu, QAction, QLabel

    )

from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap


class DragMixin(object):

    def mousePressEvent(self, e):
        print('DragMixin press')
        self.offset = e.pos()

    def mouseMoveEvent(self, e):
        x = e.globalX()
        y = e.globalY()

        if self.offset is not None:
            x_w = self.offset.x()
            y_w = self.offset.y()

            self.move(x-x_w, y-y_w)
            new_xy = "{}{}".format(x,y)
            if self.last_xy != new_xy:
                self.moved = True
            self.last_xy = new_xy

    def mouseReleaseEvent(self, e):
        # print('Mouse release')

        if self.offset is not None:
            print('DragMixin release')
        self.offset = None


def png_asset(filename, set_to=None, size=32, color=(255, 255,255), mask_color=(0,0,0,)):

    fp = os.path.abspath(filename)
    if os.path.exists(fp):
        raise FileNotFoundError(fp)

    icon = QPixmap(fp)
    #icon.setStyleSheet("text-color: red")
    # scaled_icon = icon.scaled(30, 30, Qt.KeepAspectRatio & Qt.SmoothTransformation)
    mask = icon.createMaskFromColor(QColor(*mask_color), Qt.MaskOutColor)

    p = QPainter()
    p.begin(icon)
    p.setPen(QColor(*color))
    p.drawPixmap(icon.rect(), mask, mask.rect())
    p.end()

    scaled_icon = icon.scaledToHeight(size, Qt.SmoothTransformation)
    #scaled_icon.drawPixmap(pix.rect(), mask, mask.rect())

    if set_to is not None:
        set_to.setPixmap(scaled_icon)

    return scaled_icon


def add_icon(filename, parent, **kw):
    pic = QLabel('apples', parent)

    return pic, png_asset(filename, pic, **kw)


class RGB():
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

rgb = RGB()


class VideoFrame(QFrame):
    '''A Video player hosts the x server ot hwnd hook to VLC through as a QFrame
    The video player unit lives within the application - designed to be as
    dumb as possible.'''


    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.is_mousedown = False
        self.setStyleSheet("background-color: #3f4d82;")
        self.setMinimumHeight(20)
        # self.setMouseTracking(True)
        self.initUI()

    def initUI(self):
        # self.move(300, 300)
        container, icon = add_icon('player/assets/images/teapot', self,
            size=50, color=rgb.WHITE)

        parent = self.parent
        psize = parent.size()
        offset = parent.settings.get('bezel', 0)
        size = icon.size()
        x = (psize.width() / 2) - (size.width() / 2) - offset
        y = (psize.height() / 2) - (size.height() / 2) - offset - 20

        # container.setStyleSheet("background-color: #4499EE;")
        container.move(x, y)

        self.show()
