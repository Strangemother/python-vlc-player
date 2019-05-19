
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction
from PyQt5.QtCore import Qt, QSettings, pyqtSignal, QTimer


from view.frame import VideoFrame
from view import api, overlay

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


from input.mouse import MouseActionQWidget


class OverlayMixin(object):

    def overlay_above_all(self):
        self.overlay.above_all()

    def init_overlay(self):
        self.overlay = overlay.Overlay(self)
        self.resized.connect(self.overlay_above_all)
        self.moved.connect(self.overlay_above_all)
        self.play_event.connect(self.overlay_above_all)


class ContextMenuMixin(object):

    pop_menu = None

    def on_context_menu(self, point):
        # show context menu
        print('context', point)
        self.pop_menu.exec_(self.mapToGlobal(point))

    def create_mouse_menu(self):
        # set button context menu policy
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

        # mainMenu = self.menuBar()
        # fileMenu = mainMenu.addMenu('File')
        # editMenu = mainMenu.addMenu('Edit')
        # viewMenu = mainMenu.addMenu('View')
        # searchMenu = mainMenu.addMenu('Search')
        # toolsMenu = mainMenu.addMenu('Tools')
        # helpMenu = mainMenu.addMenu('Help')

        # create context menu
        self.pop_menu = QMenu(self)
        toggle_play = QAction('&Play | &Pause', self)
        self.pop_menu.addAction(toggle_play)
        toggle_play.triggered.connect(self.toggle_play_triggered)
        self.pop_menu.addAction(QAction('test1', self))
        self.pop_menu.addSeparator()
        quit_app = QAction('&Quit', self)
        quit_app.triggered.connect(self.quit_app_triggered)
        self.pop_menu.addAction(quit_app)
        self.pop_menu.setStyleSheet("color: white")

    def toggle_play_triggered(self, event):
        print('toggle play pause')

    def quit_app_triggered(self, event):
        print('exit')

class MediaPlayer(ResizeEventMixin, MoveEventMixin, OverlayMixin,
                  ContextMenuMixin,
                  MouseActionQWidget,
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

        if build is True:
            self.create_ui()

    def create_ui(self):
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
        self.build_view()
        self.show()
        self.init_overlay()
        self.overlay_above_all()
        self.create_mouse_menu()

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

        self.bind_window_frame(frame)
        uri = self.settings.get('file', None)
        if uri is not None:
            self.play(uri)

    def bind_window_frame(self, frame):
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

        return player

    def play(self, uri=None, player=None):
        if uri is not None:
            player = self.set_media(uri)
        if player is None:
            player = self.get_player()

        player.play()
        QTimer.singleShot(10, self.play_event.emit)
        #self.play_event.emit()
