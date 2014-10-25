from idl.Module import Module
from idl.Type import Type

from idl2.Compiler import Compiler


class Environment:
    def __init__(self):
        self.types = []
        
        # Add primitives to the list
        for typeId in Type.primitives:
            self.types.append( Type(self, typeId) )
            
        self.modules = []
            
    def resolveType(self, name):
        for i in self.types:
            if i.name == name:
                return i

        return None
    
    def _addType(self, typeObj):
        self.types.append( typeObj )

    def compileModule(self, name, source):
        module = Module(self, name)
        
        # Duplicate name check
        for module in self.modules:
            if module.name == name:
                raise RuntimeError('Module named %r already exists in environment' % module.name)
            
        self.modules.append(module)
        
        compiler = Compiler(module)
        
        compiler.compile(source)
        
        compiler.link()
        
        return module