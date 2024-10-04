from webq.base.styling.css import CSSFunction
from webq.core.placeholders.base_placeholder import _detect_placeholder


def css_url(url):
    return CSSUrl(url)


class CSSUrl(CSSFunction):
    def __init__(self, url):
        self.url = url

        self.is_placeholder = _detect_placeholder(url)

    def render(self):
        return f"url({self.url})"
