from idl.Type import Type

from idl.Method import Method


class Interface(Type):
    def __init__(self, module, info):
        Type.__init__(self, module, Type.INTERFACE, info.name)

        self.info = info
        
        self.methods = []
        
        for methodInfo in info.methods:
            newMethod = Method(self, methodInfo)
            
            # Duplicate method check
            for method in self.methods:
                if method.name == newMethod.name:
                    raise RuntimeError('Method named %r already exists in interface %r' % (method.name, self.name))
                
            self.methods.append(newMethod)
        
    def _link(self):
        for method in self.methods:
            method._link()
