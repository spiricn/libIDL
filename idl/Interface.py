from idl.Method import Method
from idl.Type import Type

from idl.IDLSyntaxError import IDLSyntaxError


class Interface(Type):
    def __init__(self, module, info):
        Type.__init__(self, module, Type.INTERFACE, info.name)

        self._info = info
        
        self._methods = []
        
        for methodInfo in info.methods:
            newMethod = Method(self, methodInfo)
            
            # Duplicate method check
            for method in self._methods:
                if method.name == newMethod.name:
                    raise IDLSyntaxError(self.module, methodInfo.line, 'Method named %r already exists in interface %r' % (method.name, self.name))
                
            self._methods.append(newMethod)
            
    @property
    def methods(self):
        '''
        List of methods defined in this interface.
        '''
        
        return self._methods
        
    def _link(self):
        for method in self._methods:
            method._link()
