"""
Wrapper module to easily create html tags

Provides every html tag as of the HTML5 specification
    (https://html.spec.whatwg.org/dev/indices.html#elements-3).
"""
import re
import warnings

from webq.base.templates.base import HTMLBaseTemplate
from webq.core.nodes.component import HTMLComponent as _HTMLComponent

__all__ = (
    "HTML5_EVENTS_ATTRIBUTES",
    "HTML5_GLOBAL_ATTRIBUTES",
    "HTML5_ATTRIBUTES_PER_TAG",
    "ALL_TAGS",
    "ALL_TAGS_MAPPING",
    "resolve_attribute",
    "html_q",
    'base_q',
    'head_q',
    'link_q',
    'meta_q',
    'style_q',
    'title_q',
    'body_q',
    'address_q',
    'article_q',
    'aside_q',
    'footer_q',
    'header_q',
    'h1_q',
    'h2_q',
    'h3_q',
    'h4_q',
    'h5_q',
    'h6_q',
    'hgroup_q',
    'main_q',
    'nav_q',
    'section_q',
    'search_q',
    'blockquote_q',
    'dd_q',
    'div_q',
    'dl_q',
    'dt_q',
    'figcaption_q',
    'figure_q',
    'hr_q',
    'li_q',
    'menu_q',
    'ol_q',
    'p_q',
    'pre_q',
    'ul_q',
    'a_q',
    'abbr_q',
    'b_q',
    'bdi_q',
    'bdo_q',
    'br_q',
    'cite_q',
    'code_q',
    'data_q',
    'dfn_q',
    'em_q',
    'i_q',
    'kbd_q',
    'mark_q',
    'q_q',
    'rp_q',
    'rt_q',
    'ruby_q',
    's_q',
    'samp_q',
    'small_q',
    'span_q',
    'strong_q',
    'sub_q',
    'sup_q',
    'time_q',
    'u_q',
    'var_q',
    'wbr_q',
    'area_q',
    'audio_q',
    'img_q',
    'map_q',
    'track_q',
    'video_q',
    'embed_q',
    'iframe_q',
    'object_q',
    'picture_q',
    'portal_q',
    'source_q',
    'svg_q',
    'canvas_q',
    'noscript_q',
    'script_q',
    'del_q',
    'ins_q',
    'caption_q',
    'col_q',
    'colgroup_q',
    'table_q',
    'tbody_q',
    'td_q',
    'tfoot_q',
    'th_q',
    'thead_q',
    'tr_q',
    'button_q',
    'datalist_q',
    'fieldset_q',
    'form_q',
    'input_q',
    'label_q',
    'legend_q',
    'meter_q',
    'optgroup_q',
    'option_q',
    'output_q',
    'progress_q',
    'select_q',
    'textarea_q',
    'details_q',
    'dialog_q',
    'summary_q',
    'slot_q',
    'template_q',

    "component_q"
)


class _DefaultHTMLComponent(_HTMLComponent):
    def __init__(self, tagname, children, attributes, **kw):
        super().__init__(tagname, children, attributes, **kw)


def _factory(tagname, accepted_attributes=None, has_closing=True):
    def _(*children, **attributes):
        if accepted_attributes:
            for key in attributes:
                if key not in accepted_attributes and not key.startswith("data"):
                    warnings.warn(f"{key} is not a valid attribute for tag <{tagname}>")
        return _DefaultHTMLComponent(tagname, children, attributes, has_closing=has_closing)

    _.__name__ = tagname + "_q"
    # _.__doc__ = f"Create a new {tagname} tag\n\nSupported attributes: \n{['\t' + z + '\n' for z in accepted_attributes]}"
    return _


def resolve_attribute(name):
    if name == "class_":
        return "class"
    elif name == "for_":
        return "for"
    elif name.startswith("data"):
        return "data-" + resolve_attribute(name[4:])
    return "-".join(re.findall("[A-Z][^A-Z]*", name))


# Attributes


