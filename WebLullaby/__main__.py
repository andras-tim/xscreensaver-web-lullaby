#!/usr/bin/env python2
import logging

import os
import sys
import gtk
import subprocess
from ctypes import c_int
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtWebKitWidgets import QWebPage, QWebView
from PyQt5.QtWidgets import QApplication, QMessageBox

from WebLullaby import APP_NAME

_logger = logging.getLogger(APP_NAME)


class Browser(object):
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
        self.__web_view.setPage(_CustomQWebPage())

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
        web_view_window = gtk.gdk.window_foreign_new(c_int(self.__web_view.winId()).value)
        foreign_window = gtk.gdk.window_foreign_new(foreign_window_id)

        foreign_window.set_events(
            gtk.gdk.EXPOSURE_MASK
            | gtk.gdk.STRUCTURE_MASK
        )

        # INFO: https://github.com/jsdf/previous/blob/master/python-ui/tests/pygtk-hatari-embed-test.py
        web_view_window.reparent(foreign_window, 0, 0)
        while gtk.events_pending():
            gtk.main_iteration()

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


class _CustomQWebPage(QWebPage):
    def javaScriptConsoleMessage(self, message, line_number, source):
        _logger.debug('JsConsole: {message} - {source}:{line}'.format(
            message=message,
            source=source,
            line=line_number
        ))


def main():
    """
    :rtype: int
    """
    logging.basicConfig(level=logging.INFO)
    parent_wid = os.environ.get('XSCREENSAVER_WINDOW')

    url = 'https://web-animations.github.io/web-animations-demos/#galaxy/'
    if len(sys.argv) > 1:
        url = sys.argv[1]

    subprocess.Popen(['/home/tia/bin/my/tia-layout-reset'], stdin=None, stdout=sys.stdout, stderr=sys.stderr)

    app = QApplication(sys.argv[:1])
    app.setApplicationDisplayName(APP_NAME)

    browser = Browser(app)
    if parent_wid is None:
        browser.show_window()
    else:
        browser.embed_window(int(parent_wid, 16))
    browser.open(url)

    return app.exec_()


if __name__ == '__main__':
    sys.exit(main())
