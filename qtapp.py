import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import (
        QApplication, QWidget, QFrame, QHBoxLayout,
        QVBoxLayout, QLabel, QTextEdit, QMainWindow,
        QPushButton, QMenu, QAction, QLabel

    )


import simple
from api import *


from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap
from PyQt5.QtCore import Qt, QTimer

class Controls(QMainWindow):

    def __init__(self, view):
        super().__init__()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)
        self.text='Mouse'
        self.attached_view = view
        self.manual_offset = self.pos()
        self.offset = None
        self.label = QLabel(self.text, self)
        self.label.setStyleSheet("background-color: rgba(10,10,10, 0); color: white")

        pic = QLabel('apples', self)
        fp = os.path.abspath('doors.png')
        print(os.path.exists(fp), fp)
        icon = QPixmap(fp)
        #icon.setStyleSheet("text-color: red")
        scaled_icon = icon.scaled(30, 30, Qt.KeepAspectRatio)
        #scaled_icon.drawPixmap(pix.rect(), mask, mask.rect())
        pic.setPixmap(scaled_icon)
        pic.resize(30, 30)
        #pic.show() # You were missing this.
        self.pic = pic

        self.initUI()

    def mousePressEvent(self, e):
        print('Mouse click')
        self.offset = e.pos()
        self.manual_offset = self.offset

    def mouseMoveEvent(self, event):
        x=event.globalX()
        y=event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.manual_offset = self.offset
        self.move(x-x_w, y-y_w)

    def initUI(self):

        self.text = "Init UI Text"

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Control Panel')

        self.show()


    # def paintEvent(self, event):

    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawText(event, qp)
    #     qp.end()


    # def drawText(self, event, qp):

    #     qp.setPen(QColor(168, 34, 3))
    #     qp.setFont(QFont('Decorative', 10))
    #     qp.drawText(event.rect(), Qt.AlignCenter, self.text)


s=simple.Service()
p=s.get_player('D:/movies/Rising Damp/104  Night Out.divx')
p.video_set_key_input(0)
p.video_set_mouse_input(0)
s.info()


class Lay(QWidget):
    def __init__(self, parent=None):
        super(Lay, self).__init__(parent)
        # self = MainWindow()
        self.setWindowFlags(Qt.FramelessWindowHint, Qt.WindowStaysOnTopHint)
        self.move(0, 0)
        # self.show()
        self.setStyleSheet("background-color: red")
        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)
        self.setPalette(palette)
        self.show()

    # def paintEvent(self, event):
    #     painter = QtGui.QPainter()
    #     painter.begin(self)
    #     painter.setRenderHint(QtGui.QPainter.Antialiasing)
    #     painter.fillRect(event.rect(), QtGui.QBrush(QColor(255, 255, 255, 127)))
    #     painter.drawLine(self.width()/8, self.height()/8, 7*self.width()/8, 7*self.height()/8)
    #     painter.drawLine(self.width()/8, 7*self.height()/8, 7*self.width()/8, self.height()/8)
    #     painter.setPen(QtGui.QPen(Qt.NoPen))


