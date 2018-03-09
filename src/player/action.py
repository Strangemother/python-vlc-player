
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizeGrip
from PyQt5.QtCore import Qt, QSettings
from PyQt5 import QtGui

import sys
from player.media import VideoFrame, DragMixin
from player.flags import FlagsMixin, FRAMELESS
from player import simple


UNDEFINED = 'undefined'

class ConfigMixin(FlagsMixin):

    frameless = None

    def config_set_frame(self, settings=None, value=None):
        # no windows buttons or edge
        settings = settings or self.settings
        on = settings.get('frameless', value or self.frameless)
        if value is not None:
            on = value
        print('turn', on)
        flag = Qt.FramelessWindowHint

        if on is True:
            self.add_flag(flag)
            return True
            #self.setWindowFlags(Qt.FramelessWindowHint)

        self.remove_flag(flag)
        return False

    def config_set_title(self, settings=None):
        settings = settings or self.settings
        title = settings.get('player_title', 'Video Player')
        self.setWindowTitle(title)

    def config_set_size(self, settings=None):
        settings = settings or self.settings
        size = settings.get('init_size', (500, 400,))
        self.resize(*size)

    def config_set_bezel(self, settings=None):
        settings = settings or self.settings
        size = settings.get('bezel', 5)
        opts = size

        if isinstance(size, (int)):
            size = [size]

        if isinstance(size, (list, tuple,)):
            if len(size) == 1:
                opts = size * 4
            if len(size) == 2:
                tb, lr = opts
                opts = tb, lr, tb, lr
            if len(size) == 3:
                tb, l, r = size
                opts = tb, l, tb, r

        self.layout.setContentsMargins(*opts)


class KeyAction(object):

    def hook_keys(self, filepath=None):
        '''Start the action monitoring for the keyboard.'''
        self.actions = Actions()

    def keyReleaseEvent(self, e):
        self.actions.event_up(e.key(), event=e)

    def keyPressEvent(self, e):

        self.actions.event_down(e.key(), event=e)
        # q, esc
        if e.key() in [81, 16777216]:
            # self.controls.close()
            self.close()
            sys.exit(0)


class Actions(object):
    '''Covert simple events to complex string monitoring.'''

    def event_up(self, num, event=None):
        self.down.remove(num)
        print( "Down Key", event.text(), event.key())


    def event_down(self, num, event=None):
        self.down.append(num)


class Action(object):
    """An extendable unit to build an action reacting to an event
    Add a perform() method accepting the media player.

    If the action has never loaded, the user should accept the new action. """

    def perform(self, media_player):
        pass


class CloseAction(Action):

    def perform(self, media_player):
        media_player.close()
        sys.exit(0)



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
        print('mouse down')
        self.mouse_down(event)
        self._mouse_down = event.pos()
        return super(MouseActionQWidget, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        print('mouse up')
        self._mouse_down = None
        self.dragging = False
        self.mouse_up(event)
        return super(MouseActionQWidget, self).mouseReleaseEvent(event)

    def enterEvent(self, event):
        print( "Mouse Entered")
        self.mouse_enter(event)
        return super(MouseActionQWidget, self).enterEvent(event)

    def leaveEvent(self, event):
        print( "Mouse Left")
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


