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
        
        # List of imported packages
        self._importedPackages = []
        
        # List of imported types
        self._importedTypes = []
        
        # List of imported modules
        self._importedModules = []
        
        # List of aliased imports
        self._aliases = {}
        
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
    def path(self):
        '''
        Module package path.
        '''
        
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
        '''
        Check if a package with the given path is imported by this modul.
        '''
        
        for package in self._importedPackages:
            if package.isBase(path):
                return True
            
        return False
    
    def _isModuleImported(self, path):
        '''
        Check if the module with the given path is imported by this module.
        '''
        
        for module in self._importedModules:
            if module.path == path:
                return True
            
        return False
    
    def _resolveType(self, typeInfo):
        # Is the reference aliased ?
        aliasName = typeInfo.path[0]
        
        if aliasName in self._aliases:
            # It's an alias
            alias = self._aliases[aliasName]
            
            if isinstance(alias.loc, Module):
                # Aliased entity is a module so the import must be:
                #    module.type
                assert(len(typeInfo.path) == 2)
                
                typeName = typeInfo.path[1]
                
                # Get the type from the module
                return alias.loc.getType( typeName )
            
            elif isinstance(alias.loc, Package):
                # Aliased entity is a package so the import must be:
                #    package.com.....module.type
                return alias.loc.resolvePath(typeInfo.path[1:])
            
            else:
                # TODO
                raise RuntimeError('Type aliases not implemented')
            
        else:
            # Try without aliases
            return self._resolvePath(typeInfo.path)
        
    def _resolvePath(self, path):
        '''
        Attempts to resolve the given path in the context of this module.
        '''
        
        # Check imported types
        typeName = path[-1]
                 
        if len(path) == 1:
            # Go trough all the imported types and try to find it
            for typeObj in self._importedTypes:
                if typeObj.name == typeName:
                    return typeObj
                
            return None
                    
        elif len(path) >= 3:
            # Package of the type we're trying to import
            typePackage = path[:-2]
             
            # Module of the type we're trying to import
            typeModule = path[-2]

            # Check if the package is imported             
            packageImported = self._isPackageImported(typePackage)
             
            # Now check if the module is imported
            modulePath = [i for i in typePackage]
             
            modulePath.append(typeModule)
             
            moduleImported = self._isModuleImported(modulePath)

            # If either of those are imported             
            if moduleImported or packageImported:
                # First resolve the package
                typePackage = self.package.env.getPackageByPath(typePackage)
                 
            else:
                # Neither are imported
                return None
   
            # Next resolve the module
            typeModule = typePackage.getModule(typeModule)
             
            if not typeModule:
                return None

            # Finally get the type from the module
            return typeModule.getType(typeName)              

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
        
        
    def _importFromModule(self, module, typeName):
        '''
        Imports a type name from a module. Type name may be a wildcard.
        '''
        
        for typeObj in module.types:
            if typeName == '*' or typeName == typeObj.name:
                self._importedTypes.append( typeObj )
        
    def _link(self):
        # Import all types from self
        self._importFromModule(self, '*')
        
        # Import all primitive types from the environment
        self._importFromModule(self.package.env._getLangModule(), '*')
        
        # Iterate over imports received from the parser
        for importInfo in self._importsInfo.imports:
            if not importInfo.source:
                # It's an import of type:
                #     import com.package.module
                # or:
                #    import com.package.module as alias
                
                # Resolve the given path
                loc = self.package.env.resolvePath(importInfo.path)
                
                if not loc:
                    # Path could not be resolved
                    raise IDLImportError(self, importInfo.line, 'Could not resolve import %r' % importInfo.pathStr)
                
                # Is it an aliased import ?
                if importInfo.alias:
                    # Create an alias
                    self._aliases[importInfo.alias] = Module.Alias(importInfo.alias, importInfo.path, loc) 
                    
                else:
                    if isinstance(loc, Package):
                        # The given path is a package
                        self._importedPackages.append( loc )
                    
                    elif isinstance(loc, Module):
                        # The given path is a module
                        self._importedModules.append( loc )
                    
                    elif isinstance(loc, Type):
                        # Type can't be imported like
                        self._importedTypes.append( loc )
                    
                    else:
                        # Sanity check (should never happen)
                        assert(0)
            else:
                # It's an import of type:
                #    from com.package.source import something
                # or:
                #     from com.package.source import something as alias
                
                # Resolve the given path
                loc = self.package.env.resolvePath(importInfo.source)
                
                if len(importInfo.path) != 1:
                    # The thing we're importing can only be a single module, package or type
                    raise IDLImportError(self, importInfo.line, 'Invalid syntax')
                
                # Name of the thing we're trying to import
                name = importInfo.path[0]
                
                # Alias ?
                alias = name if not importInfo.alias else importInfo.alias
                
                if isinstance(loc, Package):
                    # Source is a package
                    
                    # Check if the name is another package
                    package = loc.getChild(name)
                    
                    if package:
                        # It's another package
                        path = importInfo.source + importInfo.path
                        
                        self._aliases[alias] = Module.Alias(name, path, package)
                        
                        continue
                    
                    # Check if the name is a module 
                    module = loc.getModule(name)
                    
                    if module:
                        # It's a module
                        
                        self._aliases[alias] = Module.Alias(name, module.path, module)
                        
                        continue
                        
                    # It's neither
                    raise IDLImportError(self, importInfo.line, 'Could not resolve import %r' % importInfo.pathStr)
                    
                elif isinstance(loc, Module):
                    # Source is a module, so we must be importing a type
                    if importInfo.alias:
                        # TODO
                        raise RuntimeError('Type aliases not implemented')

                    # Get the type object we're trying to import                    
                    typeObj = loc.getType(name)
                    
                    if typeObj:
                        # Import it
                        self._importedTypes.append( typeObj )
                        
                    else:
                        raise IDLImportError(self, importInfo.line, 'Could not resolve import %r' % importInfo.pathStr)
                    
                else:
                    raise IDLImportError(self, importInfo.line, 'Could not resolve import %r' % importInfo.pathStr)
                    
