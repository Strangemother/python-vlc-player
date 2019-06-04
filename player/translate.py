"""Convert the events sent trough the pipe to and from a transport
"""

register = {}
cache = {}

class Enum:
    """  Not an event"""
    _0 = "None"
    """A new action has been added (QActionEvent)."""
    _114 = "action_added"
    """An action has been changed (QActionEvent)."""
    _113 = "action_changed"
    """An action has been removed (QActionEvent)."""
    _115 = "action_removed"
    """ A widget's top-level window activation state has changed."""
    _99 = "activation_change"
    """This enum has been deprecated. Use ApplicationStateChange instead."""
    _121 = "application_activate"
    """This enum has been deprecated. Use ApplicationStateChange instead."""
    _ApplicationActivate = "application_activated"
    """This enum has been deprecated. Use ApplicationStateChange instead."""
    _122 = "application_deactivate"
    """ The default application font has changed."""
    _36 = "application_font_change"
    """ The default application layout direction has changed."""
    _37 = "application_layout_direction_change"
    """ The default application palette has changed."""
    _38 = "application_palette_change"
    """The state of the application has changed."""
    _214 = "application_state_change"
    """ The application's icon has changed."""
    _35 = "application_window_icon_change"
    """ An object gets a child (QChildEvent)."""
    _68 = "child_added"
    """ A widget child gets polished (QChildEvent)."""
    _69 = "child_polished"
    """ An object loses a child (QChildEvent)."""
    _71 = "child_removed"
    """ The clipboard contents have changed."""
    _40 = "clipboard"
    """ Widget was closed (QCloseEvent)."""
    _19 = "close"
    """A widget wants to close the software input panel (SIP)."""
    _200 = "close_software_input_panel"
    """The margins of the widget's content rect changed."""
    _178 = "contents_rect_change"
    """ Context popup menu (QContextMenuEvent)."""
    _82 = "context_menu"
    """The widget's cursor has changed."""
    _183 = "cursor_change"
    """ The object will be deleted after it has cleaned up (QDeferredDeleteEvent)"""
    _52 = "deferred_delete"
    """ The cursor enters a widget during a drag and drop operation (QDragEnterEvent)."""
    _60 = "drag_enter"
    """ The cursor leaves a widget during a drag and drop operation (QDragLeaveEvent)."""
    _62 = "drag_leave"
    """ A drag and drop operation is in progress (QDragMoveEvent)."""
    _61 = "drag_move"
    """ A drag and drop operation is completed (QDropEvent)."""
    _63 = "drop"
    """A dynamic property was added, changed, or removed from the object."""
    _170 = "dynamic_property_change"
    """ Widget's enabled state has changed."""
    _98 = "enabled_change"
    """ Mouse enters widget's boundaries (QEnterEvent)."""
    _10 = "enter"
    """An editor widget gains focus for editing. QT_KEYPAD_NAVIGATION must be defined."""
    _150 = "enter_edit_focus"
    """Send to toplevel widgets when the application enters "What's This?" mode."""
    _124 = "enter_whats_this_mode"
    """Sent to a window when its on-screen contents are invalidated and need to be flushed from the backing store."""
    _206 = "expose"
    """File open request (QFileOpenEvent)."""
    _116 = "file_open"
    """  Widget or Window gains keyboard focus (QFocusEvent)."""
    _8 = "focus_in"
    """  Widget or Window loses keyboard focus (QFocusEvent)."""
    _9 = "focus_out"
    """ Widget or Window focus is about to change (QFocusEvent)"""
    _23 = "focus_about_to_change"
    """ Widget's font has changed."""
    _97 = "font_change"
    """A gesture was triggered (QGestureEvent)."""
    _198 = "gesture"
    """A gesture override was triggered (QGestureEvent)."""
    _202 = "gesture_override"
    """Item gains keyboard grab (QGraphicsItem only)."""
    _188 = "grab_keyboard"
    """Item gains mouse grab (QGraphicsItem only)."""
    _186 = "grab_mouse"
    """Context popup menu over a graphics scene (QGraphicsSceneContextMenuEvent)."""
    _159 = "graphics_scene_context_menu"
    """The cursor enters a graphics scene during a drag and drop operation (QGraphicsSceneDragDropEvent)."""
    _164 = "graphics_scene_drag_enter"
    """The cursor leaves a graphics scene during a drag and drop operation (QGraphicsSceneDragDropEvent)."""
    _166 = "graphics_scene_drag_leave"
    """A drag and drop operation is in progress over a scene (QGraphicsSceneDragDropEvent)."""
    _165 = "graphics_scene_drag_move"
    """A drag and drop operation is completed over a scene (QGraphicsSceneDragDropEvent)."""
    _167 = "graphics_scene_drop"
    """The user requests help for a graphics scene (QHelpEvent)."""
    _163 = "graphics_scene_help"
    """The mouse cursor enters a hover item in a graphics scene (QGraphicsSceneHoverEvent)."""
    _160 = "graphics_scene_hover_enter"
    """The mouse cursor leaves a hover item in a graphics scene (QGraphicsSceneHoverEvent)."""
    _162 = "graphics_scene_hover_leave"
    """The mouse cursor moves inside a hover item in a graphics scene (QGraphicsSceneHoverEvent)."""
    _161 = "graphics_scene_hover_move"
    """Mouse press again (double click) in a graphics scene (QGraphicsSceneMouseEvent)."""
    _158 = "graphics_scene_mouse_double_click"
    """Move mouse in a graphics scene (QGraphicsSceneMouseEvent)."""
    _155 = "graphics_scene_mouse_move"
    """Mouse press in a graphics scene (QGraphicsSceneMouseEvent)."""
    _156 = "graphics_scene_mouse_press"
    """Mouse release in a graphics scene (QGraphicsSceneMouseEvent)."""
    _157 = "graphics_scene_mouse_release"
    """Widget was moved (QGraphicsSceneMoveEvent)."""
    _182 = "graphics_scene_move"
    """Widget was resized (QGraphicsSceneResizeEvent)."""
    _181 = "graphics_scene_resize"
    """Mouse wheel rolled in a graphics scene (QGraphicsSceneWheelEvent)."""
    _168 = "graphics_scene_wheel"
    """ Widget was hidden (QHideEvent)."""
    _18 = "hide"
    """ A child widget has been hidden."""
    _27 = "hide_to_parent"
    """The mouse cursor enters a hover widget (QHoverEvent)."""
    _127 = "hover_enter"
    """The mouse cursor leaves a hover widget (QHoverEvent)."""
    _128 = "hover_leave"
    """The mouse cursor moves inside a hover widget (QHoverEvent)."""
    _129 = "hover_move"
    """ The main icon of a window has been dragged away (QIconDragEvent)."""
    _96 = "icon_drag"
    """Widget's icon text has been changed. (Deprecated)"""
    _101 = "icon_text_change"
    """ An input method is being used (QInputMethodEvent)."""
    _83 = "input_method"
    """A input method query event (QInputMethodQueryEvent)"""
    _207 = "input_method_query"
    """The keyboard layout has changed."""
    _169 = "keyboard_layout_change"
    """  Key press (QKeyEvent)."""
    _6 = "key_press"
    """  Key release (QKeyEvent)."""
    _7 = "key_release"
    """ The application translation changed."""
    _89 = "language_change"
    """ The direction of layouts changed."""
    _90 = "layout_direction_change"
    """ Widget layout needs to be redone."""
    _76 = "layout_request"
    """ Mouse leaves widget's boundaries."""
    _11 = "leave"
    """An editor widget loses focus for editing. QT_KEYPAD_NAVIGATION must be defined."""
    _151 = "leave_edit_focus"
    """Send to toplevel widgets when the application leaves "What's This?" mode."""
    _125 = "leave_whats_this_mode"
    """ The system locale has changed."""
    _88 = "locale_change"
    """A mouse double click occurred outside the client area (QMouseEvent)."""
    _176 = "non_client_area_mouse_button_dbl_click"
    """A mouse button press occurred outside the client area (QMouseEvent)."""
    _174 = "non_client_area_mouse_button_press"
    """A mouse button release occurred outside the client area (QMouseEvent)."""
    _175 = "non_client_area_mouse_button_release"
    """A mouse move occurred outside the client area (QMouseEvent)."""
    _173 = "non_client_area_mouse_move"
    """The user changed his widget sizes (macOS only)."""
    _177 = "mac_size_change"
    """ An asynchronous method invocation via QMetaObject::invokeMethod()."""
    _43 = "meta_call"
    """Widgets modification state has been changed."""
    _102 = "modified_change"
    """  Mouse press again (QMouseEvent)."""
    _4 = "mouse_button_dbl_click"
    """  Mouse press (QMouseEvent)."""
    _2 = "mouse_button_press"
    """  Mouse release (QMouseEvent)."""
    _3 = "mouse_button_release"
    """  Mouse move (QMouseEvent)."""
    _5 = "mouse_move"
    """The mouse tracking state has changed."""
    _109 = "mouse_tracking_change"
    """ Widget's position changed (QMoveEvent)."""
    _13 = "move"
    """The system has detected a gesture (QNativeGestureEvent)."""
    _197 = "native_gesture"
    """The screens orientation has changes (QScreenOrientationChangeEvent)."""
    _208 = "orientation_change"
    """ Screen update necessary (QPaintEvent)."""
    _12 = "paint"
    """ Palette of the widget changed."""
    _39 = "palette_change"
    """The widget parent is about to change."""
    _131 = "parent_about_to_change"
    """ The widget parent has changed."""
    _21 = "parent_change"
    """A platform specific panel has been requested."""
    _212 = "platform_panel"
    """A native platform surface has been created or is about to be destroyed (QPlatformSurfaceEvent)."""
    _217 = "platform_surface"
    """ The widget is polished."""
    _75 = "polish"
    """ The widget should be polished."""
    _74 = "polish_request"
    """The widget should accept the event if it has "What's This?" help (QHelpEvent)."""
    _123 = "query_whats_this"
    """Widget's read-only state has changed (since Qt 5.4)."""
    _106 = "read_only_change"
    """A widget wants to open a software input panel (SIP)."""
    _199 = "request_software_input_panel"
    """ Widget's size changed (QResizeEvent)."""
    _14 = "resize"
    """The object needs to fill in its geometry information (QScrollPrepareEvent)."""
    _204 = "scroll_prepare"
    """The object needs to scroll to the supplied position (QScrollEvent)."""
    _205 = "scroll"
    """Key press in child for shortcut key handling (QShortcutEvent)."""
    _117 = "shortcut"
    """ Key press in child, for overriding shortcut key handling (QKeyEvent). When a shortcut is about to trigger, ShortcutOverride is sent to the active window. This allows clients (e.g. widgets) to signal that they will handle the shortcut themselves, by accepting the event. If the shortcut override is accepted, the event is delivered as a normal key press to the focus widget. Otherwise, it triggers the shortcut action, if one exists."""
    _51 = "shortcut_override"
    """ Widget was shown on screen (QShowEvent)."""
    _17 = "show"
    """ A child widget has been shown."""
    _26 = "show_to_parent"
    """ Socket activated, used to implement QSocketNotifier."""
    _50 = "sock_act"
    """A signal delivered to a state machine (QStateMachine::SignalEvent)."""
    _192 = "state_machine_signal"
    """The event is a wrapper for, i.e., contains, another event (QStateMachine::WrappedEvent)."""
    _193 = "state_machine_wrapped"
    """A status tip is requested (QStatusTipEvent)."""
    _112 = "status_tip"
    """Widget's style has been changed."""
    _100 = "style_change"
    """ Wacom tablet move (QTabletEvent)."""
    _87 = "tablet_move"
    """ Wacom tablet press (QTabletEvent)."""
    _92 = "tablet_press"
    """ Wacom tablet release (QTabletEvent)."""
    _93 = "tablet_release"
    """Wacom tablet enter proximity event (QTabletEvent), sent to QApplication."""
    _171 = "tablet_enter_proximity"
    """Wacom tablet leave proximity event (QTabletEvent), sent to QApplication."""
    _172 = "tablet_leave_proximity"
    """The Wacom tablet tracking state has changed (since Qt 5.9)."""
    _219 = "tablet_tracking_change"
    """ The object is moved to another thread. This is the last event sent to this object in the previous thread. See QObject::moveToThread()."""
    _22 = "thread_change"
    """  Regular timer events (QTimerEvent)."""
    _1 = "timer"
    """The toolbar button is toggled on macOS."""
    _120 = "tool_bar_change"
    """A tooltip was requested (QHelpEvent)."""
    _110 = "tool_tip"
    """The widget's tooltip has changed."""
    _184 = "tool_tip_change"
    """Beginning of a sequence of touch-screen or track-pad events (QTouchEvent)."""
    _194 = "touch_begin"
    """Cancellation of touch-event sequence (QTouchEvent)."""
    _209 = "touch_cancel"
    """End of touch-event sequence (QTouchEvent)."""
    _196 = "touch_end"
    """Touch-screen event (QTouchEvent)."""
    _195 = "touch_update"
    """Item loses keyboard grab (QGraphicsItem only)."""
    _189 = "ungrab_keyboard"
    """Item loses mouse grab (QGraphicsItem, QQuickItem)."""
    _187 = "ungrab_mouse"
    """ The widget should be queued to be repainted at a later time."""
    _78 = "update_later"
    """ The widget should be repainted."""
    _77 = "update_request"
    """The widget should reveal "What's This?" help (QHelpEvent)."""
    _111 = "whats_this"
    """A link in a widget's "What's This?" help was clicked."""
    _118 = "whats_this_clicked"
    """ Mouse wheel rolled (QWheelEvent)."""
    _31 = "wheel"
    """A Windows-specific activation event has occurred."""
    _132 = "win_event_act"
    """ Window was activated."""
    _24 = "window_activate"
    """The window is blocked by a modal dialog."""
    _103 = "window_blocked"
    """ Window was deactivated."""
    _25 = "window_deactivate"
    """ The window's icon has changed."""
    _34 = "window_icon_change"
    """The window's state (minimized, maximized or full-screen) has changed (QWindowStateChangeEvent)."""
    _105 = "window_state_change"
    """ The window title has changed."""
    _33 = "window_title_change"
    """The window is unblocked after a modal dialog exited."""
    _104 = "window_unblocked"
    """The window system identifer for this native widget has changed."""
    _203 = "win_id_change"
    """The widget's z-order has changed. This event is never sent to top level windows."""
    _126 = "z_order_change"