HTML5_EVENTS_ATTRIBUTES = {
    'onabort', 'onafterprint', 'onbeforeprint', 'onbeforeunload', 'onblur', 'oncanplay', 'oncanplaythrough', 'onchange',
    'onclick', 'oncontextmenu', 'oncopy', 'oncuechange', 'oncut', 'ondblclick', 'ondrag', 'ondragend', 'ondragenter',
    'ondragleave', 'ondragover', 'ondragstart', 'ondrop', 'ondurationchange', 'onemptied', 'onended', 'onerror',
    'onfocus', 'onhashchange', 'oninput', 'oninvalid', 'onkeydown', 'onkeypress', 'onkeyup', 'onload', 'onloadeddata',
    'onloadedmetadata', 'onloadstart', 'onmousedown', 'onmousemove', 'onmouseout', 'onmouseover', 'onmouseup',
    'onmousewheel', 'onoffline', 'ononline', 'onpagehide', 'onpageshow', 'onpaste', 'onpause', 'onplay', 'onplaying',
    'onpopstate', 'onprogress', 'onratechange', 'onreset', 'onresize', 'onscroll', 'onsearch', 'onseeked', 'onseeking',
    'onselect', 'onstalled', 'onstorage', 'onsubmit', 'onsuspend', 'ontimeupdate', 'ontoggle', 'onunload',
    'onvolumechange', 'onwaiting', 'onwheel'
}

HTML5_GLOBAL_ATTRIBUTES = {
    'accesskey',
    'anchor',
    'autocapitalize',
    'autofocus',
    'class_',
    'contenteditable',
    'dir',
    'draggable',
    'enterkeyhint',
    'exportparts',
    'hidden',
    'id',
    'inert',
    'inputmode',
    'is',
    'itemid',
    'itemprop',
    'itemref',
    'itemscope',
    'itemtype',
    'lang',
    'nonce',
    'part',
    'popover',
    'role',
    'slot',
    'spellcheck',
    'style',
    'tabindex',
    'title',
    'translate',
    'virtualkeyboardpolicy',
    'writingsuggestions'
} | HTML5_EVENTS_ATTRIBUTES
HTML5_ATTRIBUTES_PER_TAG = {
    'form': {'accept', 'accept-charset', 'action', 'autocomplete', 'enctype', 'method', 'name', 'novalidate', 'target'},
    'input': {'accept', 'alt', 'autocomplete', 'capture', 'checked', 'dirname', 'disabled', 'form', 'formaction',
              'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'height', 'list', 'max', 'maxlength',
              'minlength', 'min', 'multiple', 'name', 'pattern', 'placeholder', 'readonly', 'required', 'size', 'src',
              'step', 'type', 'usemap', 'value', 'width'},
    'caption': {'align'},
    'col': {'align', 'bgcolor', 'span'},
    'colgroup': {'align', 'bgcolor', 'span'},
    'hr': {'align', 'color'},
    'iframe': {'align', 'allow', 'height', 'loading', 'name', 'referrerpolicy', 'sandbox', 'src', 'srcdoc', 'width'},
    'img': {'align', 'alt', 'border', 'crossorigin', 'decoding', 'height', 'ismap', 'loading', 'referrerpolicy',
            'sizes', 'src', 'srcset', 'usemap', 'width'},
    'table': {'align', 'background', 'bgcolor', 'border'},
    'tbody': {'align', 'bgcolor'}, 'td': {'align', 'background', 'bgcolor', 'colspan', 'headers', 'rowspan'},
    'tfoot': {'align', 'bgcolor'},
    'th': {'align', 'background', 'bgcolor', 'colspan', 'headers', 'rowspan', 'scope'},
    'thead': {'align'},
    'tr': {'align', 'bgcolor'},
    'area': {'alt', 'coords', 'download', 'href', 'media', 'ping', 'referrerpolicy', 'rel', 'shape', 'target'},
    'link': {'as', 'crossorigin', 'href', 'hreflang', 'integrity', 'media', 'referrerpolicy', 'rel', 'sizes', 'type'},
    'script': {'async', 'crossorigin', 'defer', 'integrity', 'referrerpolicy', 'src', 'type'},
    'select': {'autocomplete', 'disabled', 'form', 'multiple', 'name', 'required', 'size'},
    'textarea': {'autocomplete', 'cols', 'dirname', 'disabled', 'enterkeyhint', 'form', 'inputmode', 'maxlength',
                 'minlength', 'name', 'placeholder', 'readonly', 'required', 'rows', 'wrap'},
    'audio': {'autoplay', 'controls', 'crossorigin', 'loop', 'muted', 'preload', 'src'},
    'video': {'autoplay', 'controls', 'crossorigin', 'height', 'loop', 'muted', 'playsinline', 'poster', 'preload',
              'src', 'width'},
    'body': {'background', 'bgcolor'},
    'marquee': {'bgcolor', 'loop'},
    'object': {'border', 'data', 'form', 'height', 'name', 'type', 'usemap', 'width'},
    'meta': {'charset', 'content', 'http-equiv', 'name'},
    'blockquote': {'cite'},
    'del': {'cite', 'datetime'},
    'ins': {'cite', 'datetime'},
    'q': {'cite'},
    'font': {'color'},
    'time': {'datetime'},
    'track': {'default', 'kind', 'label', 'src', 'srclang'},
    'button': {'disabled', 'form', 'formaction', 'formenctype', 'formmethod', 'formnovalidate', 'formtarget', 'name',
               'type', 'value'},
    'fieldset': {'disabled', 'form', 'name'},
    'optgroup': {'disabled', 'label'},
    'option': {'disabled', 'label', 'selected', 'value'},
    'a': {'download', 'href', 'hreflang', 'media', 'ping', 'referrerpolicy', 'rel', 'shape', 'target'},
    'contenteditable': {'enterkeyhint', 'inputmode'},
    'label': {'for', 'form'},
    'output': {'for', 'form', 'name'},
    'meter': {'form', 'high', 'low', 'max', 'min', 'optimum', 'value'},
    'progress': {'form', 'max', 'value'},
    'canvas': {'height', 'width'},
    'embed': {'height', 'src', 'type', 'width'},
    'base': {'href', 'target'},
    'source': {'media', 'sizes', 'src', 'srcset', 'type'},
    'style': {'media', 'type'},
    'map': {'name'},
    'param': {'name', 'value'},
    'details': {'open'},
    'dialog': {'open'},
    'ol': {'reversed', 'start', 'type'},
    'menu': {'type'},
    'data': {'value'},
    'li': {'value'}
}
NO_ATTRIBUTES = set()


