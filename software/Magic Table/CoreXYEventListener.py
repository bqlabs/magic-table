__author__ = 'def'


class CoreXYEventListener(object):

    def on_connect(self):
        raise NotImplementedError

    def on_disconnect(self):
        raise NotImplementedError

    def on_home(self):
        raise NotImplementedError

    def on_move(self, x, y):
        raise NotImplementedError

