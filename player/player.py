from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizeGrip
from media import VideoFrame


class MediaPlayer(QWidget):
    '''A application interface hosting a VideoFrame and managing its
    interactivity.'''

    frameless = False

    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings or {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Video Player')

        # no windows buttons or edge
        if self.settings.get('frameless', self.frameless):
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setFocusPolicy(Qt.WheelFocus)
        self.resize(500, 400)
        self.build_view()

    def build_view(self):
        # self.setStyleSheet("background-color: #3f4d82")
        # self.overlays = (Overlay(), )
        frame = VideoFrame(self)

        layout = QVBoxLayout(self)
        self.setLayout(layout)
        layout.addWidget(frame, 9)

        #controls = QWidget()
        controls = ControlPanel()
        #controls.setStyleSheet("background-color: red")
        layout.addWidget(controls, 1)

        sizegrip = QSizeGrip(self)
        layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)

        self._layout = layout
        self.controls = controls
        self.show()


class ControlPanel(QWidget):
    '''Main panel of minimal controls.
    '''

    #def initUI(self):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('View')
        # print('Controls')
        self.setStyleSheet("background-color: #884d32;")
        # self.resize(50, 200)
        self.setMaximumHeight(60)
        self.setMinimumHeight(20)
        self.setMinimumWidth(500)
        self.label = QLabel("controls", self)
        self.label2 = QLabel("other controls", self)
        self.label2.setGeometry(40, 50, 20,20)
        # self.show()

