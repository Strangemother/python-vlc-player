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
import asyncio

from quamash import QEventLoop, QThreadExecutor
from bus import async_mananger
from concurrent.futures import CancelledError, ProcessPoolExecutor
import os

import bus


class App(object):
    '''A Non-Qt abstraction of all the components running the player
    '''
    built = False

    def __init__(self, argv=None):
        self.argv = argv

    def build(self, init_settings=None):
        print("\n!! - App::build", os.getpid(), os.getppid())
        self.app = QApp(sys.argv)
        self.app.aboutToQuit.connect(self.kill)

        self.loop = QEventLoop(self.app)
        asyncio.set_event_loop(self.loop)
        self.configure(init_settings)

    def configure(self, init_settings):
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
        self.async_loop()
        #self.wait_exit()

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
        self.players = (MediaPlayer(settings=settings, app=self.app), )
        # An application can host more than one video panel

    def kill(self):
        print('App Kill')
        bus.get_bus().close()
        for player in self.players:
            player.player.stop()

    def async_loop(self):
        error = None
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(async_mananger(self))
            # loop.run_forever()
        except Exception as e:
            print("Except of async_mananger::", e)
            error = e
        finally:
            for task in asyncio.Task.all_tasks():
                task.cancel()
            print('Closing loop')
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

        print('async_loop closed')
        if error:
            sys.exit(1)
        self.wait_exit()

    def wait_exit(self):
        print('wait_exit')
        ev  = self.app.exec_()
        print('Closed. sys.exit', ev)
        #asyncio.run_coroutine_threadsafe(async_mananger(self), loop)
        # if error:
        #     raise error
        sys.exit(ev)

class QApp(QApplication):
    pass
