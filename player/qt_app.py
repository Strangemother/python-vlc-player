"""Main interface for a QT app.

1. Main video screen
2. Overlay for screen extras
"""
import sys

from PyQt5 import QtGui
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
        QApplication, QWidget, QFrame, QHBoxLayout,
        QVBoxLayout, QLabel, QTextEdit, QMainWindow,
        QPushButton, QMenu, QAction, QLabel

    )

from player import MediaPlayer

class App(object):
    '''A Non-Qt abstraction of all the components running the player
    '''
    def run(self):
        self.app = QApplication(sys.argv)
        self.build_ui()

    def build_ui(self):
        self.players = (MediaPlayer(), )
        sys.exit(self.app.exec_())
        # An application can host more than one video panel



class Overlay(QMainWindow):
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
        self.setWindowFlags(self.flags)
        self.setMouseTracking(True)
        self.setWindowTitle('Video Player Overlay')

        self.text = 'Overlay'
        self.label = QLabel(self.text, self)
        self.label.setStyleSheet("background-color: rgba(10,10,10, 0); color: white")

        self.show()

