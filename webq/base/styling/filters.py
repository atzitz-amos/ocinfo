from webq.base.styling.css import CSSDefaultFunction


def css_grayscale(amount):
    return CSSDefaultFunction("filter", "grayscale", amount)


def css_hue_rotate(angle):
    return CSSDefaultFunction("filter", "hue-rotate", angle)


def css_invert(amount):
    return CSSDefaultFunction("filter", "invert", amount)


def css_opacity(amount):
    return CSSDefaultFunction("filter", "opacity", amount)


def css_saturate(amount):
    return CSSDefaultFunction("filter", "saturate", amount)


def css_sepia(amount):
    return CSSDefaultFunction("filter", "sepia", amount)
