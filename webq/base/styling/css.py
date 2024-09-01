"""
Provides the hyper-overloaded css() function.

Usage:

1) css(filename='file.css') - Include a css file
2) css(filenames=['file.css', 'file2.css']) - Include multiple css files
3) css('.selector {background: red;}') - Include raw css
4) css(background="red") - Convert a dictionary to css
5) css('.selector', background='red') - Convert a dictionary to css
6) css('.selector-1', '.selector-2', background='red') - Convert a dictionary to css
"""


class CascadingStyleSheet:

    def render(self):
        raise NotImplementedError


class FileCSS(CascadingStyleSheet):

    def __init__(self, filenames):
        self.filenames = filenames


class RawCSS(CascadingStyleSheet):

    def __init__(self, raw_css):
        self.raw_css = raw_css


class DictionaryCSS(CascadingStyleSheet):

    def __init__(self, attrs):
        self.attrs = attrs


class AttrsCSS(CascadingStyleSheet):

    def __init__(self, selectors, attrs):
        self.selectors = selectors
        self.attrs = attrs


def css(*args, filename=None, filenames=None, **options):
    """
    Usage:

    1) `css(filename='file.css')` - Include a css file
    2) `css(filenames=['file.css', 'file2.css'])` - Include multiple css files
    3) `css('.selector {background: red;}')` - Include raw css
    4) `css(background="red")` - Convert a dictionary to css
    5) `css('.selector', background='red')` - Convert a dictionary to css
    6) `css('.selector-1', '.selector-2', background='red')` - Convert a dictionary to css

    :return: the resulting CascadingStyleSheet, should not be used directly but rather passed to a component
    """
    if filename:
        return FileCSS([filename])
    if filenames:
        return FileCSS(filenames)
    if options:
        if args:
            return AttrsCSS(args, options)
        return DictionaryCSS(options)
    if args:
        return RawCSS(''.join(args))
    raise ValueError("Invalid arguments for css()")
