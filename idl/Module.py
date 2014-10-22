from idl.TypeGetter import TypeGetter


class Module(TypeGetter):
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.types = []
