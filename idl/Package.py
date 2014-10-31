from idl.IDLTypeError import IDLTypeError
from idl.TypeGetter import TypeGetter

from idl.IDLError import IDLError


class Package(TypeGetter):
    def __init__(self, parent, name):
        TypeGetter.__init__(self)
        
        self._parent = parent
        self._modules = []
        self._types = []
        self._name = name
        self._children = []
        
    def _createChildPackage(self, name):
        package = Package(self, name) 
        
        if self.getChild(name):
            raise RuntimeError('Package with name %r already exists' % name)
        
        self._children.append( package )
        
        return package
        
    @property
    def types(self):
        return self._types
    
    @property
    def module(self):
        return self._modules

    @property
    def name(self):
        return self._name
    
    @property
    def path(self):
        path = []
        
        package = self
        
        while package:
            if package.parent:
                path.append(package.name)
            
            package = package.parent
            
        path.reverse()
        
        return path
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def packageStr(self):
        return '.'.join( self.path )
    
    def _addModule(self, module):
        # Duplicate name check
        for i in self._modules:
            if i.name == module.name:
                raise IDLError('Module named %r already exists in package %r' % (module.name, self.packageStr))
            
        module._setPackage(self)
        
        self._modules.append( module )
        
    def _addType(self, typeObj):
        '''
        Adds a new type to the list of types.
        '''
         
        if self.getType(typeObj.name):
            raise IDLTypeError(typeObj.module, 0, "Type named %r already exists" % typeObj.name)
         
        self._types.append( typeObj )
        
    def getChild(self, arg):
        if isinstance(arg, str):
            return self._getChildByName(arg)
        
        elif isinstance(arg, list):
            return self._getChildByPath(arg)
        
        else:
            raise RuntimeError('Invalid child search parameter %s' % str(arg))

    def _getChildByPath(self, path):
        # Copy list
        path = [i for i in path]
        
        package = self
        
        while path:
            name = path.pop(0)
            
            package = package.getChild(name)
            
            if not package:
                return None
            
        return package
    
    def _getChildByName(self, name):
        for child in self._children:
            if child.name == name:
                return child
            
        return None
    
    def _createChildTree(self, path):
        # Copy list
        path = [i for i in path]
        
        package = self
        
        while path:
            name = path.pop(0)
            
            newPackage = package.getChild(name)
            
            if not newPackage:
                newPackage = package._createChildPackage(name)
        
            package = newPackage
            
        return package

