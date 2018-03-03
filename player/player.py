from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizeGrip
from media import VideoFrame
from flags import FlagsMixin, FRAMELESS


class MediaPlayer(QWidget, FlagsMixin):
    '''A application interface hosting a VideoFrame and managing its
    interactivity.'''

    frameless = False
    flags = FRAMELESS

    def __init__(self, settings=None):
        super().__init__()
        self.settings = settings or {}
        self.initUI()

    def initUI(self):

        self.setFocusPolicy(Qt.WheelFocus)

        self.config_set_title()
        self.config_set_size()
        self.set_flags()

        self.build_view()

    def config_set_frame(self):
        # no windows buttons or edge
        on = self.settings.get('frameless', self.frameless)
        flag = Qt.FramelessWindowHint

        if on:
            self.add_flag(flag)
            return True
            #self.setWindowFlags(Qt.FramelessWindowHint)

        self.remove_flag(flag)
        return False

    def config_set_title(self):
        title = self.settings.get('player_title', 'Video Player')
        self.setWindowTitle(title)

    def config_set_size(self):
        size = self.settings.get('init_size', (500, 400,))
        self.resize(*size)

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
        self.setMinimumWidth(20)
        self.label = QLabel("controls", self)
        self.label2 = QLabel("other controls", self)
        self.label2.setGeometry(0, 50, 20,20)
        # self.show()

