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

from __future__ import annotations

__all__ = (
    "css",
    "formatCSS",
    "formatCSSKey",
    "formatCSSValue",
    "CascadingStyleSheet",
    "FileCSS",
    "RawCSS",
    "DictionaryCSS",
    "AttrsCSS",
    "CSSFunction",
    "CSSDefaultFunction",
)

from fileinput import filename

from webq.core.nodes.etree import ETreeCursor
from webq.core.nodes.renderers import NodeRenderer, NodeRendererBuilder, NodeRendererMappers

from webq.core.placeholders.base_placeholder import _detect_placeholder
from webq.core.nodes import etree


class CascadingStyleSheet(etree.ElementNode):
    def __init__(self):
        super().__init__([])

    def reattach_at(self, app, cursor: "ETreeCursor") -> None:
        with cursor as cursor:
            self.level = cursor.level
            self.tree = cursor.tree

            cursor.insert_head(self)


class FileCSS(CascadingStyleSheet):

    def __init__(self, filenames):
        super().__init__()
        self.filenames = filenames

    def get_renderer(self) -> NodeRenderer:
        return NodeRendererBuilder() \
            .with_content("".join("<link rel='stylesheet' href='{}' />".format(x) for x in self.filenames)) \
            .build()


class RawCSS(CascadingStyleSheet):

    def __init__(self, raw_css):
        super().__init__()
        self.raw_css = raw_css

    def reattach_at(self, app, cursor: "ETreeCursor") -> None:
        with cursor as cursor:
            self.level = cursor.level
            self.tree = cursor.tree

            cursor.insert_inplace(self)

    def get_renderer(self) -> NodeRenderer:
        return NodeRendererBuilder() \
            .as_html_tag("style") \
            .with_content(self.raw_css) \
            .build()


class DictionaryCSS(CascadingStyleSheet):

    def __init__(self, attrs):
        super().__init__()
        self.attrs = attrs

    def reattach_at(self, app, cursor: "ETreeCursor") -> None:
        raise NotImplementedError("DictionaryCSS should not be reattached to the tree")

    def get_renderer(self) -> NodeRenderer:
        return NodeRendererBuilder() \
            .with_syntax("{}={}").applied_to(*zip(*self.attrs.items())).with_sep(";") \
            .build()


class AttrsCSS(CascadingStyleSheet):

    def __init__(self, selectors, attrs):
        super().__init__()
        self.selectors = selectors
        self.attrs = attrs

    def get_renderer(self) -> NodeRenderer:
        return NodeRendererBuilder() \
            .as_html_tag("style") \
            .with_syntax("{} {{ {} }}").applied_to(self.selectors, self.attrs).with_sep(";") \
            .build()


def formatCSSKey(k):
    s = ""
    for c in k:
        if c.isupper():
            s += "-" + c.lower()
        else:
            s += c
    if s == "class_":
        return "class"
    return s.replace("_", "-")


def formatCSSValue(v, k):
    if isinstance(v, list):
        v = " ".join(v)
    elif isinstance(v, CSSFunction):
        v = v.render()
    else:
        v = str(v)

    if k == "content":
        return f'"{v}"'
    return v


def formatCSS(kw):
    newkw = {}
    for k, v in kw.items():
        key = formatCSSKey(k)
        newkw[key] = formatCSSValue(v, key)
    return newkw


def css(*args, filename=None, filenames=None, **options) -> CascadingStyleSheet:
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
        options = formatCSS(options)
        if args:
            return AttrsCSS(args, options)
        return DictionaryCSS(options)
    if args:
        return RawCSS(''.join(args))
    raise ValueError("Invalid arguments for css()")


class CSSFunction:
    def render(self):
        raise NotImplementedError()


class CSSDefaultFunction(CSSFunction):
    def __init__(self, type_, function, *args):
        self.type_ = type_
        self.function = function
        self.args = args

        self.is_placeholder = _detect_placeholder(args)

    def render(self):
        return f"{self.function}({', '.join(map(str, self.args))})"
