#!/usr/bin/env python

import signal
from contextlib import contextmanager

class SignalHandler:
    def __init__(self, callback, what=signal.SIGUSR2):
        self.callback = callback
        self.received = False
        self.working  = False
        signal.signal(what, self.on_signal)

    def on_signal(self, signal, frame):
        self.received = True
        if not self.working:
            self.run_callback()

    def run_callback(self):
        self.received = False
        self.callback()

    @contextmanager
    def block_signals(self):
        self.working = True
        try:
            yield
        finally:
            self.working = False
            if self.received:
                self.run_callback()
                
