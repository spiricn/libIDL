from idl.Annotatable import Annotatable
from idl.Type import Type
from idl.Variable import Variable

from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError


class Method(Annotatable):
    class Argument(Variable):
        def __init__(self, method, argType, name, mods, arraySize):
            Variable.__init__(self, argType, name, mods, arraySize)
            
            self._method = method
            
        @property
        def method(self):
            '''
            Method this argument is associated with.
            '''
            
            return self._method
            
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
    def ret(self):
        return self._returnType
    
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
    
    def _linkReturnType(self):
        # Resolve return type
        try:
            returnType = self._interface.module._resolveType(self._info.returnTypeInfo)
        except IDLSyntaxError as e:
            # Re-raise exception with module/line information
            raise IDLSyntaxError(self._interface.module, self._info.line, e.message)
        
        if not returnType:
            raise IDLTypeError(self.interface.module, self._info.line, 'Could not resolve return type %r of method %s::%s' % (self._info.returnTypeInfo.typeName, self._interface.name, self._name))
        
        # Modifiers
        try:
            mods = Variable._resolveModifiers(returnType, self._info.returnTypeInfo.mods)
        except IDLSyntaxError as e:
            raise IDLSyntaxError(self._interface.module, self._info.line, e.message)
        
        self._returnType = Variable(returnType, name=None, mods=mods, arraySize=self._info.returnTypeInfo.arraySize)

    def _linkArg(self, index, arg):
        try:
            argType = self._interface.module._resolveType(arg.varInfo.typeInfo)
        except IDLSyntaxError as e:
            # Re-raise exception with module/line information
            raise IDLSyntaxError(self._interface.module, arg.line, e.message)
        
        if not argType:
            raise IDLTypeError(self._interface.module, arg.line, 'Could not resolve #%d argument type %r of method %s::%s' % (index + 1, arg.varInfo.typeInfo.typeName, self._interface.name, self._name))
        
        # Argument modifiers
        try:
            mods = Variable._resolveModifiers(argType, arg.varInfo.typeInfo.mods)
        except IDLSyntaxError as e:
            raise IDLSyntaxError(self._interface.module, arg.line, e.message)
        
        newArg = Method.Argument(self, argType, arg.varInfo.name, mods, arg.varInfo.typeInfo.arraySize)
        
        # Duplicate name check
        for i in self._args:
            if i.name == newArg.name:
                raise IDLSyntaxError(self._interface.module, arg.line, 'Duplicate argument name %r in method \'%s::%s\'' % (newArg.name, self._interface.name, self._name))
            
        self._args.append(newArg)
        
    def _link(self):
        self._linkReturnType()
        
        # Resolve args
        for index, arg in enumerate(self._info.args):
            self._linkArg(index, arg)
            
        # Annotations
        self._assignAnnotations(self._info.annotations)
        
        for arg in self._args:
            if arg.mod(Type.MOD_CALLBACK_REG):
                self._type = Method.CALLBACK_REGISTER
                self._callbackType = arg.type
                
            elif arg.mod(Type.MOD_CULLBACK_UNREG):
                self._type = Method.CALLBACK_UNREGISTER
                self._callbackType = arg.type
                
