import unittest
from CoreXYEventListener import CoreXYEventListener
from CoreXYEventObservable import CoreXYEventObservable

__author__ = 'def'

class MockupCoreXYEventListener(CoreXYEventListener):
    def __init__(self):
        self.reset()

    def reset(self):
        self.on_connect_notified = False
        self.on_disconnect_notified = False
        self.on_home_notified = False
        self.on_move_notified = False

    def on_connect(self):
        self.on_connect_notified = True

    def on_disconnect(self):
        self.on_disconnect_notified = True

    def on_home(self):
        self.on_home_notified = True

    def on_move(self, x, y):
        self.on_move_notified = (x, y)


class CoreXYObservableTest(unittest.TestCase):

    def test_add_listener(self):
        listener = MockupCoreXYEventListener()
        observable = CoreXYEventObservable()

        self.assertTrue(observable.add_listener(listener))
        self.assertEqual(len(observable.listeners), 1)

    def test_add_listener_bad(self):
        observable = CoreXYEventObservable()

        self.assertRaises(TypeError, observable.add_listener, "This is not an observer")
        self.assertFalse(observable.listeners)

    def test_on_connect_works(self):
        listener = MockupCoreXYEventListener()
        observable = CoreXYEventObservable()
        self.assertTrue(observable.add_listener(listener))

        observable._notify_listeners("connect")
        self.assertTrue(listener.on_connect_notified)

    def test_on_disconnect_works(self):
        listener = MockupCoreXYEventListener()
        observable = CoreXYEventObservable()
        self.assertTrue(observable.add_listener(listener))

        observable._notify_listeners("disconnect")
        self.assertTrue(listener.on_disconnect_notified)

    def test_on_home_works(self):
        listener = MockupCoreXYEventListener()
        observable = CoreXYEventObservable()
        self.assertTrue(observable.add_listener(listener))

        observable._notify_listeners("home")
        self.assertTrue(listener.on_home_notified)

    def test_on_move_works(self):
        listener = MockupCoreXYEventListener()
        observable = CoreXYEventObservable()
        self.assertTrue(observable.add_listener(listener))

        observable._notify_listeners("move", 1, 2)
        self.assertTrue(listener.on_move_notified)
        self.assertEqual(listener.on_move_notified[0], 1)
        self.assertEqual(listener.on_move_notified[1], 2)