import action
from wlog import color_plog, log as _log
log = color_plog('magenta').announce(__spec__)


def to_string(name, event=None, **kw):
    """
    given an event and an optional name, return the str translated event object
    """

    if event is None and (isinstance(name, str) is False):
        event = name
        # get correct name attr
        name = event.Type

    Class = register.get(name, DefaultTranslate)
    translator = cache.get(Class.__name__, None)

    if translator is None:
        translator = Class()
        cache[Class.__name__] = translator

    kw['name'] = kw.get('name', name)
    return translator.to_transport(event, **kw)


async def from_string(string_event):
    try:
        return await execute(string_event)
    except NameError as e:
        _log('-- translate.from_string error', str(e), color='red')
        log('-- String:', string_event)

async def execute(code):
    # Make an async function with the code and `exec` it
    exec(
        f'async def __ex(): ' +
        ''.join(f'\n {l}' for l in code.split('\n'))
    )

    # Get `__ex` from local variables, call it and return the result
    return await locals()['__ex']()

class Translate(object):
    """Any event transport should extend a translate, for mapping through
    the pipe.
    """
    # The name of the event to capture
    event = 'mouse_something'

    def to_transport(self, event, **kw):
        """Convert the expensive _not_ threadsafe entity to a transportable
        unit.
        Return a string to transport and convert back to a (cheaper) event
        object.
        """
        result = self.clean(event,**kw)
        return str(result)

    def clean(self, event, **kw):
        try:
            num = event.type if event is not None else kw.get('name')
        except AttributeError as e:
            print('Translate.clean unexpected Event structure', event)
            if isinstance(event, dict):
                num = event.get('type', kw.get('name'))
                print('Recovering from thin event:', num)
            else:
                raise e


        if callable(num):
            num = num()
        name = getattr(Enum,  f"_{num}", None)
        res = {'q_type': (num, name), 'Class': self.__class__.__name__}
        res.update(kw)
        return res

    async def from_transport(self, str_event):
        """Convert the given string to an event object
        return an instance of a cheap translate event - an object like entity.

        This will directly translate the result from to_transport
        """
        return await execute(str_event)


class DefaultTranslate(Translate):

    def to_transport(self, event, **kw):
        return str(self.clean(event, **kw))

    def clean(self, event, **kw):
        res = super().clean(event, **kw)
        addon = {}
        res.update(addon)
        return res
