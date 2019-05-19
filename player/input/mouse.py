from PyQt5.QtWidgets import QWidget

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


