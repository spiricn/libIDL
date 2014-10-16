from idl.Type import Type
from idl.Variable import Variable

class Method(Type):
    MOD_CALLBACK_DECLARATION = 'callback'
    MOD_CALLBACK_REGISTER = 'callback_register'
    MOD_CALLBACK_UNREGISTER = 'callback_unregister'
    
    def __init__(self, interface, module, token):
        Type.__init__(self, Type.INVALID)
        
        self.interface = interface
        
        self.module = module
        
        if not token.mods:
            # No modifier, it's a regular method
            self.id = Type.METHOD
            
        elif len(token.mods) > 1:
            raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (token.body, "Unrecognized method modifier"))
        
        else:
            mod = token.mods[0]
            
            if mod == Method.MOD_CALLBACK_DECLARATION:
                self.id = Type.CALLBACK
                
            elif mod == Method.MOD_CALLBACK_REGISTER:
                self.id = Type.CALLBACK_REGISTER
                 
            elif mod == Method.MOD_CALLBACK_UNREGISTER:
                self.id = Type.CALLBACK_UNREGISTER
                
            else:
                raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (token.body, "Unrecognized method modifier \"%s\"" % mod))
            
        # Method name
        self.name = token.name
        
        # Method return type
        self.returnType = self.module.resolveType(self, token.returnType)
        
        if  self.returnType == None or self.returnType == Type.INVALID:
            raise RuntimeError('Invalid method return type "%s"' % token.returnType)
        
        self.rawMethod = token
        
        # Only valid if we're a callback register/unregister methods
        self.callbackType = None

    def create(self):
        self.args = []
        
        for rawArg in self.rawMethod.args:
            var = self.module.createVariable(self.interface, rawArg)
            
            if var == None:
                raise RuntimeError('Invalid method argument type method="%s"; argument="%s"' % (self.rawMethod.body, rawArg.name))
            
            self.args.append(var)
    
        # Deduce callback type from method arguments
        if self.id in [Type.CALLBACK_REGISTER, Type.CALLBACK_UNREGISTER]:
            numCallbackTypes = 0
            
            for arg in self.args:
                # Callback can be either a callback method or an interface
                if arg.type in [Type.CALLBACK, Type.INTERFACE]:
                    numCallbackTypes += 1
                    self.callbackType = arg.type
                    
            if numCallbackTypes != 1:
                raise RuntimeError('Could not deduce callback type from arguments list in method "%s"' % self.rawMethod.body)
            
    def __str__(self):
        return '<IDLMethod name="%s" type=%d>' % (self.name, self.id)
