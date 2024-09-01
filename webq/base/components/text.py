from webq.core.components.component import HTMLComponent


class TextNode(HTMLComponent):
    def __init__(self, value):
        super().__init__("_text_", [], {})

        self.value = value

    def render(self):
        return self.value
