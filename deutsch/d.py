import functools
from typing import Callable, Any, Tuple


class Signature:
    def __init__(self, *args, **kwargs):
        self.args = list(args)
        self.kwargs = kwargs

    def __getitem__(self, item):
        if type(item) is int and item < len(self.args):
            return self.args[item]
        return self.kwargs.get(item, None)

    def __setitem__(self, key, value):
        if type(key) is int and key < len(self.args):
            self.args[key] = value
        else:
            self.kwargs[key] = value


def Begin[X: Callable[[*Tuple[Any]], Any]](handler: Callable[[X, Signature], bool]) -> Callable[[X], X]:
    def mod_decorator(f: X) -> X:
        @functools.wraps(f)
        def mod_func(*args, **kwargs):
            sig = Signature(*args, **kwargs)
            if handler(f, sig):
                return f(*sig.args, **sig.kwargs)

        return mod_func

    return mod_decorator


def After[X: Callable[[*Tuple[Any]], Any]](handler: Callable[[X, Any], Any]) -> Callable[[X], X]:
    def mod_decorator(f: X) -> X:
        @functools.wraps(f)
        def mod_func(*args, **kwargs):
            return handler(f, f(*args, **kwargs))

        return mod_func

    return mod_decorator


@Begin
def on_before(f, sig):
    print(f"Before {f.__name__}")
    sig[0] = 0
    return True


@After
def on_after(f, result):
    print(f"After {f.__name__}")
    return bin(result)


@on_after
@on_before
def add[X](a: int, b: int, x: X=2):
    return a + b


print(on_before)

print(add(1, 2))
