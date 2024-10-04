import collections

__all__ = (
    "BasePlaceholder",
    "UnknownPlaceholder",
    "_detect_placeholder",
)


class BasePlaceholder:
    pass


class UnknownPlaceholder(BasePlaceholder):
    """ Base placeholder used before compilation when type is unknown """


def _detect_placeholder(args):
    if isinstance(args, collections.Iterable):
        return any(_detect_placeholder(a) for a in args)
    if hasattr(args, "is_placeholder"):
        return args.is_placeholder
    return isinstance(args, BasePlaceholder)
