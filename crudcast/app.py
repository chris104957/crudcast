from views import app


class App(object):
    """
    TODO: implement Flask configuration options here
    """
    def __init__(self, config_file='config.yml'):
        self.config_file = config_file

    def run(self):
        app.run()
