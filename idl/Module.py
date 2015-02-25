import os

from idl.IDLTypeError import IDLTypeError
from idl.Package import Package
from idl.Type import Type
from idl.TypeGetter import TypeGetter

from idl.IDLImportError import IDLImportError


class Module(TypeGetter):
    class Alias:
        def __init__(self, name, path, loc):
            self.name = name
            self.path = path
            self.loc = loc
        
    def __init__(self, name, filePath, package=None):
        TypeGetter.__init__(self)
        
        # Parent package
        self._package = package
        
        # Module name (unique in package)
        self._name = name
        
        # List of types defined in this module
        self._types = []
        
        # Module source file path
        self._filePath = '' if not filePath else os.path.abspath(filePath)
        
        # Imports information (recieved from the parser
        self._importsInfo = None
        
        # List of imported types
        self._importedTypes = []
        
    @property
    def dependencies(self):
        '''
        Compiles a list of all the types this module is dependent on
        '''
        
        res = []
        
        for typeObj in self._types:
            for i in typeObj.dependencies:
                if i not in res:
                    res.append(i)
                    
        return res
    
    @property
    def package(self):
        '''
        The package object this module belongs to.
        '''
        
        return self._package
    
    @property
    def name(self):
        '''
        Module name.
        '''
        
        return self._name
    
    @property
    def types(self):
        '''
        Types defined by this module.
        '''
        
        return self._types
    
    @property
    def filePath(self):
        '''
        File path of this module (may be None).
        '''
        
        return self._filePath
    
    def _setPath(self, path):
        '''
        Set the package path (called by the compiler)
        '''
        
        self._path = path
        
    def _resolveType(self, typeInfo):
        '''
        Attempts to resolve the given path in the context of this module.
        '''
        path = typeInfo.path
        
        typeName = path[-1]
        
        # Check imported types
        if len(path) == 1:
            # Go trough all the imported types and try to find a type with this name
            for typeObj in self._importedTypes:
                if typeObj.name == typeName:
                    return typeObj
                
            return None
                    
        else:
            # Package of the type we're trying to import
            typePackagePath = path[:-1]
            
            # Resolve package 
            package = self.package.env.getPackageByPath(typePackagePath)
            
            if not package:
                return None
            
            # Check all types in package
            for typeObj in package.types:
                if typeName == typeObj.name:
                    return typeObj
                
        return None
    
    def _setPackage(self, package):
        '''
        Sets the parent package (called by the compiler
        '''
        
        self._package = package
        
    def _setImportsInfo(self, importsInfo):
        '''
        Sets the import information received from the parser, by the compiler.
        '''
        
        self._importsInfo = importsInfo
        
    def _addType(self, typeObj):
        '''
        Adds a new type to the list of types.
        '''
         
        if self.getType(typeObj.name):
            raise IDLTypeError(typeObj.module, 0, "Type named %r already exists" % typeObj.name)
         
        self._types.append( typeObj )
        
    def _import(self, obj):
        if isinstance(obj, Type):
            if obj not in self._importedTypes:
                self._importedTypes.append(obj)
                
        elif isinstance(obj, Package):
            for typeObj in obj.types:
                self._import(typeObj)
        
        else:
            # Sanity check
            assert(0)
            
    def _link(self):
        # Import types from this package
        self._import(self.package)
            
        # Import built-in types from lang module
        self._import(self.package.env._getLangPackage())

        for importInfo in self._importsInfo.imports:
            path = importInfo.path
            
            # Does it resolve to a type ?
            obj = self.package.env.resolvePath(path)
            
            if not obj:
                raise IDLImportError(self, importInfo.line, 'Could not resolve import %r' % importInfo.pathStr)
                 
            self._import(obj)
