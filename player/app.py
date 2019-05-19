"""Main interface for a QT app.

1. Main video screen
2. Overlay for screen extras
"""
import sys
import os
import json

from PyQt5.QtWidgets import (
        QApplication
        )

# from PyQt5 import QtGui
# from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
# from PyQt5.QtCore import Qt, QTimer, QSize
# from PyQt5.QtWidgets import (
#         QApplication, QWidget, QFrame, QHBoxLayout,
#         QVBoxLayout, QLabel, QTextEdit, QMainWindow,
#         QPushButton, QMenu, QAction, QLabel

#     )

# from player.player import MediaPlayer
# from player.flags import FlagsMixin
# from player.keyboard import thread_listen as external_listener
# from player.media import png_asset
import asset
import settings
from view.mediaplayer import MediaPlayer


class App(object):
    '''A Non-Qt abstraction of all the components running the player'''
    built = False

    def build(self, init_settings=None):
        print('Build')
        self.app = QApplication(sys.argv)
        config = settings.load_settings(init_settings)
        self.config = config
        self.build_ui(config)
        self.built = True

    def run(self):
        print('Run::pre')
        if self.built is False:
            self.build()
        print('Run')
        self.set_app_icon(self.config)
        sys.exit(self.app.exec_())

    def set_app_icon(self, config):
        name = 'teapot'
        # image_path = resolve_in(config, 'images')
        # player_root = resolve_in(config, 'root')
        # icon_path = os.path.join(player_root, image_path, name)
        # app_icon.addFile(icon_path, QSize(16,16))
        # app_icon.addFile(icon_path, QSize(24,24))
        # app_icon.addFile(icon_path, QSize(32,32))
        # app_icon.addFile(icon_path, QSize(48,48))
        # app_icon.addFile(icon_path, QSize(256,256))
        # png_asset = asset.png_asset(icon_path, size=256)

        # png_asset = asset.resolve_png_asset(config, name=name, size=256)
        # app = self.app
        # app_icon = QtGui.QIcon()
        # app_icon.addPixmap(png_asset)

        app_icon = asset.resolve_as_icon(config, name='teapot', size=256)
        self.app.setWindowIcon(app_icon)
        print('set_app_icon')
        return app_icon


    def build_ui(self, settings=None):
        print('Build UI')
        self.players = ( MediaPlayer(settings=settings, app=self.app), )
        # An application can host more than one video panel


