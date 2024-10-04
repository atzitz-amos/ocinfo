from webq.core.resolver.template import TemplateResolver


class AppTemplatesManager:
    def __init__(self, app):
        self.app = app
        self.templates = {}
        self.custom_components = {}

    def template_provider(self, url, f, **options):
        def template_parser(*args, **kwargs):
            return TemplateResolver(self.app, f(*args, **kwargs)).parse(**options)

        self.templates[url] = template_parser

        return template_parser

    def register_component(self, name, f, kw):
        self.custom_components[name] = f
