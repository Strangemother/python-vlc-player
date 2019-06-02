from PyQt5.QtWidgets import QWidget
from bus import get_bus
from PyQt5.QtCore import Qt, QSettings, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMenu, QAction



class MouseActionQWidget(QWidget):
    """Attach mouse click, doubleclick and dragging motion.
    combined to ensure dragging and clicking are relatively related.
    """

    draggable = True

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.dragging = False
        self._mouse_down = None
        self.setMouseTracking(True)

    def mouseDoubleClickEvent(self, event):
        self.last = "double click"
        print('Double click')
        self.mouse_double_press(event)
        return super(MouseActionQWidget, self).mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event):

        if self.draggable is True:
            self.dragging = True

            x = event.globalX()
            y = event.globalY()

            if self._mouse_down is not None:
                x_w = self._mouse_down.x()
                y_w = self._mouse_down.y()

                self.move(x-x_w, y-y_w)

        self.mouse_move(event)
        return super(MouseActionQWidget, self).mouseMoveEvent(event)

    def mousePressEvent(self, event):
        # print('mouse down')
        self.mouse_down(event)
        self._mouse_down = event.pos()
        return super(MouseActionQWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # print('mouse up')
        self._mouse_down = None
        self.dragging = False
        self.mouse_up(event)
        return super(MouseActionQWidget, self).mouseReleaseEvent(event)

    def enterEvent(self, event):
        # print( "Mouse Entered")
        self.mouse_enter(event)
        return super(MouseActionQWidget, self).enterEvent(event)

    def leaveEvent(self, event):
        # print( "Mouse Left")
        self.mouse_leave(event)
        return super(MouseActionQWidget, self).enterEvent(event)

    def wheelEvent(self, event):
        print('wheel', event)
        self.mouse_wheel(event)
        return super(MouseActionQWidget, self).wheelEvent(event)

    def mouse_double_press(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_move(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_down(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_up(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_enter(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_leave(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass

    def mouse_wheel(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        pass


class MouseActionQWidgetBus(MouseActionQWidget):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.bus = get_bus()

    def mouse_double_press(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        self.bus.mouse('mouse_double_press', event)

    def mouse_move(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        self.bus.mouse('mouse_move', event)

    def mouse_down(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        self.bus.mouse('mouse_down', event)

    def mouse_up(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        self.bus.mouse('mouse_up', event)

    def mouse_enter(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        self.bus.mouse('mouse_enter', event)

    def mouse_leave(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        self.bus.mouse('mouse_leave', event)

    def mouse_wheel(self, event):
        '''Action override for the event without altering _builtin_ functionality'''
        self.bus.mouse('mouse_wheel', event)


class ContextMenuMixin(object):
    """Apply a 'right-click' context ment to the interface. Upon 'context'
    the 'pop_menu' will display the loaded QMenu
    """
    pop_menu = None

    def on_context_menu(self, point):
        # show context menu
        print('context', point)
        self.bus.contextmenu_point(id(self), point)
        if self.pop_menu is None:
            print('No right click menu.')
            return False
        self.pop_menu.exec_(self.mapToGlobal(point))

    def create_mouse_menu(self):
        # set button context menu policy
        print('Make context menu')
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
        res = self.bus.contextmenu_create(id(self))
        if res is None:
            self.pop_menu = self.default_contextmenu()

    def default_contextmenu(self):
        pop_menu = QMenu(self)
        # toggle_play = QAction('&Play | &Pause', self)
        # pop_menu.addAction(toggle_play)
        # toggle_play.triggered.connect(self.toggle_play_triggered)
        # pop_menu.addAction(QAction('test1', self))
        # pop_menu.addSeparator()
        quit_app = QAction('&Quit', self)
        quit_app.triggered.connect(self.quit_app_triggered)
        pop_menu.addAction(quit_app)
        pop_menu.setStyleSheet("color: white")
        self.bus.contextmenu('contextmenu_created', id(self), pop_menu)
        return pop_menu

    def toggle_play_triggered(self, event):
        print('toggle play pause')

    def quit_app_triggered(self, event):
        print('exit')

