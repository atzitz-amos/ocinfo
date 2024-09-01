from webq.core.components import etree
from webq.core.components.iterator import HTMLComponentsIterator


class HTMLComponent(etree.ElementNode):

    @staticmethod
    def to_html_element(element):
        from webq.base.components.text import TextNode
        from webq.base.components.tags_q import br_q

        if isinstance(element, str):
            if element == "\n":
                return br_q()
            return TextNode(element)
        return element

    def __init__(self, tagname, children=None, attributes=None, **kw):
        super().__init__(map(self.to_html_element, children))

        self.tagname = tagname
        self.attributes = attributes or {}

        self._kw = kw

        for child in self.children:
            child.parent = self

    def __repr__(self):
        return f"<{self.tagname}{(" " + " ".join(f'{k}="{v}"' for k, v in self.attributes.items())) if self.attributes else ""}" + (f">...</{self.tagname}>" if self.has_closure else "/>")

    def __iter__(self):
        return HTMLComponentsIterator(self).iterator()


    @property
    def has_closure(self):
        return self._kw.get("has_closure", True)


if __name__ == '__main__':
    h = HTMLComponent("")
