
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction
from PyQt5.QtCore import Qt, QSettings, pyqtSignal, QTimer



from input.mouse import MouseActionQWidgetBus, ContextMenuMixin
from view.overlay import OverlayMixin
from view.frame import VideoFrame
from view import api, overlay
from bus import get_bus

import flags


class AbstractVLC(object):
    instance = None

    def get_instance(self):
        if self.instance is None:
            self.instance = api.Instance()

        return self.instance


class ResizeEventMixin(object):
    resized = pyqtSignal()

    def resizeEvent(self, event):
        self.resized.emit()
        return super(ResizeEventMixin, self).resizeEvent(event)


class MoveEventMixin(object):
    moved = pyqtSignal()

    def moveEvent(self, event):
        self.moved.emit()
        return super(MoveEventMixin, self).moveEvent(event)


class MediaPlayer(ResizeEventMixin, MoveEventMixin, OverlayMixin,
                  ContextMenuMixin,
                  MouseActionQWidgetBus,
                  flags.FlagsMixin, QWidget, AbstractVLC):

    player = None
    flags = (Qt.FramelessWindowHint,

            # | Qt.WindowStaysOnBottomHint
            )
    play_event = pyqtSignal()

    def __init__(self, settings=None, app=None, build=True):
        super().__init__()

        self.offset = None
        self.frame = None
        self.last_xy = None
        self.is_fullscreen = False
        self.app = app
        self.settings = settings or {}
        self.sys_conf = QSettings('SMPlayer', 'MediaPlayer')
        self.bus = get_bus()

        if build is True:
            self.create_ui()

        self.setAcceptDrops(True)


    def dragEnterEvent(self, e):
        mime = e.mimeData()
        print('dragEnter', mime.urls())
        e.accept()

    def dropEvent(self, e):
        mime = e.mimeData()
        #mime.dumpObjectInfo()
        self.play(e.mimeData().text())


    def create_ui(self):
        self.bus.emit('create_media_player')
        self.setFocusPolicy(Qt.WheelFocus)
        self.resize(500, 400)

        geometry = self.sys_conf.value('geometry', '')
        if isinstance(geometry, str) is False:
            self.restoreGeometry(geometry)

        self.set_flags()
        color = self.settings.get('background-color',  '#3f4d82')
        self.setStyleSheet("background-color: {}".format(color))
        self.present()


    def present(self):
        self.bus.emit('pre-present')
        self.build_view()
        self.show()
        self.init_overlay()
        self.overlay_above_all()
        self.create_mouse_menu()
        self.bus.emit('presented')

    def mouse_down(self, event):
        self.overlay_above_all()
        super().mouse_down(event)

    def build_view(self):

        # self.overlays = (Overlay(), )
        frame = VideoFrame(self, app=self.app)
        self.frame = frame
        layout = QVBoxLayout(self)
        self.layout = layout

        layout.addWidget(frame, 10)
        #controls = QWidget()
        #self.progress = ProgressBar(self)
        #controls.setStyleSheet("background-color: red")
        #layout.addWidget(controls, 1)
        #controls.setGeometry(10, 50, 400, 10)
        self.setLayout(layout)
        # controls = ControlPanel(self)
        # self.controls = controls

        self.show()


        self.bind_player_frame(frame)
        uri = self.settings.get('file', None)
        if uri is not None:
            self.play(uri)

    def bind_player_frame(self, frame):
        frame_win_id = frame.winId()
        player = self.get_player()
        print('Bind', player, frame_win_id)
        player.set_hwnd(frame_win_id)
        player.video_set_key_input(0)
        player.video_set_mouse_input(0)

    def get_player(self):
        """Fetch the media player from the VLC instance.
        If the self.player does not exist, a new _unload_ player is returned.
        """
        if self.player is None:
            vlc = self.get_instance()
            self.player = vlc.media_player_new()
        return self.player

    def set_media(self, uri=None):
        """Apply the URI to the internal media player through the VLC
        instance.
        if URI is none, the settings.file is used. This does not bind a new
        player window.
        """
        uri = uri or self.settings.get('file', None)
        vlc = self.get_instance()
        player = self.get_player()

        player.set_media(vlc.media_new(uri))
        self.setWindowTitle(uri)
        self.bus.emit('set_media', uri)
        return player

    def play(self, uri=None, player=None):
        if uri is not None:
            player = self.set_media(uri)
        if player is None:
            player = self.get_player()

        player.play()
        QTimer.singleShot(10, self.play_event.emit)
        #self.play_event.emit()
        self.bus.emit('play', uri)
