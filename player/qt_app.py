"""Main interface for a QT app.

1. Main video screen
2. Overlay for screen extras
"""
import sys
import os
import json
from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
        QApplication, QWidget, QFrame, QHBoxLayout,
        QVBoxLayout, QLabel, QTextEdit, QMainWindow,
        QPushButton, QMenu, QAction, QLabel

    )

from player import MediaPlayer
from flags import FlagsMixin
from keyboard import thread_listen as external_listener

# Base settings to override
SETTINGS = dict(
    # set the main window OS frame - set True to remove the OS frame
    frameless=False,
    json_file='config.json',
    init_size=[500, 400],
    player_title='My Fancy Player',
)


class App(object):
    '''A Non-Qt abstraction of all the components running the player
    '''

    def run(self, settings=None):
        self.app = QApplication(sys.argv)
        config = self.load_settings(settings)
        self.build_ui(config)

    def load_settings(self, settings=None):
        config = SETTINGS.copy()

        fp = os.path.join(os.path.dirname(__file__), config['json_file'])
        file_conf = {}
        if os.path.isfile(fp):
            with open(fp, 'r') as stream:
                file_conf = json.load(stream)
            config.update(file_conf)

        if settings is not None:
            config.update(settings)

        return config

    def build_ui(self, settings=None):
        self.players = (MediaPlayer(settings=settings), )
        sys.exit(self.app.exec_())
        # An application can host more than one video panel


class Overlay(QMainWindow, FlagsMixin):
    '''An overlay is a standard (or standalone) window positon over
    the VideoFrame for presenting player information. Using a seperate layer
    bypasses issues with an external hooked hwnd frame, allowing fully
    transparent text and graphics with the OS handling antialiasing

    + transparent
    + always on top
    + no OS buttons
    '''
    flags = Qt.FramelessWindowHint | Qt.Tool | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint

    def __init__(self):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowFlags(self.flags)
        self.set_flags()
        self.setMouseTracking(True)
        self.setWindowTitle('Video Player Overlay')

        self.text = 'Overlay'
        self.label = QLabel(self.text, self)
        self.label.setStyleSheet("background-color: rgba(10,10,10, 0); color: white")

        self.show()

