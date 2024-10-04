from webq.core.nodes.renderers import NodeRenderer


class ElementTree:
    """ An element tree composed of `ElementNode`s, which represents a page html """

    def __init__(self):
        self.head = []

        self.body_el = None
        self.head_el = None

        self.html_el = None

    @property
    def body(self):
        return self.body_el.children if self.body_el else []

    def insert_head(self, element: "ElementNode") -> None:
        self.head.append(element)

    def render(self) -> str:
        s = "\n"
        return f"\n<!DOCTYPE html><html><head>{s.join(map(lambda x: x.get_renderer().render(), self.head))}</head><body>{s.join(map(lambda x: x.get_renderer().render(), self.body))}</body></html>"

    @classmethod
    def from_html_element(cls, html: "ElementNode", *, app) -> "ElementTree":
        etree = cls()
        html.tree = etree

        html.reattach_at(app, ETreeCursor.toplevel(html))
        return etree


class ElementNode:
    def __init__(self, children):
        self.children = list(children)

        self.parent = None
        self.tree = None
        self.level = 0

    @classmethod
    def with_children(cls, children: ["ElementNode"]) -> "ElementNode":
        inst = cls(None)
        for child in children:
            child.parent = inst
        inst.children = children
        return inst

    def reattach_at(self, app, cursor: "ETreeCursor") -> None:
        raise NotImplementedError()

    def cursor(self) -> "ETreeCursor":
        return ETreeCursor(self, self.level)

    def get_renderer(self) -> NodeRenderer:
        raise NotImplementedError(
            "This component should not have been reattached to the tree and thus has no render method")


class ETreeCursor:
    def __init__(self, node, level, tree=None):
        self.root = node
        self.tree = tree or node.tree
        self.level = level

        self._modifications = []
        self._head_modifications = []

    def __enter__(self) -> "ETreeCursor":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.root.children.extend(self._modifications)
        self.root.tree.head.extend(self._head_modifications)

    def insert_inplace(self, element: ElementNode) -> None:
        self._modifications.append(element)

    def insert_head(self, element: ElementNode) -> None:
        self._head_modifications.append(element)

    def child(self, node: ElementNode) -> "ETreeCursor":
        return ETreeCursor(node, self.level + 1, self.tree)

    def nth_child(self, n: int) -> "ETreeCursor":
        return ETreeCursor(self.root.children[n], self.level + 1, self.tree)

    @property
    def parent(self) -> ElementNode:
        return self.parent

    @classmethod
    def toplevel(cls, html: ElementNode) -> "ETreeCursor":
        return cls(html, 0)

    def __repr__(self) -> str:
        return f"<ETreeCursor [{self.level}] at {self.root}>"
