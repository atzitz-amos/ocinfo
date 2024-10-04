from webq.base.styling.color import css_color
from webq.base.styling.css import CSSFunction
from webq.core.placeholders.base_placeholder import _detect_placeholder


def parse_step(s):
    if isinstance(s, tuple):
        return f"{css_color(s[0])} {s[1]}"
    return css_color(s)


def css_linear_gradient(direction, *steps):
    if len(steps) == 1:
        steps = steps[0]

    return CSSLinearGradient(direction, list(map(parse_step, steps)))


def css_radial_gradient(*args, shape=None, size=None, position=None):
    if len(args) == 1:
        args = args[0]

    return CSSRadialGradient(args, shape, size, position)


def css_conic_gradient(*args, angle=None, position=None, interpolation=None):
    if len(args) == 1:
        args = args[0]

    return CSSConicGradient(args, angle, position, interpolation)


class CSSLinearGradient(CSSFunction):
    def __init__(self, direction, steps):
        self.direction = direction
        self.steps = steps

        self.is_placeholder = _detect_placeholder(direction) or _detect_placeholder(steps)

    def __str__(self):
        return f"linear-gradient({self.direction}, {', '.join(self.steps)})"


class CSSRadialGradient(CSSFunction):
    def __init__(self, args, shape, size, position):
        self.args = args
        self.shape = shape
        self.size = size
        self.position = position

        self.is_placeholder = _detect_placeholder(args) or _detect_placeholder(shape) or _detect_placeholder(size) or _detect_placeholder(position)

    def render(self):
        result = "radial-gradient("
        if self.shape:
            result += f"{self.shape} "
        if self.size:
            result += f"{self.size} "
        if self.position:
            result += f"at {self.position} "
        if self.shape or self.size or self.position:
            result += ", "
        result += f"{', '.join(map(parse_step, self.args))})"


class CSSConicGradient(CSSFunction):
    def __init__(self, args, angle, position, interpolation):
        self.args = args
        self.angle = angle
        self.position = position
        self.interpolation = interpolation

        self.is_placeholder = _detect_placeholder(args) or _detect_placeholder(angle) or _detect_placeholder(position) or _detect_placeholder(interpolation)

    def render(self):
        result = "conic-gradient("
        if self.angle:
            result += f"from {self.angle} "
        if self.position:
            result += f"at {self.position} "
        if self.interpolation:
            result += f"{self.interpolation} "
        if self.angle or self.position or self.interpolation:
            result += ", "
        result += f"{', '.join(map(parse_step, self.args))})"