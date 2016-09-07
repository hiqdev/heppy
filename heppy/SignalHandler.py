#!/usr/bin/env python

import signal
from contextlib import contextmanager

from pprint import pprint

class SignalHandler:
    def __init__(self, callbacks):
        """Defines callbacks.
        callbacks -- hash: signal name => callback
        """
        self.working = False
        self.received = False
        self.callbacks = {}
        for name, callback in callbacks.iteritems():
            no = getattr(signal, name)
            self.callbacks[str(no)] = callback
            signal.signal(no, self.on_signal)

    def on_signal(self, signal, frame):
        self.received = True
        if not self.working:
            self.run_callback(signal)

    def run_callback(self, no):
        callback = self.callbacks[str(no)]
        self.received = False
        callback()

    @contextmanager
    def block_signals(self):
        self.working = True
        try:
            yield
        finally:
            self.working = False
            if self.received:
                self.run_callback()
                
