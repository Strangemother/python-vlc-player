from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QVBoxLayout, QFrame
from PyQt5.QtCore import Qt, QSettings, pyqtSignal

import asset

class CenterIconFrame(QFrame):
    '''A Video player hosts the x server ot hwnd hook to VLC through as a QFrame
    The video player unit lives within the application - designed to be as
    dumb as possible.'''

    icon_path = 'player/assets/images/teapot'
    background_color = '#333333'

    def __init__(self, parent, app=None):
        super().__init__(parent)
        self.parent = parent
        self.app = app
        self.is_mousedown = False
        self.setStyleSheet("background-color: {};".format(self.background_color))
        self.setMinimumHeight(20)
        # self.setMouseTracking(True)
        self.initUI()
        parent.resized.connect(self._resize)


    def initUI(self):
        # self.move(300, 300)
        icon_container, icon = add_icon(self.icon_path, self,
                                   size=50, color=rgb.WHITE)
        self.icon = icon
        self.icon_container = icon_container
        self._resize()
        self.show()

    def _resize(self):
        parent = self.parent
        psize = parent.size()
        offset = parent.settings.get('bezel', 0)
        size = self.icon.size()
        x = (psize.width() / 2) - (size.width() / 2) - offset
        y = (psize.height() / 2) - (size.height() / 2) - offset - 20

        # container.setStyleSheet("background-color: #4499EE;")
        self.icon_container.move(x, y)



def add_icon(filename, parent, **kw):
    pic = QLabel('apples', parent)

    return pic, asset.png_asset(filename, pic, **kw)


class RGB():
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)

rgb = RGB()



class VideoFrame(CenterIconFrame):
    pass
