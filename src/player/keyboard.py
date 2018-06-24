from threading import Thread
from time import sleep
from pynput.keyboard import Key, Controller, Listener

#keyboard = Controller()

def thread_listen():
    t = Thread(target=listen, name='keyboard-listener')
    t.start()
    return t


def listen():
    last_string = tuple()
    # Collect events until released
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    print('Listener death')

def on_press(key):
    print('{0} pressed'.format(key))


def on_release(key):
    print('{0} release'.format(key))
    if key == Key.esc:
        # Stop listener
        return False

