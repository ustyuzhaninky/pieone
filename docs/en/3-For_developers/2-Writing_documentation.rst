Writing Documentation
=====================

Documentation is written in reStructuredText_ format. Any documents should be contained in
the language-specific folder for the app to find them and add to the list of documents.

An example of a reStructuredText is displayed below by following code:
::

    text = """
    .. _top:

    Hello world
    ===========

    This is an **emphased text**, some ``interpreted text``.
    And this is a reference to top_::

        $ print("Hello world")

    """
    document = RstDocument(text=text)

The rendering will output:

.. image:: https://kivy.org/doc/stable/_images/rstdocument.png
    :height: 100
    :width: 200
    :scale: 50
    :alt: A rendering example (if you see this message, you have no internet connection or the link is broken)

Sources:
    - http://docutils.sourceforge.net/rst.html
    - https://kivy.org/doc/stable/api-kivy.uix.rst.html

.. _reStructuredText: http://docutils.sourceforge.net/rst.html