# Tags

def html_q(*children, **attributes) -> HTMLBaseTemplate:
    return HTMLBaseTemplate(_DefaultHTMLComponent("html", children, attributes))

base_q = _factory('base', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('base', NO_ATTRIBUTES), has_closing=False)
head_q = _factory('head', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('head', NO_ATTRIBUTES))
link_q = _factory('link', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('link', NO_ATTRIBUTES), has_closing=False)
meta_q = _factory('meta', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('meta', NO_ATTRIBUTES), has_closing=False)
style_q = _factory('style', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('style', NO_ATTRIBUTES))
title_q = _factory('title', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('title', NO_ATTRIBUTES))
body_q = _factory('body', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('body', NO_ATTRIBUTES))
address_q = _factory('address', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('address', NO_ATTRIBUTES))
article_q = _factory('article', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('article', NO_ATTRIBUTES))
aside_q = _factory('aside', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('aside', NO_ATTRIBUTES))
footer_q = _factory('footer', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('footer', NO_ATTRIBUTES))
header_q = _factory('header', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('header', NO_ATTRIBUTES))
h1_q = _factory('h1', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('h1', NO_ATTRIBUTES))
h2_q = _factory('h2', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('h2', NO_ATTRIBUTES))
h3_q = _factory('h3', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('h3', NO_ATTRIBUTES))
h4_q = _factory('h4', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('h4', NO_ATTRIBUTES))
h5_q = _factory('h5', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('h5', NO_ATTRIBUTES))
h6_q = _factory('h6', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('h6', NO_ATTRIBUTES))
hgroup_q = _factory('hgroup', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('hgroup', NO_ATTRIBUTES))
main_q = _factory('main', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('main', NO_ATTRIBUTES))
nav_q = _factory('nav', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('nav', NO_ATTRIBUTES))
section_q = _factory('section', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('section', NO_ATTRIBUTES))
search_q = _factory('search', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('search', NO_ATTRIBUTES))
blockquote_q = _factory('blockquote', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('blockquote', NO_ATTRIBUTES))
dd_q = _factory('dd', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('dd', NO_ATTRIBUTES))
div_q = _factory('div', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('div', NO_ATTRIBUTES))
dl_q = _factory('dl', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('dl', NO_ATTRIBUTES))
dt_q = _factory('dt', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('dt', NO_ATTRIBUTES))
figcaption_q = _factory('figcaption', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('figcaption', NO_ATTRIBUTES))
figure_q = _factory('figure', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('figure', NO_ATTRIBUTES))
hr_q = _factory('hr', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('hr', NO_ATTRIBUTES), has_closing=False)
li_q = _factory('li', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('li', NO_ATTRIBUTES))
menu_q = _factory('menu', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('menu', NO_ATTRIBUTES))
ol_q = _factory('ol', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('ol', NO_ATTRIBUTES))
p_q = _factory('p', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('p', NO_ATTRIBUTES))
pre_q = _factory('pre', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('pre', NO_ATTRIBUTES))
ul_q = _factory('ul', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('ul', NO_ATTRIBUTES))
a_q = _factory('a', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('a', NO_ATTRIBUTES))
abbr_q = _factory('abbr', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('abbr', NO_ATTRIBUTES))
b_q = _factory('b', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('b', NO_ATTRIBUTES))
bdi_q = _factory('bdi', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('bdi', NO_ATTRIBUTES))
bdo_q = _factory('bdo', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('bdo', NO_ATTRIBUTES))
br_q = _factory('br', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('br', NO_ATTRIBUTES), has_closing=False)
cite_q = _factory('cite', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('cite', NO_ATTRIBUTES))
code_q = _factory('code', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('code', NO_ATTRIBUTES))
data_q = _factory('data', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('data', NO_ATTRIBUTES))
dfn_q = _factory('dfn', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('dfn', NO_ATTRIBUTES))
em_q = _factory('em', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('em', NO_ATTRIBUTES))
i_q = _factory('i', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('i', NO_ATTRIBUTES))
kbd_q = _factory('kbd', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('kbd', NO_ATTRIBUTES))
mark_q = _factory('mark', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('mark', NO_ATTRIBUTES))
q_q = _factory('q', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('q', NO_ATTRIBUTES))
rp_q = _factory('rp', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('rp', NO_ATTRIBUTES))
rt_q = _factory('rt', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('rt', NO_ATTRIBUTES))
ruby_q = _factory('ruby', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('ruby', NO_ATTRIBUTES))
s_q = _factory('s', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('s', NO_ATTRIBUTES))
samp_q = _factory('samp', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('samp', NO_ATTRIBUTES))
small_q = _factory('small', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('small', NO_ATTRIBUTES))
span_q = _factory('span', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('span', NO_ATTRIBUTES))
strong_q = _factory('strong', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('strong', NO_ATTRIBUTES))
sub_q = _factory('sub', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('sub', NO_ATTRIBUTES))
sup_q = _factory('sup', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('sup', NO_ATTRIBUTES))
time_q = _factory('time', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('time', NO_ATTRIBUTES))
u_q = _factory('u', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('u', NO_ATTRIBUTES))
var_q = _factory('var', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('var', NO_ATTRIBUTES))
wbr_q = _factory('wbr', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('wbr', NO_ATTRIBUTES), has_closing=False)
area_q = _factory('area', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('area', NO_ATTRIBUTES), has_closing=False)
audio_q = _factory('audio', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('audio', NO_ATTRIBUTES))
img_q = _factory('img', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('img', NO_ATTRIBUTES), has_closing=False)
map_q = _factory('map', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('map', NO_ATTRIBUTES))
track_q = _factory('track', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('track', NO_ATTRIBUTES), has_closing=False)
video_q = _factory('video', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('video', NO_ATTRIBUTES))
embed_q = _factory('embed', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('embed', NO_ATTRIBUTES), has_closing=False)
iframe_q = _factory('iframe', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('iframe', NO_ATTRIBUTES))
object_q = _factory('object', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('object', NO_ATTRIBUTES))
picture_q = _factory('picture', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('picture', NO_ATTRIBUTES))
portal_q = _factory('portal', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('portal', NO_ATTRIBUTES))
source_q = _factory('source', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('source', NO_ATTRIBUTES), has_closing=False)
svg_q = _factory('svg', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('svg', NO_ATTRIBUTES))
canvas_q = _factory('canvas', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('canvas', NO_ATTRIBUTES))
noscript_q = _factory('noscript', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('noscript', NO_ATTRIBUTES))
script_q = _factory('script', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('script', NO_ATTRIBUTES))
del_q = _factory('del', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('del', NO_ATTRIBUTES))
ins_q = _factory('ins', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('ins', NO_ATTRIBUTES))
caption_q = _factory('caption', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('caption', NO_ATTRIBUTES))
col_q = _factory('col', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('col', NO_ATTRIBUTES), has_closing=False)
colgroup_q = _factory('colgroup', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('colgroup', NO_ATTRIBUTES))
table_q = _factory('table', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('table', NO_ATTRIBUTES))
tbody_q = _factory('tbody', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('tbody', NO_ATTRIBUTES))
td_q = _factory('td', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('td', NO_ATTRIBUTES))
tfoot_q = _factory('tfoot', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('tfoot', NO_ATTRIBUTES))
th_q = _factory('th', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('th', NO_ATTRIBUTES))
thead_q = _factory('thead', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('thead', NO_ATTRIBUTES))
tr_q = _factory('tr', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('tr', NO_ATTRIBUTES))
button_q = _factory('button', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('button', NO_ATTRIBUTES))
datalist_q = _factory('datalist', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('datalist', NO_ATTRIBUTES))
fieldset_q = _factory('fieldset', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('fieldset', NO_ATTRIBUTES))
form_q = _factory('form', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('form', NO_ATTRIBUTES))
input_q = _factory('input', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('input', NO_ATTRIBUTES), has_closing=False)
label_q = _factory('label', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('label', NO_ATTRIBUTES))
legend_q = _factory('legend', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('legend', NO_ATTRIBUTES))
meter_q = _factory('meter', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('meter', NO_ATTRIBUTES))
optgroup_q = _factory('optgroup', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('optgroup', NO_ATTRIBUTES))
option_q = _factory('option', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('option', NO_ATTRIBUTES))
output_q = _factory('output', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('output', NO_ATTRIBUTES))
progress_q = _factory('progress', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('progress', NO_ATTRIBUTES))
select_q = _factory('select', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('select', NO_ATTRIBUTES))
textarea_q = _factory('textarea', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('textarea', NO_ATTRIBUTES))
details_q = _factory('details', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('details', NO_ATTRIBUTES))
dialog_q = _factory('dialog', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('dialog', NO_ATTRIBUTES))
summary_q = _factory('summary', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('summary', NO_ATTRIBUTES))
slot_q = _factory('slot', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('slot', NO_ATTRIBUTES))
template_q = _factory('template', accepted_attributes=HTML5_GLOBAL_ATTRIBUTES | HTML5_ATTRIBUTES_PER_TAG.get('template', NO_ATTRIBUTES))

