import collections

import flask
import werkzeug

from webq.core.resolver.endpoint import EndpointResolver
from webq.core.templates.manager import AppTemplatesManager
from webq.web.endpoint import Endpoint
from webq.web.static.manager import StaticFilesManager


class App:
    """ Wrapper around flask.Flask """

    def __init__(self,
                 import_name,
                 *,
                 use_static_files=True,
                 static_folder=None,
                 static_url_path=None):

        self._flask = flask.Flask(import_name)
        self._flask.url_map.add(werkzeug.routing.Rule("/<path:path>", endpoint="_url_wrapper"))
        self._flask.view_functions["_webq__url_wrapper"] = self._url_wrapper

        self._templates = AppTemplatesManager(self)
        self._routes = collections.defaultdict(list)

        if use_static_files:
            self.static_files = StaticFilesManager(self, static_folder, static_url_path)
        else:
            self.static_files = None


    """ Routing """

    def route(self, url, **kw):
        def decorator(f):
            self._build_route(url, f, **kw)
            return f

        return decorator

    def template(self, url: str, **kw):
        def decorator(f):
            self._build_route(url, self._templates.template_provider(url, f, **kw), **kw)
            return f

        return decorator

    def component(self, name: str, **kw):
        def decorator(f):
            self._templates.register_component(name, f, kw)
            return f

        return decorator

    """ Internal """

    def _build_route(self, url, endpoint, **kw):
        methods = kw.pop("methods", ["GET"])
        for method in methods:
            self._routes[url].append(Endpoint(url, endpoint, method=method, **kw))  # type: ignore

    def _url_wrapper(self, path):
        kw = {
            "method": flask.request.method,
            "path": path,
            "query": flask.request.args,
            "form": flask.request.form,
            "files": flask.request.files,
            "json": flask.request.json,
            "cookies": flask.request.cookies,
            "headers": flask.request.headers,
            "data": flask.request.data,
            "session": flask.session,
        }
        for endpoint in self._routes.get(path, []):
            if endpoint.method == flask.request.method:
                return EndpointResolver(self, endpoint, **kw).to_response()
        return flask.abort(404)
