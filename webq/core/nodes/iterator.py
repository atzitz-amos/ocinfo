class HTMLComponentsIterator:
    """ Iterate over all HTML nodes in a web page. """

    def __init__(self, component):
        self.component = component

        self.index = 0

    def default(self):
        if hasattr(self.component, "tagname"):
            yield "<" + self.component.tagname + ">", self.component

            for child in self.component.children:
                yield from HTMLComponentsIterator(child).default()

            yield "</" + self.component.tagname + ">", None
        else:
            yield None, self.component

    def linear(self):
        yield self.component
        if hasattr(self.component, "children") and self.component.children:
            for child in self.component.children:
                yield from HTMLComponentsIterator(child).linear()

    def withparents(self):
        if hasattr(self.component, "parent"):
            yield self.component.parent, self.component
        for child in self.component.children:
            yield from HTMLComponentsIterator(child).withparents()
