from idl.Annotatable import Annotatable
from idl.Type import Type


class Method(Annotatable):
    class Argument:
        def __init__(self, method, argType, name):
            self.method = method
            self.type = argType
            self.name = name
            
    NORMAL, \
    CALLBACK_REGISTER, \
    CALLBACK_UNREGISTER, \
    = range(3)
    
    def __init__(self, interface, info):
        Annotatable.__init__(self)
        
        self.interface = interface
        
        self.info = info
        
        self.type = Method.NORMAL
        
        self.name = info.name
        
        self.args = []
        
        self.callbackType = None

    def _link(self):
        # Resolve return type
        self.returnType = self.interface.module._resolveType(self.info.returnTypeInfo)
        
        if not self.returnType:
            raise RuntimeError('Could not resolve return type %r of method %s::%s' % (self.info.returnTypeInfo.name, self.interface.name, self.name))
        
        # Resolve args
        for index, arg in enumerate(self.info.args):
            argType = self.interface.module._resolveType(arg.typeInfo)
            
            if not argType:
                raise RuntimeError('Could not resolve #%d argument type %r of method %s::%s' % (index, arg.typeInfo.name, self.interface.name, self.name))
            
            newArg = Method.Argument(self, argType, arg.name)
            
            # Duplicate name check
            for i in self.args:
                if i.name == newArg.name:
                    raise RuntimeError('Duplicate argument name %r in method %s::%s' % (newArg.name, self.interface.name, self.name))
                
            self.args.append(newArg)
            
        # Annotations
        self._assignAnnotations(self.info.annotations)
        
        for arg in self.args:
            if arg.type.mod(Type.MOD_CALLBACK_REG):
                self.type = Method.CALLBACK_REGISTER
                self.callbackType = arg.type
                
            elif arg.type.mod(Type.MOD_CULLBACK_UNREG):
                self.type = Method.CALLBACK_UNREGISTER
                self.callbackType = arg.type
                
