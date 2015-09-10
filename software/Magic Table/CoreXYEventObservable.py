from CoreXYEventListener import CoreXYEventListener

__author__ = 'def'


class CoreXYEventObservable(object):
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        if isinstance(listener, CoreXYEventListener):
            self.listeners.append(listener)
            return True
        else:
            raise TypeError("Tried to add a non-listener object")

    def remove_listeners(self):
        pass

    def _notify_listeners(self, event_type, *args):
        for listener in self.listeners:
            if event_type == "connect":
                listener.on_connect()
            elif event_type == "disconnect":
                listener.on_disconnect()
            elif event_type == "home":
                listener.on_home()
            elif event_type == "move":
                if len(args) == 2:
                    listener.on_move(args[0], args[1])
                else:
                    raise TypeError("on_move() takes exactly two arguments")
            else:
                raise ValueError("Event type %s does not exist" % str(event_type))

        return True