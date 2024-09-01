class ElementTree:
    """ An element tree composed of `ElementNode`s, which represents a page html """

    def __init__(self):
        self.head = []
        self.body = []

    def insert_head(self, element):
        self.head.append(element)

    def insert_body(self, element):
        self.body.append(element)

    def render(self):
        return f"\n<!DOCTYPE html><html><head>{'\n'.join(map(lambda x: x.render(), self.head))}</head><body>{'\n'.join(map(lambda x: x.render(), self.body))}</body></html>"

    @classmethod
    def from_html_element(cls, html):
        pass


class ElementNode:
    def __init__(self, children):
        self.children = list(children)

        self.parent = None
        self.tree = None
        self.level = None

    @classmethod
    def with_children(cls, children):
        inst = cls(None)
        for child in children:
            child.parent = inst
        inst.children = children
        return inst

    def rattach(self, parent, tree=None):
        self.parent = parent
        self.tree = tree or parent.tree
        self.level = parent.level + 1

    def cursor(self):
        return ETreeCursor(self, self.level)

    def render(self):
        raise NotImplementedError()


class ETreeCursor:
    def __init__(self, node, level):
        self.node = node
        self.level = level

        self._modifications = []
        self._head_modifications = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.node.children.extend(self._modifications)
        self.node.tree.extend(self._head_modifications)

    def insert_child(self, element):
        self._modifications.append(element)

    def insert_head(self, element):
        self._head_modifications.append(element)

    @property
    def parent(self):
        return self.parent