ALL_TAGS = ['base', 'head', 'link', 'meta', 'style', 'title', 'body', 'address', 'article', 'aside', 'footer', 'header', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hgroup', 'main', 'nav', 'section', 'search', 'blockquote', 'dd', 'div', 'dl', 'dt', 'figcaption', 'figure', 'hr', 'li', 'menu', 'ol', 'p', 'pre', 'ul', 'a', 'abbr', 'b', 'bdi', 'bdo', 'br', 'cite', 'code', 'data', 'dfn', 'em', 'i', 'kbd', 'mark', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'small', 'span', 'strong', 'sub', 'sup', 'time', 'u', 'var', 'wbr', 'area', 'audio', 'img', 'map', 'track', 'video', 'embed', 'iframe', 'object', 'picture', 'portal', 'source', 'svg', 'canvas', 'noscript', 'script', 'del', 'ins', 'caption', 'col', 'colgroup', 'table', 'tbody', 'td', 'tfoot', 'th', 'thead', 'tr', 'button', 'datalist', 'fieldset', 'form', 'input', 'label', 'legend', 'meter', 'optgroup', 'option', 'output', 'progress', 'select', 'textarea', 'details', 'dialog', 'summary', 'slot', 'template']

ALL_TAGS_MAPPING = {"base": base_q, "head": head_q, "link": link_q, "meta": meta_q, "style": style_q, "title": title_q, "body": body_q, "address": address_q, "article": article_q, "aside": aside_q, "footer": footer_q, "header": header_q, "h1": h1_q, "h2": h2_q, "h3": h3_q, "h4": h4_q, "h5": h5_q, "h6": h6_q, "hgroup": hgroup_q, "main": main_q, "nav": nav_q, "section": section_q, "search": search_q, "blockquote": blockquote_q, "dd": dd_q, "div": div_q, "dl": dl_q, "dt": dt_q, "figcaption": figcaption_q, "figure": figure_q, "hr": hr_q, "li": li_q, "menu": menu_q, "ol": ol_q, "p": p_q, "pre": pre_q, "ul": ul_q, "a": a_q, "abbr": abbr_q, "b": b_q, "bdi": bdi_q, "bdo": bdo_q, "br": br_q, "cite": cite_q, "code": code_q, "data": data_q, "dfn": dfn_q, "em": em_q, "i": i_q, "kbd": kbd_q, "mark": mark_q, "q": q_q, "rp": rp_q, "rt": rt_q, "ruby": ruby_q, "s": s_q, "samp": samp_q, "small": small_q, "span": span_q, "strong": strong_q, "sub": sub_q, "sup": sup_q, "time": time_q, "u": u_q,
                    "var": var_q,
                    "wbr": wbr_q, "area": area_q, "audio": audio_q, "img": img_q, "map": map_q, "track": track_q, "video": video_q, "embed": embed_q, "iframe": iframe_q, "object": object_q, "picture": picture_q, "portal": portal_q, "source": source_q, "svg": svg_q, "canvas": canvas_q, "noscript": noscript_q, "script": script_q, "del": del_q, "ins": ins_q, "caption": caption_q, "col": col_q, "colgroup": colgroup_q, "table": table_q, "tbody": tbody_q, "td": td_q, "tfoot": tfoot_q, "th": th_q, "thead": thead_q, "tr": tr_q, "button": button_q, "datalist": datalist_q, "fieldset": fieldset_q, "form": form_q, "input": input_q, "label": label_q, "legend": legend_q, "meter": meter_q, "optgroup": optgroup_q, "option": option_q, "output": output_q, "progress": progress_q, "select": select_q, "textarea": textarea_q, "details": details_q, "dialog": dialog_q, "summary": summary_q, "slot": slot_q, "template": template_q}


def component_q(value: str, default_cls=None):
    name = ""
    classes = []
    id_ = ""
    props = {}

    i = 0

    def _():
        nonlocal i
        s = ""
        while i < len(value) and value[i] not in ".#[],=":
            s += value[i]
            i += 1
        return s

    name = _()
    while i < len(value):
        if value[i] == ".":
            i += 1
            classes.append(_())
        elif value[i] == "#":
            i += 1
            id_ = _()
        elif value[i] == "[":
            i += 1
            while True:
                if i >= len(value):
                    raise ValueError("Missing closing bracket in component declaration")
                key = _()
                if value[i] == "=":
                    i += 1
                    if value[i] in "'\"":
                        sep = value[i]
                        i += 1

                        v = ""
                        while value[i] != sep:
                            v += value[i]
                            i += 1
                        i += 1
                    else:
                        v = _()
                    props[key] = v
                else:
                    props[key] = ''
                if value[i] == ",":
                    i += 1
                    while value[i] == " ":
                        i += 1
                elif value[i] == "]":
                    i += 1
                    break
                else:
                    raise ValueError("Invalid character in component declaration")

    if name not in ALL_TAGS_MAPPING:
        if default_cls is None:
            raise ValueError(f"Unknown tag {name}")
        return default_cls(id=id_, class_=" ".join(classes), **props)
    return ALL_TAGS_MAPPING[name](id=id_, class_=" ".join(classes), **props)