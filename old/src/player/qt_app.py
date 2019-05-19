"""Main interface for a QT app.

1. Main video screen
2. Overlay for screen extras
"""
import sys
import os
import json
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import (
        QApplication, QWidget, QFrame, QHBoxLayout,
        QVBoxLayout, QLabel, QTextEdit, QMainWindow,
        QPushButton, QMenu, QAction, QLabel

    )

from player.player import MediaPlayer
from player.flags import FlagsMixin
from player.keyboard import thread_listen as external_listener


# Base settings to override
SETTINGS = dict(
    # set the main window OS frame - set True to remove the OS frame
    frameless=True,
    json_file='config.json',
    init_size=[500, 400],
    player_title='My Fancy Player',
    bezel=2,
    assets='assets',
    images='{assets}/images',
    cache='{assets}/cache',
    # Filename loaded initially
    file="M:/tv/Men.Behaving.Badly.Season.5.DVD.x264/Men.Behaving.Badly.S05E02.The.Good.Pub.Guide.mkv",
    # If a file is given, should the app autoplay on init load
    autoplay=True,
)

PLAYER_ROOT = os.path.abspath(os.path.dirname(__file__))
RAISE = '__defraise__'


def resolve_in(conf, name, default=RAISE):
    '''Return a key `name` from the given conf `dict`. Resolved strings are
    formatted through the same conf dict, returning a templated string.
    '''
    if (name in conf) is False and default == RAISE:
        # Raise a default error early.
        return conf.get(name)

    val = conf.get(name, default)
    return val.format(**conf)


from player.media import png_asset


class App(object):
    '''A Non-Qt abstraction of all the components running the player'''
    built = False
    def build(self, settings=None):
        self.app = QApplication(sys.argv)
        config = self.load_settings(settings)
        self.config = config
        self.build_ui(config)
        self.built=True

    def run(self, settings=None):
        if self.built is False:
            self.build()
        self.set_app_icon(self.config)
        sys.exit(self.app.exec_())

    def set_app_icon(self, config):

        app = self.app
        image_path = resolve_in(config, 'images')
        app_icon = QtGui.QIcon()
        icon_path = os.path.join(PLAYER_ROOT, image_path, 'teapot')

        # app_icon.addFile(icon_path, QSize(16,16))
        # app_icon.addFile(icon_path, QSize(24,24))
        # app_icon.addFile(icon_path, QSize(32,32))
        # app_icon.addFile(icon_path, QSize(48,48))
        # app_icon.addFile(icon_path, QSize(256,256))

        app_icon.addPixmap(png_asset(icon_path, size=256))
        app.setWindowIcon(app_icon)
        return app_icon

    def load_settings(self, settings=None):
        config = SETTINGS.copy()

        fp = os.path.join(PLAYER_ROOT, config['json_file'])
        file_conf = {}
        if os.path.isfile(fp):
            with open(fp, 'r') as stream:
                file_conf = json.load(stream)
            config.update(file_conf)

        if settings is not None:
            config.update(settings)

        return config

    def build_ui(self, settings=None):
        print(MediaPlayer)
        self.players = (MediaPlayer(settings=settings, app=self.app), )
        # An application can host more than one video panel
