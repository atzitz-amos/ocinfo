from webq.base.styling.css import CSSFunction
from webq.core.placeholders.base_placeholder import _detect_placeholder


def css_calc(expression):
    return CSSCalcFunction(expression)


def css_min(*args):
    return CSSArithmetic("min", *args)


def css_max(*args):
    return CSSArithmetic("max", *args)


def css_clamp(*args):
    return CSSArithmetic("clamp", *args)


def css_sin(*args):
    return CSSArithmetic("sin", *args)


def css_cos(*args):
    return CSSArithmetic("cos", *args)


def css_tan(*args):
    return CSSArithmetic("tan", *args)


def css_asin(*args):
    return CSSArithmetic("asin", *args)


def css_acos(*args):
    return CSSArithmetic("acos", *args)


def css_atan(*args):
    return CSSArithmetic("atan", *args)


def css_exp(*args):
    return CSSArithmetic("exp", *args)


def css_log(*args):
    return CSSArithmetic("log", *args)


def css_sqrt(*args):
    return CSSArithmetic("sqrt", *args)


def css_pow(base, exponent):
    return CSSArithmetic("pow", base, exponent)


class CSSCalcFunction(CSSFunction):
    def __init__(self, expression):
        self.expression = expression

        self.is_placeholder = _detect_placeholder(expression)

    def __str__(self):
        return f"calc({self.expression})"


class CSSArithmetic(CSSFunction):
    def __init__(self, name, *args):
        self.name = name
        self.args = args

        self.is_placeholder = _detect_placeholder(args)

    def __str__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"
