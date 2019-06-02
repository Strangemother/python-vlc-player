import udp
import asyncio
import os
from wlog import color_plog, log as _log
log = color_plog('white').announce(__spec__)

def init_all():
    print('\n\nInitialize Actions Executed', os.getpid(), os.getppid())
    #yield from asyncio.wait(main())


def get_action(event):
    log('Action', event)
    return None

#udp.main()
bind='0.0.0.0'
port=8888
remote_host='127.0.0.1'
remote_port=9999

async def main():
    loop = asyncio.get_event_loop()
    log("Starting datagram proxy...")
    coro = udp.start_datagram_proxy(bind, port, remote_host, remote_port)
    #await loop.create_task(coro())
    transport, _ = loop.run_until_complete(coro)
    return transport
