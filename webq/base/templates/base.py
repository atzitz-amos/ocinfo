from webq.core.nodes import etree


class HTMLBaseTemplate:

    def __init__(self, html_element):
        self.htmlElement = html_element

    def prepare(self, app, **options):
        return etree.ElementTree.from_html_element(self.htmlElement, app=app)
