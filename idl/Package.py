from idl.IDLError import IDLError
from idl.TypeGetter import TypeGetter


class Package():
    def __init__(self, env, parent, name):
        TypeGetter.__init__(self)
        
        self._env = env
        self._parent = parent
        self._modules = []
        self._name = name
        self._children = []
        
    
    @property
    def children(self):
        '''
        List of all children (infinite depth) of this package.
        '''
        
        packages = [self]
        
        res = []
        
        while packages:
            package = packages.pop(0)
            
            res.append(package)
            
            packages += package._children
        
        return res
        
    @property
    def types(self):
        '''
        List of types exposed by modules contained in this package.
        '''
        
        res = []
        
        for module in self._modules:
            res += module.types
            
        return res
    
    @property
    def env(self):
        '''
        Parent environment of this package.
        '''
        
        return self._env
    
    @property
    def modules(self):
        '''
        List of modules contained in this package.
        '''
        
        return self._modules
    
    @property
    def dependencies(self):
        '''
        List of type dependencies this package is dependant on.
        '''
        
        res = []
        
        todo = [self]
        
        while todo:
            package = todo.pop(0)
            
            print('proc %r' % package.name)
            
            for module in package.modules:
                for i in module.dependencies:
                    if i not in res:
                        res.append(i)
                        
            todo += package._children
            
        return res

    @property
    def name(self):
        '''
        Name of this package.
        '''
        
        return self._name
    
    @property
    def path(self):
        '''
        Path of this package.
        '''
        
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
        '''
        Parent package.
        '''
        
        return self._parent
    
    @property
    def packageStr(self):
        '''
        Package string (e.g. com.example.packge)
        '''
        
        return '.'.join( self.path )
    
    def getChild(self, arg):
        '''
        Gets a child package by name or path.
        '''
        
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
        '''
        Gets a child packge by path
        '''
        
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
        '''
        Gets a child package by name.
        '''
        
        for child in self._children:
            if child.name == name:
                return child
            
        return None
    
    def resolvePath(self, path):
        '''
        Resolves an entity path in the context of this package.
        '''
        
        # Package
        package = self.getPackageByPath(path)
        
        if package:
            return package
        
        # Type
        typeObj = self.getTypeByPath(path)
        
        if typeObj:
            return typeObj
        
        # It's neither
        return None
        
    def getTypeByPath(self, path):
        '''
        Gets a chlid type by path.
        '''
      
        if len(path) == 1:
            # At least two path components necessary (i.e. module.type)
            return None
        
        package = self.getPackageByPath(path[:-1])
        
        if not package:
            return None
        else:
            for typeObj in package.types:
                if typeObj.name == path[-1]:
                    return typeObj
                
        return None
        
    def getPackageByPath(self, path):
        '''
        Gets a child package by path.
        '''
        
        return self.getChildByPath(path)
    
    def _createChildTree(self, path):
        '''
        Creates a child tree structure. If a child already exists it simply returns a reference to it.
        '''
        
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
    
    def _addModule(self, module):
        '''
        Adds a new module to the list of modules.
        '''
        
        # Duplicate name check
        for i in self._modules:
            if i.name == module.name:
                raise IDLError('Module named %r already exists in package %r' % (module.name, self.packageStr))
            
        module._setPackage(self)
        
        self._modules.append( module )
        
    def _createChildPackage(self, name):
        '''
        Creates a child package with a given name.
        '''
        
        package = Package(self.env, self, name) 
        
        if self.getChild(name):
            raise RuntimeError('Package with name %r already exists' % name)
        
        self._children.append( package )
        
        return package
