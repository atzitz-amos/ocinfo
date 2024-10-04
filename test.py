from webq.responsive.http import http_request
from webq.responsive.json.unpacker import unpack_json
from webq.responsive.json import json_string, json_list_item

from webq.base.components import components

from webq.base.components.tags_q import *
from webq.base.styling.css import css
from webq.core.resolver.template import TemplateResolver
from webq.web.app import App

app = App(__name__)


@app.template("/")
def index():
    return html_q(
        body_q(
            h1_q("Hello, World!"),
            p_q("This is a paragraph.", class_="para"),
            a_q("Click me!", href="/about", style=css(color="blue", textDecoration="none")),

            css(".para", background="red"),
        )
    )


"""
{
    "lists": ["1", "2", "3"],
    "items": [
        {"item_name": "A", "list": "1"},
        {"item_name": "B", "list": "1"},
        {"item_name": "C", "list": "2"},
        {"item_name": "D", "list": "2"},
        {"item_name": "E", "list": "3"}
    ]
}
"""


@app.component("my_list")
def my_list():
    return div_q(unpack_json(
        http_request("GET", "https://127.0.0.1:5000/mydata"),
        lambda model: model["lists"].to([
            *components.lists.CollapsableList(
                title="List " + model["$0"],
                children=model["items"].where(lambda item: item["list"] == model["$0"]).to([
                    *components.lists.Item(
                        "Item " + model["$1"]["item_name"],
                        class_="searchable-item"
                    )
                ]),
                hide_when_empty=True,
                class_="collapsible-list"
            )
        ])
    ))


@app.template("/smth")
def something():
    return html_q(
        components.searchable.SearchableList(
            ".searchable-item",
            components.searchable.SearchBar(
                placeholder="Search...",
                search_button="icon",
                search_button_icon=components.icons.fa.fa_search,
            ),
            components.custom.custom_component("my_list")
        )
    )

x = index()
print(TemplateResolver(app, x).parse())
