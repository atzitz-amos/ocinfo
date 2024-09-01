from webq.core.resolver.template import TemplateResolver


class AppTemplatesManager:
    def __init__(self, app):
        self.app = app
        self.templates = {}

    def template_provider(self, url, f, **options):
        def template_parser(*args, **kwargs):
            return TemplateResolver(f(*args, **kwargs)).parse(**options)

        self.templates[url] = template_parser

        return template_parser
