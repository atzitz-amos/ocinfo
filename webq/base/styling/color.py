import collections

from webq.core.placeholders.base_placeholder import _detect_placeholder


def css_color(*args):
    if len(args) == 1:
        if isinstance(args, str):
            return CSSColor.from_string(args)
        elif isinstance(args, int):
            return CSSColor.from_string(f"#{hex(args)[2:]}")
        elif isinstance(args, collections.Iterable):
            return css_color(*args)
        return str(args[0])
    if len(args) == 3:
        return CSSColor("rgb", *args)
    if len(args) == 4:
        if isinstance(args[0], str):
            return CSSColor(args[0], *args[1:])
        return CSSColor("rgba", *args)
    if len(args) == 5:
        return CSSColor(args[0], *args[1:-1], transparency=args[-1])


class CSSColor:
    def __init__(self, mode, *args, transparency=None):
        self.mode = mode
        self.args = args

        self.transparency = transparency or (args[-1] if mode.endswith("a") else None)

        self.is_placeholder = _detect_placeholder(args)

    def render(self):
        return f"{self.mode}({', '.join(map(css_color, self.args))}{"" if self.transparency is None else f" / {int(self.transparency)}"})"

    class from_string:
        def __init__(self, value):
            self.value = value

            self.is_placeholder = False

        def render(self):
            return self.value
