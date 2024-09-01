class HTMLComponentsIterator:
    """ Iterate over all HTML components in a web page. """

    def __init__(self, component):
        self.component = component

        self.index = 0

    def iterator(self):
        if hasattr(self.component, "tagname"):
            yield "<" + self.component.tagname + ">", self.component

            for child in self.component.children:
                yield from HTMLComponentsIterator(child).iterator()

            yield "</" + self.component.tagname + ">", None
        else:
            yield None, self.component
