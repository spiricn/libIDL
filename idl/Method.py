from idl.Type import Type
from idl.Variable import Variable
from idl.lexer.TokenType import TokenType


class Method():
    NORMAL, \
    CALLBACK_REGISTER, \
    CALLBACK_UNREGISTER, \
    = range(3)
    
    MOD_CALLBACK_REGISTER = 'callback_register'
    MOD_CALLBACK_UNREGISTER = 'callback_unregister'
    
    def __init__(self, interface, module, tokens):
        self.module = module
        
        token = tokens.pop(0)
        
        # Sanity check
        assert(token.type == TokenType.METHOD)
        
        self.interface = interface
        
        if not token.mods:
            # No modifier, it's a regular method
            self.id = Method.NORMAL
            
        elif len(token.mods) > 1:
            # TODO add support for multiple custom modifiers ?
            raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (token.body, "Unrecognized method modifier"))
        
        else:
            mod = token.mods[0]
            
            if mod == Method.MOD_CALLBACK_REGISTER:
                self.id = Method.CALLBACK_REGISTER
                 
            elif mod == Method.MOD_CALLBACK_UNREGISTER:
                self.id = Method.CALLBACK_UNREGISTER
                
            else:
                raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (token.body, "Unrecognized method modifier \"%s\"" % mod))
            
        # Method name
        self.name = token.name
        
        # Method return type
        self.returnType = self.module.resolveType(token.returnType)
        
        if  self.returnType == None or self.returnType == Type.INVALID:
            raise RuntimeError('Invalid method return type "%s"' % token.returnType)
        
        # Save the method token, until the first pass is complete
        # Will use it later in 'create'
        self.rawMethod = token
        
        # Only valid if we're a callback register/unregister methods
        self.callbackType = None

    def create(self):
        self.args = []
        
        # Iterate over a list of raw arguments (strings type, name)
        for rawArg in self.rawMethod.args:
            # Resolve the argument type
            var = self.module.createVariable(rawArg)
            
            if var == None:
                # Unable to resolve type
                raise RuntimeError('Could not resolve method argument type method="%s"; argument="%s %s"' % (self.rawMethod.name, rawArg.type, rawArg.name))
            
            # Type resolved OK, add it to the list
            self.args.append(var)
    
        # If this method is a callback register/unregister, attempt to deduce callback interface
        if self.id in [Method.CALLBACK_REGISTER, Method.CALLBACK_UNREGISTER]:
            numCallbackTypes = 0
            
            for arg in self.args:
                # Callback can be either a callback method or an interface
                if arg.type == Type.INTERFACE:
                    numCallbackTypes += 1
                    self.callbackType = arg.type
                    
            if numCallbackTypes != 1:
                raise RuntimeError('Could not deduce callback type from arguments list in method "%s"' % self.rawMethod.body)
            
    def __str__(self):
        return '<IDLMethod name="%s" type=%d>' % (self.name, self.id)
