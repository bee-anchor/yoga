
class Context(object):

    class __Context:
        def __init__(self):
            self.args = None
            self.config = None
            self.driver = None

    instance = None

    def __init__(self):
        if not Context.instance:
            Context.instance = Context.__Context()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def update_args(self, args):
        self.instance.args = args

    def update_config(self, config):
        self.instance.config = config

    def update_driver(self, driver):
        self.instance.driver = driver

    def clear_context(self):
        self.instance.args = None
        self.instance.config = None
        self.instance.driver = None


CONTEXT = Context()
