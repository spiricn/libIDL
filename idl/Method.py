from idl.Annotatable import Annotatable
from idl.IDLSyntaxError import IDLSyntaxError
from idl.IDLTypeError import IDLTypeError
from idl.Type import Type
from idl.Variable import Variable


class MethodArgument(Variable):
    def __init__(self, method, argType, name, mods, arraySize):
        Variable.__init__(self, argType, name, mods, arraySize)
        
        self._method = method
        
    @property
    def method(self):
        '''
        Method this argument is associated with.
        '''
        
        return self._method
        
class Method(Annotatable):
    # Method type enumeration
    NORMAL, \
    CALLBACK_REGISTER, \
    CALLBACK_UNREGISTER, \
    = range(3)
    
    def __init__(self, interface, desc):
        Annotatable.__init__(self)
        
        self._interface = interface
        
        self._desc = desc
        
        self._type = Method.NORMAL
        
        self._name = desc.name
        
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
        '''
        Object contaning return type information.
        '''
        
        return self._returnType
    
    @property
    def type(self):
        '''
        Type of method. May be one of the following:
            Method.NORMAL - Regular method
            Method.CALLBACK_REGISTER - Used to indicate that a method is used for callback listener registration.
            Method.CALLBACK_UNREGISTER - Used to indicate that a method is used to unregister a callback listener.
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
            returnType = self._interface.module._resolveType(self._desc.returnTypeDesc)
        except IDLSyntaxError as e:
            # Re-raise exception with module/line information
            raise IDLSyntaxError(self._interface.module, self._desc.line, e.message)
        
        if not returnType:
            raise IDLTypeError(self.interface.module, self._desc.line, 'Could not resolve return type %r of method %s::%s' % (self._desc.returnTypeDesc.pathStr, self._interface.name, self._name))
        
        # Modifiers
        try:
            mods = Variable._resolveModifiers(returnType, self._desc.returnTypeDesc.mods)
        except IDLSyntaxError as e:
            raise IDLSyntaxError(self._interface.module, self._desc.line, e.message)
        
        self._returnType = Variable(returnType, name=None, mods=mods, arraySize=self._desc.returnTypeDesc.arraySize)

    def _linkArg(self, index, arg):
        try:
            argType = self._interface.module._resolveType(arg.varDesc.typeDesc)
        except IDLSyntaxError as e:
            # Re-raise exception with module/line information
            raise IDLSyntaxError(self._interface.module, arg.line, e.message)
        
        if not argType:
            raise IDLTypeError(self._interface.module, arg.line, 'Could not resolve #%d argument type %r of method %s::%s' % (index + 1, '.'.join(arg.varDesc.typeDesc.path), self._interface.name, self._name))
        
        # Argument modifiers
        try:
            mods = Variable._resolveModifiers(argType, arg.varDesc.typeDesc.mods)
        except IDLSyntaxError as e:
            raise IDLSyntaxError(self._interface.module, arg.line, e.message)
        
        newArg = MethodArgument(self, argType, arg.varDesc.name, mods, arg.varDesc.typeDesc.arraySize)
        
        # Duplicate name check
        for i in self._args:
            if i.name == newArg.name:
                raise IDLSyntaxError(self._interface.module, arg.line, 'Duplicate argument name %r in method \'%s::%s\'' % (newArg.name, self._interface.name, self._name))
            
        self._args.append(newArg)
        
    def _link(self):
        self._linkReturnType()
        
        # Resolve arguments
        for index, arg in enumerate(self._desc.args):
            self._linkArg(index, arg)
            
        # Annotations
        self._assignAnnotations(self._desc.annotations)
        
        for arg in self._args:
            if arg.mod(Type.MOD_CALLBACK_REG):
                self._type = Method.CALLBACK_REGISTER
                self._callbackType = arg.type
                
            elif arg.mod(Type.MOD_CULLBACK_UNREG):
                self._type = Method.CALLBACK_UNREGISTER
                self._callbackType = arg.type
                
