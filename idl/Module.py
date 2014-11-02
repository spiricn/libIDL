import os

from idl.IDLError import IDLError
from idl.IDLTypeError import IDLTypeError
from idl.Package import Package
from idl.Type import Type
from idl.TypeGetter import TypeGetter

from idl.Trace import Trace


class Module(TypeGetter):
    class Alias:
        def __init__(self, name, path, loc):
            self.name = name
            self.path = path
            self.loc = loc
        
    def __init__(self, name, filePath, package=None):
        TypeGetter.__init__(self)
        
        self._package = package
        self._name = name
        self._types = []
        self._filePath = '' if not filePath else os.path.abspath(filePath)
        self._importsInfo = None
        
        self._importedPackages = []
        self._importedTypes = []
        self._importedModules = []
        
        self._aliases = {}
        
    @property
    def path(self):
        packagePath = self.package.path
        
        packagePath.append( self.name )
        
        return packagePath
        
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
        
    def _isPackageImported(self, path):
        for package in self._importedPackages:
            if package.isBase(path):
                return True
            
        return False
    
    def _isModuleImported(self, path):
        for module in self._importedModules:
            if module.path == path:
                return True
            
        return False
    
    def _resolveType(self, typeInfo):
        # Is the reference aliased ?
        aliasName = typeInfo.path[0]
        if aliasName in self._aliases:
            alias = self._aliases[aliasName]
            
            if isinstance(alias.loc, Module):
                assert(len(typeInfo.path) == 2)
                
                return alias.loc.getType(typeInfo.path[1])
            
            elif isinstance(alias.loc, Package):
                return alias.loc.resolvePath(typeInfo.path[1:])
            
            else:
                assert(0)
            
        else:
            # Try without aliases
            return self._resolvePath(typeInfo.path)
        
    def _resolvePath(self, path):
        # Check imported types
        typeName = path[-1]
        
                 
        if len(path) == 1:
            # Go trough all the imported types and try to find it
            for typeObj in self._importedTypes:
                if typeObj.name == typeName:
                    return typeObj
                
            return None
                    
        elif len(path) >= 3:
            typePackage = path[:-2]
             
            typeModule = path[-2]
             
            packageImported = self._isPackageImported(typePackage)
             
            modulePath = [i for i in typePackage]
             
            modulePath.append(typeModule)
             
            moduleImported = self._isModuleImported(modulePath)
             
            if moduleImported or packageImported:
                typePackage = self.package.env.getPackageByPath(typePackage)
                 
            else:
                return None
   
            typeModule = typePackage.getModule(typeModule)
             
            if not typeModule:
                return None
              
            typeObj = typeModule.getType(typeName)
              
            return typeObj
                
                    
        return None
    
    def isBase(self, path):
        if len(path) < len(self.path):
            return False
        
        else:
            return path[:len(self.path)] == self.path
    
    def _setPackage(self, package):
        '''
        Sets the parent package (called by the compiler
        '''
        
        self._package = package
        
    def _setImportsInfo(self, importsInfo):
        self._importsInfo = importsInfo
        
    def _addType(self, typeObj):
        '''
        Adds a new type to the list of types.
        '''
         
        if self.getType(typeObj.name):
            raise IDLTypeError(typeObj.module, 0, "Type named %r already exists" % typeObj.name)
         
        self._types.append( typeObj )
        
        
    def _importFromModule(self, module, typeName):
        for typeObj in module.types:
            if typeName == '*' or typeName == typeObj.name:
                self._importedTypes.append( typeObj )
        
    def _link(self):
        self._importFromModule(self, '*')
        self._importFromModule(self.package.env._getLangModule(), '*')
        
        for importInfo in self._importsInfo.imports:
            if not importInfo.source:
                loc = self.package.env.resolvePath(importInfo.path)
                
                if not loc:
                    raise IDLError('Could not resolve import %r' % importInfo.pathStr)
                
                if importInfo.alias:
                    self._aliases[importInfo.alias] = Module.Alias(importInfo.alias, importInfo.path, loc) 
                    
                else:
                    if isinstance(loc, Package):
                        self._importedPackages.append( loc )
                    
                    elif isinstance(loc, Module):
                        self._importedModules.append( loc )
                    
                    elif isinstance(loc, Type):
                        raise RuntimeError('%r is not a package' % importInfo.pathStr)  
                    
                    else:
                        # Sanity check
                        assert(0)
            else:
                loc = self.package.env.resolvePath(importInfo.source)
                
                if len(importInfo.path) != 1:
                    raise RuntimeError('Invalid syntax')
                
                name = importInfo.path[0]
                
                alias = name if not importInfo.alias else importInfo.alias
                
                if isinstance(loc, Package):
                    package = loc.getChild(name)
                    
                    if package:
                        # it's another package
                        path = importInfo.source + importInfo.path
                        
                        self._aliases[alias] = Module.Alias(name, path, package)
                        
                        continue
                    
                    # Is it a module ?    
                    module = loc.getModule(name)
                    
                    if module:
                        self._aliases[alias] = Module.Alias(name, module.path, module)
                        
                        continue
                        
                    # Unresolved
                    raise RuntimeError('Unresolved import %r' % importInfo.pathStr)
                    
                elif isinstance(loc, Module):
                    if importInfo.alias:
                        raise RuntimeError('Type aliases not supported')
                    
                    typeObj = loc.getType(name)
                    
                    if typeObj:
                        self._importedTypes.append( typeObj )
                        
                    else:
                        raise RuntimeError('Unresolved import')
                    
                else:
                    raise RuntimeError('Unresolved import')
                    
