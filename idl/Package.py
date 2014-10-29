from idl.IDLTypeError import IDLTypeError
from idl.TypeGetter import TypeGetter

from idl.IDLError import IDLError


class Package(TypeGetter):
    def __init__(self, path):
        TypeGetter.__init__(self)
        
        self._modules = []
        self._path = path
        self._types = []
        
    @property
    def types(self):
        return self._types
    
    @property
    def module(self):
        return self._modules

    @property
    def path(self):
        return self._path
    
    @property
    def packageStr(self):
        return '.'.join( self.path )
    
    def _addModule(self, module):
        # Duplicate name check
        for i in self._modules:
            if i.name == module.name:
                raise IDLError('Module named %r already exists in package %r' % (module.name, self.packageStr))
            
        module._setPackage(self)
        
        self._modules.append( module )
        
    def _addType(self, typeObj):
        '''
        Adds a new type to the list of types.
        '''
         
        if self.getType(typeObj.name):
            raise IDLTypeError(typeObj.module, 0, "Type named %r already exists" % typeObj.name)
         
        self._types.append( typeObj )

