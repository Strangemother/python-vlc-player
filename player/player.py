
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizeGrip
from PyQt5.QtCore import Qt, QSettings
from PyQt5 import QtGui

import sys
from player.media import VideoFrame, DragMixin
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


class KeyAction(object):

    def keyReleaseEvent(self, e):
        pass

    def keyPressEvent(self, e):
        print( "Key", e.key())

        # q, esc
        if e.key() in [81, 16777216]:
            self.controls.close()
            self.close()
            sys.exit(0)


class MouseActionQWidget(QWidget):
    """Attach mouse click, doubleclick and dragging motion.
    combined to ensure dragging and clicking are relatively related.
    """

    draggable = True

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.dragging = False
        self._mouse_down = None
        self.setMouseTracking(True)

    def mouseDoubleClickEvent(self, event):
        self.last = "double click"
        print('Double click')
        self.mouse_double_press(event)
        return super(MouseActionQWidget, self).mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):

        if self.draggable is True:
            self.dragging = True

            x = event.globalX()
            y = event.globalY()

            if self._mouse_down is not None:
                x_w = self._mouse_down.x()
                y_w = self._mouse_down.y()

                self.move(x-x_w, y-y_w)

        self.mouse_move(event)
        return super(MouseActionQWidget, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        print('mouse down')
        self.mouse_down(event)
        self._mouse_down = event.pos()
        return super(MouseActionQWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        print('mouse up')
        self._mouse_down = None
        self.dragging = False
        self.mouse_up(event)
        return super(MouseActionQWidget, self).mouseReleaseEvent(event)

    def enterEvent(self, event):
        print( "Mouse Entered")
        self.mouse_enter(event)
        return super(MouseActionQWidget, self).enterEvent(event)

    def leaveEvent(self, event):
        print( "Mouse Left")
        self.mouse_leave(event)
        return super(MouseActionQWidget, self).enterEvent(event)

    def wheelEvent(self, event):
        print('wheel', event)
        self.mouse_wheel(event)
        return super(MouseActionQWidget, self).wheelEvent(event)

    def mouse_double_press(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_move(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_down(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_up(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_enter(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_leave(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_wheel(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass


class MediaPlayer(MouseActionQWidget, ConfigMixin):
    '''A application interface hosting a VideoFrame and managing its
    interactivity.'''
    double_click_timeout = 200
    frameless = False
    flags = FRAMELESS

    def __init__(self, settings=None, app=None, build=True):
        super().__init__()

        self.offset = None
        self.frame = None
        self.is_fullscreen = False
        self.app = app
        self.settings = settings or {}
        self.last_xy = None
        self.sys_conf = QSettings('SMPlayer', 'MediaPlayer')
        if build is True:
            self.initUI()


    def initUI(self):

        self.setFocusPolicy(Qt.WheelFocus)

        self.config_set_title()
        self.config_set_size()

        self.config_set_frame()
        self.set_flags()
        self.build_view()
        geometry = self.sys_conf.value('geometry', '')
        if isinstance(geometry, str) is False:
            self.restoreGeometry(geometry)

    def keyPressEvent(self, e):
        print( "Key", e.key())

        # q, esc
        if e.key() in [81, 16777216]:
            self.close()
            sys.exit(0)

    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.sys_conf.setValue('geometry', geometry)

    def build_view(self):
        self.setStyleSheet("background-color: #3f4d82")
        # self.overlays = (Overlay(), )
        frame = VideoFrame(self, app=self.app)
        self.frame = frame
        layout = QVBoxLayout(self)
        self.layout = layout

        self.config_set_bezel()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(frame, 10)

        #controls = QWidget()
        #self.progress = ProgressBar(self)
        #controls.setStyleSheet("background-color: red")
        #layout.addWidget(controls, 1)
        #controls.setGeometry(10, 50, 400, 10)

        sizegrip = QSizeGrip(self)
        footer_layout = QHBoxLayout(self)
        label_left = QLabel("PLEFT", self)
        label_left.setStyleSheet("padding: 2; color: #AAA")

        footer_layout.addWidget(label_left, 0, Qt.AlignBottom | Qt.AlignLeft)
        footer_layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        layout.addLayout(footer_layout)
        self.setLayout(layout)

        # controls = ControlPanel(self)
        # self.controls = controls
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
        self.player = player

        if self.frame is not None:
            player.set_hwnd(self.frame.winId())

        if self.settings.get('autoplay', False) is True:
            player.play()

    def mouse_double_press(self, event):
        if self.is_fullscreen is False:
            self.showFullScreen()
            self.is_fullscreen = True
            self.raise_()
        else:
            self.showNormal()
            self.is_fullscreen = False

        self.draggable = not self.is_fullscreen


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

    show_progress = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('View')
        # print('Controls')
        self.setStyleSheet("background-color: red;")
        # self.resize(50, 200)
        self.setMinimumHeight(20)

        if self.show_progress:
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
        if self.show_progress:
            layout.addWidget(self.bar, 1)
        layout.setContentsMargins(0,0,0,0)
        #self.geometry().setTop(200)
        #self.show()


    def enterEvent(self, event):

        if self.show_progress:
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

        if self.show_progress:
            #self._prev_geom.setHeight(30)
            self.setGeometry(self._prev_geom)
            #self.resize(100, 300)
        print('leave')
        return super(ControlPanel, self).leaveEvent(event)
