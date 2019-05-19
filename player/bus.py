"""The Bus centralises all communcation across the components and out into the
external pipes.
Useful for plugin management and state work.
"""

bus = None

def autoload():
    global bus
    bus = Bus()


def get_bus():
    return bus


class Bus(object):

    def emit(self, name, *args):
        """Send an event though the bus.
        """
        pass

autoload()
