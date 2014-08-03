from idl.RawMethod import RawMethod
from idl.IDLType import IDLType
from idl.IDLVariable import IDLVariable

class IDLMethod(IDLType):
    MOD_CALLBACK_DECLARATION = 'callback'
    MOD_CALLBACK_REGISTER = 'callback_register'
    MOD_CALLBACK_UNREGISTER = 'callback_unregister'
    
    def __init__(self, interface, module, fragment):
        IDLType.__init__(self, IDLType.INVALID)
        
        self.interface = interface
        
        self.module = module
        
        # Create a method from the fragment
        try:
            rawMethod = RawMethod(fragment)
        except Exception as e:
            raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (fragment.body, str(e)))
        
        # Determine method type
        if not rawMethod.mods:
            # No modifier, it's a regular method
            self.type = IDLType.METHOD
            
        elif len(rawMethod.mods) > 1:
            raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (fragment.body, "Unrecognized method modifier"))
        
        else:
            mod = rawMethod.mods[0]
            
            if mod == IDLMethod.MOD_CALLBACK_DECLARATION:
                self.type = IDLType.CALLBACK
                
            elif mod == IDLMethod.MOD_CALLBACK_REGISTER:
                self.type = IDLType.CALLBACK_REGISTER
                 
            elif mod == IDLMethod.MOD_CALLBACK_UNREGISTER:
                self.type = IDLType.CALLBACK_UNREGISTER
                
            else:
                raise RuntimeError('Malformed method declaration "%s"; reason="%s"' % (fragment.body, "Unrecognized method modifier \"%s\"" % mod))
            
        # Method name
        self.name = rawMethod.name
        
        # Method return type
        self.returnType = IDLType(rawMethod.returnType)
        
        if self.returnType == IDLType.INVALID:
            raise RuntimeError('Invalid method return type "%s"' % rawMethod.returnType)
        
        self.rawMethod = rawMethod
        
        # Only valid if we're a callback register/unregister methods
        self.callbackType = None

    def create(self):
        self.args = []
        
        for rawArg in self.rawMethod.args:
            var = self.module.createVariable(self.interface, rawArg)
            if var == None:
                raise RuntimeError('Invalid method arrgument type method="%s"; argument="%s"' % (self.rawMethod.body, rawArg.type))
            
            self.args.append(var)
    
        # Deduce callback type from method arguments
        if self.type in [IDLType.CALLBACK_REGISTER, IDLType.CALLBACK_UNREGISTER]:
            numCallbackTypes = 0
            
            for arg in self.args:
                if arg.type == IDLType.CALLBACK:
                    numCallbackTypes += 1
                    self.callbackType = arg.type
                    
            if numCallbackTypes != 1:
                raise RuntimeError('Could not deduce callback type from arguments list in method "%s"' % self.rawMethod.body)
            
    def __str__(self):
        return '<IDLMethod name="%s" type=%d>' % (self.name, self.type)
