from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
        QApplication, QWidget, QFrame, QHBoxLayout,
        QVBoxLayout, QLabel, QTextEdit, QMainWindow,
        QPushButton, QMenu, QAction, QLabel

    )


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
            self.parent.move(x-x_w, y-y_w)
            new_xy = "{}{}".format(x,y)
            if self.last_xy != new_xy:
                self.moved = True
            self.last_xy = new_xy

    def mouseReleaseEvent(self, e):
        # print('Mouse release')

        if self.offset is not None:
            print('Finished drag')
        self.offset = None


class VideoFrame(QFrame, DragMixin):
    '''A Video player hosts the x server ot hwnd hook to VLC through as a QFrame
    The video player unit lives within the application - designed to be as
    dumb as possible.'''

    double_click_timeout = 200

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.offset = None
        self.moved = False
        self.last_xy = None
        self.is_mousedown = False
        self.setStyleSheet("background-color: #3f4d82;")
        self.setMinimumHeight(20)

        self.setMouseTracking(True)
        self.initUI()

    def initUI(self):
        # self.move(300, 300)
        self.show()

    def enterEvent(self, event):
        print( "VF Entered")
        return super(VideoFrame, self).enterEvent(event)

    def leaveEvent(self, event):
        print( "VF Left")

    def mouseDoubleClickEvent(self, event):
        self.last = "double click"
        print('VF Double click')

    def mouse_click(self):

        if self.last == "click":
            self.update()

