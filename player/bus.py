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
        send_pipe, recv_pipe = Pipe()
        conf = config or self.config
        p = Process(target=process_start, args=(conf, send_pipe, recv_pipe))
        # recv_pipe = child_send_pipe
        # send_pipe = child_recv_pipe
        print('start proc, parent sleep 1')
        p.start()
        print('Parent Wait for child "hello"')
        print("Parent recv:", recv_pipe.recv())
        print('Parent received ^^. Sending response...')
        send_pipe.send('No eggs.')
        print('Parent sent reponse.')
        time.sleep(1)
        send_pipe.send('foo')
        self.process = p
        self._send_pipe = send_pipe
        self._recv_pipe = recv_pipe

        #atexit.register(self.atexit_close)

    def emit(self, name, *args):
        """Send an event though the bus.
        """
        self._send_pipe.send(name)

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
def _async_mananger(app):
    print("\n!! - async_mananger Executed", os.getpid(), os.getppid())
    counter = 0
    run = 1

    while run:

        yield from asyncio.sleep(.1)

        if bus.exit:
            print('async_mananger loop bus.exit')
            run = 0
            continue

        counter += 1

        if counter > 60:
            app.players[0].get_player().stop()
            counter = 0
            print('Executing shutdown')
        print("- async_mananger Executed", os.getpid(), os.getppid())
    print("- xx async_mananger exit", os.getpid(), os.getppid())


autoload()
