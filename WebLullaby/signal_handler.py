import logging
import signal

import gi
gi.require_version('GLib', '2.0')
from gi.repository import GLib


class SignalHandler:
    HANDLED_SIGNALS_W_EXIT_CODE = {
        signal.SIGINT: 130,
        signal.SIGTERM: 143,
    }

    def __init__(self, general_signal_callback=None, gtk_signal_callback=None):
        self.__general_signal_callback = general_signal_callback
        self.__gtk_signal_callback = gtk_signal_callback

        self.__received_signal = None

    def __enter__(self):
        self.__register_general_signal_handlers()
        self.__register_gtk_started_handler()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # TODO: unregister signal handlers
        self.__received_signal = None

    @property
    def received_signal(self):
        return self.__received_signal

    @property
    def exit_code(self):
        if self.__received_signal is None:
            return 0

        return self.HANDLED_SIGNALS_W_EXIT_CODE[self.__received_signal]

    def __register_general_signal_handlers(self):
        for sig in self.HANDLED_SIGNALS_W_EXIT_CODE:
            signal.signal(
                sig,
                self.__get_signal_handler(sig, self.__general_signal_callback)
            )

    def __register_gtk_started_handler(self):
        GLib.idle_add(
            self.__register_gtk_signal_handlers,
            priority=GLib.PRIORITY_HIGH
        )

    def __register_gtk_signal_handlers(self):
        for sig in self.HANDLED_SIGNALS_W_EXIT_CODE:
            GLib.unix_signal_add(
                GLib.PRIORITY_HIGH,
                sig,
                self.__get_signal_handler(sig, self.__gtk_signal_callback)
            )

    def __get_signal_handler(self, sig, callback=None):
        message = 'Received signal {}: {}'.format(sig.value, sig.name)

        def on_signal(*args):
            logging.warning(message)
            self.__received_signal = sig
            if callback is not None:
                callback()

        return on_signal
