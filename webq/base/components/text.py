from webq.core.nodes.component import HTMLComponent
from webq.core.nodes.renderers import NodeRendererBuilder


class TextNode(HTMLComponent):
    def __init__(self, value):
        super().__init__("_text_", [], {})

        self.value = value

    def get_renderer(self):
        return NodeRendererBuilder() \
            .with_prefix(self.value) \
            .build()
