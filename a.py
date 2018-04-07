import signal

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit', '3.0')
from gi.repository import Gtk, WebKit


window = Gtk.Window(title='Foo')
window.connect('delete-event', Gtk.main_quit)
window.set_default_size(800, 600)

scrolled_window = Gtk.ScrolledWindow()
scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)


def web_view_on_title_change(web_view, property_spec):
    browser_title = web_view.get_title()

    title = 'Foo'
    if browser_title is not None:
        title = 'Foo: {}'.format(browser_title)

    window.set_title(title)


def web_view_on_console_message(web_view, message, line, source):
    print('JsConsole: {message} - {source}:{line}'.format(
        message=message,
        source=source,
        line=line
    ))


webview = WebKit.WebView()
webview.set_sensitive(False)
webview.get_settings().set_property("enable-webgl", True)

#webview.open('http://google.com/')
#webview.open('https://goo.gl/sJembB')
#webview.open('https://get.webgl.org/')
webview.open('file:///home/tia/codes/github-com/xscreensaver-web-lullaby/example-screensaver.html')
webview.connect('notify::title', web_view_on_title_change)
webview.connect('console-message', web_view_on_console_message)
scrolled_window.add(webview)


window.add(scrolled_window)
window.show_all()

# Handle properly Ctrl+C while QT App is running
signal.signal(signal.SIGINT, signal.SIG_DFL)

Gtk.main()
