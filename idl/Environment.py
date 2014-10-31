from idl.Compiler import Compiler
from idl.IDLTypeError import IDLTypeError
from idl.Module import Module
from idl.Type import Type
from idl.TypeGetter import TypeGetter
import os

from idl.IDLError import IDLError
from idl.Package import Package


class Environment(Package):
    class BuildEntry:
        '''
        Helper class used for compiling.
        '''
        
        def __init__(self, moduleName, source, filePath):
            self.moduleName = moduleName
            self.source = source
            self.filePath = filePath
            
    def __init__(self):
        Package.__init__(self, None, '')
        
        # Add primitives to the list
        for typeId in Type.primitives:
            self._addType( Type(self, typeId) )

    @property
    def packages(self):
        return self._packages
        
    @property
    def types(self):
        '''
        List of all types defined in this environment.
        '''
        
        return self._types
    
    def getModule(self, name):
        '''
        Gets a module object with the given name.
        '''
        
        for i in self._modules:
            if i.name == name:
                return i
            
        return None

    def compileSource(self, source, moduleName):
        '''
        Compiles given source code into a module with the given name.
        
        @param source: Source code
        @param moduleName: Name of the module (must be unique if provided).
        
        @return: Module object
        '''
        
        # If not module name is given, generate one
        if not moduleName:
            # Generate name
            n = 0
            
            while True:
                moduleName = 'Module%d' % n
                
                if self.getModule(moduleName):
                    n += 1
                else:
                    break
                
        # Compile source code
        modules = self._build([Environment.BuildEntry(moduleName, source, None)])
        
        return modules[0]
    
    def _build(self, entries):
        '''
        Compiles a list of build entries.
        '''
        
        # Modules created in this run
        createdModules = []
        
        for entry in entries:                        
            # Create module object
            module = Module(self, entry.moduleName, entry.filePath)
        
            # Create compiler
            entry.compiler = Compiler(module)
        
            # Compile
            entry.compiler.compile(entry.source)
            
            createdModules.append( module )
            
            # Add to list
            self._modules.append(module)

        for module in createdModules:
            module._link()

        # Link            
        for entry in entries:
            entry.compiler.link()
            
        return createdModules

    def compileFiles(self, paths):
        '''
        Compiles a list of files. File are directly translated into module names (e.g. 'my_module.idl' becomes 'my_module'
        
        @param paths: List of paths of source files.
        
        @return: List of modules created.
        '''
        
        # Build entry list
        entries = []
        
        for path in paths:
            # Try to open the file
            try:
                fileObj = open(path, 'r')
            except Exception as e:
                raise IDLError('Error opening idl file %r:\n %s' % (path, str(e)))
            
            # Get the source code
            source = fileObj.read()
            
            fileObj.close()
            
            # Get file name
            moduleName = os.path.basename(path)
            
            # Discard extension
            moduleName = os.path.splitext(moduleName)[0]
            
            # Add it to the list of build entries
            entries.append( Environment.BuildEntry(moduleName, source, path) )
            
        # Actually compile the sources
        return self._build( entries )        
        
    
    def compileFile(self, path):
        '''
        Compiles a single file. File name is translated into module name.
        
        @param path: Path to the source code.
        
        @return: Compiled module.
        '''
        
        modules = self.compileFiles([path])
        
        return modules[0]
    
