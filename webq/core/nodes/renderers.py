from __future__ import annotations

import typing


class NodeRenderer:
    def __init__(self, children=None, *, prefix=None, node=None, suffix=None, mappers=None, filterers=None):
        self.children = children or []
        self.prefix = prefix or ""
        self.node = node or ""
        self.suffix = suffix or ""
        self.mappers = mappers or []
        self.filterers = filterers or []

    def mapper(self, i, child):
        for mapper in self.mappers:
            child = mapper(i, child)
        return child

    def filterer(self, i, child):
        for filterer in self.filterers:
            if not filterer(i, child):
                return False
        return True

    def render(self):
        s = self.prefix
        s += self.node
        s += "".join(self.mapper(i, child) for i, child in enumerate(self.children) if self.filterer(i, child))
        s += self.suffix
        return s


class NodeRendererMappers:
    @staticmethod
    def from_component() -> typing.Callable[[int, "ElementNode"], str]:
        def mapper(i: int, component: "ElementNode"):
            return component.get_renderer().render()

        return mapper

    @staticmethod
    def formatted(*formatting) -> typing.Callable[[int, str], str]:
        def mapper(i: int, child: str):
            return child.format(*formatting)

        return mapper


class NodeRendererBuilder:
    def __init__(self):
        self.children = None

        self.prefix = None
        self.node = None
        self.suffix = None

        self.syntax = None
        self.formattings = None
        self.sep = None

        self.mappers = []
        self.filterers = []

    def with_children(self, children) -> 'NodeRendererBuilder':
        self.children = children
        return self

    def with_prefix(self, prefix, *formatting_args, sep="") -> 'NodeRendererBuilder':
        self.prefix = sep.join(prefix.format(*x) for x in zip(*formatting_args))
        return self

    def with_sep(self, sep) -> 'NodeRendererBuilder':
        self.sep = sep
        return self

    def with_content(self, node) -> 'NodeRendererBuilder':
        self.node = node
        return self

    def with_suffix(self, suffix, *formatting_args, sep="") -> 'NodeRendererBuilder':
        self.prefix = sep.join(suffix.format(*x) for x in zip(*formatting_args))
        return self

    def with_mapper(self, mapper) -> 'NodeRendererBuilder':
        self.mappers.append(mapper)
        return self

    def with_filterer(self, filterer) -> 'NodeRendererBuilder':
        self.filterers.append(filterer)
        return self

    def as_html_tag(self, tagname, *, attributes=None) -> 'NodeRendererBuilder':
        self.prefix = f"""<{tagname}{(' ' + ' '.join(f'{k}="{v}"' for k, v in attributes.items())) if attributes else ''}>"""
        self.suffix = f"</{tagname}>"
        return self

    def with_syntax(self, syntax: str) -> 'NodeRendererBuilder':
        self.syntax = syntax
        return self

    def applied_to(self, *formattings) -> 'NodeRendererBuilder':
        if self.syntax is None:
            raise ValueError("Syntax not set")
        self.formattings = formattings
        return self

    def build(self) -> NodeRenderer:
        if self.syntax:
            self.node = self.sep.join(self.syntax.format(*formatting) for formatting in zip(self.formattings))

        return NodeRenderer(
            children=self.children,
            prefix=self.prefix,
            node=self.node,
            suffix=self.suffix,
            mappers=self.mappers,
            filterers=self.filterers,
        )
