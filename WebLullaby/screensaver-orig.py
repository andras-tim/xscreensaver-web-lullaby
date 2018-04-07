import gi
gi.require_version('Gtk', '2.0')
gi.require_version('GdkX11', '2.0')
from gi.repository import Gtk, GdkX11

import logging
import os
import signal
from ctypes import c_int
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from PyQt5.QtWidgets import QMessageBox, QApplication

from . import config

_logger = logging.getLogger(config.APP_NAME)


class _Browser(object):
    def __init__(self, app, enable_user_interaction=False):
        """
        :type app: QApplication
        :type enable_user_interaction: bool
        """
        self.__app = app

        self.__web_view = QWebView()
        self.__web_view.setDisabled(not enable_user_interaction)
        self.__web_view.setStyleSheet('* { background-color: rgb(0, 0, 0); }')

        self.__web_view.closeEvent = self.__web_view_on_close
        self.__web_view.titleChanged.connect(self.__web_view_on_title_change)
        self.__web_view.setPage(_WebPage())

    def show_window(self, width=800, height=800):
        """
        :type width: int
        :type height: int
        """
        self.__web_view.setBaseSize(width, height)

        self.__web_view.show()

    def embed_window(self, foreign_window_id):
        """
        :type foreign_window_id: int
        """
        display = GdkX11.X11Display.get_default()
        web_view_window = GdkX11.X11Window.foreign_new_for_display(display, c_int(self.__web_view.winId()).value)
        foreign_window = GdkX11.X11Window.foreign_new_for_display(display, foreign_window_id)

        # foreign_window.set_events(
        #     gtk.gdk.EXPOSURE_MASK
        #     | gtk.gdk.STRUCTURE_MASK
        # )

        # INFO: https://github.com/jsdf/previous/blob/master/python-ui/tests/pygtk-hatari-embed-test.py
        web_view_window.reparent(foreign_window, 0, 0)
        while Gtk.events_pending():
            Gtk.main_iteration()

        self.__web_view.setWindowFlags(
            Qt.Tool
            | Qt.FramelessWindowHint
            | Qt.NoDropShadowWindowHint
        )

        width, height = foreign_window.get_size()
        self.__web_view.setFixedSize(QSize(width, height))

        self.__web_view.setVisible(False)
        self.__web_view.loadFinished.connect(self.__web_view_on_load_finished)

        self.__web_view.show()

    def open(self, url):
        """
        :type url: str
        """
        self.__web_view.load(QUrl(url))

    @classmethod
    def __web_view_on_close(self, event):
        """
        :type event: PyQt5.QtGui.QCloseEvent.QCloseEvent
        """
        mbox = QMessageBox()
        mbox.setModal(True)
        mbox.setText('Click on \'Cancel\' to leave the application open.')
        mbox.setIcon(QMessageBox.Question)
        mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        event.setAccepted(mbox.exec_() == QMessageBox.Ok)

    def __web_view_on_load_finished(self):
        self.__web_view.setVisible(True)

    def __web_view_on_title_change(self, browser_title):
        """
        :type browser_title: str
        """
        self.__web_view.setWindowTitle(browser_title)


class _WebPage(QWebPage):
    def javaScriptConsoleMessage(self, message, line_number, source):
        """
        :type message: str
        :type line_number: int
        :type source: str
        """
        _logger.debug('JsConsole: {message} - {source}:{line}'.format(
            message=message,
            source=source,
            line=line_number
        ))


def run(url):
    """
    :type url: str
    :rtype: int
    """
    parent_wid = os.environ.get('XSCREENSAVER_WINDOW')

    app = QApplication([__file__])
    app.setApplicationDisplayName(config.APP_NAME)

    browser = _Browser(app)
    if parent_wid is None:
        browser.show_window()
    else:
        browser.embed_window(int(parent_wid, 16))
    browser.open(url)

    # Handle properly Ctrl+C while QT App is running
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    return app.exec_()
