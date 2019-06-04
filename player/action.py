import udp
import asyncio
import os
from wlog import color_plog, log as _log
log = color_plog('white').announce(__spec__)

def init_all():

    log(f"\n - Initialize Actions - PID: {os.getpid()}, Parent: {os.getppid()}")
    #yield from asyncio.wait(main())
    #loop = asyncio.get_event_loop()
    # task = await asyncio.create_task(main())
    #task = asyncio.create_task(server())
    # await all()

async def all():
    log('\n\nRun action::all()\n\n')
    await asyncio.gather(
            main(),
            server(),
        )


async def get_action(event):
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


class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)


async def server():
    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('127.0.0.1', 9999))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


