from webq.core.components import etree


class HTMLBaseTemplate:

    def __init__(self, html_element):
        self.htmlElement = html_element

    def prepare(self, **options):
        return etree.ElementTree.from_html_element(self.htmlElement, **options)
