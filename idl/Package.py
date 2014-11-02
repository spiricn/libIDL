from idl.TypeGetter import TypeGetter

from idl.IDLError import IDLError


class Package():
    def __init__(self, env, parent, name):
        TypeGetter.__init__(self)
        
        self._env = env
        self._parent = parent
        self._modules = []
        self._name = name
        self._children = []
        
    @property
    def env(self):
        return self._env
    
    def _createChildPackage(self, name):
        package = Package(self.env, self, name) 
        
        if self.getChild(name):
            raise RuntimeError('Package with name %r already exists' % name)
        
        self._children.append( package )
        
        return package
    
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
    
    def getModule(self, name):
        '''
        Gets a module object with the given name.
        '''
        
        for i in self._modules:
            if i.name == name:
                return i
            
        return None
    
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
        
    def getChild(self, arg):
        if isinstance(arg, str):
            return self.getChildByName(arg)
        
        elif isinstance(arg, list):
            return self.getChildByPath(arg)
        
        else:
            raise RuntimeError('Invalid child search parameter %s' % str(arg))

    def isBase(self, path):
        '''
        Checks if given path is in base of this package.
        
        e.g. for package 'com.test.package', 'com.test' is in base
        '''
        
        if len(path) < len(self.path):
            return False
        
        else:
            return path[:len(self.path)] == self.path
        
    def getChildByPath(self, path):
        # Copy list
        path = [i for i in path]
        
        package = self
        
        while path:
            name = path.pop(0)
            
            package = package.getChild(name)
            
            if not package:
                return None
            
        return package
    
    def getChildByName(self, name):
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
    
    def resolvePath(self, path):
        # Package
        package = self.getPackageByPath(path)
        
        if package:
            return package
            
        # Module
        module = self.getModuleByPath(path)
        
        if module:
            return module
        
        # Type
        typeObj = self.getTypeByPath(path)
        
        if typeObj:
            return typeObj
        
        # It's neither
        return None
        
    def getModuleByPath(self, path):
        moduleName = path[-1]
        
        if len(path) == 1:
            package = self
            
        else:
            packagePath = path[:-1]
            
            package = self.getChildByPath(packagePath)
            
        if not package:
            return None
        else:
            return package.getModule(moduleName)
        
    def getTypeByPath(self, path):
        if len(path) == 1:
            # At least two path components necessary (i.e. module.type)
            return None
        
        module = self.getModuleByPath(path[:-1])
        
        if not module:
            return None
        else:
            return module.getType(path[-1])
        
    def getPackageByPath(self, path):
        return self.getChildByPath(path)

