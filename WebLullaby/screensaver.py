import logging
import os
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('GdkX11', '3.0')
gi.require_version('WebKit2', '4.0')  # apt install gir1.2-webkit2-4.0
from gi.repository import Gtk, Gdk, GdkX11, WebKit2

from . import config
from .signal_handler import SignalHandler

_logger = logging.getLogger(config.APP_NAME)


class _Browser:
    def __init__(self, enable_user_interaction=False):
        """
        :type enable_user_interaction: bool
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(b'* { background-color: rgb(0, 0, 0); }')

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # WebView - https://lazka.github.io/pgi-docs/WebKit2-4.0/classes/WebView.html
        self.__web_view = WebKit2.WebView()
        self.__web_view.set_sensitive(enable_user_interaction)

        settings = self.__web_view.get_settings()
        settings.set_property('enable-write-console-messages-to-stdout', True)
        settings.set_property('enable-webgl', True)

        self.__web_view.connect('load-changed', self.__web_view_on_load_changed)

    def show_window(self, width=800, height=600):
        """
        :type width: int
        :type height: int
        """
        enable_user_interaction = False

        # Window
        window = Gtk.Window(title=config.APP_NAME)
        window.set_default_size(width, height)

        window.connect('delete-event', Gtk.main_quit)
        if not enable_user_interaction:
            window.connect('key-press-event', Gtk.main_quit)
            # window.connect('button-press-event', Gtk.main_quit)
            # window.connect('scroll-event', Gtk.main_quit)

        def web_view_on_title_change(web_view, property_spec):
            """
            :type web_view: WebKit2.WebView
            :type property_spec: GParamSpec
            """
            browser_title = web_view.get_title()

            title = config.APP_NAME
            if browser_title is not None:
                title = '{}: {}'.format(title, browser_title)

            window.set_title(title)

        self.__web_view.connect('notify::title', web_view_on_title_change)
        window.add(self.__web_view)

        window.show_all()
        self.__web_view.set_visible(False)

    def embed_window(self, parent_window_id):
        """
        TODO https://github.com/lmartinking/webscreensaver/blob/master/webscreensaver

        :type parent_window_id: int
        """
        display_root_windows = GdkX11.X11Display.get_default()
        foreign_parent = GdkX11.X11Window.foreign_new_for_display(display_root_windows, parent_window_id)
        foreign_width, foreign_height = foreign_parent.get_width(), foreign_parent.get_height()

        plug_window = Gtk.Window(Gtk.WindowType.POPUP)
        plug_window.set_default_size(foreign_width, foreign_height)
        plug_window.connect('destroy', Gtk.main_quit)
        plug_window.add(self.__web_view)

        plug_window.realize()
        plug_window.get_window().reparent(foreign_parent, 0, 0)

        plug_window.show_all()
        self.__web_view.set_visible(False)

    def open(self, url):
        """
        :type url: str
        """
        self.__web_view.load_uri(url)

    def __web_view_on_load_changed(self, web_view, load_event):
        """
        :type web_view: WebKit2.WebView
        :type load_event: WebKit2.LoadEvent
        """
        if load_event == WebKit2.LoadEvent.FINISHED:
            self.__web_view.set_visible(True)


def run(url):
    """
    :type url: str
    :rtype: int
    """

    with SignalHandler(gtk_signal_callback=Gtk.main_quit) as sig_handler:
        parent_wid = os.environ.get('XSCREENSAVER_WINDOW')
        #
        # ################################################################################################################
        #
        # def response_to_dialog(entry, dialog, response):
        #     dialog.response(response)
        #
        # md = Gtk.MessageDialog(
        #     None,
        #     0,  # Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
        #     Gtk.MessageType.QUESTION,
        #     Gtk.ButtonsType.OK_CANCEL,
        #     'parent_wid'
        # )
        #
        # content_area = md.get_content_area()
        # textbox = Gtk.Entry()
        # textbox.connect('activate', response_to_dialog, md, Gtk.ResponseType.OK)
        # textbox.set_text('{}'.format(parent_wid))
        # textbox.set_size_request(200, 50)
        # textbox.show()
        # content_area.pack_end(textbox, True, True, 0)
        #
        # if md.run() == Gtk.ResponseType.CANCEL:
        #     return
        #
        # result_wid = textbox.get_text().strip()
        # md.destroy()
        #
        # if result_wid and result_wid != 'None':
        #     parent_wid = result_wid
        #
        # ################################################################################################################
        #
        # print(repr(parent_wid))

        browser = _Browser()
        if parent_wid is None:
            browser.show_window()
        else:
            browser.embed_window(int(parent_wid, 16))
        browser.open(url)

        if sig_handler.received_signal:
            return sig_handler.exit_code

        Gtk.main()

        return sig_handler.exit_code
