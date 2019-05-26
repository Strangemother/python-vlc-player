# architecture

+ An `App` maintains many `MediaPlayer` in `app.players`.
+ A `MediaPlayer` maintains
  + 1 DirectDraw (or show) hwnd frame `VideoFrame`
  + Input, Overlay and Context menu (right click) managers

## Bus

All units communiate the `bus` as events. The bus is an asyncio coroutine, managing input and _control_ of the `MediaPlayer` instances in each `App`.

+ Lives independently on its own loop
+ Is not threaded; allowing for a player instance binding
+ Has a pool Process; for other long tasks
+ Can capture events and `emit` cleaned data.

The `emit` sends an event to the Pipe of the waiting Process. At any point the pool process may return information for the bus to execute. The background process will perform management actions; such as pausing the currently playing media on keyboard spacebar. Given all the events are pushed to the bus background process, the system can maintain a small state machine to chain events actions.

All units of the application can connect to the bus such as the `MouseMixin` or `ContextMenu`.


