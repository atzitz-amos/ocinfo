from webq.core.nodes import etree
from webq.core.nodes.etree import ETreeCursor
from webq.core.nodes.iterator import HTMLComponentsIterator
from webq.core.nodes.renderers import NodeRendererBuilder, NodeRenderer
from webq.core.nodes.searcher import HTMLSearcher


class HTMLComponent(etree.ElementNode):
    _REATTACH_SPECIFICATIONS = {}

    @staticmethod
    def to_html_element(element):

        if isinstance(element, str):
            from webq.base.components.text import TextNode
            from webq.base.components.tags_q import br_q
            if element == "\n":
                return br_q()
            return TextNode(element)
        return element

    @staticmethod
    def normalize_attributes(attributes):
        def _normalize_key(k):
            if k == "class_":
                return "class"
            s = ""
            for c in k:
                if c.isupper():
                    s += "-" + c.lower()
                else:
                    s += c
            return s.replace("_", "-")

        return {_normalize_key(k): v for k, v in attributes.items() if v is not None}

    def __init__(self, tagname, children=None, attributes=None, **kw):
        super().__init__([])

        self.tagname = tagname
        self.html_children = list(map(self.to_html_element, children))
        self.attributes = self.normalize_attributes(attributes) or {}

        self._kw = kw

    def reattach_at(self, app, cursor) -> None:
        def reattach_default():
            nonlocal cursor
            with cursor as cursor:
                self.level = cursor.level
                self.tree = cursor.tree

                for c in list(self.html_children):
                    c.reattach_at(app, cursor.child(self))

                cursor.insert_inplace(self)

        if self.tagname in self._REATTACH_SPECIFICATIONS:
            return self._REATTACH_SPECIFICATIONS[self.tagname](self, cursor, reattach_default)
        return reattach_default()

    def get_renderer(self) -> NodeRenderer:
        return NodeRendererBuilder() \
            .as_html_tag(self.tagname, attributes=self.attributes) \
            .build()

    def iterators(self):
        return HTMLComponentsIterator(self)

    @property
    def has_closing(self):
        return self._kw.get("has_closing", True)

    def find(self, q):
        return HTMLSearcher(self).find_one(q)

    def find_all(self, q):
        return HTMLSearcher(self).find_all(q)

    def __repr__(self):
        r = '"'
        return f"<{self.tagname}{(' ' + ' '.join(f'{k}={r}{v}{r}' for k, v in self.attributes.items())) if self.attributes else ''}" + (
            f">{'...' if self.html_children else ''}</{self.tagname}>" if self.has_closing else "/>")

    def __iter__(self):
        return HTMLComponentsIterator(self).default()

    @classmethod
    def specification(cls, tagname):
        def decorator(func):
            cls._REATTACH_SPECIFICATIONS[tagname] = func
            return func

        return decorator


@HTMLComponent.specification("html")
def reattach_html(self, cursor, default):
    cursor.tree.html_el = self
    default()

@HTMLComponent.specification("body")
def reattach_body(self, cursor, default):
    cursor.tree.body_el = self
    default()


if __name__ == '__main__':
    h = HTMLComponent("")
