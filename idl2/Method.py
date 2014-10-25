class Method:
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
        self.interface = interface
        
        self.info = info
        
        self.type = Method.NORMAL
        
        self.name = info.name
        
        self.args = []

    def _link(self):
        # Resolve return type
        self.returnType = self.interface.module.env.resolveType(self.info.returnTypeName)
        
        if not self.returnType:
            raise RuntimeError('Could not resolve return type %r of method %s::%s' % (self.info.returnTypeName, self.interface.name, self.name))
        
        # Resolve args
        for index, arg in enumerate(self.info.args):
            argType = self.interface.module.env.resolveType(arg.typeName)
            
            if not argType:
                raise RuntimeError('Could not resolve #%d argument type %r of method %s::%s' % (index, arg.typeName, self.interface.name, self.name))
            
            newArg = Method.Argument(self, argType, arg.name)
            
            # Duplicate name check
            for i in self.args:
                if i.name == newArg.name:
                    raise RuntimeError('Duplicate argument name %r in method %s::%s' % (newArg.name, self.interface.name, self.name))
                
            self.args.append(newArg)
