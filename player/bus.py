"""The Bus centralises all communcation across the components and out into the
external pipes.
Useful for plugin management and state work.
"""
from concurrent.futures import CancelledError, ProcessPoolExecutor
import asyncio
from multiprocessing import Process, Pipe
import os, time


bus = None

def autoload():
    global bus
    bus = Bus()


def get_bus():
    return bus

from plugin import process_start, DEATH_PILL

import atexit

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
        print('start proc, parent sleep 1')
        p.start()
        print('Parent Wait for child "hello"')
        print("Parent recv:", from_pipe.recv())
        print('Parent received ^^. Sending response...')
        to_pipe.send('No eggs.')
        print('Parent sent reponse.')
        #time.sleep(1)
        to_pipe.send('foo')
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
        if len(msgs) > 0:
            print('Bus.pump recv:', len(msgs))
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
        self.emit('dragdrop-drop')

    def mouse(self, name, event):
        self.emit(name,)

    def contextmenu_create(self, owner_id):
        """An event for creating the 'right click' menu
        Return None to allow the default men"""
        self.emit('contextmenu_create')
        return None

    def contextmenu_point(self, owner_id, point):
        self.emit('contextmenu_point')

    def contextmenu(self, name, owner_id, menu=None):
        self.emit(name,)

    def move(self, owner_id, event):
        self.emit('move', owner_id, )

    def resize(self, owner_id, event):
        self.emit('resize', owner_id, )

import os

@asyncio.coroutine
async def async_mananger_process(*args):
    # Loop slowly in the background pumping the asyc queue. Upon keyboard error
    # this will error earlier than a silent websocket message queue.
    loop = asyncio.get_event_loop()

    with ProcessPoolExecutor() as pool:
        result = await loop.run_in_executor(pool, _async_mananger, *args)
        print('custom process pool', result)


@asyncio.coroutine
async def async_mananger(*args):
    # Loop slowly in the background pumping the asyc queue. Upon keyboard error
    # this will error earlier than a silent websocket message queue.
    #loop = asyncio.get_event_loop()
    return await _async_mananger(*args)

@asyncio.coroutine
async def bus_pump():
    return bus.pump()


@asyncio.coroutine
def _async_mananger(app):
    print("\n!! - async_mananger Executed", os.getpid(), os.getppid())
    counter = 0
    run = 1

    while run:

        yield from asyncio.sleep(1)

        if bus.exit:
            print('async_mananger loop bus.exit')
            run = 0
            continue

        counter += 1
        yield from bus_pump()
        #print('_async_mananger while step', counter)
        if counter > 60:
            # app.players[0].get_player().stop()
            counter = 0
            # print('Executing shutdown')
        # print("- async_mananger Executed", os.getpid(), os.getppid())
    print("- xx async_mananger exit", os.getpid(), os.getppid())


autoload()
