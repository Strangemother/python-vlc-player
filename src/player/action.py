
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
        self.actions = Actions(self)

    def keyReleaseEvent(self, e):
        self.actions.event_up(e.key(), event=e)

    def keyPressEvent(self, e):
        self.actions.event_down(e.key(), event=e)


import os

keymap = None

class Actions(object):
    '''Covert simple events to complex string monitoring.

    CTRL+ALT+N
    CTRL+N
    UP>DOWN>LEFT>RIGHT
    "window"
    SHIFT * 5
    '''

    def __init__(self, owner=None):
        self.down = []
        self.space = {}
        self.owner=owner
        if keymap is None:
            self.load_map()
            self.tape = KeyTape(keymap, self.space, host=self.owner or self).load_keytape()

    def load_map(self):
        global keymap

        keys = {}
        fp = './assets/config/key-map.cfg'
        afp = os.path.abspath(os.path.join( os.path.dirname(__file__), fp))
        with open(afp, 'r') as stream:
            for line in stream:
                els = tuple(str.strip(x) for x in line.split('|'))
                if len(els) != 2:
                    print('BAD', els)

                code, name = els
                name = name.lower()
                # print(els )
                keys[name] = code
        keymap = dict(keys)

    def event_up(self, num, event=None):
        try:
            self.down.remove(num)
        except ValueError:
            # not in list
            pass
        # print( "Down Key", event.text(), event.key())
        self.tape.react('up', self.down)

    def event_down(self, num, event=None):
        self.down.append(num)
        self.tape.react('down', self.down)


class Key(object):
    def __new__(cls, char, tape=None):
        if isinstance(char, _Key):
            return char
        return _Key(char, tape=tape)


class _Key(object):

    strict = True

    def __init__(self, char, tape=None):

        self._or = []
        self._add = []
        self.tape = tape
        self.line = tape.line if tape else None
        self.group_id = tape.uuid if tape else -1
        self.char = char.lower()
        self.id = id(self)

    def __unicode__(self):
        return u'{}'.format(self.char)

    def __repr__(self):
        return "<Key {} (+{}) (|{})>".format(
            self.id,
            '+'.join((self.char, ) + tuple(x.char for x in self._add)),
            len(self._or)
            )

    def __or__(self, other):
        """Given a char or key, append an 'OR' strategy to the key map
        """
        item = Key(other, self.tape)
        self._or.append(item)
        pkm = self.tape is not None
        if pkm:
            print('Keeping self in tape', self)
            self.tape.gl_keep(self)

        return item

    def __add__(self, other):
        print('Push and')
        self._add.append(Key(other, self.tape))
        return self

    def __eq__(self, other):
        if isinstance(other, (str, )):
            return self.char == other.lower()
        if isinstance(other, _Key):
            return self.char == other.char
        return self.char == other


    def match(self, keys, keymap, rkeymap):
        #print(self, 'test', keys)
        count = 0

        if int(keymap.get(self.char)) in keys:
            # print('Detect partial', self.char)
            count += 1

        for x in keys:
            char = rkeymap.get(str(x))
            if char is None:
                print('Unmapped keycheck', x, char)
            if char in self._or:
                pass
                # print('OR match potenial.', char)
            if char in self._add:
                #print('Partial map', char)
                count += 1

        self_len = len(self._add) + 1
        if self_len == count:
            # All the additional mapped buttons are down, including the
            # initial character.

            if self.strict is True:
                if len(keys) == self_len:
                    return True
                else:
                    print("Nearly", self)
                    return False

            return True

        return False

    def lower(self):
        return self


class KeyTape(dict):
    '''Read python string like eval through a given context for keys
    '''
    def __init__(self, keymap, action_space=None, host=None):
        self.host=host
        self.action_space = self.build_space(action_space)
        self.keymap = keymap
        self.rkeymap = {y: x for x, y in keymap.items()}
        self.keys = ()
        a = sorted(list(keymap.keys()))
        b = sorted({keymap[x]:x for x in keymap}.values())
        try:
            assert len(a) == len(b)
        except AssertionError as e:
             print('Dups detected', set(a) - set(b))

    def __getitem__(self, key):
        '''Given a key, convert to a manageablr'''
        k = key.lower()
        if self.keymap.get(k, None) is not None:
            return Key(k, self)
        raise KeyError('Key does not exist {}'.format(k))
        return None

    def gl_keep(self, key):
        print('keep', key)
        self.keys += ( (key, None, ), )
        print('keep', len(self.keys))

    def build_space(self, space=None):
        space = space or {}
        space['close'] = self.close
        return space

    def close(self):
        self.host.close()
        sys.exit(0)


    def load_keytape(self):
        fp = './assets/config/keys.cfg'
        afp = os.path.abspath(os.path.join( os.path.dirname(__file__), fp))

        km = KeyTape(self.keymap)
        stack = None
        key = None
        keys = ()

        with open(afp, 'r') as stream:
            count = 0
            for line in stream:
                if line[0] == '$':
                    line = line[1:]
                    km.line = line
                    km.uuid = len(keys)
                    key = eval(line, km)
                    print('KEYS', self.keys, km.keys)
                    stack = []
                elif line[0] == ' ':
                    if key is None:
                        print('Out of order', line)
                    stack.append((count, line))
                else:
                    if (key is not None) and (stack is not None):
                        keys += ( (key, stack,),)
                count += 1

        if (key is not None) and (stack is not None):
            keys += ( (key.lower(), stack,),)

        res = self.keys + keys + km.keys
        self.keys = res
        return self

    def react(self, direction, keys):
        for keyt in self.keys:
            key, func_strs = keyt
            if key.match(keys, self.keymap, self.rkeymap):
                key, stack = self.keys[key.group_id]
                print('line "{}":'.format(key.line.strip()))
                for lineno, statement in stack:
                    print('Running', statement)
                    res = eval(statement, self.action_space)
                    if callable(res):
                        print('Calling', res)
                        res()
                print('\n')



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


