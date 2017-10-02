WebLullaby
==========

|CodeQuality| |License|

Browser embedded `xscreensaver <https://en.wikipedia.org/wiki/XScreenSaver/>`__ module for web based screensavers.


Story
-----

Two proof-of-concept tasks failed before this project:

* `Native GTK implementation <https://github.com/andras-tim/poc/tree/master/x11/webview-xscreensaver-py>`__
    **Result:** This could manipulates windows properly, but could't creates GPU accelerated *WebView*.

* `Native QT implementation <https://github.com/andras-tim/poc/tree/master/x11/webview-xscreensaver-qt>`__
    **Result:** This could create GPU accelerated WebView, but could't re-parents *QtMainWindow* into the *xscreensaver*
    window (`foreign window related bugs <https://bugreports.qt.io/browse/QTBUG-40320>`__)

Now, this project combines advantages of the two POCs, so I use **PyQt** for create GPU accelerated *WebView* and
**PyGTK** for window manipulation.


Dependencies
------------

* `PyGTK <https://pypi.python.org/pypi/PyGTK/>`__ >=2.0, <3.0
* `PyQt5 <https://pypi.python.org/pypi/PyQt5/>`__ >=5.5, <6.0


Install dependencies on Ubuntu Xenial
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    sudo ./setup.sh


Setup
-----

1. Screensaver to ``~/.xscreensaver`` config:
    .. code-block::

        ...

        programs:                                                             \
                   /full/path/of/xscreensaver-web-lullaby/bin/web-lullaby   \n\

        ...

2. Open the **XScreenSaver Preferences** and select the **WebLullaby.py**


Configure
---------

You can specify the desired URL by command line argument.

1. Open the **XScreenSaver Preferences** and select the **WebLullaby.py**

2. Click on **Settings...** and after that **Advanced >>**

3. You can extend the command in **Command Line:** field with the URL, e.g.:
    .. code-block:: bash

        /full/path/of/xscreensaver-web-lullaby/WebLullaby/WebLullaby.py \
            'https://web-animations.github.io/web-animations-demos/#galaxy/'


Bugs
----

Bugs or suggestions? Visit the `issue tracker <https://github.com/andras-tim/xscreensaver-web-lullaby/issues>`__.


.. |License| image:: https://img.shields.io/badge/license-GPL%203.0-blue.svg
    :target: https://github.com/andras-tim/xscreensaver-web-lullaby/blob/master/LICENSE
    :alt: License

.. |CodeQuality| image:: https://www.codacy.com/project/badge/e84a77d864144516b1258aa392ba13ef
    :target: https://www.codacy.com/app/andras-tim/xscreensaver-web-lullaby
    :alt: Code Quality

.. |IssueStats| image:: https://img.shields.io/github/issues/andras-tim/xscreensaver-web-lullaby.svg
    :target: http://issuestats.com/github/andras-tim/xscreensaver-web-lullaby
    :alt: Issue Stats
