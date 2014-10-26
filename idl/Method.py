from idl.Annotatable import Annotatable
from idl.Type import Type

from idl.IDLSyntaxError import IDLSyntaxError


class Method(Annotatable):
    class Argument:
        def __init__(self, method, argType, name):
            self._method = method
            self._type = argType
            self._name = name
            
        @property
        def method(self):
            '''
            Method this argument is associated with.
            '''
            
            return self._method
        
        @property
        def type(self):
            '''
            Argument type.
            '''
            
            return self._type
        
        @property
        def name(self):
            '''
            Argument name.
            '''
            
            return self._name
            
    # Method type enumeration
    NORMAL, \
    CALLBACK_REGISTER, \
    CALLBACK_UNREGISTER, \
    = range(3)
    
    def __init__(self, interface, info):
        Annotatable.__init__(self)
        
        self._interface = interface
        
        self._info = info
        
        self._type = Method.NORMAL
        
        self._name = info.name
        
        self._args = []
        
        self._callbackType = None
        
    @property
    def interface(self):
        '''
        Interface this method is associated with.
        '''
        
        return self._interface
    
    @property
    def type(self):
        '''
        Type of method.
        '''
        
        return self._type
    
    @property
    def name(self):
        '''
        Method name.
        '''
        
        return self._name
    
    @property
    def args(self):
        '''
        List of method arguments.
        '''
        
        return self._args
        
    @property
    def callbackType(self):
        '''
        Callback type (may be None).
        '''
        
        return self._callbackType
    
    def _link(self):
        # Resolve return type
        try:
            self.returnType = self._interface.module._resolveType(self._info.returnTypeInfo)
        except IDLSyntaxError as e:
            # Re-raise exception with module/line information
            raise IDLSyntaxError(self._interface.module, self._info.line, e.message)
        
        if not self.returnType:
            raise RuntimeError('Could not resolve return type %r of method %s::%s' % (self._info.returnTypeInfo.name, self._interface.name, self._name))
        
        # Resolve args
        for index, arg in enumerate(self._info.args):
            try:
                argType = self._interface.module._resolveType(arg.typeInfo)
            except IDLSyntaxError as e:
                # Re-raise exception with module/line information
                raise IDLSyntaxError(self._interface.module, arg.line, e.message)
            
            if not argType:
                raise RuntimeError('Could not resolve #%d argument type %r of method %s::%s' % (index, arg.typeInfo.name, self._interface.name, self._name))
            
            newArg = Method.Argument(self, argType, arg.name)
            
            # Duplicate name check
            for i in self._args:
                if i.name == newArg.name:
                    raise IDLSyntaxError(self._interface.module, arg.line, 'Duplicate argument name %r in method \'%s::%s\'' % (newArg.name, self._interface.name, self._name))
                
            self._args.append(newArg)
            
        # Annotations
        self._assignAnnotations(self._info.annotations)
        
        for arg in self._args:
            if arg.type.mod(Type.MOD_CALLBACK_REG):
                self._type = Method.CALLBACK_REGISTER
                self._callbackType = arg.type
                
            elif arg.type.mod(Type.MOD_CULLBACK_UNREG):
                self._type = Method.CALLBACK_UNREGISTER
                self._callbackType = arg.type
                
