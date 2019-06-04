"""The Bus centralises all communcation across the components and out into the
external pipes.
Useful for plugin management and state work.
"""
import atexit
import asyncio
import os, time
from multiprocessing import Process, Pipe
from concurrent.futures import CancelledError, ProcessPoolExecutor

from player import translate
from plugin import process_start, DEATH_PILL


bus = None


def autoload():
    global bus
    bus = Bus()


def get_bus():
    return bus


from wlog import color_plog, log as _log
log = color_plog('cyan').announce(__spec__)


class Bus(object):
    config = None
    exit = False

    def __init__(self, config=None):

        # In duplex mode False, a pip may only be one direction
        # RECV, SEND.
        client_to_pipe, to_pipe = Pipe(duplex=False)
        from_pipe, client_from_pipe = Pipe(duplex=False)
        conf = config or self.config
        p = Process(target=process_start, args=(conf, client_to_pipe, client_from_pipe))
        # recv_pipe = child_send_pipe
        # send_pipe = child_recv_pipe
        log(f'-- Bus::init start process. Current PID:{os.getpid()}, Parent PID: {os.getppid()}')
        p.start()
        log('-- Bus::init Wait for child "hello"')
        log("-- Bus::init recv:", from_pipe.recv())
        log('-- Bus::init received ^^. Sending response...')
        to_pipe.send('No eggs.')
        log('-- Bus::init sent reponse.')
        # accepted at translate.Translate::from_transport
        to_pipe.send('action.init_all()')
        self.process = p
        self._send_pipe = to_pipe
        self._recv_pipe = from_pipe

        #atexit.register(self.atexit_close)

    def emit(self, name, *args):
        """Send an event though the bus.
        """
        if self.exit:
            return
        self._send_pipe.send(name)

    def transmit(self, name, event=None, **kw):
        self.emit(translate.to_string(name, event, **kw))

    def pump(self, counter=-1):
        """Step the bus pipe and receive any waiting messages.
        """
        pipe = self._recv_pipe
        msg = None

        # print('>')

        msgs = ()
        while pipe.poll(.1):
            msg = pipe.recv()
            if msg is not None:
                msgs += (msg, )

        # if len(msgs) > 0:
            # print('Bus.pump recv sending back actions:', len(msgs))
        return msgs

    def atexit_close(self):
        print('atexit_close')
        self.exit = True
        #self.close()
        self.process.terminate()

    def close(self):
        print('Bus close')
        self.exit = True
        if self._send_pipe is not None:
            self._send_pipe.send(DEATH_PILL)
            self._send_pipe.close()
            self._recv_pipe.close()

        self._send_pipe = None
        self._recv_pipe = None
        self.process.join()
        print('bus closed')

    def drop_event(self, event, name='dragdrop-drop'):
        """Content given to the interface in the form of 'drag drop'.
        The event is not threadsafe. Convert the event to a thin object
        and dispatch an event.
        """
        #self.emit('dragdrop-drop')
        self.transmit(name, event)

    def mouse(self, name, event):
        #self.emit(name,)
        #self.emit(translate.to_string(name, event))
        self.transmit(name, event)

    def contextmenu_create(self, owner_id):
        """An event for creating the 'right click' menu
        Return None to allow the default men"""
        #self.emit('contextmenu_create')
        self.transmit('contextmenu_create', owner_id=owner_id)
        return None

    def contextmenu_point(self, owner_id, point):
        #self.emit('contextmenu_point')
        self.transmit('contextmenu_point',
            owner_id=owner_id,
            point=point
            )

    def contextmenu(self, name, owner_id, menu=None):
        #self.emit(name,)
        self.transmit(name, owner_id=owner_id)

    def move(self, owner_id, event):
        #self.emit('move', owner_id, )
        self.transmit('move', event, owner_id=owner_id)

    def resize(self, owner_id, event):
        #self.emit('resize', owner_id, )
        self.transmit('resize', event, owner_id=owner_id)

    def quit(self, event):
        self.transmit('quit', event)


#@asyncio.coroutine
async def async_mananger_process(*args):
    # Loop slowly in the background pumping the asyc queue. Upon keyboard error
    # this will error earlier than a silent websocket message queue.
    loop = asyncio.get_event_loop()
    log(f"\n!! - async_mananger_process - PID: {os.getpid()}, Parent: {os.getppid()}")

    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, _async_mananger, *args)
        print('custom process pool', result)


#@asyncio.coroutine#
async def async_mananger(*args):
    # Loop slowly in the background pumping the asyc queue. Upon keyboard error
    # this will error earlier than a silent websocket message queue.
    #loop = asyncio.get_event_loop()
    return await _async_mananger(*args)


#@asyncio.coroutine
async def _async_mananger(app):
    log(f"\n!! - async_mananger Executed - PID: {os.getpid()}, Parent: {os.getppid()}")
    run = 1

    while run:
        # yield from asyncio.sleep(.2)
        await asyncio.sleep(.2)

        if bus.exit:
            print('async_mananger loop bus.exit')
            run = 0
            continue
        # yield from bus_pump()
        actions = await bus_pump()
        # actions = yield from bus_pump()
        for action in actions:
            print('perform', action)
            eval(action)
        # print("- async_mananger Executed", os.getpid(), os.getppid())
    log(f"- xx async_mananger exit - PID: {os.getpid()}, Parent: {os.getppid()}")


#@asyncio.coroutine
async def bus_pump():
    return bus.pump()



autoload()
