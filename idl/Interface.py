from idl.IDLSyntaxError import IDLSyntaxError
from idl.Method import Method
from idl.Type import Type


class Interface(Type):
    def __init__(self, module, info):
        Type.__init__(self, module, Type.INTERFACE, info.name)

        self._info = info

        self._methods = []
        
        # Iterate over all method informations received from the parser
        for methodInfo in info.methods:
            # Add it to the list
            self._methods.append( Method(self, methodInfo) )

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
