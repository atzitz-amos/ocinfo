class JSAction:
    pass


class ReloadPageJSA(JSAction):
    pass


# Actions

def _factory(cls, name):
    return cls


reload_page = _factory(ReloadPageJSA, "reload_page")
