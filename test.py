from webq.base.components.tags_q import *
from webq.base.styling import css
from webq.web.app import App

app = App(__name__)


def index():
    return html_q(
        body_q(
            h1_q("Hello, World!"),
            p_q("This is a paragraph.", class_="para"),
            a_q("Click me!", href="/about", style=css(color="blue", textDecoration="none")),

            css(".para", background="red"),
        )
    )


x = index()
print(x)