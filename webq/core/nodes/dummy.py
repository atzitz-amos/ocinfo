import pathlib

from webq.core.nodes.etree import ElementNode


class DummyHTMLNode(ElementNode):
    def __init__(self, html):
        super().__init__([])

        self.html = html

    def get_renderer(self):
        return self.html


class DummyFileNode(ElementNode):
    def __init__(self, filename):
        super().__init__([])
        self.filename = filename
        self.base = pathlib.Path(__file__.split("\\")[:-2]) / "templates"

    def get_renderer(self):
        with open(str(self.base / self.filename), "r") as io_reader:
            return io_reader.read()
