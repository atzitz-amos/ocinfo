from webq.base.components.tags_q import component_q
from webq.core.nodes.etree import ElementNode


class CustomComponent(ElementNode):
    def __init__(self, children=None, attributes=None, **kw):
        super().__init__(children)
        self.attributes = attributes or {}
        self._kw = kw

    def get_renderer(self):
        pass


def custom_component(value, *children, **attrs):
    return component_q(value, default_cls=CustomComponent)(*children, **attrs)

