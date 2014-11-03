from idl.Method import Method
from idl.Type import Type

from idl.IDLSyntaxError import IDLSyntaxError


class Interface(Type):
    def __init__(self, module, info):
        Type.__init__(self, module, Type.INTERFACE, info.name)

        self._info = info

        self._methods = []
        
        # Iterate over all method informations received from the parser
        for methodInfo in info.methods:
            # Create a method
            newMethod = Method(self, methodInfo)
            
            # Duplicate method check
            for method in self._methods:
                if method.name == newMethod.name:
                    raise IDLSyntaxError(self.module, methodInfo.line, 'Method named %r already exists in interface %r' % (method.name, self.name))
                
            # Add it to the list
            self._methods.append(newMethod)
            
            
    @property
    def dependencies(self):
        res = []
        
        for method in self._methods:
            # Return type
            
            if method.ret.type not in res:
                res.append( method.ret.type )
            
            # Arguments
            for arg in method.args:
                if arg.type not in res:
                    res.append( arg.type )

        return res
            
    @property
    def methods(self):
        '''
        List of methods defined in this interface.
        '''
        
        return self._methods
        
    def _link(self):
        '''
        Link all method return types/arguments.
        '''
        
        for method in self._methods:
            method._link()
