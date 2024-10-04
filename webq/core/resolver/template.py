class TemplateResolver:
    def __init__(self, app, template):
        self.app = app
        self.template = template

    def parse(self, **options):
        """ Convert template to HTML """

        self.tree = self.template.prepare(app=self.app, **options)
        return self.tree
