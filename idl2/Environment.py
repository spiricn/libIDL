from idl.Module import Module
from idl.Type import Type
from idl.TypeGetter import TypeGetter

from idl2.Compiler import Compiler


class Environment(TypeGetter):
    def __init__(self):
        self.types = []
        
        # Add primitives to the list
        for typeId in Type.primitives:
            self.types.append( Type(self, typeId) )
            
        self.modules = []
            
    def _addType(self, typeObj):
        self.types.append( typeObj )
        
    def getModule(self, name):
        for i in self.modules:
            if i.name == name:
                return i
            
        return None

    def compileSource(self, source, moduleName=None):
        if not moduleName:
            # Generate name
            n = 0
            
            while True:
                moduleName = 'Module%d' % n
                
                if self.getModule(moduleName):
                    n += 1
                else:
                    break
                
        # Duplicate name check
        if self.getModule(moduleName):
            raise RuntimeError('Module named %r already exists in environment' % moduleName)
                        
        # Create module object
        module = Module(self, moduleName)
        
        # Add to list
        self.modules.append(module)
        
        # Create compiler
        compiler = Compiler(module)
        
        # Compile
        compiler.compile(source)
        
        # Link
        compiler.link()
        
        return module