class View(QWidget):

    init_size = (500,400, )

    def __init__(self, app):
        super().__init__()

        self.app = app
        self.offset = None
        self.text='Mouse'

        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        # self.setWindowFlags(Qt.WindowCloseButtonHint)
        # self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint)
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.WheelFocus)
        self.frame = VideoFrame(self)
        # self.label = QLabel('TEXT', Co)
        # self.label.setAttribute(Qt.WA_TranslucentBackground)
        # self.label.setStyleSheet("background-color: rgba(10,10,10, 0); color: white")
        self.controls = Controls(self)
        self.frame.resize(*self.init_size)
        self.initUI()

    def initUI(self):
        # self.move(300, 300)
        self.setWindowTitle('View')
        self.setGeometry(0,0, 200, 200)

        # self.setLayout(hbox)
        self.resize(*self.init_size)

        self.palette = self.frame.palette()
        self.palette.setColor(QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.frame.setPalette(self.palette)
        self.frame.setAutoFillBackground(True)

        attach = p.event_manager().event_attach
        EVENTS = ['MediaPlayerTimeChanged', 'MediaPlayerPositionChanged']

        for name in EVENTS:
            Event = getattr(EventType, name)
            attach(Event, self.event_handler, name, p)

        # self.editor = QTextEdit()
        # self.editor.setPlainText("OVERLAY"*100)
        # self.editor.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        # self.editor.setText("OVERLAY TEXT")
        #self.editor.show()

        self.setStyleSheet("background-color: #3f4d82; margin: 0; padding: 0; border-width:0")
        # self.overlay = Lay(self)
        # self.overlay.resize(200,300)

        #
        #self.overlay.setGeometry(0,0, 100, 100)
        layout = QVBoxLayout()
        layout.setContentsMargins(2,2,2,2)
        layout.addWidget(self.frame)
        #layout.addWidget(self.overlay)
        layout.setStretch(0, 3)
        #layout.addWidget(self.editor)

        self.ov = QWidget()
        #self.ov.button = QPushButton('Test', self.ov)
        self.ov.setMouseTracking(True)
        self.ov.mouseMoveEvent = self.check_cursor_state

        layout.addWidget(self.ov)
        layout.setStretch(1, 4)

        p.set_hwnd(self.frame.winId())

        self.ov.setGeometry(0, 0, 10, 10)
        self.ov.setStyleSheet("background-color: green")
        self.ov.setMaximumHeight(20)

        cw = self.controls.label.fontMetrics().width(self.controls.label.text())

        self.controls.label.setText(p.get_media().get_mrl())
        self.setLayout(layout)
        self.show()
        self.controls.label.adjustSize()


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
        self.pop_menu.addAction(QAction('&Play | &Pause', self))
        self.pop_menu.addAction(QAction('test1', self))
        self.pop_menu.addSeparator()
        self.pop_menu.addAction(QAction('&Quit', self))
        self.pop_menu.setStyleSheet("color: white")

        p.play()

    def on_context_menu(self, point):
        # show context menu
        self.pop_menu.exec_(self.mapToGlobal(point))

    def check_cursor_state(self, pos):
        # vx, vy = self.parent.init_size
        # pixel padding
        p = 13

        lx = pos.x()
        vx = self.width()
        ly = pos.y()
        vy = self.height()

        if self.controls.offset is None:
            new_pos = self.controls.manual_offset
            self.controls.move(new_pos + self.pos())

        at_bottom = (vy + p) > ly > (vy-p)
        at_top = ly < p
        at_right = (vx + p) > lx > (vx-p)
        at_left = lx < p

        cur = Qt.ArrowCursor
        if at_top or at_bottom:
            cur = Qt.SizeVerCursor

        if at_left or at_right:
            cur = Qt.SizeHorCursor

        if at_top or at_bottom:
            if at_left:
                cur = Qt.SizeFDiagCursor if at_top else Qt.SizeBDiagCursor

            if at_right:
                cur = Qt.SizeFDiagCursor if at_bottom else Qt.SizeBDiagCursor

        if cur is False:
            QApplication.restoreOverrideCursor()
        else:
            QApplication.setOverrideCursor(cur)
        # do lengthy process

        #print('bottom edge', at_bottom)
        #print('top edge', at_top)
        #print('right edge', lx )
        #print('left', lx )

    def event_handler(self, event, name, player):
        pass

    def enterEvent(self, event):
        print( "Mouse Entered")
        self.controls.show()
        return super(View, self).enterEvent(event)

    def leaveEvent(self, event):
        print( "Mouse Left")
        self.controls.hide()
        return super(View, self).enterEvent(event)

    def mousePressEvent(self, e):
        print('Mouse click')
        self.offset = e.pos()

    def mouseReleaseEvent(self, e):
        print('Mouse release')
        self.offset = None

    def mouseMoveEvent(self, e):
        x=e.globalX()
        y=e.globalY()

        if self.offset is not None:
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.move(x-x_w, y-y_w)

        self.check_cursor_state(e.localPos())


    def keyPressEvent(self, e):
        print( "Key", e.key())

        # q, esc
        if e.key() in [81, 16777216]:
            self.controls.close()
            self.close()
            sys.exit(0)


    # def paintEvent(self, event):

    #     qp = QPainter()
    #     qp.begin(self)
    #     self.drawText(event, qp)
    #     self.drawRectangles(qp)
    #     qp.end()


    # def drawText(self, event, qp):

    #     qp.setPen(QColor(255,0,255))
    #     qp.setFont(QFont('Decorative', 20))
    #     qp.drawText(event.rect(), Qt.AlignCenter, self.text)


    # def drawRectangles(self, qp):

    #     col = QColor(0, 0, 0)
    #     col.setNamedColor('#d4d4d4')
    #     qp.setPen(col)

    #     qp.setBrush(QColor(200, 0, 0))
    #     qp.drawRect(10, 15, 90, 60)

    #     qp.setBrush(QColor(255, 80, 0, 160))
    #     qp.drawRect(130, 15, 90, 60)

    #     qp.setBrush(QColor(25, 0, 90, 200))
    #     qp.drawRect(250, 15, 90, 60)

def close_app(app, cont):

    return


def main():
    app = QApplication(sys.argv)
    w = View(app)
    sys.exit(app.exec_())


class VideoFrame(QFrame):

    double_click_timeout = 200

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.offset = None
        self.moved = False
        self.last_xy = None
        self.is_mousedown = False

        self.setMouseTracking(True)
        self.initUI()

    def initUI(self):
        # self.move(300, 300)
        self.show()

    def enterEvent(self, event):
        print( "VF Entered")
        return super(VideoFrame, self).enterEvent(event)

    def leaveEvent(self, event):
        print( "VF Left")
        return super(VideoFrame, self).leaveEvent(event)

    def mousePressEvent(self, e):
        if self.moved is False:
            print('VF press')

        self.last = "click"
        self.is_mousedown = True
        self.mouse_press_late_done = False

        QTimer.singleShot(self.double_click_timeout * 2,
                                self.mouse_press_late)
        self.offset = e.pos()

    def mouse_press_late(self):
        if self.is_mousedown:
            self.mouse_press_late_done = True
            if self.moved is True:
                print('dragging')
            else:
                print('Hold')

    def mouseMoveEvent(self, e):
        x = e.globalX()
        y = e.globalY()


        if self.offset is not None:
            x_w = self.offset.x()
            y_w = self.offset.y()
            self.parent.move(x-x_w, y-y_w)
            new_xy = "{}{}".format(x,y)
            if self.last_xy != new_xy:
                self.moved = True
            self.last_xy = new_xy

        self.parent.check_cursor_state(e.localPos())

    def mouseReleaseEvent(self, e):
        # print('Mouse release')
        if self.mouse_press_late_done is True:
            self.mouse_press_late_done = False
            print('release hold')
        elif self.moved is False:
            print('Detected click')

        if self.offset is not None:
            if self.moved is True:
                print('Finished drag')
            self.moved = False
            self.offset = None


        self.is_mousedown = False

        if self.last == "click":
            QTimer.singleShot(self.double_click_timeout,
                                self.mouse_click)
        else:
            # Perform double click action.
            # self.mouse_doubleclick(e)
            self.update()

    def mouseDoubleClickEvent(self, event):
        self.last = "double click"
        print('VF Double click')

    def mouse_click(self):

        if self.last == "click":
            self.update()


if __name__ == '__main__':
    main()

