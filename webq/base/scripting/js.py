"""
Provides the hyper-overloaded js() function.

Usage:

1) js(filename='file.js') - Include a js file
2) js(filenames=['file.js', 'file2.js']) - Include multiple js files
3) js('console.log("Hello, World!")') - Include raw js
4) js(onclick='console.log("Hello, World!")') - Provide event handlers
5) js(jsactions.reload_page()) - Include a predefined js action
6) js(jsactions.reload_page(), jsactions.edit_css()) - Include multiple predefined js actions
"""
from webq.base.scripting import jsactions


class JavaScript:
    def __init__(self):
        pass


class FileJS(JavaScript):
    def __init__(self, filenames):
        super().__init__()

        self.filenames = filenames


class RawJS(JavaScript):
    def __init__(self, raw_js):
        super().__init__()

        self.raw_js = raw_js


class EventJS(JavaScript):
    def __init__(self, events):
        super().__init__()

        self.events = events


class ActionJS(JavaScript):
    def __init__(self, actions):
        super().__init__()

        self.actions = actions


def js(*args, filename=None, filenames=None, **options):
    if filename:
        return FileJS([filename])
    elif filenames:
        return FileJS(filenames)
    elif args:
        if isinstance(args[0], str):
            return RawJS(args[0])
        elif isinstance(args[0], jsactions.JSAction):
            return ActionJS(args)
    elif options:
        return EventJS(options)
    raise ValueError("Invalid arguments for `js` function")
