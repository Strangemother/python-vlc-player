import queue
import time, os, sys

from player import translate
from player import action

from wlog import color_plog, log as _log
log = color_plog('magenta').announce(__spec__)

DEATH_PILL = '~~some arbitrary string for STOP~~'


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

import asyncio


def process_start(config, from_pipe, send_pipe, ):
    """Start the plugin manager - knowning this method runs within an isolated
    process. Communicate through pipes to the parent.

    send_pipe: send to the parent
    recv_pipe: receive from the parent
    """
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        main(config, from_pipe, send_pipe)
    )

    #loop.run_loop()



async def main(config, from_pipe, send_pipe):
    # info('plugin::process_start send hello')
    log(f'Child process_start. Send hello. Current PID:{os.getpid()}, Parent PID: {os.getppid()}')
    send_pipe.send('hello')
    log("sent. Child Waiting...")
    log("child recv:", from_pipe.recv())
    log("sleep 1")

    await run(config, from_pipe, send_pipe)

async def run(config, from_pipe, send_pipe):
    run = 1
    while run:
        try:
            msg = from_pipe.recv()
        except queue.Empty:
            time.sleep(.1)

        if msg == DEATH_PILL:
            run = 0
            log('Receive death')
            break

        return_val = message_translate(msg)

        if DEATH_PILL in (msg, return_val, ):
            run = 0
            log('Receive late death')
            break

        if return_val is None:
            continue

        send_pipe.send(return_val)

    log("child close.")
    return 0


TRANS = {}


def print_msg(msg):
    last = TRANS.get('last', None)
    count = TRANS.get('count', 0)

    if str(last) == str(msg):
        print('.', end='')
        sys.stdout.flush()
    # else:
    #     _log(f'< {msg}', count, color='yellow')

    TRANS['last'] = str(msg)


def message_translate(msg):
    """Convert a given pipe message to the correct solution for plugin content
    return a string - or None for no action.
    """
    print_msg(msg)

    event = translate.from_string(msg)
    str_action = action.get_action(event)
    if str_action:
        return str_action

    count = TRANS.get('count', 0)
    if count > 50:
        # print('send stop from translate.')
        count = 0
        TRANS['count'] = count
        return 'app.quit()'
        return 'app.players[0].get_player().stop()'

    count += 1
    TRANS['count'] = count

    return None
