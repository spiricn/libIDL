import fnmatch
from os import path
import os
import pickle

import idl
from idl.Compiler import Compiler
from idl.IDLError import IDLError
from idl.LangConfig import LangConfig
from idl.Module import Module
from idl.Package import Package
from idl.Type import Type
from idl.linter.Linter import Linter


class Environment(Package):
    _defaultConfig = LangConfig()
    
    VERSION_KEY = '__version__'
    
    class _BuildEntry:
        '''
        Private helper class used for compiling.
        '''
        
        def __init__(self, moduleName, source, filePath):
            self.moduleName = moduleName
            self.source = source
            self.filePath = filePath
            
    def __init__(self, config=None):
        Package.__init__(self, self, None, '')
        
        self._createLangPackage()
        
        if not config:
            self._config = Environment._defaultConfig
            
        else:
            self._config = config
            
        self._defines = []
        
        self._fileCompileCallback = None
        
        self._fileScanCallback = None
        
    def save(self, path):
        '''
        Saves a compiled environment to a file. Can be loaded later using Environment.load method.
        
        @param path: Destination file path.
        '''
        
        fileObj = open(path, 'wb')
        
        # Structure should NEVER change between library versions
        fileHeader = {Environment.VERSION_KEY : idl.__version__}
        
        # Write header
        pickle.dump(fileHeader, fileObj)
        
        # Write object
        pickle.dump(self, fileObj)
            
        fileObj.close()
            
    @staticmethod
    def load(path):
        '''
        Loads an environment object from a file saved via Environment.save method.
        May throw RuntimeError if attempted to load a file saved with a different version of library.
        
        @param path: Source file path.
        @return Environment object.
        '''
        
        fileObj = open(path, 'rb')
        
        # Check version
        fileHeader = pickle.load(fileObj)
        
        if Environment.VERSION_KEY not in fileHeader or fileHeader[Environment.VERSION_KEY] != idl.__version__:
            raise RuntimeError('Invalid precompiled file')
        
        res = pickle.load(fileObj)
            
        fileObj.close()
        
        return res

    def define(self, name):
        '''
        Ads a preprocessor definition.
        
        @param name: Definition name.
        '''
        
        self._defines.append(name)
        
    def isDefined(self, name):
        '''
        Checks whether a preprocessor definition with given name exists.
        
        @param name: Definition name.
        
        @return: True if definition, exists False otherwise.
        '''
        
        return name in self._defines
        
    @staticmethod
    def setDefaultConfig(config):
        '''
        Sets default environment configuration used by every other Environment instantiated.
        
        @param config: Object of type idl.LangConfig 
        '''
        
        Environment._defaultConfig = config
        
    @property
    def config(self):
        '''
        Environment configuration.
        '''
        
        return self._config
                
    def compileTree(self, treePath, filterExpr='*.idl', enforcePackageConvention=True, fileCompileCallback=None, fileScanCallback=None):
        '''
        Walks a directory recursively and compiles all encountered IDL files.
        
        @param root: Root directory
        @param filterExpr: Idl file name filter
        @param fileCompileCallback: Called before compiling a scanned file, may be None
        @param fileScanCallback: Called when a file is scanned; if False is return by the called function file is discarded
        '''
        
        idlFiles = []
        
        _fileScanCallback = fileScanCallback
        
        for root, dirs, files in os.walk(treePath):
            for fileName in fnmatch.filter(files, filterExpr):
                fullPath = os.path.join(root, fileName)
                
                if _fileScanCallback and not _fileScanCallback(fullPath):
                    continue
                
                idlFiles.append(fullPath)
                
        if enforcePackageConvention:
            for path in idlFiles:
                if not Linter.verifyModulePackage(treePath, path):
                    raise IDLError('Lint', 'Package declaration-path mismatch in module %r' % path)
        
        modules = self.compileFiles(idlFiles, fileCompileCallback)
            
        self._fileScanCallback = None
        
        return modules 
            
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
        modules = self._build([Environment._BuildEntry(moduleName, source, None)])
        
        return modules[0]
    
    def compileFiles(self, paths, fileCompileCallback=None):
        '''
        Compiles a list of files. File are directly translated into module names (e.g. 'my_module.idl' becomes 'my_module'
        
        @param paths: List of paths of source files.
        @param fileCompileCallback: Called before compiling a scanned file, may be None
        
        @return: List of modules created.
        '''
        
        # Build entry list
        entries = []
        
        self._fileCompileCallback = fileCompileCallback
        
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
            entries.append( Environment._BuildEntry(moduleName, source, path) )
            
        # Actually compile the sources
        result = self._build( entries )
        
        self._fileCompileCallback = None
        
        return result        
        
    def compileFile(self, path):
        '''
        Compiles a single file. File name is translated into module name.
        
        @param path: Path to the source code.
        
        @return: Compiled module.
        '''
        
        modules = self.compileFiles([path])
        
        return modules[0]

    def _createLangPackage(self):
        '''
        Creates a package containing all primitive types.
        '''
        
        # Create primitives package
        langPackage = self._createChildTree(['idl'])
        
        langModule = Module('Lang', None, langPackage)
        
        for typeId in Type.primitives:
            langModule._addType( Type(langModule, typeId) )
            
        langPackage._addModule(langModule)
        
        self._langPackage = langPackage
         
    def _getLangPackage(self):
        '''
        Default language package.
        '''
        return self._langPackage

    def _build(self, entries):
        '''
        Compiles a list of build entries.
        '''
        
        # Modules created in this run
        createdModules = []
        
        for entry in entries:                        
            if self._fileCompileCallback:
                self._fileCompileCallback(entry.filePath)

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