import os

from idl.Module import Module
from idl.Type import Type
from idl.TypeGetter import TypeGetter

from idl.Compiler import Compiler


class Environment(TypeGetter):
    class BuildEntry:
        def __init__(self, moduleName, source, filePath):
            self.moduleName = moduleName
            self.source = source
            self.filePath = filePath
            
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
                
        modules = self._build([Environment.BuildEntry(moduleName, source, None)])
        
        return modules[0]
                
    def _build(self, entries):
        createdModules = []
        
        for entry in entries:
            # Duplicate name check
            if self.getModule(entry.moduleName):
                raise RuntimeError('Module named %r already exists in environment' % entry.moduleName)
                        
            # Create module object
            module = Module(self, entry.moduleName, entry.filePath)
        
            # Add to list
            self.modules.append(module)
        
            # Create compiler
            entry.compiler = Compiler(module)
        
            # Compile
            entry.compiler.compile(entry.source)
            
            createdModules.append( module )

        # Link            
        for entry in entries:
            entry.compiler.link()
            
        return createdModules

    def compileFiles(self, paths):
        entries = []
        
        for path in paths:
            try:
                fileObj = open(path, 'r')
            except Exception as e:
                raise RuntimeError('Error opening idl file %r:\n %s' % (path, str(e)))
            
            source = fileObj.read()
            
            fileObj.close()
            
            # Get file name
            moduleName = os.path.basename(path)
            
            # Discard extension
            moduleName = os.path.splitext(moduleName)[0]
            
            entries.append( Environment.BuildEntry(moduleName, source, path) )
            
            
        return self._build( entries )        
        
    
    def compileFile(self, path):
        modules = self.compileFiles([path])
        
        return modules[0]
    