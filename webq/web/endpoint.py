class Endpoint:

    def __init__(self, url: str, f, method, **kw):
        self.url = url
        self.provider = f

        self.method = method

        self.kw = kw

    def __call__(self, *args, **kwargs):
        return self.provider(*args, **kwargs)
