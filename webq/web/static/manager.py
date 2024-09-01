class StaticFilesManager:

    def __init__(self, app, static_folder=None, static_url_path=None):
        self.app = app
        self.static_folder = static_folder or "resources"
        self.static_url_path = static_url_path or "/resources"
