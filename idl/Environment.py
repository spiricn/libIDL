import fnmatch
import os

from idl.Compiler import Compiler
from idl.IDLError import IDLError
from idl.Module import Module
from idl.Package import Package
from idl.Type import Type


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
        Package.__init__(self, self, None, '')
        
        self._createLangPackage()
            
    def _createLangPackage(self):
        '''
        Creates a package containing all primitive types.
        '''
        
        # Create primitives package
        langPackage = self._createChildTree(['idl'])
        
        langModule = Module('Lang', None, langPackage)
        
        for typeId in Type.primitives:
            langModule._addType( Type(self, typeId) )
            
        langPackage._addModule(langModule)
        
        self._langPackage = langPackage
         
    def _getLangPackage(self):
        return self._langPackage
    
    def compileTree(self, root, filterExpr='*.idl'):
        '''
        Walks a directory recursively and compiles all encountered IDL files.
        
        @param root: Root directory
        @param filterExpr: Idl file name filter
        '''
        
        idlFiles = []
        
        for root, dirs, files in os.walk(root):
            for fileName in fnmatch.filter(files, filterExpr):
                idlFiles.append(fileName)
                
        return self.compileFiles(idlFiles)
            
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
            module = Module(entry.moduleName, entry.filePath)
        
            # Create compiler
            entry.compiler = Compiler(self, module)
        
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
    
