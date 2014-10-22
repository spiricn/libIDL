from idl.TypeGetter import TypeGetter
import os


class Module(TypeGetter):
    def __init__(self, env, name, filePath=None):
        self.env = env
        self.name = name
        self.types = []
        self.filePath = '' if not filePath else os.path.abspath(filePath)
