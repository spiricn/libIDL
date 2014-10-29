from idl.TypeGetter import TypeGetter
from idl.TypeInstance import TypeInstance
import os

from idl.IDLError import IDLError


class Module(TypeGetter):
    def __init__(self, env, name, filePath=None):
        self._env = env
        self._name = name
        self._types = []
        self._filePath = '' if not filePath else os.path.abspath(filePath)
        self._package = None
        self._importsInfo = None
        self._importedPackages = []
        self._importedTypes = []
        
    @property
    def package(self):
        '''
        The package object this module belongs to.
        '''
        
        return self._package
    
    @property
    def env(self):
        '''
        Parent environment of this module.
        '''
        
        return self._env
    
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
        typeSearch = [self.env, self.package]
        
        typeSearch += self._importedPackages
        
        baseType = None
        
        # Imported types
        
        for i in self._importedTypes:
            if i.name == typeInfo.name:
                return TypeInstance(i, typeInfo)
        
        for location in typeSearch: 
            for i in location.types:
                if i.name == typeInfo.name:
                    baseType = i
                    break
                
            if baseType:
                break
            
        if not baseType:
            # undefined reference
            return None
        
        return TypeInstance(baseType, typeInfo)
    
    def _setPackage(self, package):
        '''
        Sets the parent package (called by the compiler
        '''
        
        self._package = package
        
    def _setImportsInfo(self, importsInfo):
        self._importsInfo = importsInfo
        
    def _link(self):
        for importInfo in self._importsInfo.imports:
            if importInfo == self.package.path:
                # Cause a warning maybe ?
                continue
            
            # Is it a package ?
            package = self.env.getPackage(importInfo)
            
            if package:
                if package in self._importedPackages:
                    raise IDLError('Attempting to import package %r twice' % ('.'.join(importInfo)))
                
                self._importedPackages.append( package )
                
            else:
                # It may be a type
                typePackage = self.env.getPackage( importInfo[:-1] )
                
                if not typePackage:
                    raise IDLError('Unexisting package %r' % ('.'.join(typePackage)))
                
                # Find type in subpackage
                typeName = importInfo[-1]
                
                typeObj = typePackage.getType( typeName )
                
                if not typeObj:
                    raise IDLError('Unkown type %r' % '.'.join(importInfo))
                
                else:
                    self._importedTypes.append( typeObj )
