
class Context(object):

    class __Context:
        def __init__(self):
            self.args = None
            self.config = None
            self.driver = None
            self.capabilities = None

    instance = None

    def __init__(self):
        if not Context.instance:
            Context.instance = Context.__Context()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def update_args(self, args):
        self.instance.args = args

    def clear_args(self):
        self.instance.args = None

    def update_config(self, config):
        self.instance.config = config

    def clear_config(self):
        self.instance.config = None

    def update_driver(self, driver):
        self.instance.driver = driver

    def clear_driver(self,):
        self.instance.driver = None

    def update_capabilities(self, caps):
        self.instance.capabilities = caps

    def clear_capabilities(self):
        self.instance.capabilities = None


CONTEXT = Context()
