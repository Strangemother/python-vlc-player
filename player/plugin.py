import queue
import time, os

DEATH_PILL = '~~some arbitrary string for STOP~~'

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())



def process_start(config, send_pipe, recv_pipe):
    """Start the plugin manager - knowning this method runs within an isolated
    process. Communicate through pipes to the parent.

    send_pipe: send to the parent
    recv_pipe: receive from the parent

    """
    # info('plugin::process_start send hello')
    print('Child process_start. Send hello')
    send_pipe.send('hello')
    print("sent. Child Waiting...")
    print("child recv:", recv_pipe.recv())
    print("sleep 1")
    run = 1
    while run:
        try:
            msg = recv_pipe.recv()

        except queue.Empty:
            time.sleep(.1)

        if msg == DEATH_PILL:
            run = 0
            print('Receive death')
            break


        return_val = translate(msg)

        if DEATH_PILL in (msg, return_val, ):
            run = 0
            print('Receive late death')
            break

        if return_val is None:
            continue

        send_pipe.send(return_val)

    print("child close.")


def translate(msg):
    """Convert a given pipe message to the correct solution for plugin content
    return a string - or None for no action.
    """
    print(f'translate recv {msg}')

    return None
