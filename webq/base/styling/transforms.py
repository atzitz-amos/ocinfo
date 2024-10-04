from webq.base.styling.css import CSSDefaultFunction
from webq.core.placeholders.base_placeholder import _detect_placeholder


def css_translate(x, y):
    return CSSDefaultFunction("transform", "translate", x, y)


def css_translate3d(x, y, z):
    return CSSDefaultFunction("transform", "translate3d", x, y, z)


def css_rotate(angle):
    return CSSDefaultFunction("transform", "rotate", angle)


def css_rotate3d(x, y, z, angle):
    return CSSDefaultFunction("transform", "rotate3d", x, y, z, angle)


def css_scale(x, y=None):
    if y is None:
        y = x
    return CSSDefaultFunction("transform", "scale", x, y)


def css_scale3d(x, y, z):
    return CSSDefaultFunction("transform", "scale3d", x, y, z)


def css_skew(x_angle, y_angle):
    return CSSDefaultFunction("transform", "skew", x_angle, y_angle)


def css_matrix(a, b, c, d, e, f):
    return CSSDefaultFunction("transform", "matrix", a, b, c, d, e, f)


def css_matrix3d(a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p):
    return CSSDefaultFunction("transform", "matrix3d", a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p)


def css_perspective(value):
    return CSSDefaultFunction("transform", "perspective", value)
