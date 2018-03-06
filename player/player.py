
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizeGrip
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

from player.media import VideoFrame
from player.flags import FlagsMixin, FRAMELESS
from player import simple

UNDEFINED = 'undefined'

class ConfigMixin(FlagsMixin):

    frameless = None

    def config_set_frame(self, settings=None, value=None):
        # no windows buttons or edge
        settings = settings or self.settings
        on = settings.get('frameless', value or self.frameless)
        if value is not None:
            on = value
        print('turn', on)
        flag = Qt.FramelessWindowHint

        if on is True:
            self.add_flag(flag)
            return True
            #self.setWindowFlags(Qt.FramelessWindowHint)

        self.remove_flag(flag)
        return False

    def config_set_title(self, settings=None):
        settings = settings or self.settings
        title = settings.get('player_title', 'Video Player')
        self.setWindowTitle(title)

    def config_set_size(self, settings=None):
        settings = settings or self.settings
        size = settings.get('init_size', (500, 400,))
        self.resize(*size)

    def config_set_bezel(self, settings=None):
        settings = settings or self.settings
        size = settings.get('bezel', 5)
        opts = size

        if isinstance(size, (int)):
            size = [size]

        if isinstance(size, (list, tuple,)):
            if len(size) == 1:
                opts = size * 4
            if len(size) == 2:
                tb, lr = opts
                opts = tb, lr, tb, lr
            if len(size) == 3:
                tb, l, r = size
                opts = tb, l, tb, r

        self.layout.setContentsMargins(*opts)


class MediaPlayer(QWidget, ConfigMixin):
    '''A application interface hosting a VideoFrame and managing its
    interactivity.'''

    frameless = False
    flags = FRAMELESS

    def __init__(self, settings=None, app=None, build=True):
        super().__init__()

        self.frame = None
        self.app = app
        self.settings = settings or {}

        if build is True:
            self.initUI()


    def initUI(self):

        self.setFocusPolicy(Qt.WheelFocus)

        self.config_set_title()
        self.config_set_size()

        self.config_set_frame()
        self.set_flags()

        self.build_view()

    def build_view(self):
        # self.setStyleSheet("background-color: #3f4d82")
        # self.overlays = (Overlay(), )
        frame = VideoFrame(self, app=self.app)
        self.frame = frame
        layout = QVBoxLayout(self)
        self.layout = layout
        self.setLayout(layout)
        self.config_set_bezel()

        layout.addWidget(frame, 9)

        #controls = QWidget()
        controls = ControlPanel(self)
        #self.progress = ProgressBar(self)
        #controls.setStyleSheet("background-color: red")
        #layout.addWidget(controls, 1)
        #controls.setGeometry(10, 50, 400, 10)

        sizegrip = QSizeGrip(self)
        layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        self.controls = controls
        self.show()
        self.play(self.settings.get('file', None))

    def play(self, filepath=UNDEFINED):

        fn = filepath
        if fn == UNDEFINED:
            fn = self.settings.get('file', None)

        if fn is None:
            return False

        s = simple.Service()
        player = s.get_player(fn)
        player.video_set_key_input(0)
        player.video_set_mouse_input(0)

        if self.frame is not None:
            player.set_hwnd(self.frame.winId())

        if self.settings.get('autoplay', False) is True:
            player.play()


class ProgressBar(QWidget):
    """docstring for ProgressBar"""
    def __init__(self, parent=None):
        super().__init__()
        self.mouse_down = False
        self.setMouseTracking(True)
        self._left_offset = 100
        self.setStyleSheet("background-color: green")
        self._size = [500, 100]
        self._label_width = 100

        width = self._label_width
        size = self._size

        self.label_left = QLabel("PLEFT", self)
        self.label_left.setGeometry(0, 0, width, size[1])
        self.label_left.setAlignment(Qt.AlignTop)

        self.label_right = QLabel("RLEFT", self)
        self.label_right.setGeometry(size[0] - width, 0, width, size[1])
        self.label_right.setAlignment(Qt.AlignTop | Qt.AlignRight)

        self.label_left.setStyleSheet("color: white; padding: 0 10")
        self.label_right.setStyleSheet("color: white; padding: 0 10")
        # self.show()

    def mouseMoveEvent(self, event):
        self._left_offset = event.pos().x()
        # update painter event
        self.update()
        return super(ProgressBar, self).mouseMoveEvent(event)

    def leaveEvent(self, event):
        self._left_offset = 1
        # update painter event
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_down = True

    def mouseReleaseEvent(self, event):
        self.mouse_down = False

    def paintEvent(self, event):
        painter = QtGui.QPainter()

        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Background
        pw = self._size[0] - (self._label_width * 2)
        height = self._size[1]
        painter.fillRect(self._label_width, 0, pw, height, QtGui.QBrush(QtGui.QColor(0, 100, 100, 255)))

        # play progress
        painter.fillRect(self._label_width, 0, self._label_width + 50, height, QtGui.QBrush(QtGui.QColor(0, 200, 100, 255)))

        # mouse point
        painter.drawLine(self._left_offset, 1, self._left_offset, self.height() - 1)

        # Test X
        painter.drawLine(self.width()/8, self.height()/8, 7*self.width()/8, 7*self.height()/8)
        painter.drawLine(self.width()/8, 7*self.height()/8, 7*self.width()/8, self.height()/8)

        # Close
        painter.setPen(QtGui.QPen(Qt.NoPen))

    def resizeEvent(self, event):
        pass




class ControlPanel(QWidget):
    '''Main panel of minimal controls.'''
    #def initUI(self):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('View')
        # print('Controls')
        self.setStyleSheet("background-color: red;")
        # self.resize(50, 200)
        self.setMinimumHeight(20)
        self.bar = ProgressBar(self)
        self.bar.setGeometry(0, 20, 30, 100)
        #self.bar.show()

        # left, top, width, height
        self.setGeometry(0, 370, 500, 50)
        self.initUI()

    def initUI(self):
        # self.setStyleSheet("background-color: #3f4d82")
        # self.overlays = (Overlay(), )
        layout = QVBoxLayout(self)
        self.layout = layout
        self.setLayout(layout)
        layout.addWidget(self.bar, 1)
        layout.setContentsMargins(0,0,0,0)
        #self.geometry().setTop(200)
        #self.show()


    def enterEvent(self, event):
        self._prev_geom = self.geometry()
        self._last_height = self._prev_geom.height()

        geom = self.geometry()
        #geom.setHeight(80)
        geom.setTop(self._prev_geom.top() - (self._last_height * .5) - 20)
        geom.setBottom(self._prev_geom.bottom() - self._last_height * .5)
        self.setGeometry(geom)

        #self.setMaximumHeight(80)
        #self.setMinimumHeight(80)
        print('enter')
        #self.geometry().setTop(-10)
        return super(ControlPanel, self).enterEvent(event)

    def leaveEvent(self, event):
        # self.setMaximumHeight(80)
        #self.setMinimumHeight(30)

        #self._prev_geom.setHeight(30)
        self.setGeometry(self._prev_geom)
        #self.resize(100, 300)
        print('leave')
        return super(ControlPanel, self).leaveEvent(event)
